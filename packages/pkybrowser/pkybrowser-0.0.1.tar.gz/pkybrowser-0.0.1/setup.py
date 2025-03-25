from setuptools import setup, find_packages

setup(
    name='pkybrowser',
    version='0.0.1',
    description='selenium을 이용한 데이타 수집하기 위한 기본 브라우저 설정 - chrome, firefox 용',
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