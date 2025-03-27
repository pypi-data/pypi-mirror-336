from setuptools import setup, find_packages

setup(
    name="TerminatorCore",
    version="0.1.16",
    description="TerminatorCore",
    long_description=open("TerminatorBaseCore/README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="bws",
    author_email="m13277096902@gmail.com",
    url="https://github.com/UsedRoses/TerminatorCore",
    license="MIT",
    packages=find_packages(where="."),  # 自动查找所有Python包
    package_dir={"TerminatorBaseCore": "TerminatorBaseCore"},
    include_package_data=True,  # 包含非 Python 文件
    install_requires=[
    ],
    python_requires=">=3.8",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
