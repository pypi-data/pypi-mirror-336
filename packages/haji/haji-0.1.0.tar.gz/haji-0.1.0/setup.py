from setuptools import setup

setup(
    name="haji",
    version="0.1.0",
    py_modules=["haji"],
    install_requires=["click", "requests", "g4f"],
    entry_points={
        "console_scripts": [
            "haji=haji:haji",
        ],
    },
)
