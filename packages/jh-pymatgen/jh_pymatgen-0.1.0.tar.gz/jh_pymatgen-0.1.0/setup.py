from setuptools import setup, find_packages

setup(
    name='jh_pymatgen',
    version='0.1.0',
    packages=find_packages(),  # Automatically find packages
    description='This is an augmentation of pymatgen package. It has two components: i) structure_process, ii) cp2k_script_generator.',
    author='Md Nur Kutubul Alam',
    author_email='alamjhilam@gmail.com',
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
    install_requires=[
            'pymatgen',  # pymatgen is a key dependency
            'mp-api',  # For MPRester
            'numpy',  # For numerical operations
            'matplotlib',  # For plotting (assuming you're using it for visualization)
            'py3Dmol',  # For 3D molecule visualization
            'IPython',  # For Jupyter notebook display
            'ipywidgets' #helps create interactive widgets in Jupyter Notebooks
    ]

)
