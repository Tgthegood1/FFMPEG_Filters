from setuptools import setup, find_packages

setup(
    name="FFMPEG_Filters",
    version="1",
    packages=find_packages(),
    install_requires=[
        'Pillow'
    ],
    description="FFMPEG_Filters is a set of effects for images to create a video.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author="Tgthegood",
    author_email="almeidaaxel52@gmail.com",
    url="https://github.com/tu_usuario/mi_libreria",
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)