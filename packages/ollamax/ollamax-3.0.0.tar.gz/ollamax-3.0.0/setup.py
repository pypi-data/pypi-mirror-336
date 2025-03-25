from setuptools import setup, find_packages

setup(
    name='ollamax',
    version='3.0.0',
    description='A package to manage Ollama service and models.',  # Direct description
    packages=find_packages(),  # Finds all packages (no "src" now since it's renamed)
    install_requires=['ollama'],  # Add dependencies needed for your package
    author='John Codes',
    author_email='efexzium@gmail.com',
    license='MIT',  # Optional but recommended
    url='https://github.com/yourusername/ollamax',  # Replace with your repository URL if available
)