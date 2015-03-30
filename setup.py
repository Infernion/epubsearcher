
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='epubseacher',
    version='0.2',
    packages=['', 'epubsearch', 'epubsearch.morpho_engines', 'epubsearch.search_engines'],
    url='https://bitbucket.org/Infernion/epubseacher/overview',
    license='',
    author='infernion',
    author_email='sergiykhalimon@gmail.com',
    description='Search word in epub publications',
    install_requires=['whoosh', 'pymorphy2', 'lxml']
)
