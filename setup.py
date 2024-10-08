from setuptools import setup


if __name__ == '__main__':
    setup(
        name='tab2space',
        version='0.0.1',
        packages=['tab2space'],
        entry_points={
            'console_scripts': [
                'tab2space=tab2space.t2s:main'
            ]
        },
        install_requires=['wcwidth']
    )
