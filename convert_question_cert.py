import pandas as pd

from pathlib import Path


def convert_from_pasted(
    split_by_character: str,
):

    assert split_by_character in (
        "\n",
        "\"",
    )

    pasted_from_excel = """"A company has a mobile application that makes HTTP API calls to an Application Load Balancer (ALB). The ALB routes requests to an AWS Lambda function. Many different versions of the application are in use at any given time, including versions that are in testing by a subset of users. The version of the application is defined in the user-agent header that is sent with all requests to the API.
After a series of recent changes to the API, the company has observed issues with the application. The company needs to gather a metric for each API operation by response code for each version of the application that is in use. A DevOps engineer has modified the Lambda function to extract the API operation name, version information from the user-agent header and response code.
Which additional set of actions should the DevOps engineer take to gather the required metrics?"	Configure the ALB access logs to write to an Amazon CloudWatch Logs log group. Modify the Lambda function to respond to the ALB with the API operation name, response code, and version number as response metadata. Configure a CloudWatch Logs metric filter that increments a metric for each API operation name. Specify response code and application version as dimensions for the metric.
"A company has a mobile application that makes HTTP API calls to an Application Load Balancer (ALB). The ALB routes requests to an AWS Lambda function. Many different versions of the application are in use at any given time, including versions that are in testing by a subset of users. The version of the application is defined in the user-agent header that is sent with all requests to the API.
After a series of recent changes to the API, the company has observed issues with the application. The company needs to gather a metric for each API operation by response code for each version of the application that is in use. A DevOps engineer has modified the Lambda function to extract the API operation name, version information from the user-agent header and response code.
Which additional set of actions should the DevOps engineer take to gather the required metrics?"	Modify the Lambda function to write the API operation name, response code, and version number as a log line to an Amazon CloudWatch Logs log group. Configure a CloudWatch Logs metric filter that increments a metric for each API operation name. Specify response code and application version as dimensions for the metric.
"A company has a mobile application that makes HTTP API calls to an Application Load Balancer (ALB). The ALB routes requests to an AWS Lambda function. Many different versions of the application are in use at any given time, including versions that are in testing by a subset of users. The version of the application is defined in the user-agent header that is sent with all requests to the API.
After a series of recent changes to the API, the company has observed issues with the application. The company needs to gather a metric for each API operation by response code for each version of the application that is in use. A DevOps engineer has modified the Lambda function to extract the API operation name, version information from the user-agent header and response code.
Which additional set of actions should the DevOps engineer take to gather the required metrics?"	Modify the Lambda function to write the API operation name, response code, and version number as a log line to an Amazon CloudWatch Logs log group. Configure a CloudWatch Logs Insights query to populate CloudWatch metrics from the log lines. Specify response code and application version as dimensions for the metric.
"A company has a mobile application that makes HTTP API calls to an Application Load Balancer (ALB). The ALB routes requests to an AWS Lambda function. Many different versions of the application are in use at any given time, including versions that are in testing by a subset of users. The version of the application is defined in the user-agent header that is sent with all requests to the API.
After a series of recent changes to the API, the company has observed issues with the application. The company needs to gather a metric for each API operation by response code for each version of the application that is in use. A DevOps engineer has modified the Lambda function to extract the API operation name, version information from the user-agent header and response code.
Which additional set of actions should the DevOps engineer take to gather the required metrics?"	Configure AWS X-Ray integration on the Lambda function. Modify the Lambda function to create an X-Ray subsegment with the API operation name, response code, and version number. Configure X-Ray insights to extract an aggregated metric for each API operation name and to publish the metric to Amazon CloudWatch. Specify response code and application version as dimensions for the metric.
"""

    lines = [
        _line.strip()
        for _line in pasted_from_excel.split(split_by_character)
        if len(_line.strip()) > 0
    ]

    if split_by_character == "\n":
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

    elif split_by_character == "\"":
        pasted_from_excel

        answers = None

    else:
        raise ValueError(split_by_character)



    answers = [
        f"{chr(ord('A') + i)}. {_answer}"
        for i, _answer in enumerate(answers)
    ]

    question_all = question_text + "\n\n" + "\n".join(answers)

    print("\n" * 10 + "Without intro: " + "\n" * 10)
    print(question_all)

    print("\n" * 10 + "With intro: " + "\n" * 10)
    print("In Snowflake, " + question_all[0].lower() + question_all[1:])


def convert_from_excel_file(
    file_path: Path,
    question_id: int,
):
    # TODO permission denied because it's open
    df = pd.read_excel(
        file_path,
    )
    df_question = df[
        df["ID"] == question_id
    ]

    print(df_question)


def convert_from_question_and_answers():
    question_text = """"A company is using an Amazon Aurora cluster as the data store for its application. The Aurora cluster is configured with a single DB instance. The application performs read and write operations on the database by using the cluster's instance endpoint.
The company has scheduled an update to be applied to the cluster during an upcoming maintenance window. The cluster must remain available with the least possible interruption during the maintenance window.
What should a DevOps engineer do to meet these requirements?"
"""

    answers_pasted_from_excel = """Turn on the Multi-AZ option on the Aurora cluster. Update the application to use the Aurora cluster endpoint for write operations. Update the Aurora cluster’s reader endpoint for reads.
Add a reader instance to the Aurora cluster. Update the application to use the Aurora cluster endpoint for write operations. Update the Aurora cluster's reader endpoint for reads.
Turn on the Multi-AZ option on the Aurora cluster. Create a custom ANY endpoint for the cluster. Update the application to use the Aurora cluster's custom ANY endpoint for read and write operations
Add a reader instance to the Aurora cluster. Create a custom ANY endpoint for the cluster. Update the application to use the Aurora cluster's custom ANY endpoint for read and write operations.
"""

    question_text = question_text.replace("\"", "").strip()

    lines_answers = [
        _line.strip()
        for _line in answers_pasted_from_excel.split("\n")
        if len(_line.strip()) > 0
    ]

    lines_unexpected = [
        _line
        for _line in lines_answers
        if "\"" in _line
    ]
    if len(lines_unexpected) > 0:
        raise ValueError(f"Unexpected lines: {lines_unexpected}")

    answers = [
        f"{chr(ord('A') + i)}. {_answer}"
        for i, _answer in enumerate(lines_answers)
    ]

    question_all = question_text + "\n\n" + "\n".join(answers)

    print("\n" * 10 + "Without intro: " + "\n" * 10)
    print(question_all)

    print("\n" * 10 + "Analyze single" + "\n" * 10)
    print("""\
You are analyzing the following AWS DevOps Engineer exam question:

```
""" + question_text + """
```

One of the options is

```
A. """
+ lines_answers[0] + """
```

Find information on the internet to evaluate whether the option is correct or incorrect.""")

    prefix_how_many_correct = {
        4: "one option",
        5: "two options",
        6: "three options",
    }[len(answers)]

    print("\n" * 10 + "With prefix and suffix: " + "\n" * 10)
    print(
        f"""# Your task
Reason step by step before choosing ONLY {prefix_how_many_correct} as correct.

# AWS DevOps Engineer exam question
""" + question_all)


if __name__ == '__main__':
    convert_from_question_and_answers()
