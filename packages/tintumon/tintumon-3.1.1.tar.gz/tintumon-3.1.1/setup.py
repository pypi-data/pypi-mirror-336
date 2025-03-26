from setuptools import setup, find_packages

setup(
    name="tintumon",
    version="3.1.1",
    packages=find_packages(),
    install_requires=[
    "pytelegrambotapi",
    "opencv-python",
    "numpy",
    "pyautogui",
    "pillow",
    "pycryptodome",
    "pypiwin32",
    "pycryptodomex",
    "secretstorage",
    "cryptography"
],
    entry_points={
        "console_scripts": [
            "tintumon = tintumon.bot:run_bot"
        ]
    },
    author="Tintumon",
    author_email="info@projectss.me",
    description="nothing just use this :)",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/appuachu",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
