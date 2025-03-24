from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="easycpp",
    version="1.0.0",
    packages=find_packages(include=['easycpp', 'easycpp.precompile']),
    description="Enjoyably using embedded C++ code or dynamic libraries",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Chris Ju",
    author_email="mchrisju@gmail.com",
    url="https://github.com/chrisju/easycpp",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires=">=3.7",
    entry_points={
        'console_scripts': [
            'easycpp-precompiler=easycpp.precompile:main',
        ],
    },
)

