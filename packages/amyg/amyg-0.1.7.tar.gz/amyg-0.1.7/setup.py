# setup.py
import setuptools

setuptools.setup(
    name="amyg",
    version="0.1.7",             # adjust as needed
    author="Carlos Farkas",
    author_email="carlosfarkas@gmail.com",
    description="A pipeline for De Novo Genomic Annotation of Non-Model Organisms compatible with Single Cell RNA-seq",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/cfarkas/amyg",   # your GitHub repo
    license="MIT",                           # matches your LICENSE
    py_modules=["amyg"],        # since you have amyg.py at top-level
    python_requires=">=3.7",
    # If you want a console script called "amyg" that calls amyg.py's main(),
    entry_points={
        "console_scripts": [
            "amyg=amyg:main",  
            # means: user can type 'amyg' in shell => runs amyg.py's main()
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
