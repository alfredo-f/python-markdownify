from markdownify import markdownify as md


nested_uls = """
    <ul>
        <li>1
            <ul>
                <li>a
                    <ul>
                        <li>I</li>
                        <li>II</li>
                        <li>III</li>
                    </ul>
                </li>
                <li>b</li>
                <li>c</li>
            </ul>
        </li>
        <li>2</li>
        <li>3</li>
    </ul>"""

nested_ols = """
    <ol>
        <li>1
            <ol>
                <li>a
                    <ol>
                        <li>I</li>
                        <li>II</li>
                        <li>III</li>
                    </ol>
                </li>
                <li>b</li>
                <li>c</li>
            </ol>
        </li>
        <li>2</li>
        <li>3</li>
    </ul>"""


def test_ol():
    assert md('<ol><li>a</li><li>b</li></ol>') == '''\
1. a
2. b
'''
    assert md('<ol start="3"><li>a</li><li>b</li></ol>') == '''\
3. a
4. b
'''


def test_nested_ols():
    assert md(nested_ols) == '''
1. 1
\t1. a
\t\t1. I
\t\t2. II
\t\t3. III
\t2. b
\t3. c
2. 2
3. 3
'''


def test_ul():
    assert md('<ul><li>a</li><li>b</li></ul>') == '''* a
* b
'''
    assert md("""<ul>
     <li>
             a
     </li>
     <li> b </li>
     <li>   c
     </li>
 </ul>""") == '''* a
* b
* c
'''


def test_inline_ul():
    assert md('<p>foo</p><ul><li>a</li><li>b</li></ul><p>bar</p>') == '''foo

* a
* b

bar

'''


def test_nested_uls():
    """
    Nested ULs should alternate bullet characters.

    """
    assert md(nested_uls) == '''
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
    assert md(nested_uls, bullets='-') == '''
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
    assert md('<ul><li>foo <a href="#">bar</a></li><li>foo bar  </li><li>foo <b>bar</b>   <i>space</i>.</ul>') == '''* foo [bar](#)
* foo bar
* foo **bar** *space*.
'''
