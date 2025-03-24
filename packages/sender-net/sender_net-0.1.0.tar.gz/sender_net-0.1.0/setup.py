from setuptools import setup, find_packages

setup(
    name='sender_net',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    license='MIT',  # Or your license
    description='A reusable Django app that integrates Wagtail with Sender.net.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/sender_net',  # Update if public
    author='Your Name',
    author_email='you@example.com',
    install_requires=[
        'Django>=5.1',
        'wagtail>=4.0',
        'requests',
        'mjml',
    ],
    classifiers=[
        'Framework :: Django',
        'Framework :: Wagtail',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
