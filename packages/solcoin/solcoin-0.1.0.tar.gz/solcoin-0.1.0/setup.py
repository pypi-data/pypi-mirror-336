from setuptools import find_packages, setup
setup(
    name='solcoin',
    packages=find_packages(include=['solcoin']),
    version='0.1.0',
    description="A package for Solana transactions token transactions",
    author='bear102',
    license='MIT',
    install_requires=["solders",
        "solana",
        "borsh_construct",
        "requests",
        "construct",],
    url='https://github.com/bear102/solcoin',
)