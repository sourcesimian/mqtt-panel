Show the received value and a vertical bar gauge where the text, icon and color will change based on the value of the subscribed payload. Additionally when tapped, show a slider which can be used to input and publish a value between the max and min value.

```
    - title: <string>       # Title text
      type: slider          # Widget type
      live: [False | True]  # optional: Realtime publishing. Default: False
      ... (same as gauge)
```
Setting `live: True` the current value of the slider will be published as it changes. The default behaviour is to publish only the final selected value when the slider is released.
