from markdownify import markdownify as md


nested_dls = """
    <dl>
        <li>1
            <dl>
                <li>a
                    <dl>
                        <li>I</li>
                        <li>II</li>
                        <li>III</li>
                    </dl>
                </li>
                <li>b</li>
                <li>c</li>
            </dl>
        </li>
        <li>2</li>
        <li>3</li>
    </dl>"""


def test_dl():
    assert md('<dl><li>a</li><li>b</li></dl>') == '''* a
* b
'''
    assert md("""<dl>
     <li>
             a
     </li>
     <li> b </li>
     <li>   c
     </li>
 </dl>""") == '''* a
* b
* c
'''


def test_inline_dl():
    assert md('<p>foo</p><dl><li>a</li><li>b</li></dl><p>bar</p>') == '''foo

* a
* b

bar

'''


def test_nested_dls():
    """
    Nested DLs should alternate bullet characters.

    """
    assert md(nested_dls) == '''
* 1
\t+ a
\t\t- I
\t\t- II
\t\t- III
\t+ b
\t+ c
* 2
* 3
'''


def test_bullets():
    assert md(nested_dls, bullets='-') == '''
- 1
\t- a
\t\t- I
\t\t- II
\t\t- III
\t- b
\t- c
- 2
- 3
'''


def test_li_text():
    assert md('<dl><li>foo <a href="#">bar</a></li><li>foo bar  </li><li>foo <b>bar</b>   <i>space</i>.</dl>') == '''* foo [bar](#)
* foo bar
* foo **bar** *space*.
'''
