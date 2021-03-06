import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="qchainpy",
    version="0.0.1",
    author="Eblanium Admin",
    author_email="admin@eblanium.com",
    description="A package to use blockchain QChain API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/eblanium/qchainpy",
    project_urls={
        "Bug Tracker": "https://github.com/eblanium/qchainpy/issues",
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