import pyglet
from enum import IntEnum


class PanelGeometry(IntEnum):
    PANEL_GEOMETRY_STRIP = 0,
    PANEL_GEOMETRY_SQUARE = 1,
    #  TODO: add RECT support


class PanelType(IntEnum):
    PANEL_TYPE_STRAIGHT = 0,
    PANEL_TYPE_ZIGZAG = 1,


class PanelSim:
    def __init__(
        self,
        geometry: PanelGeometry = PanelGeometry.PANEL_GEOMETRY_SQUARE,
        panel_type: PanelType = PanelType.PANEL_TYPE_STRAIGHT,
        num_leds: int = 0,
        width: int = 0,
        height: int = 0,
    ) -> None:
        self._num_leds = num_leds
        self._width = width
        self._height = height
        self._geometry = geometry
        self._panel_type = panel_type

        self._window = pyglet.window.Window()
        self.on_draw = self._window.event(self.on_draw)

        self._label = pyglet.text.Label(
            'Hello, world',
            font_size=25,
            color=(123, 123, 123, 255),
            x=self._window.width//2,
            y=self._window.height//2,
            anchor_x='center', anchor_y='center'
        )

    def label_update_set(self, func, interval: float = 0.05):
        pyglet.clock.schedule_interval(func, interval)

    def label_text_update(self, text: str = '', color: list = (123, 123, 123, 255)):
        self._label.color = color
        self._label.text = text

    def on_draw(self):
        self._window.clear()
        self._label.draw()

    def window(self) -> pyglet.window.Window:
        return self._window

    def run(self):
        pyglet.app.run()

    def stop(self):
        pyglet.app.exit()
