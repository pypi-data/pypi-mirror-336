from setuptools import setup, find_packages

setup(
    name="serverhackgr",
    version="1.0",
    packages=find_packages(),
    install_requires=["requests"],
    entry_points={
        "console_scripts": [
            "htmlview=htmlview:HtmlView"
        ]
    },
    description="serverhackgr",
    author="panoscodergr",
    license="MIT"
)
