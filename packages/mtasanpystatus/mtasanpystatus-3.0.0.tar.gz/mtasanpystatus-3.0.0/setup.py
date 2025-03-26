from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="mtasanpystatus",
    version="3.0.0", 
    author="ieoub",
    author_email="rib7daily@gmail.com",
    description="Simple MTA:SA server monitoring library with direct module access",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ieoub/mtasanpystatus",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Games/Entertainment",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    keywords="mtasa multiplayer san-andreas gaming server-monitoring",
    project_urls={
        "Bug Reports": "https://github.com/ieoub/mtasanpystatus/issues",
        "Source": "https://github.com/ieoub/mtasanpystatus",
    },
)