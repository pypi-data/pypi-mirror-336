from setuptools import setup, find_packages

setup(
    name="email_utils_helpdesk",
    version="0.1",
    packages=find_packages(),
    install_requires=[],  # Add dependencies if needed
    author="Ali",
    description="A simple package for email handling.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
