from setuptools import setup, find_packages

setup(
    name="website-screenshot-generator",
    version="0.1.0",
    author="Your Name",
    author_email="your_email@example.com",
    description="A simple website screenshot generator using Selenium",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/website-screenshot-generator",
    packages=find_packages(),
    install_requires=[
        "selenium",
        "webdriver_manager"
    ],
   )
