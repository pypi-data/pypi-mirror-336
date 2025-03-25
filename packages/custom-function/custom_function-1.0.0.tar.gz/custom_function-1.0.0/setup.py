import setuptools
import io

try:
    with io.open("README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()
except FileNotFoundError:
    long_description = "No README found"

# 以下代码用于处理 setuptools 可能的编码问题
import setuptools.command.setopt
from setuptools.dist import Distribution

def patched_read(self, filenames):
    for filename in filenames:
        try:
            with io.open(filename, encoding='utf-8') as fp:
                self._read(fp, filename)
        except Exception as e:
            print(f"Error reading {filename}: {e}")

setuptools.command.setopt.configparser.RawConfigParser.read = patched_read

setuptools.setup(
    name="custom_function",
    version="1.0.0",
    author="jlpersist",
    author_email="jlpersist@163.com",
    description="自用常用函数",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
)