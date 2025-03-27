from setuptools import setup, find_packages


setup(
    name="LCD_16x2",
    version="0.1.0-alpha13",
    packages=["lcd_16x2",
              "lcd_16x2.drivers",
              "lcd_16x2.emulators",
              "demo"],
    install_requires=['requests~=2.32.3',
                      'beautifulsoup4~=4.13.3',
                      'setuptools~=78.1.0'],
    author="Matthew Timmons-Brown (the-raspberry-pi-guy)",
    maintainer="https://github.com/the-raspberry-pi-guy/lcd/contributors",
    description="Python package for interfacing with a 16x2 character I2C liquid-crystal display (LCD).",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/the-raspberry-pi-guy/lcd",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS",
        "Operating System :: Unix",
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'lcd-setup=lcd_16x2.lcd_install:run_install'
        ]
    },
    include_package_data=True
)
