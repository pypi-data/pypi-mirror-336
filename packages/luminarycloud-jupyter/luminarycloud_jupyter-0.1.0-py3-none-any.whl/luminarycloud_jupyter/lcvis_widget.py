import anywidget
import pathlib
import traitlets
from typing import Any, Optional

base_path = pathlib.Path(__file__).parent / "static"


class LCVisWidget(anywidget.AnyWidget):
    _esm: pathlib.Path = base_path / "lcvis.js"

    # TODO: we'll bundle the single threaded wasm here for vanilla Jupyter

    data: traitlets.Bytes = traitlets.Bytes().tag(sync=True)
    last_screenshot: Optional[bytes] = None

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.on_msg(self.receive_widget_message)

    def receive_widget_message(self, widget: Any, content: str, buffers: list[bytes]) -> None:
        if content == "screenshot taken":
            self.last_screenshot = buffers[0]

    def take_screenshot(self) -> None:
        self.last_screenshot = None
        self.send("screenshot")
