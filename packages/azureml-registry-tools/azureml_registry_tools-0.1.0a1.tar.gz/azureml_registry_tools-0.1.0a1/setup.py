# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Set up package."""

from setuptools import setup, find_packages

DEPENDENCIES = [
    "azure-ai-ml<2.0",
    "azureml-assets<2.0"
]

exclude_list = ["*.tests"]

setup(
    name='azureml-registry-tools',
    version="0.1.0a1",
    description='AzureML Registry tools and CLI',
    author='Microsoft Corp',
    license="https://aka.ms/azureml-sdk-license",
    packages=find_packages(exclude=exclude_list),
    install_requires=DEPENDENCIES,
    python_requires=">=3.9,<3.12",
    entry_points={
        'console_scripts': [
            'repo2registry = azureml.registry._cli.repo2registry_cli:main'
        ],
    }
)
