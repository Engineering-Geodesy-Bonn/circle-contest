from src.CircleContest import Database, EvaluationMetric


def main():
    # read database
    db = Database.from_file()

    """
    ID
    """
    id = "0ac0c0d5-3ab6-417b-8bc1-87c70b22e32f"

    try:
        print(
            f"Position: {db.position(id=id, ev_metric=EvaluationMetric.STD):<10} {db.get_run(id)}"
        )
    except ValueError:
        print("ID nicht gefunden!")


if __name__ == "__main__":
    main()
