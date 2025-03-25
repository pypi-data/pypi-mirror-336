from setuptools import setup, find_packages

setup(
    name='loki-django-logger',
    version='1.0.9',
    description='Loki logger for Django applications',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Irwin Rex',
    author_email='irwinrex.a@gmail.com',
    url='https://github.com/irwinrex/django-loki-logger',
    packages=find_packages(),
    install_requires=[
        'Django>=4.0',
        'requests>=2.26.0'
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: System :: Logging',
    ],
    keywords='django loki logger async log-aggregation',
    python_requires='>=3.8',
    include_package_data=True,
)
