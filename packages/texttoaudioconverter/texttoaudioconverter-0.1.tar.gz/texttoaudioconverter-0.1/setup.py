from setuptools import setup, find_packages

setup(
    name='texttoaudioconverter',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'gTTS',
    ],
    author='Your Name',
    description='A simple package to convert text to audio',
    url='https://github.com/yourusername/text_to_audio_converter',
)
