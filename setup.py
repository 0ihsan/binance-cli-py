from setuptools import setup

setup(
    name='binance-cli',
    version="0.0.1",
    py_modules=['binance_cli'],
    packages=['binance_cli'],
    entry_points={
        'console_scripts': [
            'binance-cli = binance_cli.cli:main',
        ],
    }
)
