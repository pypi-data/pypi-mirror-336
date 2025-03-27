from setuptools import setup, find_packages
from Cython.Build import cythonize

setup(
    name="Funleaker",  # The name of your library
    version="1.4.4",  # Version number
    packages=find_packages(),  # Automatically discover all packages
    install_requires=[          # List dependencies
        "requests",  # Mandatory dependency
        "tqdm",      # Add tqdm for progress bars
        "colorama",  # Add colorama for colored console output
        'platformdirs',
    ],
    ext_modules=cythonize("funleaker/*.pyx"),  # Compiling .pyx files with Cython
    entry_points={  # Entry point for your console app
        "console_scripts": [
            "funleaker = funleaker.main:main",
        ],
    },
    author="Syn_Tw",  # Author's name as "Anonymous"
    author_email="announmoseemail@notreal.com",  # Placeholder email as you requested
    description="This is the official funleaker core functions (beta) for Python. Users can now log in to their Syn account and use basic functions. This can be included in your web API app. This project is NSFW, and all results will return NSFW content. Please be aware.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[  # Classifiers for your library
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",  # Custom License
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # Adjust Python version compatibility
    license="Custom License (Non-Commercial Use Only)",  # Referencing your custom license
)
