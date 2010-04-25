from os.path import abspath, dirname, join as pjoin
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

fn = abspath(pjoin(dirname(__file__), 'README'))
fp = open(fn, 'r')
long_description = fp.read()
fp.close()

setup(
    name='aino-jstools',
    version='0.1.0.0',
    url='http://bitbucket.org/aino/aino-jstools/',
    license='BSD',
    author='Mikko Hellsing',
    author_email='mikko@aino.se',
    description='JavaScript tools for Django',
    long_description=long_description,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: JavaScript',
        'Framework :: Django',
    ],
    packages=[
        'jstools',
        'jstools.conf',
        'jstools.management',
        'jstools.management.commands',
        'jstools.templatetags',
    ],
    data_files=[('jstools/templates/jstools', ['jstools/templates/jstools/jshelper.js']),
                ('jstools/compiler', ['jstools/compiler/README',
                                      'jstools/compiler/COPYING',
                                      'jstools/compiler/compiler.jar'])],
    zip_safe=True,
    platforms='any',
)
