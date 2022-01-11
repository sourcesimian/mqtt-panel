Display some text, an icon and color when the defined payloads are received from the subscribed topic. When tapped, shows a list of the other values which can be published.
```
    - title: <string>       # Title text
      type: select          # Widget type
      publish: <topic>      # MQTT topic to write to
      subscribe: <topic>    # optional: MQTT topic to listen on
      values:
      - payload: <string>     # Payload to send and match
        text: <string>        # optional: Text shown
        icon: <icon>          # optional: Icon shown
        color: <color>        # optional: Color of icon and text
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
        icon: rowing
        color: cyan
      - text: "Cape Town"
        payload: "Mountain"
        icon: landscape
        color: green
```
