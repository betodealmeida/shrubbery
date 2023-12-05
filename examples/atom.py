from shrubbery.template import Template

template = Template("""<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">

    <title>{title}</title>
    <link rel="self" href="{ROOT}atom"/>
    <updated>{entries[0].updated}</updated>
    <author>
        <name>{author.name}</name>
        <email>{author.email}</email>
        <uri>{author.uri}</uri>
    </author>
    <id>{ROOT}</id>

    <entry>
        <id>{entries.href}</id>
        <title>{entries.title}</title>
        <updated>{entries.updated}</updated>

        <content type="xhtml">
            <div xmlns="http://www.w3.org/1999/xhtml">
                {entries.content}
            </div>
        </content>
        <link rel="alternate" href="{entries.href}"/>
        <summary>{entries.summary}</summary>

        <category term="{entries.category}"></category>
        <published>{entries.published}</published>
    </entry>
</feed>""")

data = {'title'  : 'A simple Atom feed',
        'ROOT'   : 'http://example.com/',
        'author' : {'name': 'John Doe', 'email': 'jdoe@example.com', 'uri': 'http://djoe.example.com/'},
        'entries': [{
            'href'     : 'http://example.com/1',
            'title'    : 'Second post!',
            'updated'  : '2007-08-10T13:29:14Z',
            'content'  : '<p>This is my second post!</p>',
            'summary'  : 'My second post',
            'category' : 'blog',
            'published': '2007-08-10T13:29:14Z'}, {

            'href'     : 'http://example.com/0',
            'title'    : 'First post!',
            'updated'  : '2007-08-10T13:28:04Z',
            'content'  : '<p>This is my first post!</p>',
            'summary'  : 'My first post',
            'category' : ['blog', 'test'],
            'published': '2007-08-10T13:28:04Z'}]}
                
print template.process(data, escape=False)
