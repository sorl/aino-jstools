from os.path import abspath, dirname, join as pjoin

try:
    from setuptools import setup, find_packages
except ImportError:
    import ez_setup
    ez_setup.use_setuptools()
    from setuptools import setup, find_packages


fn = abspath(pjoin(dirname(__file__), 'README.rst'))
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
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
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
)
