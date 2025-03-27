from setuptools import setup, find_packages

setup(
    name='long-utils',  # 包的名称
    version='0.7.1',      # 包的版本
    package_dir={'': 'src'},
    packages=find_packages('src'),  # 自动查找包
    description='A utility library for everyday use.',  # 简短描述
    long_description=open('README.md', encoding='utf-8').read(),  # 从 README.md 文件获取详细描述
    long_description_content_type='text/markdown',  # README 格式
    author='zhenzi0322',  # 作者
    author_email='82131529@qq.com',  # 作者邮箱
    url='https://codeup.aliyun.com/zheniz0322/Python/packages/long-utils',
    license='MIT',  # 许可证
    classifiers=[  # 分类信息，帮助其他开发者了解这个包
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=['oss2', 'opencv-python', 'numpy', 'requests'],
    python_requires='>=3.7',  # 支持的 Python 版本
)
