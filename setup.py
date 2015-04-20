from setuptools import setup

setup(name='grepo',
      version='0.1.1',
      description='Grepo grep and peco tool',
      author='Ville Vainio',
      author_email='vivainio@gmail.com',
      url='https://github.com/vivainio/grepo',
      packages=['grepo'],
      entry_points = {
        'console_scripts': [
            'grepo = grepo.grepo:main',
        ]
      }
     )