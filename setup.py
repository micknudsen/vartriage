from setuptools import setup, find_packages


setup(

    name='vartriage',
    version='0.1',

    packages=find_packages('src'),
    package_dir={'': 'src'},

    test_suite='tests',

    python_requires='>=3.6',

    install_requires=[
    ],

    author='Michael Knudsen',
    author_email='micknudsen@gmail.com',
    license='MIT'

)
