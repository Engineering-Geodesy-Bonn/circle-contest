import logging

from src.CircleContest import Database, EvaluationMetric

# logging configuration
logging.basicConfig(
    format="%(levelname)-8s %(asctime)s.%(msecs)03d - %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)


def main():
    # read database
    db = Database.from_file()

    """
    Session
    """
    session = "GAF 8b"
    db_s = db.get_session(session=session)

    # leaderboard
    if len(db_s.runs) > 0:
        db_s.show_leaderboard(n_max=20, ev_metric=EvaluationMetric.RATIO, title=session)
        db_s.sort(ev_metric=EvaluationMetric.RATIO)
        db_s.print_runs()
    else:
        logging.error("No runs available!")


if __name__ == "__main__":
    main()
