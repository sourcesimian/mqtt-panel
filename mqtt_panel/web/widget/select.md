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
