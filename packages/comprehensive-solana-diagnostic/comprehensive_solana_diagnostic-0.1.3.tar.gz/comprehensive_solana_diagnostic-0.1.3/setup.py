from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='comprehensive_solana_diagnostic',
    version='0.1.3',
    packages=find_packages(),
    install_requires=[
        'aiohttp>=3.8.0',
        'pydantic>=2.0.0',
        'click>=8.0.0'
    ],
    extras_require={
        'test': [
            'pytest>=7.0.0',
            'pytest-cov>=3.0.0',
            'pytest-asyncio>=0.20.0'
        ]
    },
    entry_points={
        'console_scripts': [
            'solana-diagnostic=comprehensive_solana_diagnostic:main',
        ],
    },
    python_requires='>=3.8',
    long_description=long_description,
    long_description_content_type="text/markdown",
    project_urls={
        'Source': 'https://github.com/homezloco/comprehensive-solana-diagnostic',
        'Bug Reports': 'https://github.com/homezloco/comprehensive-solana-diagnostic/issues',
    },
)
