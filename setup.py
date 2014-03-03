import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

setup(
    name='kaaterskill',
    version='0.0.8',
    packages=['kaaterskill', 'kaaterskill.blog'],
    include_package_data=True,
    license='BSD License',
    description='A minimal hypermedia blog engine based on the DocJSON document format.',
    long_description=README,
    author='Michael Paulus',
    author_email='mdpaulus@gmail.com',
    install_requires=['django', 
                      'djangorestframework', 
                      'django-model-utils',
                      'djangorestframework-docjson'],
    dependency_links=['https://github.com/mikedrawback/djangorestframework-docjson/tarball/master#egg=djangorestframework-docjson-0.0.1'],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
