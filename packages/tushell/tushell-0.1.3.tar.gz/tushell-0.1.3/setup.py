from setuptools import setup, find_packages

setup(
    name="tushell",
    version="0.1.3",
    description="The Data Diver's best Intelligent and Narrative Command-Line Tooling you will have ever had",
    author="JGWill",
    author_email="tushellframe@jgwill.com",
    url="https://github.com/jgwill/tushell",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=[
        "click",
    ],
    entry_points={
        "console_scripts": [
            "tushell=tushell.cli:main",
        ],
    },
)
