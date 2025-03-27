from setuptools import setup, find_packages

setup(
    name="excelj",          
    version="0.1",             
    packages=find_packages(),  
    entry_points={
        "console_scripts": [
            "excelj=excelj.excelj:main",
        ]
    },


    author="qq292000799",
    description="excel to json",
    url="https://github.com/qq292",
    install_requires=[        
        'openpyxl>=3.1.5',
    ],
    python_requires='>=3.6',  
)