from setuptools import setup, Extension
from Cython.Build import cythonize

extensions = [
    Extension("licensifylib.licensifylib", ["licensifylib/licensifylib.pyx"]),
]

setup(
    name="licensifylib",
    packages=["licensifylib"],
    ext_modules=cythonize(extensions, language_level="3"),
    include_package_data=True,
)