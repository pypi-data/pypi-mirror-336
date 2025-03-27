
from setuptools import setup, find_packages
try:
    from conn_utils.package._package import __name__, __version__
except Exception as e:
    __name__ = 'conn_utils'
    __version__ = '1.6.10'
    pass

setup(
    name=__name__,
    version=__version__,
    packages=find_packages(),
    description=__name__,
    long_description_content_type='text/plain',
    url='https://upload.pypi.org/legacy/',
    download_url='https://upload.pypi.org/legacy/',
    project_urls={'Documentation': 'https://upload.pypi.org/legacy/'},
    author='Zhang Yong',
    author_email='zyong@yubitusoft.com',
)
