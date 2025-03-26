from codecs import open
from os import path

from setuptools import setup

ROOT = path.abspath(path.dirname(__file__))

with open(path.join(ROOT, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='parse-document-model',
    version='0.2.1',
    description='Pydantic models for representing a text document as a hierarchical structure.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='OneOffTech',
    author_email='info@oneofftech.xyz',
    license='MIT',
    url='https://github.com/OneOffTech/parse-document-model-python',
    project_urls={
        'Source': 'https://github.com/OneOffTech/parse-document-model-python',
    },
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Operating System :: OS Independent'
    ],
    packages=['parse_document_model'],
    include_package_data=True,
    python_requires=">=3.9",
    install_requires=['pydantic>=2.9.0']
)
