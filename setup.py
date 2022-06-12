from setuptools import setup


setup(
    name='MpesaRest',
    version='0.0.2',
    description="An interaction of the Safaricom Daraja Api with Python",
    long_description=open('DESCRIPTION.txt').read(),
    author='Lumuli Ken Reagan',
    author_email='lumulikenreagan@gmail.com',
    install_requires=[
        "requests>=2.22.0",
        "SQLAlchemy>=1.4.32"
    ],
    url="https://github.com/kenreagan/MpesaRest",
    license="MIT",
    classifiers=[
      "Programming Language :: python :: 3.6",
      "License :: MIT",
      "Intended audience :: Developers",
      "Programming Language :: python :: pypy",
      "Operating System :: OS Independent"
    ],
    py_modules=[
        "managedb"
    ],
    entry_points = {
        'console_scripts': ['MpesaRest=managedb:main']
    }
)
