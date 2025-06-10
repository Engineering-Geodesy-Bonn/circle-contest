import logging
from src.CircleContest import EvaluationMetric
from src.Database import Database

# logging configuration
logging.basicConfig(
    format="%(levelname)-8s %(asctime)s.%(msecs)03d - %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)


def main():
    # connection settings
    db = Database.from_file()

    # leaderboard
    if len(db.runs) > 0:
        db.show_leaderboard(n_max=20, ev_metric=EvaluationMetric.RATIO, title="Insgesamt")
        db.sort(ev_metric=EvaluationMetric.RATIO)
        db.print_runs()
    else:
        logging.error("No runs available!")


if __name__ == "__main__":
    main()
