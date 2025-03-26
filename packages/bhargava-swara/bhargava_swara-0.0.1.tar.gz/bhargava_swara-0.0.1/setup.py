from setuptools import setup, find_packages

setup(
    name="bhargava_swara",
    version="0.0.1",
    author="Kuchi Chaitanya Krishna Deepak",
    author_email="kckdeepak29@gmail.com",
    description="A library for analysis and synthesis of Indian classical music",
    long_description=open("README.txt").read() + "\n\n" + open("CHANGELOG.txt").read(),
    long_description_content_type="text/plain",
    url="",
    licence="MIT",
    packages=find_packages(),
    install_requires=[
        "google-generativeai>=0.1.0",
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    keywords=["music","analysis","synthesis","carnatic","hindustani","indian classical music"],
)