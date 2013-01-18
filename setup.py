from distutils.core import setup

long_desc = open('README.txt').read()

setup(
    name='mediamosa',
    version='0.0.1',
    author='UGent Portaal Team',
    author_email='portaal-tech@ugent.be',
    packages=['mediamosa', 'tests'],
    scripts=[],
    url='http://www.mediamosa.org',
    license='LICENSE.txt',
    description='API wrapper for MediaMosa.',
    long_description=long_desc,
    install_requires=(
        'requests>=1.0.3'
    ),
    classifiers=[
          'Development Status :: 3 - Alpha',
          'Environment :: Console',
          'Environment :: Web Environment',
          'Intended Audience :: End Users/Desktop',
          'Intended Audience :: Developers',
          'Intended Audience :: System Administrators',
          'License :: OSI Approved :: BSD License',
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: Microsoft :: Windows',
          'Operating System :: POSIX',
          'Programming Language :: Python',
          'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
          'Topic :: Multimedia :: Video',
          'Topic :: Software Development :: Libraries',
          'Topic :: Utilities'
          ],
)
