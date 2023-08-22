from pathlib import Path
import re

import requests as requests
from bs4 import BeautifulSoup

from markdownify import markdownify, ATX


def postprocess_snowflake_docs(_md):
    # Garbling from removing links from headers
    _md = (
        _md
        .replace(
            r"¶",
            "",
        )
        .replace(
            r"“",
            "\"",
        )
        .replace(
            r"”",
            "\"",
        )
    )

    _md = re.sub(
        r"""
```

Copy
""",
        r"""
```
""",
        _md,
    )

    _md = re.sub(
        r"""
> Copy
>\s?""",
        "\n",
        _md,
    )

    return _md


def postprocess_aws_docs(_md):
    return _md


def postprocess_boto3_docs(_md):
    _md = _md.replace(
        """
```

Copy to clipboard

""",
        """
```

"""
    )

    return _md


def postprocess_awswrangler_docs(_md):
    # Garbling from removing links from headers
    _md = _md.replace(
        r"¶",
        "",
    )

    _md = _md.replace(
        """
```

Copy to clipboard

""",
        """
```

"""
    )

    return _md


def remove_artificial_new_line_in_p(_html):
    # Artificial indentation occurs e.g. the server sends a <p> tag
    # splitting the content inside of it
    # <p>For a persistent request,
    #           the request remains
    #           active</p>

    # Force indentation for all tags to identify where the artificial
    # indentation occurs
    _html = "\n".join(
        [
            "  " + _line
            for _line in _html.splitlines()
        ]
    )

    soup = BeautifulSoup(_html, "html.parser")
    for _p in soup.find_all("p"):
        _p.string = re.sub(r'\n\s+', ' ', _p.get_text())

    _html = str(soup)

    return _html


def main(
    source: str,
    path_output: Path | str,
):

    assert source in [
        "snowflake_docs",
        "aws_docs",
        "boto3_docs",
        "awswrangler_docs",
    ]

    if not isinstance(path_output, Path):
        path_output = Path(path_output)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    _html = r""""""

    _html = remove_artificial_new_line_in_p(_html)

    # TODO h1 should be ### instead of underlying
    _md = markdownify(
        _html,
        escape_underscores=False,
        wrap_width=False,
        heading_style=ATX,
        strip=["a"],
    )

    _md = re.sub(
        r"\n{3,}",
        "\n\n",
        _md,
    )

    _md = re.sub(
        r"={6,}",
        "=" * 5,
        _md,
    )

    _md = re.sub(
        r"-{6,}",
        "-" * 5,
        _md,
    )

    _md = (
        _md
        .replace("»", ">>")
        .replace("’", "'")
    )

    postprocess_function = {
        "snowflake_docs": postprocess_snowflake_docs,
        "aws_docs": postprocess_aws_docs,
        "boto3_docs": postprocess_boto3_docs,
        "awswrangler_docs": postprocess_awswrangler_docs,
    }[source]

    _md = postprocess_function(_md)

    _md = _md.strip()

    try:
        path_output.write_text(
            _md,
        )

    except UnicodeEncodeError:
        path_output.write_text(
            _md,
            # » becomes Â»
            # ’ becomes â€™
            encoding="utf-8",
        )


if __name__ == '__main__':

    main(
        source="snowflake_docs",
        # source="aws_docs",
        # source="boto3_docs",
        # source="awswrangler_docs",
        path_output=r"C:\Users\a.fomitchenko\PycharmProjects\python-markdownify\md.md",
    )
