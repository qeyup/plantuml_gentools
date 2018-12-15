import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="plantuml_gentools",
    version="0.0.1",
    author="Javier Moreno",
    author_email="jgmore@gmail.com",
    description="PlantUML gen Tools.",
    long_description="Tools for generating plantuml diagrams using python language",
    long_description_content_type="text/markdown",
    url="https://github.com/qeyup/plantuml_gentools.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)