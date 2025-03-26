from setuptools import setup, find_packages

setup(
    name="django-optimize-image",
    version="0.1.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["Pillow", "Django"],
    description="A Django middleware to optimize image uploads by converting them to WebP.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Nahom D",
    author_email="nahom@nahom.eu.org",
    url="https://github.com/nahom-d54/django-optimize-image",
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
