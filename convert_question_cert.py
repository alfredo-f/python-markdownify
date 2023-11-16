def main():

    pasted_from_excel = """What do the terms scale up and scale out refer to in Snowflake? (Choose two.)	Scaling up adds additional database servers to an existing running cluster to handle larger workloads.
What do the terms scale up and scale out refer to in Snowflake? (Choose two.)	Scaling out adds additional database servers to an existing running cluster to handle more concurrent queries.
What do the terms scale up and scale out refer to in Snowflake? (Choose two.)	Snowflake recommends using both scaling up and scaling out to handle more concurrent queries.
"""

    lines = [
        _line.strip()
        for _line in pasted_from_excel.split("\n")
        if len(_line.strip()) > 0
    ]

    lines_unexpected = [
        _line
        for _line in lines
        if _line.count("\t") != 1
    ]

    if len(lines_unexpected) > 0:
        raise ValueError(f"Unexpected lines: {lines_unexpected}")

    question_text = set(
        _line.split("\t")[0]
        for _line in lines
    )

    if len(question_text) != 1:
        raise ValueError(f"More than one question: {question_text}")

    question_text = question_text.pop()

    answers = [
        _line.split("\t")[1]
        for _line in lines
    ]

    answers = [
        f"{chr(ord('A') + i)}. {_answer}"
        for i, _answer in enumerate(answers)
    ]

    question_all = question_text + "\n\n" + "\n".join(answers)

    print("\n" * 10 + "Without intro: " + "\n" * 10)
    print(question_all)

    print("\n" * 10 + "With intro: " + "\n" * 10)
    print("In Snowflake, " + question_all[0].lower() + question_all[1:])


if __name__ == '__main__':

    main()
