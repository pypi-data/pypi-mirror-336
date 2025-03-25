# Chinese Administrative Divisions

A Python package for querying Chinese administrative divisions.


# Description
This package provides a simple way to query Chinese administrative divisions by code or name. It includes data for all provinces, cities, and districts in China.


# Installation

You can install this package using pip：

pip install chinese_administrative_divisions



# Usage

# Query by Code

from chinese_administrative_divisions import get_division_name

 
# Get division name by code

print(get_division_name("110000"))  # Output: 北京市

# Query by Name

from chinese_administrative_divisions import get_division_code


#Get division code by name

print(get_division_code("上海市"))  # Output: 310000


# Project Structure

chinese_administrative_divisions/

├── chinese_administrative_divisions/

│   ├── __init__.py
 
│   ├── data.py
   
│   └── query.py
   
├── setup.py
 
└── README.md


# Contributing
If you want to contribute to this project, please follow these steps:

1.Fork the repository

2.Create a new branch for your feature or bug fix

3.Make your changes

4.Submit a pull request


# License
This project is licensed under the MIT License - see the LICENSE file for details.
