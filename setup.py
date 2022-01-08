import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sapersolver-pkg-bloniaq",
    version="1.0",
    author="Jakub Blonski",
    author_email="j.a.blonski@outlook.com",
    description="A bot for solving an expert Win7-Minesweeper board",
    url=None,
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Windows",
    ],
    python_requires='>=3.10',
    tests_require=['pytest']
)