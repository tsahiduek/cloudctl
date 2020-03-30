from setuptools import setup, find_packages

setup(
    # mandatory
    name='cloudctl',
    # mandatory
    version='0.1',
    # mandatory
    author_email='tsahiduek@gmail.com',
    packages=['cloudctl'],
    package_data={},
    install_requires=['pylint', 'boto3', 'click', 'tabulate'],
    entry_points={
        'console_scripts': ['cloudctl = cloudctl.cloudctl:start']
    }
)
