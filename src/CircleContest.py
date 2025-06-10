import logging
import time as t
from pathlib import Path
from typing import Tuple

import keyboard
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np

from src.Database import Database, EvaluationMetric
from src.Run import Run
from src.TotalStation import TotalStation

plt.style.use("fivethirtyeight")

logger = logging.getLogger("root")


class CircleContest:
    def __init__(self, ts: TotalStation, ev_metric: EvaluationMetric = EvaluationMetric.STD) -> None:
        self.ts = ts
        self.metric = ev_metric
        self.database = Database.from_file()

        try:
            self.logo = mpimg.imread("./assets/logo-geodaesie.png")
            self.search = mpimg.imread("./assets/search.png")
        except Exception as e:
            logger.error(f"Error loading logo: {e}")
            self.logo = None
            self.search = None

    @staticmethod
    def input_name() -> str:
        return input("Bitte den Namen eingeben... ")

    def input_rad(self) -> float:
        try:
            return 0.5 * float(input("Welchen Durchmesser wird dein Kreis haben? (In Metern) "))

        except Exception:
            print("Das hat nicht geklappt! Bitte versuche es erneut und gib eine Zahl ein!")
            return self.input_rad()

    def new_run(self, session: str, manual: bool = False) -> None:
        if not self.ts.connected:
            logger.error("Connection error!")
            return

        # name und durchmesser
        name = self.input_name()
        # r_ref = self.input_rad()

        # print(f"{name} möchte einen Kreis mit einem Durchmesser von {r_ref*2} Metern laufen!")

        # reset tachy data
        self.ts.clear_points()
        self.ts.stop_tracking()

        # try to start the tracking
        fig_search = plt.figure()
        plt.get_current_fig_manager().full_screen_toggle()
        if self.search is not None:
            plt.title(f"Kandidat:in: {name}", fontsize=40)
            plt.imshow(self.search)
        else:
            plt.text(0, 0, "Suche gestartet!\nBitte nicht bewegen!", fontsize=40)
        plt.axis("off")
        plt.pause(0.01)
        status = self.ts.start_tracking(manual=manual)
        plt.close(fig_search)

        # quit if start tracking was not sucessfull
        if not status:
            logger.warning("Aborting run.")
            return

        # new figure
        fig = plt.figure(figsize=(10, 5))
        plt.get_current_fig_manager().full_screen_toggle()

        # do until space key is pressed
        while True:
            if keyboard.is_pressed("space"):
                logger.warning("Interrupted")
                self.ts.stop_tracking()
                plt.close(fig)
                self.process_run(session=session, name=name)
                break
            try:
                self.ts.add_point()
                self.ts.kinematic_animation()
            except Exception as e:
                logger.error(e)
                self.ts.stop_tracking()
            except KeyboardInterrupt:
                logger.warning("Interrupted")
                self.ts.stop_tracking()
            t.sleep(0.05)

    def process_run(self, *, session: str, name: str) -> Run:
        # evaluate run
        if len(self.ts.x_vals) > 3 and len(self.ts.x_vals) == len(self.ts.y_vals):
            logger.info("Processing run...")
            x = np.array(self.ts.x_vals)
            y = np.array(self.ts.y_vals)
            x_c, y_c, r = circle_fit(x, y)

            coords = np.c_[x - x_c, y - y_c]

            # standard deviation
            v = np.sqrt(np.power(x - x_c, 2) + np.power(y - y_c, 2)) - r
            sigma = np.sqrt((v.T @ v) / (len(v) - 3))

            # add run
            run = Run(
                session=session,
                name=name,
                circ_radius=r,
                circ_std=sigma,
                coords=coords,
            )

            self.database.insert_run(run)
            self.plot_run(run)
            return run
        else:
            logger.error("No measurements recorded!")

    def plot_run(self, run: Run) -> None:
        # circle of run
        cx, cy = gen_circle(1)

        # get position of run in total
        pos_global = self.database.position(id=run.id, ev_metric=self.metric)
        num_runs_global = len(self.database.runs)

        fig, ax = plt.subplots(1, 1, figsize=(10, 12))
        # plt.get_current_fig_manager().window.state("zoomed")
        plt.get_current_fig_manager().full_screen_toggle()
        ax.set_title(
            f"{run.name} ist auf Platz {pos_global} von {num_runs_global}!",
            fontsize=40,
        )
        plt.axis("equal")

        fig.set_facecolor("#c8cbcf")
        ax.set_facecolor("#c8cbcf")

        ax.plot(0, 0, ".k", markersize=15, label="_nolegend_")
        ax.plot([0, 1], [0, 0], "k", linewidth=2, label="_nolegend_")
        ax.text(
            1 / 3,
            0.0125 ,
            f"r = {run.circ_radius:.3f} m",
            fontsize=25,
            label="_nolegend_",
        )
        ax.text(
            1 / 3.11,
            -0.08 ,
            f"$\sigma$ = {run.circ_std:.3f} m",
            fontsize=25,
            label="_nolegend_",
        )
        ax.plot(cx, cy, linewidth=2, color="#DB1111", label="Kreis (zum Vergleich)")

        ax.plot(
            run.unit_circle_coords[:, 0],
            run.unit_circle_coords[:, 1],
            ".-",
            color="#0A49B3",
            linewidth=4,
            markersize=20,
            label="Gelaufen",
        )
        logger.info("Finished run!")

        ax.legend(loc="lower right", fontsize=20)

        if self.logo is not None:
            newax = fig.add_axes([0.05, 0.04, 0.3, 0.3], anchor="SW", zorder=-1)
            newax.imshow(self.logo)
            newax.axis("off")

        ax.axis("off")
        plt.axis("off")

        Path(f"./figures/{run.session}/").mkdir(parents=True, exist_ok=True)
        fig.savefig(
            f"./figures/{run.session}/{run.name}-{run.id}.png",
            format="png",
            dpi=300,
            facecolor=fig.get_facecolor(),
            edgecolor="none",
        )
        plt.show()

    def print_leaderboard(self, ev_metric: EvaluationMetric) -> None:
        self.database.sort(ev_metric)
        self.database.print_runs()


def gen_circle(r: float) -> None:
    phi = np.arange(0, 2 * np.pi, 0.01)
    x = np.sin(phi) * r
    y = np.cos(phi) * r
    return x, y


def circle_fit(x: np.ndarray, y: np.ndarray) -> Tuple[float, float, float]:
    A = np.c_[-2 * x, -2 * y, np.ones((len(x), 1))]
    l = -(np.power(x, 2) + np.power(y, 2))

    # least squares solve
    p = np.linalg.solve(A.T @ A, A.T @ l)

    # parameters
    x_c = p[0]
    y_c = p[1]
    r = np.sqrt(x_c**2 + y_c**2 - p[2])

    return x_c, y_c, r
