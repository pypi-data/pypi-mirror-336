from setuptools import setup, find_packages

setup(
    name='rook_helper',
    packages=find_packages(include=['rook_helper', 'rook_helper.*']),
    version='0.2.1',
    license='MIT',
    description='Helper',
    author='Tomas Rosas',
    author_email='tomas.rosas@tryrook.io',
    url='https://bitbucket.org/rook-workspace/rook_helpers/src',
    keywords=['Rook', 'helper'],
    install_requires=[],
    classifiers=[
        'Natural Language :: English',
        'Programming Language :: Python :: 3.11'
    ]
    )
