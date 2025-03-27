from setuptools import setup, find_packages

setup(
    name="euroradscraper",
    version="1.0",
    author="Santhoshkumar K",
    author_email="santhoshatwork17@gmail.com",
    description="A Python package to scrape Eurorad case data and return it as JSON.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/santhosh1705kumar/eurorad_scraper",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.1",
        "beautifulsoup4>=4.9.3"
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    # license="MIT",  # ✅ Correct field
    python_requires='>=3.6',
    include_package_data=True,
)
