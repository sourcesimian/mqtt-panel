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
