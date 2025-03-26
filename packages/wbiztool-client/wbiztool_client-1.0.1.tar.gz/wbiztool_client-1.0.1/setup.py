"""Setup file for the WbizTool client package."""

from setuptools import setup, find_packages
import os
import re

# Read the version from __init__.py
with open(os.path.join('wbiztool_client', '__init__.py'), 'r') as f:
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", f.read(), re.M)
    if version_match:
        version = version_match.group(1)
    else:
        version = '1.0.1'  # Updated version

# Read the contents of README.md
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='wbiztool-client',
    version=version,
    description='Python client for the WbizTool WhatsApp messaging API',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Anurag Meena',
    author_email='anuragmeena92@gmail.com',
    url='https://github.com/anuragmeena/wbiztool-client',
    packages=find_packages(),
    install_requires=[
        'requests>=2.25.0',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Communications :: Chat',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires='>=3.6',
    keywords='wbiztool, whatsapp, api, client, messaging, communication',
    project_urls={
        'Documentation': 'https://wbiztool.com/docs/',
        'Source': 'https://github.com/anuragmeena/wbiztool-client',
        'Tracker': 'https://github.com/anuragmeena/wbiztool-client/issues',
        'Official Website': 'https://wbiztool.com',
        'Support': 'https://wbiztool.com/contact',
    },
) 