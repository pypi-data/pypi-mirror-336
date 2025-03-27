from setuptools import setup, find_packages

with open("README.md", "r") as f:
    description = f.read()

setup(
    name = 'SQLGetterSetter',
    version = '1.0.0',
    author = 'Kannan B',
    packages = find_packages(),
    install_requires =[
        #library like 'pymongo == 3.2.1',
        'mysql-connector-python == 9.1.0',

    ],
    entry_points = {
        "console_scripts": [
            "SQL-tester = SQLGetterSetter:hello",

        ],
    },
    long_description=description,
    long_description_content_type = "text/markdown",
)