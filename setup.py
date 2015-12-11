from setuptools import setup

setup(
    name='phenopredict21',
    version='0.1',
    py_modules=['phenopredict21'],
        install_requires=[
            'Click',
    ],
    entry_points='''
        [console_scripts]
        phenopredict21=phenopredict21:cli
    ''',
)
