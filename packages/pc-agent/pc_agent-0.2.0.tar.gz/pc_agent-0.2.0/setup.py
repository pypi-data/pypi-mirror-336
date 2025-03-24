from setuptools import setup, find_namespace_packages
import os

version = os.environ.get("GitVersion_SemVer", "0.1.0")

setup(
    name="pc-agent",
    version=version,
    description="Pah Construir Agents",
    author="Pah Venture",
    author_email="hello@pahventure.com",
    packages=find_namespace_packages(include=["*", "llms", "tools"]),
    py_modules=["agent"],
    install_requires=[
        "requests>=2.32.3",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.8",
)