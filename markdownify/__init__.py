from bs4 import BeautifulSoup, NavigableString, Comment, Doctype
from textwrap import fill
import re
import six


convert_heading_re = re.compile(r'convert_h(\d+)')
line_beginning_re = re.compile(r'^', re.MULTILINE)
whitespace_re = re.compile(r'[\t ]+')
all_whitespace_re = re.compile(r'[\s]+')
html_heading_re = re.compile(r'h([1-6])')


# Heading styles
ATX = 'atx'
ATX_CLOSED = 'atx_closed'
UNDERLINED = 'underlined'
SETEXT = UNDERLINED

# Newline style
SPACES = 'spaces'
BACKSLASH = 'backslash'

# Strong and emphasis style
ASTERISK = '*'
UNDERSCORE = '_'

TAGS_IGNORE_WHEN_CONVERTING_TEXT = [
    "span",
    "div",
    "head",
    "thead",
    "tbody",
]

TAGS_DONT_SURROUND_WITH_NAME = [
    "a",
    "b",
    "strong",
    "i",
    "p",
]


def chomp(text):
    """
    If the text in an inline tag like b, a, or em contains a leading or trailing
    space, strip the string and return a space as suffix of prefix, if needed.
    This function is used to prevent conversions like
        <b> foo</b> => ** foo**
    """
    prefix = ' ' if text and text[0] == ' ' else ''
    suffix = ' ' if text and text[-1] == ' ' else ''
    text = text.strip()
    return (prefix, suffix, text)


def _todict(obj):
    return dict((k, getattr(obj, k)) for k in dir(obj) if not k.startswith('_'))


def is_nested_node(el):
    return el is not None and el.name in [
        'ol',
        'ul',
        'li',
        'table',
        'thead',
        'tbody',
        'tfoot',
        'tr',
        'td',
        'th',
    ]


class ElementInlineWithMarkup:
    def __init__(
        self,
        el,
        text,
        markup,
    ):
        self.el = el
        self.text = text
        self.markup = markup

    def convert(self):
        prefix, suffix, text = chomp(self.text)
        if not text:
            return ''
        return '%s%s%s%s%s' % (prefix, self.markup, text, self.markup, suffix)


class ElementCode:
    def __init__(
        self,
        el,
        text,
        markup,
    ):
        self.el = el
        self.text = text
        self.markup = markup

    def convert(self):
        if self.el.parent.name == 'pre':
            return self.text

        return ElementInlineWithMarkup(
            el=self.el,
            text=self.text,
            markup=self.markup,
        ).convert()


class ElementList:
    def __init__(
        self,
        el,
        text,
        bullets,
    ):
        self.el = el
        self.text = text
        self.bullets = bullets

    def indent(self, text, level):
        return line_beginning_re.sub('\t' * level, text) if text else ''

    def convert(self):
        # Converting a list to inline is undefined.
        # Ignoring convert_to_inline for list.

        nested = False
        before_paragraph = False
        if self.el.next_sibling and self.el.next_sibling.name not in ['ul', 'ol']:
            before_paragraph = True

        el = self.el
        while el:
            if el.name == 'li':
                nested = True
                break
            el = el.parent
        if nested:
            # remove trailing newline if nested
            return '\n' + self.indent(self.text, 1).rstrip()
        return self.text + ('\n' if before_paragraph else '')

    def convert_li(self):
        parent = self.el.parent
        if parent is not None and parent.name == 'ol':
            if parent.get("start"):
                start = int(parent.get("start"))
            else:
                start = 1
            bullet = '%s.' % (start + parent.index(self.el))
        else:
            depth = -1
            el = self.el
            while el:
                if el.name == 'ul':
                    depth += 1
                el = el.parent
            bullet = self.bullets[depth % len(self.bullets)]
        return '%s %s\n' % (bullet, (self.text or '').strip())


class ElementA:
    def __init__(
        self,
        el,
        text,
        autolinks: bool,
        default_title: bool,
    ):
        self.el = el
        self.text = text
        self.autolinks = autolinks
        self.default_title = default_title

    def convert(self):
        prefix, suffix, text = chomp(self.text)
        if not text:
            return ''
        href = self.el.get('href')
        title = self.el.get('title')
        # For the replacement see #29: text nodes underscores are escaped
        if (self.autolinks
                and text.replace(r'\_', '_') == href
                and not title
                and not self.default_title):
            # Shortcut syntax
            return '<%s>' % href
        if self.default_title and not title:
            title = href
        title_part = ' "%s"' % title.replace('"', r'\"') if title else ''
        return '%s[%s](%s%s)%s' % (prefix, text, href, title_part, suffix) if href else text


