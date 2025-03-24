from setuptools import setup, find_packages
import os

def read_long_description():
    """Helper function to read the content of README.md"""
    with open(os.path.join(os.path.dirname(__file__), 'README.md'), encoding='utf-8') as f:
        return f.read()
setup(
    name="perceptionpro",
    version="0.1.3",
    packages=find_packages(include=['perceptionpro', 'perceptionpro.*']),
    install_requires=[
        'opencv-python==4.11.0.86',
        'opencv-python-headless==4.11.0.86',
        'mediapipe==0.10.11',
        'ultralytics==8.3.63',
        'numpy==1.24.4',
        'protobuf>=3.11,<4.0',
        'grpcio-status>=1.70.0',
    ],
    author="Umar Balak",
    author_email="umarbalak35@gmail.com",
    description="PerceptionPro is a package for computer vision tasks such as head pose estimation, eye tracking, and object detection.",
    long_description=read_long_description(),
    long_description_content_type="text/markdown",
    license="MIT",
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
    ],
    python_requires='>=3.8',
)
