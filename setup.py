from setuptools import setup, find_packages

setup(
    name='HiddenRequest',
    packages=find_packages("src"),  # include all packages under src
    package_dir={'': 'src'},
    package_data={
        # If any package contains *.txt files, include them:
        "": ["data/*.*"],


    },
    test_suite="test",
    version="0.0.1",
    install_requires=['requests',"torrequest"],
    entry_points={
            'console_scripts': [
                'crawl=applications.main:main'
             
            ]
    }



)