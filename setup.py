from setuptools import setup

setup(
    name="mqtt-panel",
    version=open('version', 'rt', encoding="utf8").read().strip(),
    description="Self hosted Web App panel for MQTT",
    author="Source Simian",
    url="https://github.com/sourcesimian/mqtt-panel",
    license="MIT",
    packages=['mqtt_panel'],
    install_requires=open('python3-requirements.txt', encoding="utf8").readlines(),
    entry_points={
        "console_scripts": [
            "mqtt-panel=mqtt_panel.main:cli",
        ]
    },
)
