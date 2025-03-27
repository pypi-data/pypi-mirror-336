from setuptools import setup, find_packages
setup(
    name="instagramtolle",
    version="0.4",
    author="HUSSAIN",
    author_email="reco9678785@gmail.com",
    description="lib in Python for instagram",
    packages=find_packages(),
    install_requires=[
        "user_agent",
        "requests",
        "MedoSigner",
        "pycryptodome"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)