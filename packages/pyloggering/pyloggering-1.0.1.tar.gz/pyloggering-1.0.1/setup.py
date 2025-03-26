from setuptools import setup, find_packages


def readme():
  with open('README.md', 'r', encoding="utf-8") as file:
    return file.read()

setup(
  name='pyloggering',
  version='1.0.1',
  author='K1ayPVA',
  author_email='kegor6137@gmail.com',
  description='Module for sumple logging',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://github.com/K1AYPVA/logger',
  packages=['pyloggering'],
  install_requires=['colorama>=0.4.6'
                    ],
  classifiers=[
    'License :: OSI Approved :: MIT License'

  ],
  keywords='logging python ',
  project_urls={
    'Documentation': 'https://github.com/K1AYPVA/logger/tree/main'
  },
  python_requires='>=3.10.9'
)