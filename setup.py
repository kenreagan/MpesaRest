from setuptools import setup, find_packages


setup(
    name='MpesaRest',
    version='0.0.1',
    description="An interaction of the Safaricom Daraja Api with Python",
    long_description=open('DESCRIPTION.txt').read(),
    author='Lumuli Ken Reagan',
    author_email='lumulikenreagan@gmail.com',
    install_requires=[
        "requests"
    ],
    url="https://github.com/kenreagan/MpesaRest",
    license="MIT",
    packages=find_packages('./MpesaRest/__init__.py'),
#    classifiers=[
 #      "Programming Language :: python :: 3.6",
  #     "License :: MIT",
   #    "Intended audience :: Developers",
    #   "Programming Language :: python :: pypy",
     #  "Operating System :: OS Independent"
    #]
)