class ElementTable:
    def __init__(
        self,
        el,
        text,
    ):
        self.el = el
        self.text = text

    def convert_table(self):
        return '\n\n' + self.text + '\n'

    def convert_td(self):
        return ' ' + self.text + ' |'

    def convert_th(self):
        return ' ' + self.text + ' |'

    def convert_tr(self):
        cells = self.el.find_all(['td', 'th'])
        is_headrow = all([cell.name == 'th' for cell in cells])
        overline = ''
        underline = ''
        if is_headrow and not self.el.previous_sibling:
            # first row and is headline: print headline underline
            underline += '| ' + ' | '.join(['---'] * len(cells)) + ' |' + '\n'
        elif (not self.el.previous_sibling
              and (self.el.parent.name == 'table'
                   or (self.el.parent.name == 'tbody'
                       and not self.el.parent.previous_sibling))):
            # first row, not headline, and:
            # - the parent is table or
            # - the parent is tbody at the beginning of a table.
            # print empty headline above this row
            overline += '| ' + ' | '.join([''] * len(cells)) + ' |' + '\n'
            overline += '| ' + ' | '.join(['---'] * len(cells)) + ' |' + '\n'
        return overline + '|' + self.text + '\n' + underline


class ElementHeader:
    def __init__(
        self,
        el,
        text,
        convert_as_inline,
        heading_style,
    ):
        self.el = el
        self.text = text
        self.convert_as_inline = convert_as_inline
        self.heading_style = heading_style

        self.header_number = int(
            html_heading_re.match(self.el.name).group(1)
        )

    def underline(self, text, pad_char):
        text = (text or '').rstrip()
        return '%s\n%s\n\n' % (text, pad_char * len(text)) if text else ''

    def convert(self):
        if self.convert_as_inline:
            return self.text

        style = self.heading_style.lower()
        text = self.text.rstrip()
        if style == UNDERLINED and self.header_number <= 2:
            line = '=' if self.header_number == 1 else '-'
            return self.underline(text, line)
        hashes = '#' * self.header_number
        if style == ATX_CLOSED:
            return '%s %s %s\n\n' % (hashes, text, hashes)
        return '%s %s\n\n' % (hashes, text)


class ElementBlockquote:
    def __init__(
        self,
        el,
        text,
        convert_as_inline,
    ):
        self.el = el
        self.text = text
        self.convert_as_inline = convert_as_inline

    def convert(self):
        if self.convert_as_inline:
            return self.text

        return (
            '\n' + (line_beginning_re.sub('> ', self.text) + '\n\n')
            if self.text else ''
        )


class ElementBr:
    def __init__(
        self,
        el,
        text,
        convert_as_inline,
        newline_style,
    ):
        self.el = el
        self.text = text
        self.convert_as_inline = convert_as_inline
        self.newline_style = newline_style

    def convert(self):
        if self.convert_as_inline:
            return ""

        if self.newline_style.lower() == BACKSLASH:
            return '\\\n'
        else:
            return '  \n'


class ElementImg:
    def __init__(
        self,
        el,
        text,
        convert_as_inline,
        keep_inline_images_in,
    ):
        self.el = el
        self.text = text
        self.convert_as_inline = convert_as_inline
        self.keep_inline_images_in = keep_inline_images_in

    def convert(self):
        alt = self.el.attrs.get('alt', None) or ''
        src = self.el.attrs.get('src', None) or ''
        title = self.el.attrs.get('title', None) or ''
        title_part = ' "%s"' % title.replace('"', r'\"') if title else ''
        if (self.convert_as_inline
                and self.el.parent.name not in self.keep_inline_images_in):
            return alt

        return '![%s](%s%s)' % (alt, src, title_part)


class ElementP:
    def __init__(
        self,
        el,
        text,
        convert_as_inline,
        wrap,
        wrap_width,
    ):
        self.el = el
        self.text = text
        self.convert_as_inline = convert_as_inline
        self.wrap = wrap
        self.wrap_width = wrap_width

    def convert(self):
        if self.convert_as_inline:
            return self.text
        if self.wrap:
            text = fill(self.text,
                        width=self.wrap_width,
                        break_long_words=False,
                        break_on_hyphens=False)
        else:
            text = self.text
        return '%s\n\n' % text if text else ''


class ElementPre:
    def __init__(
        self,
        el,
        text,
        convert_as_inline,
        code_language,
        code_language_callback,
    ):
        self.el = el
        self.text = text
        self.convert_as_inline = convert_as_inline
        self.code_language = code_language
        self.code_language_callback = code_language_callback

    def convert(self):
        if not self.text:
            return ''

        if self.code_language_callback:
            code_language = self.code_language_callback(self.el) or self.code_language
        else:
            code_language = self.code_language

        return '\n```%s\n%s\n```\n' % (code_language, self.text)


