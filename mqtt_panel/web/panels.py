from mqtt_panel.web.component import Component

class Panels(Component):
    def __init__(self):
        super(Panels, self).__init__(4)
        self._panel_map = {}
        self._panels = []

    def add_panel(self, panel):
        self._panels.append(panel)
        self._panel_map[panel.name] = panel

    def _body(self, fh):
        for panel in self._panels:
            panel.body(fh)

    # def _script(self, fh):
    #     widgets = set()
    #     for panel in self._panels:
    #         widgets.update(panel.widgets())
    #     for widget in sorted(widgets, key=lambda w: w.widget_type):
    #         fh.write(f'/*** widget: {widget.widget_type} ***/\n')
    #         widget.javascript(fh)
    #         fh.write('\n')
