from setuptools import setup, find_packages

setup(
    name='hurst_calc',
    version='0.4',
    packages=find_packages(),
    install_requires=[
        "numpy",
        "pandas"
    ],
    author="Jeremy",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
)
