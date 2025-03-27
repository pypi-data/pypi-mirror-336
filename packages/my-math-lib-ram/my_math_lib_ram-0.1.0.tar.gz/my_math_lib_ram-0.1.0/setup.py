from setuptools import setup, find_packages

setup(
    name="my_math_lib_ram",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],
    author="Ram",
    author_email="ramvinoth1993@gmail.com",
    description="A simple library for addition and subtraction",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://pypi.org/project/my_math_lib/",
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)