from setuptools import setup, find_packages

setup(
    name="am_report",
    version="0.1.5",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "asgiref==3.8.1",
        "cffi==1.17.1",
        "Django==4.2.13",
        "django-cors-headers==4.7.0",
        "djangorestframework==3.15.2",
        "psutil==7.0.0",
        "psycopg2-binary==2.9.10",
        "pycparser==2.22",
        "sqlparse==0.5.3"

        # Add other dependencies from your requirements.txt
    ],
    entry_points={
        "console_scripts": [
            "odoo_health_monitoring_tool=health_report.cli:main",
        ],
    },
    python_requires=">=3.6",
    author="Your Name",
    author_email="your.email@example.com",
    description="A Django application for monitoring Odoo server metrics",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/odoo-health-report",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Framework :: Django",
    ],
)
