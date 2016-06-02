from setuptools import setup


__doc__ = """
Django Admin compatible ModelInline that can be related
to the primary model on fields other than a Primary Key.
"""


setup(
    name='django-arbitrary-inline',
    version='0.1.2',
    author='James Robert',
    author_email='james@mediapredict.com',
    description='Django Admin compatible ModelInline that can be related '
                'to the primary model on fields other than a Primary Key',
    license='BSD',
    keywords='django django-admin',
    url='https://github.com/mediapredict/django_arbitrary_inline',
    packages=['arbitrary_inline'],
    long_description=__doc__,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries',
        'Topic :: Utilities',
        'Environment :: Web Environment',
    ]
)
