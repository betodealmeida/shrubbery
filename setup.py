RELEASE = True

from setuptools import setup, find_packages
import sys, os

classifiers = """\
Development Status :: 4 - Beta
Intended Audience :: Developers
License :: OSI Approved :: MIT License
Operating System :: OS Independent
Programming Language :: Python
Topic :: Text Processing :: Markup
"""

version = '0.3.4'

setup(name='shrubbery',
      version=version,
      description="Simple and smart template engine to generate HTML/XML",
      long_description='''\
Shrubbery is a *Smart Html Renderer Using Blocks to Bind Expressions Repeatedly*. You can also think of it as the "world's easiest templating engine": Templates hold no logic whatsoever, with nodes being repeated implicitely as needed by the replacement data.
''',
      classifiers=filter(None, classifiers.split("\n")),
      keywords='json template html xml',
      author='Roberto De Almeida',
      author_email='roberto@dealmeida.net',
      url='http://taoetc.org/46',
      download_url = "http://cheeseshop.python.org/packages/source/s/shrubbery/shrubbery-%s.tar.gz" % version,
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      test_suite = 'nose.collector',
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          # -*- Extra requirements: -*-
          "BeautifulSoup",
      ],
      entry_points="""
      # -*- Entry points: -*-
      [python.templating.engines]
      shrubbery = shrubbery.buffet:ShrubberyTemplatePlugin
      """,
      )
     
