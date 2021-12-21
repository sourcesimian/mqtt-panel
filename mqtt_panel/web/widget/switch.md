Publish the next payload in the list of values to a topic. Update the display with text, icon and color when the payload returns on the subscribed topic.
```
    - title: <string>       # Title text
      type: switch          # Widget type
      publish: <topic>      # MQTT topic to write to
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
