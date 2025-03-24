from setuptools import setup, find_packages

setup(
    name='comprehensive_solana_diagnostic',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'aiohttp>=3.8.0',
        'pydantic>=2.0.0',
        'click>=8.0.0'
    ],
    entry_points={
        'console_scripts': [
            'solana-diagnostic=comprehensive_solana_diagnostic:main',
        ],
    },
    python_requires='>=3.8',
)
