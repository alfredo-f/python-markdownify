def main():

    pasted_from_excel = """What versions of Snowflake should be used to manage compliance with Personal Identifiable Information (PII) requirements? (Choose two.)	Business Critical Edition
What versions of Snowflake should be used to manage compliance with Personal Identifiable Information (PII) requirements? (Choose two.)	Custom Edition
What versions of Snowflake should be used to manage compliance with Personal Identifiable Information (PII) requirements? (Choose two.)	Enterprise Edition
What versions of Snowflake should be used to manage compliance with Personal Identifiable Information (PII) requirements? (Choose two.)	Virtual Private Snowflake
What versions of Snowflake should be used to manage compliance with Personal Identifiable Information (PII) requirements? (Choose two.)	Standard Edition
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
