from setuptools import setup


setup(
    name='unixtime-converter',
    version='1.0.3',
    author='Franz Wiesinger',
    author_email='py@roadrunnerserver.com',
    description='application for converting local time or UTC into Unixtime \
        and viceversa',
    url='https://docs.roadrunnerserver.com/unixtime/html/index.html',
    license='MIT license',
    packages=[
        'res',
        'tests'
    ],
    install_requires=[
        'datetime', 'tkinter', 'pytz', 'zoneinfo', 'tkhtmlview'
    ],
    python_requires='> 3.7',
    entry_points={
        'console_scripts': [
            'unixtime = unixtime.__main__:unixtime'
        ]
    },
    classifiers=[
        'Environment :: X11 Applications',
        'Environment :: Win32 (MS Windows)',
        'Intended Audience :: Customer Service',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.0',
        'Topic :: Desktop Environment',
        'Topic :: Software Development',
        'Topic :: Utilities'
    ],
    keywords=[
        'unixtime', 'utc', 'local time', 'the epoch', 'converter', 'tkinter',
        'GUI', 'timezone', 'datetime'
    ]
)
