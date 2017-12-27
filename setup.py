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
            'Pillow',
            'PiCamera',
            'zbar-py'
      ],
      dependency_links=[],
      zip_safe=False)