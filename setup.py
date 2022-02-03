import setuptools

with open('src/bisi/__version__.py', 'r') as version_file:
    exec(version_file.read())

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

with open('requirements_dev.txt') as f:
    dev_requirements = f.read().splitlines()[1:]

with open('README.md') as f:
    README = f.read()


setuptools.setup(
    name='bisi',
    version=globals()['__version__'],
    description='A Python based runner for docker images.',
    long_description=README,
    long_description_content_type='text/markdown',
    python_requires='>=3.6.0',
    packages=setuptools.find_packages(where="src", include='bisi.*'),
    package_dir={'': 'src'},
    zip_safe=False,
    install_requires=requirements,
    extras_require={
        'dev': dev_requirements
    },
    entry_points={
        'console_scripts': [
            'bisi = bisi.cli.main:cli'
        ]
    }
)