def process_text(el, escape_asterisks, escape_underscores):
    text = six.text_type(el) or ''

    # dont remove any whitespace when handling pre or code in pre
    if not (el.parent.name == 'pre'
            or (el.parent.name == 'code'
                and el.parent.parent.name == 'pre')):
        text = whitespace_re.sub(' ', text)

    if el.parent.name != 'code' and el.parent.name != 'pre':
        if not text:
            text = ''
        if escape_asterisks:
            text = text.replace('*', r'\*')
        if escape_underscores:
            text = text.replace('_', r'\_')

    # remove trailing whitespaces if any of the following condition is true:
    # - current text node is the last node in li
    # - current text node is followed by an embedded list
    if (el.parent.name == 'li'
            and (not el.next_sibling
                 or el.next_sibling.name in ['ul', 'ol'])):
        text = text.rstrip()

    return text


def extract_whitespace_children(node):
    for el in node.children:
        # Only extract (remove) whitespace-only text node if any of the
        # conditions is true:
        # - el is the first element in its parent
        # - el is the last element in its parent
        # - el is adjacent to an nested node
        can_extract = (
            not el.previous_sibling
            or not el.next_sibling
            or is_nested_node(el.previous_sibling)
            or is_nested_node(el.next_sibling)
        )

        is_whitespace = (
            isinstance(el, NavigableString)
            and six.text_type(el).strip() == ''
        )

        if (
            can_extract
            and is_whitespace
        ):
            el.extract()


def process_tag(
    node,
    convert_as_inline,
    options,
    children_only=False,
    surround_with_tag_name=False,
):
    text = ''

    # markdown headings or cells can't include
    # block elements (elements w/newlines)
    isHeading = html_heading_re.match(node.name) is not None
    isCell = node.name in ['td', 'th']
    convert_children_as_inline = convert_as_inline

    if not children_only and (isHeading or isCell):
        convert_children_as_inline = True

    if is_nested_node(node):
        extract_whitespace_children(node)

    # Convert the children first
    for el in node.children:
        if isinstance(el, Comment) or isinstance(el, Doctype):
            continue
        elif isinstance(el, NavigableString):
            text += process_text(
                el,
                escape_asterisks=options['escape_asterisks'],
                escape_underscores=options['escape_underscores'],
            )
        else:
            text += process_tag(
                node=el,
                convert_as_inline=convert_children_as_inline,
                options=options,
            )

    tag = node.name.lower()
    strip = options['strip']
    convert = options['convert']
    if strip is not None:
        should_convert_tag = tag not in strip
    elif convert is not None:
        should_convert_tag = tag in convert
    else:
        should_convert_tag = True

    if (
        not children_only
        and node.name not in TAGS_IGNORE_WHEN_CONVERTING_TEXT
        and should_convert_tag
    ):
        if node.name == "a":
            text = ElementA(
                el=node,
                text=text,
                autolinks=options['autolinks'],
                default_title=options['default_title'],
            ).convert()

        elif node.name in (
            "b",
            "strong",
        ):
            text = ElementInlineWithMarkup(
                el=node,
                text=text,
                markup=2 * options['strong_em_symbol'],
            ).convert()

        elif node.name == "blockquote":
            text = ElementBlockquote(
                el=node,
                text=text,
                convert_as_inline=convert_as_inline
            ).convert()

        elif node.name == "br":
            text = ElementBr(
                el=node,
                text=text,
                convert_as_inline=convert_as_inline,
                newline_style=options['newline_style'],
            ).convert()

        elif node.name in (
            "code",
            "kbd",
            "samp",
        ):
            text = ElementCode(
                el=node,
                text=text,
                markup='`',
            ).convert()

        elif node.name in (
            "del",
            "s",
        ):
            text = ElementInlineWithMarkup(
                el=node,
                text=text,
                markup='~~',
            ).convert()

        elif node.name == "em":
            text = ElementInlineWithMarkup(
                el=node,
                text=text,
                markup=options['strong_em_symbol'],
            ).convert()

        elif node.name in (
            f"h{i}"
            for i in range(1, 7)
        ):
            text = ElementHeader(
                el=node,
                text=text,
                convert_as_inline=convert_as_inline,
                heading_style=options['heading_style'],
            ).convert()

        elif node.name == "hr":
            text = '\n\n---\n\n'

        elif node.name == "i":
            text = ElementInlineWithMarkup(
                el=node,
                text=text,
                markup=options['strong_em_symbol'],
            ).convert()

        elif node.name == "img":
            text = ElementImg(
                el=node,
                text=text,
                convert_as_inline=convert_as_inline,
                keep_inline_images_in=options['keep_inline_images_in'],
            ).convert()

        elif node.name == "li":
            text = ElementList(
                el=node,
                text=text,
                bullets=options['bullets'],
            ).convert_li()

        elif node.name in (
            "list",
            "ol",
            "ul",
        ):
            text = ElementList(
                el=node,
                text=text,
                bullets=options['bullets'],
            ).convert()

        elif node.name == "p":
            text = ElementP(
                el=node,
                text=text,
                convert_as_inline=convert_as_inline,
                wrap=options['wrap'],
                wrap_width=options['wrap_width'],
            ).convert()

        elif node.name == "pre":
            text = ElementPre(
                el=node,
                text=text,
                convert_as_inline=convert_as_inline,
                code_language=options['code_language'],
                code_language_callback=options['code_language_callback'],
            ).convert()

        elif node.name == "sub":
            text = ElementInlineWithMarkup(
                el=node,
                text=text,
                markup=options['sub_symbol'],
            ).convert()

        elif node.name == "sup":
            text = ElementInlineWithMarkup(
                el=node,
                text=text,
                markup=options['sup_symbol'],
            ).convert()

        elif node.name == "table":
            text = process_tag_table(
                node=node,
                convert_as_inline=True,
                options=options,
            )

    if (
        surround_with_tag_name
        and node.name not in TAGS_DONT_SURROUND_WITH_NAME
    ):
        text = '<%s>%s</%s>' % (node.name, text, node.name)

    return text


