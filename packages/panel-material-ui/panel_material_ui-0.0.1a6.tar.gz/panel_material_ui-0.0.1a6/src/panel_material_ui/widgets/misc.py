from __future__ import annotations

import param
from panel.widgets.misc import FileDownload as _FileDownload

from .button import _ButtonBase


class FileDownload(_ButtonBase, _FileDownload):
    """
    The `FileDownload` widget allows a user to download a file.

    It works either by sending the file data to the browser on initialization
    (`embed`=True), or when the button is clicked.

    Reference: https://panel.holoviz.org/reference/widgets/FileDownload.html

    :Example:

    >>> FileDownload(file='IntroductionToPanel.ipynb', filename='intro.ipynb')
    """

    icon_size = param.String(default="1em", doc="""
        Size of the icon as a string, e.g. 12px or 1em.""")

    _esm_base = "FileDownload.jsx"
    _rename = {"_clicks": None, "icon": "icon", "icon_size": "icon_size"}

    def _handle_click(self, event=None):
        self._clicks += 1
