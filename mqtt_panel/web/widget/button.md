Publish a constant value to a MQTT topic
```
    - title: <string>       # Title text
      type: button          # Widget type
      text: <string>        # optional: Text to show on widget
      publish: <topic>      # MQTT topic to write to
      payload: <string>     # MQTT payload to publish
```
Example:
```
    - title: My Button
      type: button
      text: Push Me
      publish: button/command
      payload: PRESSED
```
