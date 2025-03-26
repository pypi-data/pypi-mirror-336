from setuptools import find_packages, setup

setup(
    name="django-auto-drf",
    version="0.1.0",
    description="Automated API registration for Django Rest Framework",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="marcocamplesemc@gmail.com",
    url="https://github.com/wolfmc3/django-auto-drf",
    packages=find_packages(),
    install_requires=[
        "Django>=3.2",
        "djangorestframework>=3.12",
        "django-filter>=2.4",
        "drf-spectacular>=0.22.0"
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Framework :: Django",
        "Framework :: Django :: 3.2",
        "Framework :: Django :: 4.0",
    ],
)
