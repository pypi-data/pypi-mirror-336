from setuptools import setup, find_packages

setup(
    name="django-communications",  # Unique PyPI package name
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "django>=4.0",
    ],
    python_requires=">=3.9",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Framework :: Django",
        "Framework :: Django :: 4.0",
        "Framework :: Django :: 4.1",
        "Framework :: Django :: 4.2",
        "Framework :: Django :: 5.0",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
    ],
    author="Akshat Gadodia",
    author_email="akshatgadodia@gmail.com",
    description="A Django app for tracking and sending communications like Emails and WhatsApp messages.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/akshatgadodia/django-communications",
)
