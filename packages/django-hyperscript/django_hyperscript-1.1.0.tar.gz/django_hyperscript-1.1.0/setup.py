from setuptools import setup, find_packages

setup(
    name="django-hyperscript",
    version="1.1.0",
    description="Custom Django template tags for integrating Hyperscript with Django templates.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Lucas Lorenz",
    author_email="LukeLorenzBA@gmail.com",
    url="https://github.com/LucLor06/django-hyperscript",
    license="MIT",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Django>=3.2",
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Framework :: Django",
        "Framework :: Django :: 3.2",
        "Framework :: Django :: 4.0",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords="django hyperscript template-tags frontend backend-integration",
    python_requires=">=3.6",
    project_urls={
        "Documentation": "https://github.com/LucLor06/django-hyperscript#readme",
        "Source": "https://github.com/LucLor06/django-hyperscript",
        "Tracker": "https://github.com/LucLor06/django-hyperscript/issues",
    },
)