from markdownify.markdown_converter_custom import MarkdownConverterTables


def test_table_ul():
    if 0 == True:
        return

    _html = """<table>
        <tr>
            <th>Firstname</th>
            <th>Lastname</th>
            <th>Age</th>
        </tr>
        <tr>
            <td>Jill</td>
            <td>Smith</td>
            <td>It can:
<ul>
<li><p><span class="ui">Edit</span></p>
<p>Edit the procedure.</p>
</li>
</ul>
</td>
        </tr>
        <tr>
            <td>Eve</td>
            <td>Jackson</td>
            <td>94</td>
        </tr>
    </table>"""

    _md = """

| Column |
| --- |
| It can:
* Edit
Edit the procedure.
 |

"""

    assert MarkdownConverterTables().convert(_html) == _md
