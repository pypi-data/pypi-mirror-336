from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="fastoas",
    version="0.0.1",
    packages=find_packages(),
    install_requires=requirements,
    entry_points={},
    author="Alexander Grishchenko",
    author_email="alexanderdemure@gmail.com",
    description="Customize and override OpenAPI schema details in FastAPI with ease",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/AlexDemure/fastoas",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)