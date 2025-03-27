from setuptools import setup, find_packages

setup(
    name="KPU_chip",
    version="0.1.0",
    description="Quantum-inspired neural processing module (KPUChip) with quantum operations and benchmarking.",
    author="N V R K SAI KAMESH YADAVALLI",
    author_email="saikamesh.y@gmail.com",
    packages=find_packages(),
    install_requires=[
        "tensorflow>=2.0",
        "rich",
        "matplotlib"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
