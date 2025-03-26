from pathlib import Path

import SimpleITK as sitk
from rich.markdown import Markdown
from textual.app import ComposeResult
from textual.containers import ScrollableContainer
from textual.widgets import Static, Label, TabPane, TabbedContent

from textual_file_viewer.image_viewer import ImageViewer


class MhdNiftiViewer(Static):
    def __init__(self) -> None:
        super().__init__()

    def compose(self) -> ComposeResult:
        with TabbedContent(id='image_viewer'):
            with TabPane('Image', id='tab_image'):
                yield ImageViewer()
            with TabPane('Tags', id='tab_tags'):
                yield ScrollableContainer(Label(id='image_tags'))

    def load_image(self, filename: Path) -> None:
        dataset = sitk.ReadImage(filename)
        self.query_one(ImageViewer).set_array(sitk.GetArrayFromImage(dataset))

        markdown = ['|Key|Value|', '|--|--|']
        for k in dataset.GetMetaDataKeys():  # type: ignore
            markdown.append(f'|{k}|{dataset.GetMetaData(k)}|')  # type: ignore

        self.query_one('#image_tags', Label).update(Markdown('\n'.join(markdown)))
        self.query_one('#image_viewer', TabbedContent).active = 'tab_image'
