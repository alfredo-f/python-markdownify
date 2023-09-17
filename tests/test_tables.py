from markdownify import markdownify as md


table = """<table>
    <tr>
        <th>Firstname</th>
        <th>Lastname</th>
        <th>Age</th>
    </tr>
    <tr>
        <td>Jill</td>
        <td>Smith</td>
        <td>50</td>
    </tr>
    <tr>
        <td>Eve</td>
        <td>Jackson</td>
        <td>94</td>
    </tr>
</table>"""


table_with_html_content = """<table>
    <tr>
        <th>Firstname</th>
        <th>Lastname</th>
        <th>Age</th>
    </tr>
    <tr>
        <td><b>Jill</b></td>
        <td><i>Smith</i></td>
        <td><a href="#">50</a></td>
    </tr>
    <tr>
        <td>Eve</td>
        <td>Jackson</td>
        <td>94</td>
    </tr>
</table>"""


table_with_paragraphs = """<table>
    <tr>
        <th>Firstname</th>
        <th><p>Lastname</p></th>
        <th>Age</th>
    </tr>
    <tr>
        <td><p>Jill</p></td>
        <td><p>Smith</p></td>
        <td><p>50</p></td>
    </tr>
    <tr>
        <td>Eve</td>
        <td>Jackson</td>
        <td>94</td>
    </tr>
</table>"""


table_with_header_column = """<table>
    <tr>
        <th>Firstname</th>
        <th>Lastname</th>
        <th>Age</th>
    </tr>
    <tr>
        <th>Jill</th>
        <td>Smith</td>
        <td>50</td>
    </tr>
    <tr>
        <th>Eve</th>
        <td>Jackson</td>
        <td>94</td>
    </tr>
</table>"""


table_head_body = """<table>
    <thead>
        <tr>
            <th>Firstname</th>
            <th>Lastname</th>
            <th>Age</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Jill</td>
            <td>Smith</td>
            <td>50</td>
        </tr>
        <tr>
            <td>Eve</td>
            <td>Jackson</td>
            <td>94</td>
        </tr>
    </tbody>
</table>"""

table_missing_text = """<table>
    <thead>
        <tr>
            <th></th>
            <th>Lastname</th>
            <th>Age</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Jill</td>
            <td></td>
            <td>50</td>
        </tr>
        <tr>
            <td>Eve</td>
            <td>Jackson</td>
            <td>94</td>
        </tr>
    </tbody>
</table>"""

table_missing_head = """<table>
    <tr>
        <td>Firstname</td>
        <td>Lastname</td>
        <td>Age</td>
    </tr>
    <tr>
        <td>Jill</td>
        <td>Smith</td>
        <td>50</td>
    </tr>
    <tr>
        <td>Eve</td>
        <td>Jackson</td>
        <td>94</td>
    </tr>
</table>"""

table_body = """<table>
    <tbody>
        <tr>
            <td>Firstname</td>
            <td>Lastname</td>
            <td>Age</td>
        </tr>
        <tr>
            <td>Jill</td>
            <td>Smith</td>
            <td>50</td>
        </tr>
        <tr>
            <td>Eve</td>
            <td>Jackson</td>
            <td>94</td>
        </tr>
    </tbody>
</table>"""


def test_table():
    assert md(table) == '''

| Firstname | Lastname | Age |
| --- | --- | --- |
| Jill | Smith | 50 |
| Eve | Jackson | 94 |

'''


def test_table_with_html_content():
    assert md(table_with_html_content) == '''

| Firstname | Lastname | Age |
| --- | --- | --- |
| **Jill** | *Smith* | [50](#) |
| Eve | Jackson | 94 |

'''


def test_table_with_paragraphs():
    assert md(table_with_paragraphs) == '''

| Firstname | Lastname | Age |
| --- | --- | --- |
| Jill | Smith | 50 |
| Eve | Jackson | 94 |

'''


def test_table_with_header_column():
    assert md(table_with_header_column) == '''

| Firstname | Lastname | Age |
| --- | --- | --- |
| Jill | Smith | 50 |
| Eve | Jackson | 94 |

'''


def test_table_head_body():
    assert md(table_head_body) == '''

| Firstname | Lastname | Age |
| --- | --- | --- |
| Jill | Smith | 50 |
| Eve | Jackson | 94 |

'''


def test_table_missing_text():
    assert md(table_missing_text) == '''

|  | Lastname | Age |
| --- | --- | --- |
| Jill |  | 50 |
| Eve | Jackson | 94 |

'''


def test_table_missing_head():
    assert md(table_missing_head) == '''

|  |  |  |
| --- | --- | --- |
| Firstname | Lastname | Age |
| Jill | Smith | 50 |
| Eve | Jackson | 94 |

'''


def test_table_body():
    assert md(table_body) == '''

|  |  |  |
| --- | --- | --- |
| Firstname | Lastname | Age |
| Jill | Smith | 50 |
| Eve | Jackson | 94 |

'''
