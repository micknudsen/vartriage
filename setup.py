from setuptools import setup, find_packages


setup(

    name='vartriage',
    version='0.2',

    packages=find_packages('src'),
    package_dir={'': 'src'},

    test_suite='tests',

    python_requires='>=3.7',

    entry_points={
        'console_scripts': ['vartriage = vartriage.client:main']
    },

    install_requires=[
    ],

    author='Michael Knudsen',
    author_email='micknudsen@gmail.com',
    license='MIT'

)
