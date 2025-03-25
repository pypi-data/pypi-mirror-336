from setuptools import setup

with open("README.md", "r", encoding='utf-8') as f:
    readme = f.read()

setup(name='pygeometry2d',
    version='1.1.3',
    license='MIT License',
    author='Leonardo Pires Batista',
    long_description=readme,
    long_description_content_type="text/markdown",
    url = 'https://github.com/leonardopbatista/pygeometry2d',
    project_urls = {
        "Documentation": "https://pygeometry2d.readthedocs.io/",
        'Source code': 'https://github.com/leonardopbatista/pygeometry2d',
        'Download': 'https://github.com/leonardopbatista/pygeometry2d'
    },
    author_email='leonardopbatista98@gmail.com',
    keywords='geometry 2d',
    description=u'2D Geometry Library',
    packages=['pygeometry2d'],
    install_requires=[],)