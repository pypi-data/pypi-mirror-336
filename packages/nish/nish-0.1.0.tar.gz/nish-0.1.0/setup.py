from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='nish',
    version='0.1.0',
    author='Rachit Vyas',
    author_email='vrachit106@gmail.com',
    description='A CLI tool to combine PDFs in a folder',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Nishitha03/nish',
    packages=find_packages(),
    install_requires=[
        'PyPDF2>=3.0.0',
    ],
    entry_points={
        'console_scripts': [
            'nish=pdf_combiner.cli:main',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    python_requires='>=3.8',
    keywords='pdf combine merge tool',
)