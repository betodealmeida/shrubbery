from shrubbery.template import Template

template = Template("""<html>
<head> <title>{title}</title> </head>

<body> <h1>{title}</h1>

    <div id="{entry.id}"> <h2>{entry.title}</h2>
        <div class="{entry.content.type}">{entry.content.content}</div>
        <p class="footnote">Updated on {entry.updated}</p>
        <ul>
            <li class="{entry.category}"><a href="http://example.com/{entry.category.term}">{entry.category.label}</a></li>
        </ul>
    </div>
</body>
</html>""")

data = {"entry": [{'category': [{'term': 'weblog', 'label': 'Weblog'},
                                {'term': 'python', 'label': 'Python stuff'}],
                   'content': {'content': '<p>This is my first post!</p>', 'type': 'html'},
                   'id': '1', 
                   'title': 'First post',
                   'updated': '2007-01-23T18:18:43Z'},
                  {'content': {'content': '<p>This is the second post...</p>', 'type': 'html'},
                   'id': '0', 
                   'title': 'One more post',
                   'updated': '2007-01-18T13:31:43Z'}],
        "title": "This is the title"}

print template.process(data, escape=False).prettify()
