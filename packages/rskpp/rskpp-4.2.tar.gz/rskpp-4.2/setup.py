from setuptools import setup 

setup(
    name = "rskpp",
    version = "4.2", 
    description= "Rejection Sampling Approach to k-means++ seeding",
    packages=["rskpp"], 
    author="Anonymous",  
    zip_safe = False, 
    install_requires=[
        "numpy", "scikit-learn", "matplotlib"
    ],
)