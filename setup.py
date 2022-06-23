from setuptools import setup


setup(
    name='MpesaRest',
    version='0.0.3',
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
      "Intended Audience :: Developers",
      "Programming Language :: Python",
      "Operating System :: OS Independent"
    ]
)
