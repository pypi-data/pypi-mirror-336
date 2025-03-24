import setuptools

with open('README.md', 'r') as file:
    long_description = file.read()

setuptools.setup(
    name = 'super_simplex',
    version = '1.0.1',
    
    author = 'Sylvie Isla',
    author_email = 'sylvieisla.std@gmail.com',

    description = 'Super Simplex Noise for Python',
    long_description = long_description,
    long_description_content_type = 'text/markdown',

    keywords='open_simplex_2s open_simplex2s opensimplex2s open_simplex opensimplex super_simplex supersimplex simplex noise gradient_noise coherent_noise',

    install_requires=[
        'numpy>=1.22'
    ],

    packages = setuptools.find_packages(),

    classifiers = [
        'Programming Language :: Python :: 3',
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering :: Mathematics',
        'License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication',
        'Operating System :: OS Independent'
    ],
    
    python_requires = '>=3.6',
)