from setuptools import setup, find_packages

setup(
    name='clip_cam',
    version='0.1.2',
    author='Aditya Gandhamal, Aniruddh Sikdar',
    author_email='',
    description='A package for visualizing the prompt-image feature matching in ViT-based CLIP models, highlighting the alignment between image features and textual prompts.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    license='MIT',
    url='https://github.com/adityagandhamal/clip_cam',
    packages=find_packages(),
    install_requires=[
        'torch',
        'numpy',
        'einops',
        'opencv-python',
        'matplotlib',
        'detectron2',
        'Pillow',
        'open_clip',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
