from distutils.core import setup

long_desc = open('README.txt').read()

setup(
    name='MediaMosa',
    version='0.0.1',
    author='UGent Portaal Team',
    author_email='portaal-tech@ugent.be',
    packages=['mediamosa', 'tests'],
    scripts=[],
    url='http://www.mediamosa.org',
    license='LICENSE.txt',
    description='API wrapper for MediaMosa.',
    long_description=long_desc
)