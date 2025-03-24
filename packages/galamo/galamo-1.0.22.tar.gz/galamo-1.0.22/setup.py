from setuptools import setup, find_packages
#pip install --upgrade --no-cache-dir galamo

# Read the long description from README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="galamo",
    version="1.0.22",
    author="Jashanpreet Singh Dingra",
    author_email="astrodingra@gmail.com",
    description="A Python package for classifying galaxy morphologies using deep learning.",
    long_description=long_description,  # Use the content from README.md
    long_description_content_type="text/markdown",  # Markdown format
    url="https://github.com/jdingra11/galamo", 
    include_package_data=True,  # ✅ Ensure package data is included
    package_data={"galamo": ["model.keras", "encoder.pkl"]},  # ✅ Specify extra files
   
    install_requires=[
        "tensorflow",
        "numpy",
        "opencv-python",
        "joblib",
        "matplotlib",
        "requests"
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Astronomy",
    ],
    python_requires=">=3.10",
)
