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
