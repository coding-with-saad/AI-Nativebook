from setuptools import setup

package_name = 'ros2_basics_py'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='User',
    maintainer_email='user@example.com',
    description='Module 1: ROS 2 Basics Python Examples for AI Native Book',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'simple_publisher = ros2_basics_py.simple_publisher:main',
            'simple_subscriber = ros2_basics_py.simple_subscriber:main',
            'service_server = ros2_basics_py.service_server:main',
            'service_client = ros2_basics_py.service_client:main',
            'smart_agent = ros2_basics_py.smart_agent:main',
        ],
    },
)
