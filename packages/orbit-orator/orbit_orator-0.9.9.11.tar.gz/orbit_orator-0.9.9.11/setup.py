from setuptools import setup, find_packages

setup(
    name="orbit-orator",
    version="0.9.9.5",
    description="A simple ORM for Python",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Maxiaoyu",
    author_email="maxiaoyu@example.com",
    url="https://github.com/maxiaoyu/orator",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
) 