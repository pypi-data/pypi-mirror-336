from setuptools import setup, find_packages

setup(
    name="bhargava_swara",
    version="0.0.6",
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
        "librosa>=0.10.0",  # For mel spectrogram
        "matplotlib>=3.7.0",  # For plotting
        "numpy>=1.24.0",  # Required by librosa and matplotlib
        "seaborn>=0.11.0",  # Added seaborn
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    keywords=["music","analysis","synthesis","carnatic","hindustani","indian classical music","raga","tala","spectograms","signal"],
)