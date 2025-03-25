from io import StringIO
from typing import TextIO

from PySide6 import QtWidgets


class StdRedirect(StringIO):

    def __init__(
        self,
        initial_value: str | None = "",
        newline: str | None = "\n",
    ) -> None:
        super().__init__(initial_value, newline)
        self.text_edits: list[QtWidgets.QTextEdit] = []
        self.orig_streams: list[TextIO] = []

    def write(self, s: str) -> int:
        for stream in self.orig_streams:
            stream.write(s)
        for text_edit in self.text_edits:
            text_edit.setPlainText(text_edit.toPlainText() + s)
        return super().write(s)
