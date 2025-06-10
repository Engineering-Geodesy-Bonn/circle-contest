from src.CircleContest import CircleContest
from src.Database import EvaluationMetric
from src.TotalStation import TotalStation, Connection
import logging

# logging configuration
logging.basicConfig(
    format="%(levelname)-8s %(asctime)s.%(msecs)03d - %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)


def main():
    # connection settings
    connection = Connection(com="COM5", baud=115200, tout=30)

    # Connect to total station
    Tachy = TotalStation(connection)

    manual = False
    # new CircleContest
    """
    Session
    """
    session = "GAF 8b"
    circ_con = CircleContest(ts=Tachy, ev_metric=EvaluationMetric.RATIO)

    # new run
    circ_con.new_run(session=session, manual=manual)

    # leaderboard
    circ_con.print_leaderboard(ev_metric=EvaluationMetric.RATIO)


if __name__ == "__main__":
    main()
