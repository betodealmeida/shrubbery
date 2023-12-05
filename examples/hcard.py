from shrubbery.template import Template

template = Template("""<div class="vcard">
    <img style="float:left; margin-right:4px" src="{photourl}" alt="photo" class="photo"/>

    <a class="url fn n" href="{url}">  <span class="givenname">{givenname}</span>
        <span class="additionalname">{additionalname}</span>

        <span class="familyname">{familyname}</span>
    </a>

    <div class="org">{org}</div>

    <a class="email" href="mailto:{email}">{email}</a>

    <div class="adr">
        <div class="streetaddress">{streetaddress}</div>

        <span class="locality">{locality}</span>, 
        <span class="region">{region}</span>, 
        <span class="postalcode">{postalcode}</span>

        <span class="countryname">{countryname}</span>
    </div>

    <div class="tel">{tel}</div>

    <ul><li class="{im}"><a class="url" href="{im.href}">{im.protocol}</a></li></ul>
</div>""")

data = {'additionalname': 'Ferreira',
        'countryname': 'Brazil',
        'email': 'roberto@dealmeida.net',
        'familyname': 'De Almeida',
        'givenname': 'Roberto Antonio',
        'im': [{'href': 'jabber:roberto@dealmeida.net', 'protocol': 'Jabber'},
               {'href': 'skype:robertodealmeida', 'protocol': 'Skype'}],
        'locality': 'Cachoeira Paulista',
        'org': 'CPTEC/INPE',
        'photourl': 'http://dealmeida.net/roberto-t.jpg',
        'postalcode': '12630-000',
        'region': 'SP',
        'streetaddress': 'Rod. Pres. Dutra km 40',
        'tel': '+55 12 3456 7890',
        'url': 'http://dealmeida.net'}

print template.process(data).prettify()
