from setuptools import setup, find_packages

setup(
    name="chirp_spectrogram_generator",
    version="0.1.6",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "matplotlib",
        "pandas",
        "scipy",
    ],
    description="A package to generate synthetic spectrograms of chirps.",
    author="Nooshin Bahador",
    author_email="nooshin.bah@gmail.com",
    url="https://github.com/nbahador/chirp_spectrogram_generator",
)