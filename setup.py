#!/usr/bin/env python3
"""
Setup script for ZK Middleware
"""

from setuptools import setup, find_packages

setup(
    name="zk-middleware",
    version="1.0.0",
    description="ZKTeco SpeedFace M4 Middleware for School Cafeteria",
    author="Crawford International",
    packages=find_packages(),
    install_requires=[
        "Flask==2.3.3",
        "requests==2.31.0",
        "pyzk==0.5.0",
        "python-escpos==3.0.0",
        "PyYAML==6.0",
        "gunicorn==22.1.0"
    ],
    entry_points={
        'console_scripts': [
            'zk-middleware=app:main',
        ],
    },
    python_requires='>=3.7',
)