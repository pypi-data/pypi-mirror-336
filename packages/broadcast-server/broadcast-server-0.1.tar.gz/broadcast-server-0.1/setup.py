from setuptools import setup, find_packages

setup(
    name='broadcast-server',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'websockets',
    ],
    entry_points={
        'console_scripts': [
            'broadcast-server=broadcast_server.cli:main',
        ],
    },
    author='Your Name',
    description='A simple WebSocket broadcast server and client CLI tool',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
)
