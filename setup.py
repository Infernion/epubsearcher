from distutils.core import setup

setup(
    name='epubsearcher',
    version='0.3',
    packages=['epubsearcher', 'epubsearcher.epubsearch', 'epubsearcher.epubsearch.morpho_engines',
              'epubsearcher.epubsearch.search_engines'],
    url='https://bitbucket.org/Infernion/epubsearcher/overview',
    license='MIT',
    author='Sergiy Khalymon',
    author_email='sergiykhalimon@gmail.com',
    description='Search selected word in epub book.'
)
