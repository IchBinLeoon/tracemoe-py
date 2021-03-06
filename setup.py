import re

from setuptools import setup

with open('tracemoe/__init__.py', 'r') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

with open('README.md', 'r') as f:
    readme = f.read()

setup(
    name='tracemoe-py',
    version=version,
    packages=['tracemoe'],
    url='https://github.com/IchBinLeoon/tracemoe-py',
    project_urls={
        'Issue tracker': 'https://github.com/IchBinLeoon/tracemoe-py/issues'
    },
    license='MIT',
    author='IchBinLeoon',
    description='A minimal asynchronous API wrapper for trace.moe',
    long_description=readme,
    long_description_content_type='text/markdown',
    python_requires='>=3.6',
    install_requires=[
        'aiohttp'
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities'
    ]
)