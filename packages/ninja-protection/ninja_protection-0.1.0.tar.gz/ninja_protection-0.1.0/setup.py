from setuptools import setup, find_packages

setup(
    name="ninja-protection",
    version="0.1.0",
    description="Interactive CLI tool for system optimization and monitoring using psutil (LOGGIE infrastructure)",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="loggie.eth",
    author_email="founder@loggie.ai",
    url="https://github.com/loggie-eth/ninja-protection",
    packages=find_packages(),
    install_requires=[
        "psutil",
        "redis",
        "termcolor",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Topic :: System :: Monitoring",
        "Topic :: Utilities",
    ],
    entry_points={
        "console_scripts": [
            "ninja-protection=ninja_protection.optimizer:run_optimization"
        ]
    },
    include_package_data=True,
    python_requires='>=3.7',
    license="MIT",
)
