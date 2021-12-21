### Image
```
    - title: <string>         # required
      type: image             # required
      src: <url>              # optional
      subscribe: <topic>      # optional - binds to image `src`
      height: <dimension>     # optional - sets image `height` attribute
      width: <dimension>      # optional - sets image `width` attribute
```
Example:
```
    - title: Image
      type: image
      src: "https://upload.wikimedia.org/wikipedia/commons/d/dc/Table_Mountain_DanieVDM.jpg"
      height: 300px
```