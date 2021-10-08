MQTT Panel <!-- omit in toc -->
===

***Web panel app for MQTT***

This project provides a self hostable service that connects to a MQTT broker and serves a progressive web app panel which is fully configurable via YAML.

# Containerization
Example `Dockerfile`:

```
FROM python:3.9-slim

COPY mqtt-panel/python3-requirements.txt /
RUN pip3 install -r python3-requirements.txt

COPY mqtt-panel/setup.py /
COPY mqtt-panel/mqtt_panel /mqtt_panel
RUN python3 /setup.py develop

COPY mqtt-panel/resources/* /resources/

COPY my-config.yaml /config.yaml

ENTRYPOINT ["/usr/local/bin/mqtt-panel", "/config.yaml"]
```

# Development
Setup the virtualenv:

```
python3 -m venv virtualenv
. ./virtualenv/bin/activate
python3 ./setup.py develop
```

Run the server:

```
mqtt-panel ./config-demo.yaml
```

# License

In the spirit of the Hackers of the [Tech Model Railroad Club](https://en.wikipedia.org/wiki/Tech_Model_Railroad_Club) from the [Massachusetts Institute of Technology](https://en.wikipedia.org/wiki/Massachusetts_Institute_of_Technology), who gave us all so very much to play with. The license is [MIT](LICENSE).
