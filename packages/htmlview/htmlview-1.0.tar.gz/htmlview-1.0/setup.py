from setuptools import setup, find_packages

setup(
    name="htmlview",
    version="1.0",
    packages=find_packages(),
    install_requires=["pywebview"],
    entry_points={
        "console_scripts": [
            "htmlview=htmlview:HtmlView"
        ]
    },
    description="Μια βιβλιοθήκη Python για προβολή HTML αρχείων με pywebview",
    author="panoscodergr",
    license="MIT"
)
