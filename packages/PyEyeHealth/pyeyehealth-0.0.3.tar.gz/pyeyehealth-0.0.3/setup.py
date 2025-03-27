from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="PyEyeHealth",
    version="0.0.3",
    description="PyEyeHealth, göz sağlığını analiz etmeye yönelik bir araçtır.",
    long_description=long_description,
    long_description_content_type="text/markdown",  # README.md için Markdown türü
    url="https://github.com/kullanici/PyEyeHealth",  # GitHub veya proje linkini ekle
    packages=find_packages(),
    install_requires=[
        "PyQt6",
        "imutils"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
