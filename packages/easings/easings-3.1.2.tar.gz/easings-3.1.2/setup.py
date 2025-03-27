import setuptools

with open('README.md', 'r') as file:
    long_description = file.read()

setuptools.setup(
    name = 'easings',
    version = '3.1.2',
    
    author = 'Sylvie Isla',
    author_email = 'sylvieisla.std@gmail.com',

    description = 'Customizable Optimized Easing Functions for Python',
    long_description = long_description,
    long_description_content_type = 'text/markdown',

    keywords = 'easings easing ease animation interpolation',

    install_requires = [
        'numpy>=1.22'
    ],

    packages = setuptools.find_packages(),

    classifiers = [
        'Programming Language :: Python :: 3',
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Topic :: Multimedia :: Graphics',
        'Topic :: Scientific/Engineering :: Mathematics',
        'License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication',
        'Operating System :: OS Independent'
    ],
    
    python_requires = '>=3.6',
)