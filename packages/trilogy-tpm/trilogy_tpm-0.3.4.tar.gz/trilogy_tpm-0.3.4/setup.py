from setuptools import setup, find_packages

setup(
    name="trilogy-tpm",
    version="0.3.4",
    packages=find_packages(),
    include_package_data=True,
    py_modules=[],
    scripts=["tpm"],
    entry_points={
        'console_scripts': [
            'tpm-cli=tpm:main',
        ],
    },
    install_requires=[
        "requests>=2.25.0",
        "tabulate>=0.8.7",
        "google-api-python-client>=2.0.0",
        "google-auth-httplib2>=0.1.0",
        "google-auth-oauthlib>=0.4.2",
        "markdown>=3.3.4",
        "beautifulsoup4>=4.9.3",
        "boto3>=1.18.0",
        "click>=8.0.0",
        "jira>=3.0.0",
        "rich>=10.0.0",
        "tqdm>=4.60.0",
        "neo4j-graphrag>=0.5.0",
    ],
    author="Technical Project Managers",
    author_email="dschwartz@trilogy.com",
    description="TPM CLI - Tools for Technical Project Managers",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/trilogy-group/tpm-cli",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    test_suite="tests",
)
