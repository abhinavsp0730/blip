import setuptools

setuptools.setup(
    name="django-blip",
    version="0.0.1",
    description="Python package to intercept all external api calls during django test.",
    long_description="",
    author="Abhinav Prakash",
    author_email="abhinavsp0730@gmail.com",
    license="MIT License",
    package_dir={"": "src"},
    packages=setuptools.find_namespace_packages(where="src"),
    zip_safe=False,
    install_requires=["httpretty>=1.1.4"],
    python_requires=">=3.9",
)
