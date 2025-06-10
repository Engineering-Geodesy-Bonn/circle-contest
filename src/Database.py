import logging
import uuid
from dataclasses import dataclass, field
from enum import Enum, auto
from pathlib import Path

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from src.Run import Run

logger = logging.getLogger("root")


class EvaluationMetric(Enum):
    STD = auto()
    RATIO = auto()


@dataclass
class Database:
    runs: list[Run] = field(default_factory=list)

    @classmethod
    def from_file(cls: "Database", *, filename: str = "./db/db.csv") -> "Database":
        # try to read an existing database
        runs = []
        try:
            with open(filename) as f:
                in_file = f.readlines()
        except FileNotFoundError as e:
            logger.info("There is no database yet!")
            Path("./db").mkdir(exist_ok=True)
            return cls()

        # create database
        for l in in_file:
            line_split = l.split(",")
            session = line_split[0]
            id = line_split[1]
            time = line_split[2]
            name = line_split[3]
            radius = float(line_split[4])
            std = float(line_split[5])

            run = Run(
                session=session,
                id=id,
                time=time,
                name=name,
                circ_radius=radius,
                circ_std=std,
            )
            runs.append(run)
        logger.info(f"Read {len(runs)} runs!")
        return cls(runs)

    @property
    def sessions(self) -> list:
        return [r.session for r in self.runs]

    @property
    def ids(self) -> list:
        return [r.id for r in self.runs]

    @property
    def names(self) -> list:
        return [r.name for r in self.runs]

    @property
    def ratios(self) -> np.ndarray:
        """
        Returns ratios of standard deviation and radius
        """
        return np.array([(r.circ_std / r.circ_radius) for r in self.runs])

    @property
    def radii(self) -> np.ndarray:
        return np.array([r.circ_radius for r in self.runs])

    @property
    def stds(self) -> np.ndarray:
        return np.array([r.circ_std for r in self.runs])

    def get_run(self, id: uuid.UUID) -> Run:
        ids = self.ids
        return self.runs[ids.index(id)]

    def get_session(self, session: str) -> "Database":
        runs = [r for r in self.runs if r.session == session]
        return Database(runs=runs)

    def insert_run(self, run: Run) -> None:
        self.runs.append(run)
        try:
            # write to file
            with open("./db/db.csv", "a+") as out_file:
                out_file.write(f"{run}\n")
        except Exception as e:
            logger.error(f"Failed to save run: {e}")

    def del_run(self, id: uuid.UUID) -> None:
        self.runs = [r for r in self.runs if r.id != id]

    def position(self, *, id: uuid.UUID, ev_metric: EvaluationMetric) -> int:
        self.sort(ev_metric=ev_metric)
        ids = self.ids
        return ids.index(id) + 1

    def session_position(self, *, session: str, id: uuid.UUID, ev_metric: EvaluationMetric) -> int:
        db_session = self.get_session(session=session)
        return db_session.position(id=id, ev_metric=ev_metric)

    def sort(self, ev_metric: EvaluationMetric = EvaluationMetric.STD) -> None:
        if ev_metric == EvaluationMetric.STD:
            # sort by std
            idx = np.argsort(self.stds)
        elif ev_metric == EvaluationMetric.RATIO:
            # sort by ratio of standard deviation and radius
            idx = np.argsort(self.ratios)

        self.runs = [self.runs[i] for i in idx]

    def print_runs(self) -> None:
        print(
            (
                "====================="
                "====================="
                "======================"
                "======================"
                "======================"
            )
        )
        for i, r in enumerate(self.runs):
            print(
                (f"{i + 1:<3} {r.name:<20} {r.time}: " f"Radius: {r.circ_radius:.3f} m, " f"Sigma: {r.circ_std:.4f} m")
            )

    def show_leaderboard(self, *, n_max: int = 10, ev_metric=EvaluationMetric, title: str = "Insgesamt") -> None:
        self.sort(ev_metric=ev_metric)

        fig, ax = plt.subplots(1, 1, figsize=(13, 9))
        plt.get_current_fig_manager().window.state("zoomed")

        # hide axes
        fig.patch.set_visible(False)
        ax.axis("off")
        ax.axis("tight")

        n = min(len(self.runs), n_max)

        numbers = list(range(1, n + 1))

        if ev_metric == EvaluationMetric.STD:
            df = pd.DataFrame([numbers, self.names[:n], self.stds[:n]])
            df = df.transpose()
            df.update(df[[2]].applymap("{:,.3f}".format))
            tab = ax.table(
                cellText=df.values,
                colLabels=[
                    "$\\bf{Platzierung}$",
                    "$\\bf{Name}$",
                    "$\\bf{Abweichung [m]}$",
                ],
                loc="center",
                cellLoc="center",
            )
            plt.title(f"Rundester Kreis\n({title})", fontsize=30)
        elif ev_metric == EvaluationMetric.RATIO:
            df = pd.DataFrame([numbers, self.names[:n], self.ratios[:n]])
            df = df.transpose()
            df.update(df[[2]].applymap("{:,.3f}".format))
            tab = ax.table(
                cellText=df.values,
                colLabels=[
                    "$\\bf{Platzierung}$",
                    "$\\bf{Name}$",
                    "$\\bf{Std. Abw / Radius [m]}$",
                ],
                loc="center",
                cellLoc="center",
            )
            plt.title(f"Rundester Kreis\n({title})", fontsize=30)
        tab.auto_set_font_size(False)
        tab.set_fontsize(20)
        tab.scale(1, 2)

        fig.tight_layout()

        plt.show()


def gen_circle(r: float) -> None:
    phi = np.arange(0, 2 * np.pi, 0.01)
    x = np.sin(phi) * r
    y = np.cos(phi) * r
    return x, y
