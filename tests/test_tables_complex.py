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
* Edit
 |

"""

    _md_final = """

| Firstname | Lastname | Age |
| --- | --- | --- |
| Jill | Smith | It can:<br><ul><li>Edit</li></ul> |
| Eve | Jackson | 94 |

    """

    assert MarkdownConverterTables().convert(_html) == _md
