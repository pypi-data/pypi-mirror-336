from setuptools import setup, find_packages

setup(
    name='tardis_spac',
    version='0.1.0',
    author='pkuTrasond',
    author_email='barry_2001@stu.pku.edu.cn',
    description='TArget pRioritization toolkit for perturbation Data In Spatial-omics',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
    install_requires=[
        'numpy',
        'pandas',
        'scipy',
        'scikit-learn',
        'matplotlib',
        'seaborn',
        'scanpy',
        'statsmodels',
        'tqdm',
        'scikit-learn',
        'scipy',
        'matplotlib',
        'seaborn',
    ]
)