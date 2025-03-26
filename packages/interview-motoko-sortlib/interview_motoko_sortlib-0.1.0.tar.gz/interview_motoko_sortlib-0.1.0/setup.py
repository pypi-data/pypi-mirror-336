from setuptools import setup
from pybind11.setup_helpers import Pybind11Extension

ext_modules = [
    Pybind11Extension(
        "sortlib_cpp",
        ["cpp/sortlib.cpp", "cpp/bindings.cpp"],
        include_dirs=["cpp"],
        cxx_std=17,
    ),
]

setup(
    name="interview_motoko_sortlib",
    version="0.1.0",
    packages=["sortlib"],
    ext_modules=ext_modules,
    zip_safe=False,
    install_requires=[
        "pybind11>=2.10.0",
        "numpy>=1.23.0",
        "requests",
    ],
)
