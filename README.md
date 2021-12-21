MQTT Panel <!-- omit in toc -->
===

***Web panel app for MQTT***

This project provides a self hostable service that connects to a MQTT broker and serves a progressive web app panel which is fully configurable via YAML.

- [Running](#running)
  - [Demo](#demo)
  - [Docker](#docker)
- [Configuration](#configuration)
  - [Panels](#panels)
  - [Groups](#groups)
  - [Widgets](#widgets)
    - [Text](#text)
    - [Light](#light)
    - [Button](#button)
    - [Switch](#switch)
    - [Gauge](#gauge)
    - [Select](#select)
    - [Iframe](#iframe)
- [Contribution](#contribution)
  - [Development](#development)
- [License](#license)

# Running
## Demo
Run
```
docker run -it --rm -p 8080:8080 sourcesimian/mqtt-panel:latest
```
and open http://localhost:8080

## Docker
Run
```
mkdir -p $HOME/.cache/mqtt-panel

docker run -n mqtt-panel -d -it --rm -p 8080:8080 \
    --volume my-config.yaml:/config.yaml:ro \
    --volume $HOME/.cache/mqtt-panel:/data/cache:rw \
    sourcesimian/mqtt-panel:latest
```

# Configuration
`mqtt-panel` consumes a single YAML file. To start off you can copy [config-basic.yaml](./config-basic.yaml)

```
mqtt:
  host: <host>                  # MQTT broker host
  port: 1883                    # MQTT broker port
  client-id: mqtt-panel         # MQTT client identifier, often brokers require this to be unique
  topic-prefix: <topic prefix>  # optional: Scopes the MQTT topic prefix
```
```
http:
  host: 0.0.0.0                 # Interface on which web server will listen
  port: 8080                    # Port on which web server will listen
  max-connections: 10           # optional: Limit the number of concurrent connections
```
```
auth:                           # optional: User/password auth
  users:
  - username: admin
    password: admin
```
```
cache:                          # optional: Configure cache
  root: data/cache
```
```
logging:                        # optional: Adjust logging settings
  level: INFO
```

## Panels
`mqtt-panel` is divided into panels, only one panel is show at a time, each panel is a collection of groups.
```
panels:
  - title: <string>             # Panel title text
    icon: widgets               # Icon shown on the menu bar
    groups:                     # list of group identifiers
      - <identifier>            # e.g. "group_one" 
```


## Groups
A group is a boxed collection of widgets. They can be reused on multiple panels.
```
groups:
  - title: <string>             # Title text
    name: <identifier>          # Identifier, e.g. "group_one"
    widgets:                    # List of widgets in ths group
```

## Widgets
A widget is a functional element, which is used to publish or subscribe to MQTT topics, and display and/or input some information.

All widgets have the following common attributes.:
```
    - title: <string>           # Title text
      type: <type>              # Widget type
      qos: [0 | 1 | 2]          # MQTT QoS to use, default: 1
      retain: [False | True]    # Publish with MQTT retain flag, default: False
      cache: [False | True]     # Cache last seen payloads.
```
`retain` is a flag that is set when publishing a payload to MQTT. If set the message will persist in the broker, clients will re-receive the payload when reconnecting. This is not always give the desired behaviour. To improve user experience of mqtt-panel `cache: True` will preserve the last seen payload from the subscribed MQTT topic. This allows the server to remember the state of a topic with `retain: False` during server restarts. You will note after a re-start some widgets will show "unknown" until such time as it recieves a new payload on the subscribed MQTT topic. 


### Text
<!-- include:begin mqtt_panel/web/widget/text.md -->
Simply display the payload of the subscribed MQTT topic
```
    - title: <string>
      type: text
      subscribe: <topic>        # MQTT topic to listen to
      color: <color>
```
Example:
```
    - title: Text               # Title text
      type: text                # Widget type
      subscribe: text/content
      color: "#123456"          # optional: Color of the text
```
<!-- include:end --> 
### Light
<!-- include:begin mqtt_panel/web/widget/light.md -->
Display some text, an icon and color in when the defined payloads are received from the subscribed topic.
```
    - title: <string>           # Title text
      type: light               # Widget type
      subscribe: <topic>        # MQTT topic to listen to
      values:
      - payload: <string>       # Payload to match for this value
        text: <string>          # optional: Text to display on widget
        icon: <icon>            # optional: Icon to display on widget
        color: <color>          # optional: Color of icon and text
      ... (repeat)
```

Example:
```
    - title: My Light
      type: light
      subscribe: light/state
      values:
      - payload: "false"
        text: OFF
        color: black
        icon: light
      - payload: "true"
        text: ON
        color: yellow
        icon: light
```
<!-- include:end --> 
### Button
<!-- include:begin mqtt_panel/web/widget/button.md -->
Publish a constant value to a MQTT topic
```
    - title: <string>           # Title text
      type: button              # Widget type
      text: <string>            # optional: Text to show on widget
      publish: <topic>          # MQTT topic to write to
      payload: <string>         # MQTT payload to publish
```
Example:
```
    - title: My Button
      type: button
      text: Push Me
      publish: button/command
      payload: PREDDED
```
<!-- include:end --> 

### Switch
<!-- include:begin mqtt_panel/web/widget/switch.md -->
Publish the next payload in the list of values to the topic. Update the display with text, an icon and color.
```
    - title: <string>           # Title text
      type: switch              # Widget type
      publish: <topic>          # MQTT topic to write to
      subscribe: <topic>        # MQTT topic to listen to
      values:
      - payload: <string>       # Payload to match for this value
        text: <string>          # optional: Text to display on widget
        icon: <icon>            # optional: Icon to display on widget
        color: <color>          # optional: Color of icon and text
      ... (repeat)
```

Example:
```
    - title: My Switch
      type: switch
      publish: widget/switch/command
      subscribe: widget/switch/state
      values:
      - text: "Off"
        payload: "false"
      - text: "On"
        payload: "true"
```
<!-- include:end --> 
### Gauge
<!-- include:begin mqtt_panel/web/widget/gauge.md -->
Show the received value and a vertical bar gauge where the text, icon and color will change based on the value of the subscribed payload.
```
    - title: <string>           # Title text
      type: gauge               # Widget type
      subscribe: <topic>        # MQTT topic to listen to
      icon: <icon>              # optional: The default icon
      ranges:                       
      - range: [<float>, <float>]  # Value for start and end of range
        text: <string>          # optional: Text show when value in range
        color: <color>          # optional: Color show when value in range
        icon: <icon>            # optional: Icon show when value in range
      ... (repeat)              # max and min value will be determined from starts and ends
```

Example:
```
    - title: Health
      type: gauge
      subscribe: gauge/health
      icon: health_and_safety
      ranges:
      - range: [0, 20]
        text: Poor
        color: red
        icon: warning
      - range: [20, 50]
        text: Moderate
        color: orange
      - range: [50, 80]
        text: Good
        color: yellow
      - range: [80, 100]
        text: Excellent
        color: green
```
<!-- include:end --> 
### Select
<!-- include:begin mqtt_panel/web/widget/select.md -->
Display a `<select>` box from which you can publish a list of values. Will update to matched payloads is subscribed to a topic.
```
    - title: <string>           # Title text
      type: select              # Widget type
      publish: <topic>          # MQTT topic to write to
      subscribe: <topic>        # optional: MQTT topic to listen to
      values:
      - text: <string>          # Text to show in select
        payload: <string>       # Payload to send and match
      ... (repeat)
```

Example:
```
    - title: My Select
      type: select
      publish: widget/select/command
      subscribe: widget/select/state
      values:
      - text: "Venice"
        payload: "Gondola"
      - text: "Cape Town"
        payload: "Mountain"
```
<!-- include:end --> 
### Iframe
<!-- include:begin mqtt_panel/web/widget/iframe.md -->
Display content in a `<iframe>`. The `src` attribute can be bound to a MQTT topic.
```
    - title: <string>           # Title text
      type: iframe              # Widget type
      subscribe: <topic>        # optional: MQTT topic to listen to, bound to ifram 'src'
      attr:                     # Attributes to be set on the iframe
        src: <url>                # optional: Can be set as a default vaule for 'src'
        ...                       # additional attributes
```

Example:
```
    - title: Iframe
      type: iframe
      subscribe: iframe/src
      attr:
        src: https://www.youtube.com/embed/dQw4w9WgXcQ
        width: 480px
        height: 315px
        title: YouTube video player
        allow: accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture
        allowfullscreen:
```
<!-- include:end --> 

# Contribution
Yes sure! And please. I built mqtt-panel because I couldn't find a "I'm not ready to commit to full blown HA yet" solution that was self hosted and server side configurable. I don't know much about contemporary HTML, CSS and Typescript so I will gladly accept advice from those who know more. I want it to be a project that is quick and easy to get up and running, and helps open up MQTT to anyone.
## Development
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
