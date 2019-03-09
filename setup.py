from setuptools import setup


setup(name='phase',
      version='0.1',
      description='Tools for simulated x-ray phase contrast',
      url='https://github.com/scott-trinkle/xphase',
      author='Scott Trinkle',
      author_email='tscott.trinkle@gmail.com',
      license='MIT',
      packages=['phase'],
      package_dir={'phase': 'phase'},
      package_data={'phase': ['data/*']},
      install_requires=['numpy', 'pandas'],
      zip_safe=False)
