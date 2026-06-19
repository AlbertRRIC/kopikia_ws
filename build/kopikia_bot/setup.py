from setuptools import find_packages, setup

package_name = 'kopikia_bot'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools', 'rclpy'],
    zip_safe=True,
    maintainer='rric',
    maintainer_email='rric@example.com',
    description='Kopikia Bot package for xArm and Vision integration',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        	'preparm = kopikia_bot.PrepArm:main'
        ],
    },
)
