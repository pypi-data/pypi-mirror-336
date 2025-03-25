from setuptools import setup, find_packages

setup(
    name='abhinav_greeting',
    version='0.2',
    packages=find_packages(),
    description='A simple Python package that provides personalized greetings.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Abhinav Gera',
    author_email='abhinav.gera@aligne.ai',
    url='https://github.com/abhinav-aligne/abhinav_greeting',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
