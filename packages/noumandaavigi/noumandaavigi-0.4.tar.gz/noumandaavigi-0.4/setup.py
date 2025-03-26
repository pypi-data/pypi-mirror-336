from setuptools import setup, find_packages

setup(
    name="noumandaavigi",
    version="0.4",
    packages=find_packages(),  # Automatically finds all packages, including 'aicmd'
    install_requires=[
        "google-generativeai",
        "requests",
    ],
    entry_points={
        'console_scripts': [
            'ai-cmd = aicmd.main:main',  # Entry point for 'ai-cmd'
        ],
    },
    author="Your Name",
    author_email="your_email@example.com",
    description="A brief description of what your package does",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/your-repo",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
