from setuptools import setup, find_packages

setup(
    name="DeviceUAgen",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],
    author="Fajarrrrky",
    author_email="saepulfajar440@gmail.com",
    description="Generator User-Agent untuk berbagai perangkat",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Fajarrrrky/Useragent",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)