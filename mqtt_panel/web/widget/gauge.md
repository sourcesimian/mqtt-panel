Show the received value and a vertical bar gauge where the text, icon and color will change based on the value of the subscribed payload.
```
    - title: <string>       # Title text
      type: gauge           # Widget type
      subscribe: <topic>    # MQTT topic to listen on
      text: <string>        # optional: The default text when not given with range
      color: <color>        # optional: The default color when not given with range
      icon: <icon>          # optional: The default icon when not given with range
      ranges:                       
      - range: [<int>, <int>] # Value for start and end of range
        text: <string>        # optional: Text shown when value in range
        color: <color>        # optional: Color shown when value in range
        icon: <icon>          # optional: Icon shown when value in range
      ... (repeat)              
                            # max and min value will be determined from starts and ends
```

Example:
```
    - title: Sound
      type: gauge
      subscribe: example/volume
      ranges:
      - range: [0, 10]
        text: "Quiet"
        icon: volume_off
        color: "#00c000"
      - range: [10, 30]
        text: "Gentle"
        icon: volume_mute
        color: "#02b002"
      - range: [30, 70]
        text: "Medium"
        icon: volume_down
        color: "#82b002"
      - range: [70, 90]
        text: "Noisy"
        icon: volume_up
        color: "#b08a02"
      - range: [90, 100]
        text: "Loud"
        icon: volume_up
        color: "#b03c02"
```
