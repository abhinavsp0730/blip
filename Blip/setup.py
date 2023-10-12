import os.path
import setuptools

path = os.path.join(__file__, "../README.md")
with open(path, "r") as f:
	readme = f.read()

setuptools.setup(
    name="django-blip",
    version="0.0.10",
    description="Python package to intercept all external api call during django test.",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Abhinav Prakash",
    author_email="abhinavsp0730@gmail.com",
    license="MIT License",
    package_dir={"": "src"},
    packages=setuptools.find_namespace_packages(where="src"),
    zip_safe=False,
    url="https://github.com/abhinavsp0730/blip/",
    install_requires=["httpretty>=1.1.4"],
    python_requires=">=3.9",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
