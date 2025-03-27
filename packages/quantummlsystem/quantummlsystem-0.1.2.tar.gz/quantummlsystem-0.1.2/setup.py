from setuptools import setup, find_packages

setup(
    name='quantummlsystem',
    version='0.1.2',
    description='A Flexible Quantum Machine Learning Framework',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Nikolaos Roufas',
    author_email='nikolaosroufas@gmail.com',
    url='https://github.com/nikolasroufas/quantum-ml-system',
    packages=find_packages(),
    install_requires=[
        'pennylane>=0.30.0',
        'numpy>=1.20.0',
        'scikit-learn>=1.0.0',
        'matplotlib>=3.5.0'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Scientific/Engineering :: Physics'
    ],
    keywords='quantum machine learning quantum-computing ml ai',
    python_requires='>=3.8'
)