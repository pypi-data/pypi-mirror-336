from setuptools import setup, find_packages

setup(
    name='spatialwalk-agora-realtime-ai-api',
    version='1.1.1',
    author='spatialwalk',
    author_email='liyuhang@spatialwalk.net',
    description='spatialwalk fork of Agora\'s low latency, high performance Realtime API to work with Voice Conversational AI',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/AgoraIO/agora-realtime-ai-api',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.11',
    install_requires=[
        'pyee==12.0.0',
        'agora-python-server-sdk==2.2.1'
    ],  # List of dependencies (if any)
)
