from setuptools import setup, find_packages

setup(
    name="Dency",
    version="2.1",
    packages=find_packages(),
    install_requires=["click", "requests"],
    entry_points={"console_scripts": ["dency=dependency_fetcher.cli:main"]},
    author="PRIMUS",
    author_email="alokpal2803@gmail.com",
    description="tool to fetch and generate requirements.txt for Python projects",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/11PRIMUS/Dency",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    extras_require={"dev": ["pytest", "black"]},
    include_package_data=True,
    zip_safe=False,
)
