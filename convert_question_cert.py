from dataclasses import dataclass
from time import sleep

import pandas as pd

from pathlib import Path


def configure_pandas(
    pandas,
    infinite_rows: bool = False,
    additional_params: bool = False
):  # pragma: no cover
    """Configure Pandas module.

    Args:
        pandas: Pandas module
            where to apply the configuration.
        infinite_rows (bool): Whether to configure Pandas
            to display all rows.
        additional_params (bool): Whether to configure Pandas
            to display wider and justified columns.

    Returns:

    """
    pandas.set_option("display.expand_frame_repr", False)
    pandas.options.display.width = 0
    pandas.set_option("display.max_columns", None)
    pandas.options.display.float_format = "{:,.2f}".format

    if infinite_rows:
        pandas.set_option("display.max_rows", None)

    if additional_params:
        pandas.set_option("display.max_colwidth", 100)
        pandas.set_option("display.column_space", 40)
        pandas.set_option("display.colheader_justify", "left")


configure_pandas(pd)


@dataclass
class Question:
    question_text: str
    answers_pasted_from_excel: str
    answer_correct: str


def load_most_difficult():
    PATH_PICKLE = r"C:\Users\a.fomitchenko\deleteme2\df_most_difficult.pkl"

    while True:
        try:
            df = pd.read_excel(
                r"C:\Users\a.fomitchenko\Certifications\reply_certifications__aws_devops_engineer\Exams AWS DevOps Engineer.xlsx",
                sheet_name="Sheet1",
            )
            break
        except:
            print("Is the file open?")
            df = pd.read_pickle(
                PATH_PICKLE,
            )
            sleep(10)

    df_most_difficult = df[
        df["Source"] == "MOLTO DIFFICILE PER LLM"
        ]

    df_most_difficult.to_pickle(PATH_PICKLE)

    print(df)

    # df_most_difficult
    #     Temporarily hidden (used for black conditional formatting rule)  Random single  Random question     ID  which_certification_preparation                   Source difficulty_label  Present in exam  Category                                           Question                                            Answers  Correct (1)  Unnamed: 12  False  Correct  Space                                        Explanation

    QUESTIONS_MOST_DIFFICULT = []

    for _id in df_most_difficult["ID"]:
        rows = df_most_difficult[df_most_difficult["ID"] == _id]
        question_text = rows["Question"].iloc[0]
        answers_pasted_from_excel = "\n".join(
            rows["Answers"].iloc[0].split("\n")[1:]
        )
        answer_correct = rows["Correct (1)"].iloc[0]

        QUESTIONS_MOST_DIFFICULT.append(
            Question(
                question_text=question_text,
                answers_pasted_from_excel=answers_pasted_from_excel,
                answer_correct=answer_correct,
            )
        )


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


def convert_from_question_and_answers(
    exam_name: str,
    question_text: str,
    answers_pasted_from_excel: str,
    only_final: bool = False,
    accept_quotes_in_answers_pasted: bool = False,
):
    question_text = question_text.replace("\"", "").strip()

    lines_answers = [
        _line.strip()
        for _line in answers_pasted_from_excel.split("\n")
        if len(_line.strip()) > 0
    ]

    if not accept_quotes_in_answers_pasted:
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

    prefix_how_many_correct = {
        2: "one option",
        3: "one option",
        4: "one option",
        5: "two options",
        6: "three options",
    }[len(answers)]

    if not only_final:
        print("\n" * 10 + "Without intro: " + "\n" * 10)
        print(question_all)

        print("\n" * 10 + "Analyze single" + "\n" * 10)
        print("""\
You are analyzing the following {exam_name exam question:
    
```
""" + question_text + """
```

One of the options is

```
A. """
+ lines_answers[0] + """
```

Find information on the internet to evaluate whether the option is correct or incorrect.""")

        print("\n" * 10 + "Mistral large: " + "\n" * 10)
        print(
        f"""<s>[INST]# Your task
Reason step by step before choosing EXACTLY {prefix_how_many_correct} as correct.

# {exam_name} exam question
""" + question_all
        + "[/INST]")

        print("\n" * 10 + "Gemini with documentation: " + "\n" * 10)
        print(
            question_all + "\n\n" +
            f"""# Your task
You MUST QUOTE DIRECTLY from the provided documentation, then reason step by step and choose EXACTLY {prefix_how_many_correct} as correct.""")

    print("\n" * 10 + "Study topics: " + "\n" * 10)
    print(
        f"""# Your task
Based on the following {exam_name} exam question, extract which topics I should research. DON'T suggest basic topics, this is an advanced question, so you should focus on the nooks and crannies.

# {exam_name} exam question
""" + question_all)

    print("\n" * 10 + "More structured: " + "\n" * 10)
    print(
        f"""You are tasked with answering the following {exam_name} exam question.

Explain for each answer why it is "correct" or "incorrect". VERY IMPORTANT: there MUST be EXACTLY {prefix_how_many_correct} as correct, all others MUST be incorrect.







The format of what you write is the following

<assistant_reply>

### Section where all answers are evaluated
Answer A: [explanation and reasoning step-by-step]
Answer B: [explanation and reasoning step-by-step]
...

### Evaluation based on previous explanations
- Answer A: [summary of explanation and reasoning step-by-step]. Therefore, the answer is [correct/incorrect]
- Answer B: [summary of explanation and reasoning step-by-step]. Therefore, the answer is [correct/incorrect]
...

</assistant_reply>








This is the {exam_name} exam question:

{question_all}
"""
    )

    print("\n" * 10 + "With prefix and suffix: " + "\n" * 10)
    print(
        f"""# Your task
Reason step by step before choosing EXACTLY {prefix_how_many_correct} as correct.

# {exam_name} exam question
""" + question_all)


if __name__ == '__main__':
    
    convert_from_question_and_answers(
        exam_name="AWS DevOps Engineer",
        question_text="""A company runs applications in an Amazon Elastic Kubernetes Service (Amazon EKS) cluster. The EKS cluster uses an Application Load Balancer to route traffic to the applications that run in the cluster.

A new application that was migrated to the EKS cluster is performing poorly. All the other applications in the EKS cluster maintain appropriate operation. The new application scales out horizontally to the preconfigured maximum number of pods immediately upon deployment, before any user traffic routes to the web application.

Which solution will resolve the scaling behavior of the web application in the EKS cluster?""",
        answers_pasted_from_excel="""Implement the Vertical Pod Autoscaler in the EKS cluster.
Implement the AWS Load Balancer Controller in the EKS cluster.
Implement the Cluster Autoscaler.
Implement the Horizontal Pod Autoscaler in the EKS cluster.
""",
    )

    # Most difficult IDs: 46, 49, 51, 54, 57, 66, 138, 146
    # Qwen 1.5 Chat (72B)
    # t=0.44, top-p=0.7, top-k=50
    # : 5 / 8
