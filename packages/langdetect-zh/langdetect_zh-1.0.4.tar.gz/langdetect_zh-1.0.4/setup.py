try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open('README.md') as f:
    readme = f.read()

setup(
    name='langdetect_zh',
    version='1.0.4',
    description='Google\'s langdetect modified for Chinese texts',
    long_description=readme,
    long_description_content_type='text/markdown',
    author='huyc',
    author_email='huyc@mail.ecust.edu.cn',
    keywords='language detection chinese',
    packages=['langdetect_zh', 'langdetect_zh.utils', 'langdetect_zh.tests'],
    include_package_data=True,
    install_requires=['six'],
    license='MIT',
    license_file='LICENSE',  # 关键修复点
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',  # 修正分类器
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ]
)