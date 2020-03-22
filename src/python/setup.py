import setuptools

setuptools.setup(
    name="sandboxlib",
    version="0.0.1",
    author="Shigeru Kitazaki",
    author_email="skitazaki@gmail.com",
    description="A small example package",
    url="https://github.com/skitazaki/sandbox/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 1 - Planning",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
    ],
    python_requires='>=3.8',
)
