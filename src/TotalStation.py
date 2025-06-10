import logging
from time import sleep
from typing import Tuple

import matplotlib.pyplot as plt
import numpy as np
import serial

from src.pygeocom import (
    BOOLE,
    EDMMeasurementMode,
    FineAdjustPositionMode,
    OnOff,
    PrismType,
    PyGeoCom,
    TMCInclinationMode,
    TMCMeasurementMode,
    lDirection,
)

logger = logging.getLogger("root")


class Connection:
    def __init__(self, *, com: str, baud: int, tout: int) -> None:
        self.com = com
        self.baud = baud
        self.tout = tout


class TotalStation:
    def __init__(self, connection: Connection):
        self.ser = serial.Serial(connection.com, connection.baud, timeout=int(connection.tout))
        self.geo = PyGeoCom(self.ser, debug=False)
        a, b, c = self.geo.get_software_version()
        logger.info(
            f"Connection Settings - Port: {connection.com}, Baudrate: {connection.baud}, Timeout: {connection.tout}"
        )
        logger.info(f"Software Version: {a}.{b}.{c}")
        a, b, c = self.geo.get_server_software_version()
        logger.info(f"Server Software Version: {a}.{b}.{c}")
        self.connected = True
        self.no_dist_cnt = 0

        self.x_vals = []
        self.y_vals = []

    def clear_points(self):
        self.x_vals = []
        self.y_vals = []

    def add_point(self):
        x_i, y_i = self.measure_single_point()

        # if measurement is present
        m_present = x_i != 0 and y_i != 0

        # if movement (more than 5 cm)
        if len(self.x_vals) > 0:
            mov = np.sqrt((x_i - self.x_vals[-1]) ** 2 + (y_i - self.y_vals[-1]) ** 2) > 0.05
        else:
            mov = True

        if m_present and mov:
            self.x_vals.append(x_i)
            self.y_vals.append(y_i)

    def kinematic_animation(self):
        plt.cla()
        plt.xlabel("x [m]")
        plt.ylabel("y [m]")
        plt.axis("equal")
        if len(self.x_vals) < 5:
            plt.title("Durchlauf gestartet!\nViel Erfolg!", fontsize=50)
        plt.plot(self.x_vals, self.y_vals, ".-", linewidth=4, markersize=20)
        plt.axis("off")
        plt.pause(0.05)

    def start_tracking(self, attempts: int = 3, manual: bool = False) -> bool:
        n = 1
        while n <= attempts:
            try:
                # prepare tracking
                self.geo.set_prism_type(PrismType.LEICA_360)
                self.geo.set_user_atr_state(OnOff.ON)
                self.geo.set_fine_adjust_mode(FineAdjustPositionMode.POINT)
                self.geo.set_user_lock_state(OnOff.ON)

                logger.info("Leica RTS: searching for target...")
                if manual:
                    self.lock_into_prism()
                else:
                    self.power_search()
                #self.geo.ps_search_next(l_direction=lDirection.CLKW, bool=BOOLE.TRUE)
                # self.geo.lock_in()
                logger.info("Leica RTS: locked into prism!")

                # kinematic continuous measurement mode
                self.geo.set_edm_mode(EDMMeasurementMode.CONTINUOUS_FAST)
                self.geo.do_measure(
                    TMCMeasurementMode.DISTANCE_RAPID_TRACKING,
                    TMCInclinationMode.AUTOMATIC,
                )
                logger.info("Leica RTS: switched to tracking mode!")
                return True
            except Exception as e:
                logger.error(f"({n} / {attempts}) Failed to start tracking: {e}")
                n += 1
        return False

    def power_search(self):
        self.geo.set_search_area(0, 1.5708, 6.283, 0.6, 1)
        self.geo.ps_set_range(1, 20)
        self.geo.ps_enable_range(BOOLE.TRUE)
        logger.info("Leica RTS: searching for target...")
        logger.info(f"Leica RTS: Search window: {self.geo.get_search_area()}")
        self.geo.ps_search_window()
        self.geo.set_user_lock_state(OnOff.ON)
        self.geo.lock_in()
        logger.info("Leica RTS: locked into prism!")

    def lock_into_prism(self):
        logger.info("Leica RTS: performing fine adjust!")
        self.geo.fine_adjust(horizontal_search_range=0.0872, vertical_search_range=0.0872)
        self.geo.set_user_lock_state(OnOff.ON)
        self.geo.lock_in()
        logger.info("Leica RTS: locked into prism!")

    def stop_tracking(self):
        try:
            self.geo.set_user_lock_state(OnOff.OFF)
            self.geo.set_edm_mode(EDMMeasurementMode.SINGLE_STANDARD)
            self.geo.do_measure(TMCMeasurementMode.STOP_AND_CLEAR, TMCInclinationMode.AUTOMATIC)
            self.geo.set_egl_intensity(OnOff.OFF)
            self.geo.user_lock_state_off()
            # always start with face 0
            if self.geo.get_face() == 1:
                self.geo.change_face()
            logger.info("Leica RTS: stopped tracking!")
        except Exception as e:
            logger.error(f"Failed to stop tracking: {e}")
            return False

    def stopAndClean(self):
        sleep(1)
        self.ser.reset_input_buffer()
        # optional
        self.ser.reset_output_buffer()
        sleep(1)
        self.stop_tracking()
        self.ser.close()
        logger.info("Closed serial connection.")

    def restart_distance(self):
        self.geo.do_measure(TMCMeasurementMode.STOP_AND_CLEAR, TMCInclinationMode.AUTOMATIC)
        sleep(0.5)
        self.geo.do_measure(
            TMCMeasurementMode.DISTANCE_RAPID_TRACKING,
            TMCInclinationMode.AUTOMATIC,
        )

    def measure_single_point(self) -> Tuple[float, float]:
        # try measuring
        try:
            (
                _,
                hz,
                v,
                slope_distance,
                _,
                _,
                _,
            ) = self.geo.get_full_measurement(TMCInclinationMode.AUTOMATIC, 300)
            x = slope_distance * np.sin(hz) * np.sin(v)
            y = slope_distance * np.cos(hz) * np.sin(v)

            if slope_distance == 0:
                self.no_dist_cnt += 1
                logger.warning(f"No distance measurement available! ({self.no_dist_cnt})")
                if self.no_dist_cnt > 10:
                    logger.info("Restarting distance measurement!")
                    self.restart_distance()
                    self.no_dist_cnt = 0
            else:
                self.no_dist_cnt = 0

            return x, y
        except Exception as e:
            logger.error(e)
            return (0, 0)
