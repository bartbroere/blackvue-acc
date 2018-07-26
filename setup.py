from setuptools import setup

with open('README.md', 'r') as readme:
    readme = "".join(readme.readlines())

with open('requirements.in', 'r') as requirements:
    dependencies = [dependency.split('#')[0].replace('\n', '').replace(' ', '')
                    for dependency in requirements.readlines() if
                    dependency[0] != '#']

setup(
    name='blackvue_acc',
    version='2018.7.26',
    url='https://github.com/bartbroere/blackvue-acc/',
    author='Bart Broere',
    author_email='maiil@bartbroere.eu',
    license='MIT License',
    description="Parse accelerometer records created by BlackVue Dashcams.",
    keywords='blackvue accelerometer gforce dashcam 3gf parse parser',
    long_description=readme,
    py_modules=['blackvue_acc', 'blackclue'],
    install_requires=dependencies,
    entry_points={
        'console_scripts': ['blackvue_acc=blackvue_acc:main'],
    },
    classifiers=(
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Utilities',
    )
)
