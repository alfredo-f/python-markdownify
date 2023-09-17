from markdownify import MarkdownConverter
from bs4 import BeautifulSoup


def test_img():
    # Create shorthand method for conversion
    def md(html, **options):
        return MarkdownConverter(**options).convert(html)

    assert md('<img src="/path/to/img.jpg" alt="Alt text" title="Optional title" />') == '![Alt text](/path/to/img.jpg "Optional title")'
    assert md('<img src="/path/to/img.jpg" alt="Alt text" />') == '![Alt text](/path/to/img.jpg)'
