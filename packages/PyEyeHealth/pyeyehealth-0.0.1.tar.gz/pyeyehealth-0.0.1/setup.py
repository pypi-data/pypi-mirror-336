from setuptools import setup, find_packages
setup(
    name="PyEyeHealth",
    version="0.0.1",
    packages=find_packages(),
    install_requires=[
	"cv2","PyQt6","dlib","imutils"

    ]
)