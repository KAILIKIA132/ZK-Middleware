from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read().splitlines()

setup(
    name="zk-middleware",
    version="1.0.0",
    author="Crawford International",
    author_email="support@crawford.co.za",
    description="ZKTeco SpeedFace M4 Middleware for Canteen Management",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/canteen-management-system",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Topic :: Education",
        "Topic :: System :: Monitoring",
    ],
    python_requires=">=3.9",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "zk-middleware=app:main",
        ],
    },
)