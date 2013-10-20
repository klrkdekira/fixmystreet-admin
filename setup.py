import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'pyramid',
    'pyramid_jinja2',
    'SQLAlchemy',
    'transaction',
    'pyramid_tm',
    'pyramid_debugtoolbar',
    'zope.sqlalchemy',
    'waitress',
    'pyramid_formalchemy',
    'pyramid_fanstatic',
    'pyramid_beaker',
    'pyramid_chameleon',
    'fa.jquery',
    'gevent',
    'wtforms',
    'gunicorn',
    'sqlsoup',
    ]

setup(name='admin',
      version='0.0',
      description='admin',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='',
      author_email='',
      url='',
      keywords='web wsgi bfg pylons pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='admin',
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = admin:main
      [console_scripts]
      """,
      )
