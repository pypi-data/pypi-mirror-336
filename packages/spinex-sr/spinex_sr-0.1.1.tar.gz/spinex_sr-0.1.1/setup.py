from setuptools import setup, find_packages

setup(
    name="spinex_sr",
    version="0.1.1",
    author="M.Z. Naser",
    author_email="mznaser@clemson.edu",
    description="Symbolic Regression with SPINEX algorithm",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/mznaser-clemsonr",
    packages=find_packages(),
    install_requires=[
        'numpy>=1.19.0',
        'sympy>=1.7.0',
        'scikit-learn>=0.24.0',
        'scipy>=1.6.0',
        'joblib>=1.0.0',
        'matplotlib>=3.3.0',
        'termcolor>=1.1.0',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    license="MIT",
    license_files=[],  # <--- Add this line to suppress automatic injection
    python_requires='>=3.6',
)