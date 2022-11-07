from setuptools import setup, find_packages

setup(
    name="monitify",
    version="1.0.0",
    author="Sukirno",
    author_email="mblonyox@gmail.com",
    description="Simple script to monitor and notify new email or file to WhatsApp chat or Teams channel.",
    long_description=open("README.MD", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    keywords=["monitoring", "email", "owncloud", "wa", "teams"],
    license="MIT",
    url="https://github.com/mofjs/monitify",
    packages=find_packages(),
    python_requires=">=3.9.0",
    install_requires=["typer", "pyocclient", "pymsteams", "jsonschema", "PyYAML", "wa-automate-socket-client", "rich", "shellingham"],
    entry_points={
        "console_scripts": [
            "monitify=monitify.cli:app"
        ]
    }
)