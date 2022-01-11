Display some text, an icon and color when the defined payloads are received from the subscribed topic.
```
    - title: <string>       # Title text
      type: light           # Widget type
      subscribe: <topic>    # MQTT topic to listen on
      values:
      - payload: <string>     # Payload to match for this value
        text: <string>        # optional: Text shown
        icon: <icon>          # optional: Icon shown
        color: <color>        # optional: Color of icon and text
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
