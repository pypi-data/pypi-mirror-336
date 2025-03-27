from setuptools import setup, find_packages

setup(
    name='DiffusionForTimeSeries',  
    version='0.1.0',  
    packages=find_packages(), 
    description='A diffusion model for time series forecasting and noise modeling.',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author='WEIZIHAO',  
    author_email='aweizihao@gmail.com',  # 替换为你的邮箱
    url='https://github.com/AWeizihao/DiffusionForTimeSeries.git',  
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # 适用的 Python 版本
    install_requires=[
        'matplotlib',
        'numpy',
        'pandas',
        'scikit-learn',  
        'scipy',
        'torch' ,
        'setuptools'
    ],
    entry_points={
        'console_scripts': [
            'diffusion-cli=cli:main',  # 允许命令行调用 cli.py
        ]
    }
)

import subprocess

def check_cuda():
    try:
        output = subprocess.check_output(["nvidia-smi"], stderr=subprocess.STDOUT)
        return True
    except Exception:
        return False

if check_cuda():
    print(
        "\033[93m[Note] NVIDIA GPU detected. To enable GPU acceleration, install CUDA version of PyTorch:\033[0m\n"
        "pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121\n"
    )
    print("\033[93m[Warning] 当前版本的PyTorch不会启用 GPU 加速。如果您的 GPU 支持 CUDA 加速，安装 CUDA 版本的 PyTorch 以启用。\n"
          "用代码 pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121 安装")