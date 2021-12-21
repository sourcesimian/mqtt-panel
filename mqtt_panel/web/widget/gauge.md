Show the received value and a vertical bar gauge where the text, icon and color will change based on the value of the subscribed payload.
```
    - title: <string>           # Title text
      type: gauge               # Widget type
      subscribe: <topic>        # MQTT topic to listen to
      icon: <icon>              # optional: The default icon
      ranges:                       
      - range: [<float>, <float>]  # Value for start and end of range
        text: <string>          # optional: Text show when value in range
        color: <color>          # optional: Color show when value in range
        icon: <icon>            # optional: Icon show when value in range
      ... (repeat)              # max and min value will be determined from starts and ends
```

Example:
```
    - title: Health
      type: gauge
      subscribe: gauge/health
      icon: health_and_safety
      ranges:
      - range: [0, 20]
        text: Poor
        color: red
        icon: warning
      - range: [20, 50]
        text: Moderate
        color: orange
      - range: [50, 80]
        text: Good
        color: yellow
      - range: [80, 100]
        text: Excellent
        color: green
```
