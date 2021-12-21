Display a `<select>` box from which you can publish a list of values. Will update to matched payloads if subscribed to a topic.
```
    - title: <string>       # Title text
      type: select          # Widget type
      publish: <topic>      # MQTT topic to write to
      subscribe: <topic>    # optional: MQTT topic to listen on
      values:
      - payload: <string>     # Payload to send and match
        text: <string>        # Text shown in select
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
