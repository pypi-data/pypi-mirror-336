from setuptools import setup

installation_requirements = [
    "openai==1.68.2",
    "loguru==0.7.3",
    "neo4j==5.28.1",
    "azure-identity==1.21.0",
    "azure-keyvault-secrets==4.9.0",
    "aiohttp==3.11.14"
]

setup(
    version="0.12",
    name="freeflock-contraptions",
    description="A collection of contraptions",
    author="(~)",
    url="https://github.com/freeflock/contraptions",
    package_dir={"": "packages"},
    packages=["freeflock_contraptions"],
    install_requires=installation_requirements,
)
