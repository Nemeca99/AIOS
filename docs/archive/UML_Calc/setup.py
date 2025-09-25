from setuptools import setup, find_packages

setup(
    name='uml_calculator',
    version='1.0.0',
    description='UML Calculator: Modular, explainable, and testable symbolic math engine',
    author='Your Name',
    packages=find_packages(),
    install_requires=[],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'umlcalc=ui.calculator_cli:main',
        ],
    },
    package_data={
        '': ['*.md', '*.json', '*.txt'],
    },
    python_requires='>=3.7',
)
