from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='macarer',
    version='1.0.1',
    description='The script created to optimize the battery charging state of the MacBook.',
    author='Kato Shinya',
    author_email='kato.shinya.dev@gmail.com',
    url='https://github.com/myConsciousness/mac-battery-visitor',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    entry_points="""
      [console_scripts]
      macarer = macarer.cli:execute
    """,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache License 2.0',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=open('requirements.txt').read().splitlines(),
)
