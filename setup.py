from setuptools import setup

setup(
    name="mqtt-panel",
    version=open('version', 'rt').read().strip(),
    description="Self hosted Web App panel for MQTT",
    author="Source Simian",
    url="https://github.com/sourcesimian/mqtt-panel",
    license="MIT",
    packages=['mqtt_panel'],
    install_requires=open('python3-requirements.txt').readlines(),
    entry_points={
        "console_scripts": [
            "mqtt-panel=mqtt_panel.main:cli",
        ]
    },
)
