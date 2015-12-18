try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'An implementation a basic PCFG parser/scorer in Python',
    'author': 'Arthur Tilley',
    'url': 'https://github.com/aetilley/pcfg',
    'author_email': 'aetilley@gmail.com',
    'version': '0.1',
    'install requires': ['nose'],
    'packages': ['pcfg'],
    'scripts': [],
    'name': 'pcfg'
}

setup(**config)
