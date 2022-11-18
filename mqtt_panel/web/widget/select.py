from mqtt_panel.web.widget.switch import Switch


class Select(Switch):
    widget_type = 'select'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.default = Default

    def _html_write(self, fh, ctx, state):
        color = ''
        if state.color:
            color = f' data-color="{state.color}"'
        self._write_render(fh, '''\
            <div class="value-item value-{state.name}{ctx.show}"{ctx.confirm}{color} data-icon="{state.icon}" data-text="{state.text}" data-name="{state.name}" data-ro="{state.ro}">
                <span class="material-icons"{ctx.color}>{state.icon}</span>
                <span{ctx.color}>{state.text}</span>
            </div>
        ''', {'ctx': ctx, 'state': state, 'color': color}, indent=6)


class Default:
    _map = {
        ('on', 'true'): ('toggle_on', '#52D017'),
        ('off', 'false'): ('toggle_off', 'black'),
        None: ('radio_button_unchecked', None),
    }

    @classmethod
    def _lookup(cls, *keys):
        for key in keys:
            key = key.lower()
            for k, v in cls._map.items():
                if k and key in k:
                    return v
        return cls._map[None]

    @classmethod
    def icon(cls, *key):
        return cls._lookup(*key)[0]

    @classmethod
    def color(cls, *key):
        return cls._lookup(*key)[1]
