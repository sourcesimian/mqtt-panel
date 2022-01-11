Display content in a `<iframe>`. The `src` attribute can be bound to a MQTT topic.
```
    - title: <string>       # Title text
      type: iframe          # Widget type
      subscribe: <topic>    # optional: MQTT topic to listen on, bound to iframe 'src'
      refresh: <seconds>    # optional: Interval at which to refresh the iframe
      attr:                 # Attributes to be set on the iframe
        src: <url>            # optional: Can be set as a default vaule for 'src'
        ...                   # additional attributes
```

Example:
```
    - title: Iframe
      type: iframe
      subscribe: iframe/src
      attr:
        src: https://www.youtube.com/embed/dQw4w9WgXcQ
        width: 480px
        height: 315px
        title: YouTube video player
        allow: accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture
        allowfullscreen:
```
