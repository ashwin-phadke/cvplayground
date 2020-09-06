from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()


setup(name='cvplayground-ashwin-phadke',
      version='0.2.0',
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
          'markdown', 'opencv_python', 'tensorflow', 'gunicorn', 'numpy',
          'six', 'matplotlib', 'asposestorage', 'Pillow', 'Flask',
          'werkzeug', 'imutils'
      ],
      include_package_data=True,
      zip_safe=False)
