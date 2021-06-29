from setuptools import setup

setup (
    name = "bestOf",
    version = "0.0.3",
    description = "A module that uses machine learning to chose the best image in groups",
    packages = ["src",], # Change TODO
    url = "https://github.com/apangasa/bestof",
    install_requires = ["torch", "PyQt5"],

    include_package_data = True,

    entry_points = {
        'console_scripts': ['bestOf = src.frontend:main'],
    }

)