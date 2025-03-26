from setuptools import setup, find_packages

setup(
    name="robotic_hand",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        "opencv-python",
        "mediapipe==0.10.20",
        "numpy",
        "pyserial", 

    ],
    author="Jayadev Pillai",
    author_email="jayadevpillai56@gmail.com",
    description="A Python package to control a robotic hand using OpenCV and Mediapipe",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    #url="https://github.com/yourusername/RoboticHand",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
