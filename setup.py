from setuptools import setup

setup(name='scanner',
      version='0.0.0',
      description='',
      url='https://github.com/wbornor/scanner',
      author='wbornor',
      author_email='wbornor+github@gmail.com',
      packages=[],
      install_requires=[
            'numpy',
            'SimpleCV',
            'PiCamera',
            'zbar-py'
      ],
      dependency_links=['https://github.com/sightmachine/SimpleCV'],
      zip_safe=False)