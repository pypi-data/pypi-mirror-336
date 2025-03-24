from setuptools import setup, find_packages

setup(
    name='vikdatashift',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'psycopg2>=2.8.0',
        'cx_Oracle>=7.0.0'
    ],
)