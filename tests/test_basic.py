from shrubbery.template import Template

def test_basic():
    # Simple basic tests of substitution.
    assert str(Template("{content}").process({})) == ''
    assert str(Template("{content}").process({"content": None})) == ''
    assert str(Template("{content}").process({"content": ""})) == ''
    assert str(Template("{content}").process({"content": "Hello, World!"})) == 'Hello, World!'
    assert str(Template("{content}").process({"content": ["Hello", ",", " ", "World!"]})) == 'Hello, World!'
    assert str(Template("I {verb} {noun}.").process({"verb": "like", "noun": "Python"})) == 'I like Python.'
    assert str(Template("{var1}").process({"var1": "Hello, World!"})) == 'Hello, World!'
    assert str(Template("{var_1}").process({"var_1": "Hello, World!"})) == 'Hello, World!'


def test_nested_dict():
    # Tests using nested data and the dot idiom.
    assert str(Template("I {entry.verb} {entry.noun}.").process({"entry": {"verb": "like", "noun": "Python"}})) == \
    'I like Python.'


def test_html():
    # Testing how HTML nodes are handled.
    assert str(Template("""
        <a href="{url}">{name}</a>
    """).process(
        {"url": "http://google.com/", "name": "Google"}
    )).strip() == '<a href="http://google.com/">Google</a>'
    
    assert str(Template("""
        <a href="{url}">{name}</a>
    """).process(
        [{"url": "http://google.com/", "name": "Google"},
         {"url": "http://yahoo.com/", "name": "Yahoo!"},
    ])).strip() == '<a href="http://google.com/">Google</a><a href="http://yahoo.com/">Yahoo!</a>'

    assert str(Template("""
        <li><a href="{url}">{name}</a></li>
    """).process(
        [{"url": "http://google.com/", "name": "Google"},
         {"url": "http://yahoo.com/", "name": "Yahoo!"},
    ])).strip() == '<li><a href="http://google.com/">Google</a><a href="http://yahoo.com/">Yahoo!</a></li>'

    assert str(Template("""
        <li><a href="{entry.url}">{entry.name}</a></li>
    """).process(
        {"entry": [{"url": "http://google.com/", "name": "Google"},
                   {"url": "http://yahoo.com/", "name": "Yahoo!"},
    ]})).strip() == '<li><a href="http://google.com/">Google</a><a href="http://yahoo.com/">Yahoo!</a></li>'

    # If we want to repeat the ``<li>`` in the last example we can create a dummy attribute.
    assert str(Template("""
        <li class="{entry}"><a href="{entry.url}">{entry.name}</a></li>
    """).process(
        {"entry": [{"url": "http://google.com/", "name": "Google"},
                   {"url": "http://yahoo.com/", "name": "Yahoo!"},
    ]})).strip() == '<li><a href="http://google.com/">Google</a></li><li><a href="http://yahoo.com/">Yahoo!</a></li>'


def test_meta_replacements():
    # Nodes in the replacements should be preserved.
    assert str(Template("{a} and {b}").process({"a": "{b}", "b": "foo"})) == '{b} and foo'
    assert str(Template("{a} and {b}").process({"a": "foo", "b": "{a}"})) == 'foo and {a}'


def test_ampersand_escaping():
    # Ampersands should not be escaped.
    assert str(Template("<p>{http://example.com/?a=1&b=2}</p>")) == '<p>{http://example.com/?a=1&b=2}</p>'
    assert str(Template("<p>2006&mdash;2007</p>")) == '<p>2006&mdash;2007</p>'


def test_misc():
    assert str(Template("""
        <html>I love {a} a lot, it's {b}!</html>
    """).process(
        {"a": "sushi", "b": "nice"}
    )).strip() == "<html>I love sushi a lot, it's nice!</html>"

    assert str(Template("""
        <html>I love {a} a lot, it's <span>{b}</span>!</html>
    """).process(
        {"a": "sushi", "b": "nice"}
    )).strip() == "<html>I love sushi a lot, it's <span>nice</span>!</html>"

    assert str(Template("""
        <html>I love {a} a lot, it's {b}!</html>
    """).process(
        {"a": "{b}", "b": "nice"}
    )).strip() == "<html>I love {b} a lot, it's nice!</html>"

def test_escape():
    assert str(Template("""
        <p>{content}</p>
    """).process(
        {"content": "This is content <em>with</em> HTML."}
    )).strip() == "<p>This is content &lt;em&gt;with&lt;/em&gt; HTML.</p>"

    assert str(Template("""
        <p>{content}</p>
    """).process(
        {"content": "This is content <em>with</em> HTML."},
        escape=False
    )).strip() == "<p>This is content <em>with</em> HTML.</p>"

def test_objects():
    class container(object): pass
    entry = container()
    entry.verb = "like"
    entry.noun = "Python"
    assert str(Template("I {entry.verb} {entry.noun}.").process({"entry": entry})) == \
    'I like Python.'

def test_index():
    assert str(Template("""
        <georss:point>{geometry.coordinates[0]} {geometry.coordinates[1]}</georss:point>
    """).process(
        {"geometry": { "type": "Point", "coordinates": [45.256, -71.92] }}
    )).strip() == "<georss:point>45.256 -71.92</georss:point>"

    template = Template("""<feed><updated>{entries[0].updated}</updated><entry><id>{entries.id}</id><updated>{entries.updated}</updated></entry></feed>""")
    assert str(template.process({"entries": [{"updated": "today", "id": 1}, {"updated": "yesterday", "id": 0}]})) == \
    '<feed><updated>today</updated><entry><id>1</id><updated>today</updated></entry><entry><id>0</id><updated>yesterday</updated></entry></feed>'

    template = Template("""<feed><updated>{members[0].entity.updated}</updated><entry><id>{members.id}</id><updated>{members.entity.updated}</updated></entry></feed>""")
    assert str(template.process({"members": [{'entity': {"updated": "today"}, "id": 1}, {'entity': {"updated": "yesterday"}, "id": 0}]})) == \
    '<feed><updated>today</updated><entry><id>1</id><updated>today</updated></entry><entry><id>0</id><updated>yesterday</updated></entry></feed>'
    template = Template("""<feed><updated>{entries[0].entity.updated}</updated><entry><id>{entries.id}</id><updated>{entries.entity.updated}</updated></entry></feed>""")
    assert str(template.process({"entries": [{'entity': {"updated": "today"}, "id": 1}, {'entity': {"updated": "yesterday"}, "id": 0}]})) == \
    '<feed><updated>today</updated><entry><id>1</id><updated>today</updated></entry><entry><id>0</id><updated>yesterday</updated></entry></feed>'

def test_error():
    assert str(Template("""
        <p class="{bar}">{foo}</p>
    """).process(
        {'foo': 42, 'bar': 'test'}
    )).strip() == """<p class="test">42</p>"""
    assert str(Template("""
        <p class="{bar}">{foo}</p>
    """).process(
        {'foo': range(4), 'bar': 'test'}
    )).strip() == """<p class="test">0</p><p class="test">1</p><p class="test">2</p><p class="test">3</p>"""
