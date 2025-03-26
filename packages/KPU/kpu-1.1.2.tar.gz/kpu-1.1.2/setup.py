from setuptools import setup, find_packages
import platform

# Detect the OS
os_name = platform.system().lower()

# Define dependencies
dependencies = ["tensorflow", "numpy","rich"]



setup(
    name="KPU",
    version="1.1.2",
    author="N V R K SAI KAMESH YADAVALLI ",
    author_email="saikamesh.y@gmail.com",
    description="KPU Quantum Computing Chip - AI & Cybersecurity Innovation",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=dependencies,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
