from setuptools import setup, find_packages

setup(
    name="med-interact",
    version="0.0.1",
    packages=find_packages(),
    install_requires=[
        "requests",
    ],
    tests_require=[
        "pytest",
    ],
    test_suite="tests",
    author="DrugXpert",
    author_email="contact@medinteract.com",
    description="Python library to check drug interactions, side effects and harmful effects.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/isranetoo/med-interact",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
