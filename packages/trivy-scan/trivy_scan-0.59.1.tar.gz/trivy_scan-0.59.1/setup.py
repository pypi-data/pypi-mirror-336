from setuptools import setup, find_packages

setup(
    name="trivy_scan",
    version="0.59.1",
    packages=find_packages(),
    package_data={"trivy_scan": ["bin/trivy"]},
    include_package_data=True,
    install_requires=[],
    author="Alax Alves",
    author_email="alaxallves@gmail.com",
    description="A Python package to run Trivy security scans on Docker images, including the Trivy binary.",
    url="https://github.com/yourusername/trivy_scan",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
