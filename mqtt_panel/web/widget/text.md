Simply display the payload of the subscribed MQTT topic.
```
    - title: <string>       # Title text
      type: text            # Widget type
      subscribe: <topic>    # MQTT topic to listen on
      color: <color>        # optional: Color of the text
```
Example:
```
    - title: My Text
      type: text
      subscribe: text/content
      color: "#123456"
```
