"""A simple template engine.

Shrubbery intends to be the world's easiest template language. It
has two major advantages::

1. The user doesn't need to learn a new syntax. Templates are simply
   structural, and contain no code at all. Logic is dictated by the
   data following an implicit -- though intuitive! -- algorithm.

2. Templates don't have to be valid HTML/XHTML. Shrubbery uses the
   wonderful BeautifulSoup module for the heavy lifting, and can
   handle templates with broken HTML.
"""

from template import Template
