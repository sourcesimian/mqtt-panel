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
