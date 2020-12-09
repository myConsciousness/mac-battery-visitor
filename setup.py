from setuptools import setup, find_packages

setup(
    name='macarer',
    version='1.0.1',
    description='The script created to optimize the battery charging state of the MacBook.',
    author='Kato Shinya',
    author_email='kato.shinya.dev@gmail.com',
    url='https://github.com/myConsciousness/macarer',
    packages=find_packages(),
    entry_points="""
      [console_scripts]
      macarer = macarer.cli:execute
    """,
)
