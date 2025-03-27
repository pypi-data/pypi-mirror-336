import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="RedXAISecureToolkit",  # PyPI package name
    version="1.0.0",
    author="YourName",
    author_email="youremail@example.com",
    description="A unified toolkit for Firebase/Google Cloud, secure payments, and updates.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/YourUsername/RedXAISecureToolkit",
    packages=setuptools.find_packages(),  # automatically finds subpackages
    install_requires=[
        "firebase-admin",
        "google-cloud-storage",
        "stripe",
        "requests",
        "python-dotenv",
        # etc.
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
