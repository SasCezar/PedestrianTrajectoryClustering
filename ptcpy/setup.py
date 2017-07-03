from distutils.core import setup

setup(
    name='Pedestrian Tajectory Clustering',
    version='0.1.0',
    author='Cezar Sas',
    author_email='c.sas@campus.unimib.it',
    packages=['ptcpy'],
    scripts=[],
    # url='http://pypi.python.org/pypi/TowelStuff/',
    license='LICENSE.txt',
    description='A pedestrian trajectory clustering tool.',
    long_description=open('../README.txt').read(),
    install_requires=[
    ],
)
