from pathlib import Path
from typing import cast

import numpy as np
import pydicom
from pydicom.errors import InvalidDicomError
from pydicom.pixel_data_handlers import util
from textual.app import ComposeResult
from textual.widgets import Static, TabPane, TabbedContent

from textual_file_viewer.dicom_tree import DicomTree
from textual_file_viewer.image_viewer import ImageViewer

SUPPORTED_PHOTOMETRIC_INTERPRETATIONS = {'MONOCHROME1', 'MONOCHROME2', 'YBR_FULL_422'}


class DicomViewer(Static):
    def __init__(self) -> None:
        super().__init__()

    def compose(self) -> ComposeResult:
        with TabbedContent(id='dicom_viewer'):
            with TabPane('Image', id='tab_image'):
                yield ImageViewer()
            with TabPane('Tags', id='tab_tags'):
                yield DicomTree(id='dicom_tree')

    def load_dicom(self, filename: Path) -> None:
        try:
            dataset = cast(pydicom.Dataset, pydicom.dcmread(filename))
        except InvalidDicomError:
            return

        if dataset.PhotometricInterpretation not in SUPPORTED_PHOTOMETRIC_INTERPRETATIONS:
            self.notify(message=f'Only {" ".join(SUPPORTED_PHOTOMETRIC_INTERPRETATIONS)} are supported',
                        title='No image view',
                        severity='warning')
            return

        self.query_one(DicomTree).set_dataset(dataset)

        np_array = dataset.pixel_array

        match dataset.PhotometricInterpretation:
            case 'MONOCHROME1':
                # minimum is white, maximum is black
                # (https://dicom.innolitics.com/ciods/ct-image/image-pixel/00280004)
                np_array = pydicom.pixel_data_handlers.apply_voi_lut(np_array, dataset)
                minimum, maximum = np.amin(np_array), np.amax(np_array)
                np_array = (maximum - np_array) * 255.0 / (maximum - minimum)
            case 'MONOCHROME2':
                center, width = dataset.WindowCenter, dataset.WindowWidth
                minimum, maximum = center - width / 2, center + width / 2
                np_array[np_array < minimum] = minimum
                np_array[np_array > maximum] = maximum
                np_array = (np_array - minimum) * 255.0 / (maximum - minimum)
            case 'YBR_FULL_422':
                np_array = util.convert_color_space(np_array, 'YBR_FULL', 'RGB')
            case _:
                pass

        self.query_one(ImageViewer).set_array(np_array)
