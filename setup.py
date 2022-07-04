from setuptools import setup, find_packages

requirements = open("requirements.txt").readlines()

setup(
    name='HiddenRequest',
    packages=find_packages("src"),  # include all packages under src
    package_dir={'': 'src'},
    version="0.1.1",
    author='groseries',
    description='An extension of tor/requests using ProtonVPN.',
    install_requires=requirements
)
