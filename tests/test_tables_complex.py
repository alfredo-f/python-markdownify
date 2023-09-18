from markdownify.markdown_converter_custom import MarkdownConverterTables


def test_table_ul():
    if 0 == True:
        return

    _html = """<table>
        <tr>
            <th>Column</th>
        </tr>
        <tr>
            <td>It can:
<ul class="some">
<li>Edit</li></ul>
</td>
        </tr>
    </table>"""

    _md = """

| Column |
| --- |
| It can:
<ul>* Edit<br></ul> |

"""

    _md_final = """

| Column |
| --- |
| It can:<br><ul class="some"><li>Edit</li></ul> |

    """

    assert MarkdownConverterTables().convert(_html) == _md
