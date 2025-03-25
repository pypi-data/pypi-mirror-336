import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name="HWVL",
  version="0.0.1",
  author="mohammad rakhshkhorshid",
  author_email="mohammad.rakhshkhorshid@gmail.com",
  description="The first Iranian hash",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/HWVL/hash-HWVL",
  packages=setuptools.find_packages(),
  classifiers=[
    "Programming Language :: Python :: 3",
    "Operating System :: OS Independent",
  ],
  python_requires='>=3.6',
)