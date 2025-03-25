from setuptools import setup, find_packages

setup(
    name='ollama-switch',
    version='2.0.0',
    description='A package to manage Ollama service and models.',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=['ollama'],
    author='John Codes',
    author_email='efexzium@gmail.com',
)
