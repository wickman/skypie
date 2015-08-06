from setuptools import setup


setup(
  name = 'skypie',
  version = '0.1.0',
  description = 'cost modeling for aircraft ownership',
  url = 'https://github.com/wickman/skypie',
  license = 'MIT',
  zip_safe = True,
  classifiers = [
    'Operating System :: OS Independent',
    'Programming Language :: Python',
  ],
  packages = ['skypie'],
  install_requires = [
    'ansicolors',
  ],
)
