from setuptools import setup, find_packages

setup(
    name="fengling",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],
    author="ala",
    author_email="ala9981@163.com",
    description="一个基于emoji的风铃进度条库,肥城泰西的风铃",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ala/fengling",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.6",
    keywords="progress bar, emoji, animation, terminal, cli",
) 