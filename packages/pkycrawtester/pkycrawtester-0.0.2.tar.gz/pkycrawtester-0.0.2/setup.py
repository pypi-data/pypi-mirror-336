from setuptools import setup, find_packages

setup(
    name='pkycrawtester',
    version='0.0.2',
    description='selenium을 이용한 데이타 크롤링 테스트용 - Chrome, Firefox',
    author='Lian Park',
    author_email='g1000white@gmail.com',
    url='',
    install_requires=['selenium',],
    packages=find_packages(exclude=[]),
    keywords=['python tutorial', 'pypi'],
    python_requires='>=3.6',
    package_data={},
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)