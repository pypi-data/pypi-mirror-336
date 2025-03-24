from setuptools import setup, find_packages # type: ignore
setup(
   name='dereberus',
   version='0.5',
   packages=find_packages(),
   install_requires=[
      'click',
   ],
   entry_points='''
      [console_scripts]
      dereberus=dereberus_cli:cli
      ''',
)