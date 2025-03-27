from setuptools import setup, find_packages


setup(
    author="Mikel Imaz",
    description="A wrapper for Udalmap API",
    name="udalmap",
    version="0.1.0",
    url="https://github.com/mikel-imaz/udalmap",
    keywords=["udalmap", "API", "wrapper"],
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=["requests", "pandas", "matplotlib"],
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ]
)
