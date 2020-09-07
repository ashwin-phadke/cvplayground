from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()


setup(name='cvplayground-ashwin-phadke',
      version='0.2.8',
      description='Test repo pacakge print',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='http://github.com/ashwin-phadke/cvplayground',
      author='Ashwin Phadke',
      author_email='ashwinphadke12@rediffmail.com',
      license='MIT',
      packages=find_packages(),
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
      ],
      install_requires=[
          'opencv_python>=4.0', 'tensorflow>=2.0', 'gunicorn>=20.0', 'numpy>=1.18',
          'six>=1.14', 'matplotlib', 'asposestorage>=1.0',
          'Pillow>=7.1.2', 'Flask>=1.1',
          'werkzeug>=1.0', 'imutils>=0.2'
      ],
      include_package_data=True,
      zip_safe=False)