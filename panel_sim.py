import pyglet
from enum import IntEnum

from pyglet import shapes

LED_SIDE_SIZE = 50
LED_SPACING = 10

WINDOW_HEIGHT = 480
WINDOW_WIDTH = 800


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
        self._leds = []

        self._window = pyglet.window.Window()
        self.on_draw = self._window.event(self.on_draw)
        self.on_resize = self._window.event(self.on_resize)

        self._label = pyglet.text.Label(
            'Hello, world',
            font_size=19,
            color=(123, 123, 123, 255),
            x=self._window.width - 20,
            y=30,
            height=20,
            anchor_x='right', anchor_y='center'
        )

    def label_update_set(self, func, interval: float = 0.05):
        pyglet.clock.schedule_interval(func, interval)

    def label_text_update(self, text: str = '', color: list = (123, 123, 123, 255)):
        self._label.color = color
        self._label.text = 'rms: {}'.format(text)

    def on_draw(self):
        self._window.clear()
        self._label.draw()

        for rect in self._leds:
            rect.draw()

    def on_resize(self, width, height):
        self._leds_generate()
        self._label.position = (self._window.width - 20, 30)

    def window(self) -> pyglet.window.Window:
        return self._window

    def run(self) -> None:
        pyglet.app.run()

    def stop(self):
        pyglet.app.exit()

    def leds(self) -> list:
        return self._leds

    def _leds_generate(self) -> None:
        self._leds.clear()

        led_side = ((self._window.height - (self._label.height * 2)) /
                    self._height) - LED_SPACING

        count = 1
        # print('{} x {}'.format(self._window.width, (led_side * self._width)))
        for y in range(0, self._height):
            y_pos = self._label.height * 2 + LED_SPACING / \
                2 + (led_side + LED_SPACING) * y
            for x in range(0, self._width):
                x_offset = 0  # (LED_SPACING + led_side * self._width) - \
                (self._window.width - (LED_SPACING + led_side * self._width))

                x_pos = x_offset + LED_SPACING + \
                    ((led_side + LED_SPACING) * x)

                self._leds.append(pyglet.shapes.Rectangle(
                    x=x_pos,
                    y=y_pos,
                    width=led_side,
                    height=led_side,
                    color=(count, 112, 112)
                ))
                count *= 5
