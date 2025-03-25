from setuptools import setup, find_packages

setup(
    name="smriti-todo-cli",
    version="0.1",
    description="Code",
    long_description="codessss",
    author="Smriti",
    packages=find_packages(),
    install_requires=[
        "typer",
        "rich"
    ],
    python_requires='>=3.6',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
    ]
)

