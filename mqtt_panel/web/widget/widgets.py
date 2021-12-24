
from mqtt_panel.web.widget.widget import Widget

from mqtt_panel.web.widget.button import Button
# from mqtt_panel.web.widget.dropdown import Dropdown
from mqtt_panel.web.widget.gauge import Gauge
from mqtt_panel.web.widget.iframe import Iframe
from mqtt_panel.web.widget.image import Image
from mqtt_panel.web.widget.light import Light
from mqtt_panel.web.widget.select import Select
from mqtt_panel.web.widget.switch import Switch
from mqtt_panel.web.widget.text import Text
from mqtt_panel.web.widget.value import Value


def register_widgets():
    Widget.register(Button)
    # Widget.register(Dropdown)
    Widget.register(Gauge)
    Widget.register(Iframe)
    Widget.register(Image)
    Widget.register(Light)
    Widget.register(Select)
    Widget.register(Switch)
    Widget.register(Text)
    Widget.register(Value)


__all__ = ['register_widgets']
