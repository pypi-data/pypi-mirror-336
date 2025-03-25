from setuptools import setup, find_packages

setup(
    name='vikdatashift',
    version='0.2.0',
    packages=find_packages(),
    install_requires=[
        'psycopg2>=2.8.0',
        'cx_Oracle>=7.0.0'
    ],
    long_description= open('README.md', 'r').read(),
    long_description_content_type='text/markdown',
)