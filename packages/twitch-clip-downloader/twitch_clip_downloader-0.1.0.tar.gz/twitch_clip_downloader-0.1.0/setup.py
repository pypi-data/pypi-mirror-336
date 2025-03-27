from setuptools import setup, find_packages

setup(
    name='twitch_clip_downloader',
    version='0.1.0',
    description='A simple Python module to download Twitch clips',
    author='Adrian Pernberg',
    author_email='adrian@pernberg.de',
    packages=find_packages(),
    install_requires=[
        'requests'
    ],
    python_requires='>=3.6',
)