def process_tag_table(
    node,
    convert_as_inline,
    options,
    children_only=False,
):
    text = ''

    # markdown headings or cells can't include
    # block elements (elements w/newlines)
    isHeading = html_heading_re.match(node.name) is not None
    isCell = node.name in ['td', 'th']
    convert_children_as_inline = convert_as_inline

    if not children_only and (isHeading or isCell):
        convert_children_as_inline = True

    if is_nested_node(node):
        extract_whitespace_children(node)

    # Convert the children first
    for el in node.children:
        if isinstance(el, Comment) or isinstance(el, Doctype):
            continue
        elif isinstance(el, NavigableString):
            text += process_text(
                el,
                escape_asterisks=options['escape_asterisks'],
                escape_underscores=options['escape_underscores'],
            )
        else:
            text += process_tag_table(
                node=el,
                convert_as_inline=convert_children_as_inline,
                options=options,
            )

    tag = node.name.lower()
    strip = options['strip']
    convert = options['convert']
    if strip is not None:
        should_convert_tag = tag not in strip
    elif convert is not None:
        should_convert_tag = tag in convert
    else:
        should_convert_tag = True

    if (
        not children_only
        and node.name not in TAGS_IGNORE_WHEN_CONVERTING_TEXT
        and should_convert_tag
    ):
        if node.name == "table":
            text = ElementTable(
                el=node,
                text=text,
            ).convert_table()

        elif node.name == "td":
            text = ElementTable(
                el=node,
                text=text,
            ).convert_td()

        elif node.name == "th":
            text = ElementTable(
                el=node,
                text=text,
            ).convert_th()

        elif node.name == "tr":
            text = ElementTable(
                el=node,
                text=text,
            ).convert_tr()

        else:
            text = process_tag(
                node=node,
                convert_as_inline=True,
                options=options,
                surround_with_tag_name=True,
            )

            text = text.replace(
                "\n",
                "<br>",
            )

    return text


class MarkdownConverter(object):

    class DefaultOptions:
        autolinks = True
        bullets = '*+-'  # An iterable of bullet types.
        code_language = ''
        code_language_callback = None
        convert = None
        default_title = False
        escape_asterisks = True
        escape_underscores = True
        heading_style = UNDERLINED
        keep_inline_images_in = []
        newline_style = SPACES
        strip = None
        strong_em_symbol = ASTERISK
        sub_symbol = ''
        sup_symbol = ''
        wrap = False
        wrap_width = 80

    class Options(DefaultOptions):
        pass

    def __init__(self, **options):
        # Create an options dictionary. Use DefaultOptions as a base so that
        # it doesn't have to be extended.
        self.options = _todict(self.DefaultOptions)
        self.options.update(_todict(self.Options))
        self.options.update(options)
        if self.options['strip'] is not None and self.options['convert'] is not None:
            raise ValueError('You may specify either tags to strip or tags to'
                             ' convert, but not both.')

    def convert(self, html):
        return process_tag(
            BeautifulSoup(html, 'html.parser'),
            convert_as_inline=False,
            children_only=True,
            options=self.options,
        )


def markdownify(html, **options):
    return MarkdownConverter(**options).convert(html)
