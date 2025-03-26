import dataclasses
from typing import Any

import PIL.Image
import PIL.ImageDraw
import numpy as np
from textual import on
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.widgets import Static, Label
from textual_image.widget import Image
from textual_slider import Slider


@dataclasses.dataclass
class SlicePhaseId:
    slice_id: int | None = None
    phase_id: int | None = None


# pylint: disable=too-many-instance-attributes
class ImageViewer(Static):
    DEFAULT_CSS = """
    #image_viewer {
        width: auto;
        height: 1fr;
    }
    
    #slice_id {
        width: auto;
        height: 3;
        padding: 1 1;
    }
    
    #phase_id {
        width: auto;
        height: 3;
        padding: 1 1;
    }
    
    #slice_id_slider {
        width: 1fr;
        height: 3;
    }
    
    #phase_id_slider {
        width: 1fr;
        height: 3;
    }
    
    #slice_id_container {
        width: 1fr;
        height: auto;
    }
    
    #phase_id_container {
        width: 1fr;
        height: auto;
    }
    
    #slice_id_container.remove {
        display: none;
    }
    
    #phase_id_container.remove {
        display: none;
    }   
    """
    BINDINGS = [
        Binding('ctrl-left', 'previous_slice', 'Previous Slice'),
        Binding('ctrl-right', 'next_slice', 'Next Slice'),
        Binding('ctrl-up', 'next_phase', 'Next Phase'),
        Binding('ctrl-down', 'previous_phase', 'Previous Phase'),
    ]

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._array: np.ndarray | None = None
        self.index = SlicePhaseId()
        self._image_range = (-1, -1)
        self.text_top_left = ''
        self.text_top_right = ''
        self.text_bottom_left = ''
        self.text_bottom_right = ''
        self.draw_overlay = True

    def compose(self) -> ComposeResult:
        with Vertical(id='image_viewer_vertical'):
            with Horizontal(id='phase_id_container', classes='remove'):
                yield Label('PH:    ', id='phase_id')
                yield Slider(min=0, max=1, step=1, id='phase_id_slider')
            with Horizontal(id='slice_id_container', classes='remove'):
                yield Label('SL:    ', id='slice_id')
                yield Slider(min=0, max=1, step=1, id='slice_id_slider')
            yield Image(id='image_viewer')

    def clear(self) -> None:
        self._array = None
        self.index = SlicePhaseId()
        self._image_range = (-1, -1)

    def set_array(self, array: np.ndarray) -> None:
        self._image_range = (np.amin(array), np.amax(array))
        self._array = (array - self._image_range[0]) * 255.0 / (self._image_range[1] - self._image_range[0])

        slice_id_container = self.query_one('#slice_id_container', Horizontal)
        slice_id_slider = self.query_one('#slice_id_slider', Slider)
        phase_id_container = self.query_one('#phase_id_container', Horizontal)
        phase_id_slider = self.query_one('#phase_id_slider', Slider)

        match len(self._array.shape):  # type: ignore
            case 2:
                slice_id_container.set_class(True, 'remove')
                phase_id_container.set_class(True, 'remove')
            case 3:
                slice_id_slider.max = self._array.shape[0] - 1  # type: ignore
                slice_id_slider.value = slice_id_slider.max // 2
                slice_id_container.set_class(slice_id_slider.max <= 1, 'remove')
                phase_id_container.set_class(True, 'remove')
            case 4:
                slice_id_slider.max = self._array.shape[1] - 1  # type: ignore
                phase_id_slider.max = self._array.shape[0] - 1  # type: ignore
                slice_id_slider.value = slice_id_slider.max // 2
                phase_id_slider.value = phase_id_slider.max // 2
                slice_id_container.set_class(slice_id_slider.max <= 1, 'remove')
                phase_id_container.set_class(phase_id_slider.max <= 1, 'remove')

        self.call_after_refresh(self._process_image)

    def action_next_slice(self) -> None:
        slider = self.query_one('#slice_id_slider', Slider)
        slider.value = slider.value + 1

    def action_previous_slice(self) -> None:
        slider = self.query_one('#slice_id_slider', Slider)
        slider.value = slider.value - 1

    def action_next_phase(self) -> None:
        slider = self.query_one('#phase_id_slider', Slider)
        slider.value = slider.value + 1

    def action_previous_phase(self) -> None:
        slider = self.query_one('#phase_id_slider', Slider)
        slider.value = slider.value - 1

    @on(Slider.Changed)
    def frame_changed(self, _: Slider.Changed) -> None:
        if self._array is None:
            return

        slice_id_slider = self.query_one('#slice_id_slider', Slider)
        phase_id_slider = self.query_one('#phase_id_slider', Slider)
        new_index = SlicePhaseId(
            slice_id_slider.value if not slice_id_slider.has_class('remove') else None,
            phase_id_slider.value if not phase_id_slider.has_class('remove') else None
        )

        if new_index == self.index:
            return

        self.query_one('#slice_id', Label).update(f'Sl: {new_index.slice_id:3}/{slice_id_slider.max:3}')
        self.query_one('#phase_id', Label).update(f'Ph: {new_index.phase_id:3}/{phase_id_slider.max:3}')

        self.index = new_index

        self._process_image()

    def _process_image(self) -> None:
        slice_id_slider = self.query_one('#slice_id_slider', Slider)
        phase_id_slider = self.query_one('#phase_id_slider', Slider)

        assert self._array is not None
        match len(self._array.shape):  # type: ignore
            case 2:
                im = PIL.Image.fromarray(self._array).convert('RGB')
            case 3:
                im = PIL.Image.fromarray(self._array[slice_id_slider.value]).convert('RGB')
            case 4:
                im = PIL.Image.fromarray(self._array[phase_id_slider.value][slice_id_slider.value]).convert('RGB')
            case _:
                raise RuntimeError('Unsupported dimension (<2, >4).')

        if self.draw_overlay:
            self._draw_overlay(im)

        image_viewer = self.query_one('#image_viewer', Image)
        width = image_viewer.container_viewport.width * 13  # text size
        height = image_viewer.container_viewport.height * 2 * 13  # Don't know why times 2, but it seems to work
        width = min(width, 1024)
        height = min(height, 1024)

        try:
            im.thumbnail((width, height))
            image_viewer.image = im
        except ZeroDivisionError:
            pass

    def _draw_overlay(self, im: PIL.Image.Image) -> None:
        width, height = im.size

        draw = PIL.ImageDraw.Draw(im)

        # TL
        draw.text((2, 2), self.text_top_left, fill='yellow', stroke_width=1, stroke_fill='black')

        # TR
        text_bbox = draw.textbbox(xy=(0, 0), text=self.text_top_right, stroke_width=1)
        text_w = text_bbox[2] - text_bbox[0]
        draw.text((width - text_w - 2, 2),
                  self.text_top_right, fill='yellow', align='right', stroke_width=1, stroke_fill='black')

        # BL
        text_bbox = draw.textbbox(xy=(0, 0), text=self.text_bottom_left, stroke_width=1)
        text_h = text_bbox[3] - text_bbox[1]
        draw.text((2, height - text_h - 2),
                  self.text_bottom_left, fill='yellow', stroke_width=1, stroke_fill='black')

        # BR
        text_bbox = draw.textbbox(xy=(0, 0), text=self.text_bottom_right, stroke_width=1)
        text_w, text_h = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]
        draw.text((width - text_w - 2, height - text_h - 2),
                  self.text_bottom_right, fill='yellow', align='right', stroke_width=1, stroke_fill='black')
