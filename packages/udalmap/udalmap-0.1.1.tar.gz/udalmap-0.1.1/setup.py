from setuptools import setup, find_packages


with open("README.md", "r", encoding="utf-8") as file:
    long_description = file.read()

setup(
    author="Mikel Imaz",
    description="A wrapper for Udalmap API",
    name="udalmap",
    version="0.1.1",
    url="https://github.com/mikel-imaz/udalmap",
    keywords=["udalmap", "api", "euskadi", "basque", "opendata"],
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=["requests", "pandas", "matplotlib"],
    python_requires=">=3.6",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ]
)
