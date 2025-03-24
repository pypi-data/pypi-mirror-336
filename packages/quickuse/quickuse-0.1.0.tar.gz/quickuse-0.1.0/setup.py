from setuptools import find_packages, setup

setup(
    name="quickuse",
    version="0.1.0",
    author="zhaoxuefeng",
    author_email=" ",
    description="A versatile agent that can solve various tasks using multiple tools",
    url="https://github.com/mannaandpoem/OpenManus",
    packages=find_packages(),
    install_requires=[
        "pydantic~=2.10.4",
        "pyyaml~=6.0.2",
        "loguru~=0.7.3",

    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)

# 在包的根目录下运行以下命令来构建源发行版和二进制发行版