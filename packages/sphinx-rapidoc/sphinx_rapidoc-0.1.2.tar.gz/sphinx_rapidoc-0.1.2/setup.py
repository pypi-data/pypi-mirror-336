from setuptools import setup, find_packages

setup(
    name='sphinx_rapidoc',
    version='0.1.2',
    description='Custom Sphinx extension for embedding RapiDoc in your documentation',
    author='Tirth Shah',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    url="https://github.com/TirthS24/sphinx_rapidoc",
    install_requires=[
        'sphinx>=7.2.5',
    ],
    package_data={
        'sphinx_rapidoc': [
            'static/*.js',
            'templates/*.html',
        ],
    },
    entry_points={
        'sphinx.extensions': [
            'sphinx_rapidoc = sphinx_rapidoc',
        ],
    },
    python_requires='>=3.9',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
