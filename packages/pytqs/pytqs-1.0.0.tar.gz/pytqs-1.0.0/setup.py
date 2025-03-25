from setuptools import setup

with open("README.md", "r", encoding='utf-8') as f:
    readme = f.read()

setup(name='pytqs',
    version='1.0.0',
    author='Leonardo Pires Batista',
    long_description=readme,
    long_description_content_type="text/markdown",
    url = 'https://github.com/leonardopbatista/pytqs',
    project_urls = {
        'Código fonte': 'https://github.com/leonardopbatista/pytqs',
        'Download': 'https://github.com/leonardopbatista/pytqs'
    },
    author_email='leonardopbatista98@gmail.com',
    keywords='tqs python',
    description=u'Bibliteca para facilitar a integração do Python com o TQS',
    packages=['pytqs','TQS'],
    install_requires=[
        'ezdxf==1.2.0',
        'fonttools==4.56.0',
        'numpy==2.2.4',
        'pillow==11.1.0',
        'pygeometry2d==1.1.3',
        'pygments==2.19.1',
        'PyMuPDF==1.23.26',
        'PyMuPDFb==1.23.22',
        'pyparsing==3.2.2',
        'typing_extensions==4.12.2'
        ],
    )

