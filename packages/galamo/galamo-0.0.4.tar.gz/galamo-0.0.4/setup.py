from setuptools import setup, find_packages

# Read the long description from README.md
with open("readme.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="galamo",
    version="0.0.4",
    author="Jashanpreet Singh Dingra",
    author_email="astrodingra@gmail.com",
    description="A Python package for comprehensive galaxy analysis, integrating machine learning and statistical methods. It provides automated tools for morphology classification, kinematics, photometry, and spectral analysis to aid astrophysical research.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/galamo-org/galamo",
    packages=find_packages(),  # Ensure all packages are found
    include_package_data=True,  
    package_data={"galamo": ["model.keras", "encoder.pkl"]},  
    install_requires=[
        "tensorflow",
        "numpy",
        "opencv-python",
        "joblib",
        "matplotlib",
        "termcolor",
        "requests"
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Astronomy",
    ],
    python_requires=">=3.10",
    license="BSD-3-Clause",  # ✅ Corrected License
)
