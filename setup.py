import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="odepy",
    version="0.0.1",
    author="Mateusz Soczewka",
    author_email="msoczewkas@gmail.com",
    description="Module for numerical solving of ordinary differential equations.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/msoczi/odepy",
    project_urls={
        "Bug Tracker": "https://github.com/msoczi/odepy/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
