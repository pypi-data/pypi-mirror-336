import sys

import finesse
from PySide6 import QtCore, QtGui, QtWidgets

import virgui
from virgui.action_runner import ActionRunner
from virgui.check_version import check_version
from virgui.console import StdRedirect
from virgui.kat_log import KatScriptLog
from virgui.katscript_viewer import KatScriptViewer
from virgui.model_layout import ModelLayout
from virgui.plotting import PlottingWidget

finesse.init_plotting()

QtCore.QLocale.setDefault(QtCore.QLocale("US"))


class ZoomableGraphicsScene(QtWidgets.QGraphicsScene):

    def wheelEvent(self, event: QtWidgets.QGraphicsSceneWheelEvent) -> None:
        scale_factor = 1.15
        if event.delta() > 0:
            self.views()[0].scale(scale_factor, scale_factor)
        else:
            self.views()[0].scale(1 / scale_factor, 1 / scale_factor)
        event.accept()
        return super().wheelEvent(event)


# https://www.pythonguis.com/tutorials/pyside6-qgraphics-vector-graphics/
class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"VIRGUI [{virgui.__version__}]")
        self.setMinimumSize(900, 900)

        self.kat_text = KatScriptViewer()
        self.kat_log = KatScriptLog()
        self.model_layout = ModelLayout(
            katscript_listener=self.kat_text.update,
            katlog_listener=self.kat_log.update,
        )
        self.plotter = PlottingWidget()
        self.action_runner = ActionRunner(plotter=self.plotter)

        self.tabs = QtWidgets.QTabWidget()
        self.setCentralWidget(self.tabs)

        # layout tab
        self.tabs.addTab(self.model_layout, "Layout")

        # calculate tab
        self.tab2 = QtWidgets.QWidget()
        self.tab2.setLayout(QtWidgets.QHBoxLayout())
        self.tabs.addTab(self.tab2, "Calculate")

        self.tab2.layout().addWidget(self.action_runner)
        self.tab2.layout().addWidget(self.plotter)

        # katscript tab
        self.tab3 = QtWidgets.QWidget()
        self.tab3.setLayout(QtWidgets.QHBoxLayout())
        self.tabs.addTab(self.tab3, "KatScript")
        self.tab3.layout().addWidget(self.kat_text)
        self.tab3.layout().addWidget(self.kat_log)

        self.tab4 = QtWidgets.QTextEdit()
        self.redirect = StdRedirect()
        self.tabs.addTab(self.tab4, "Console Output")

    def make_version_dialog(self):
        ret = check_version()
        if ret is None:
            return
        newest, current = ret
        QtWidgets.QMessageBox.information(
            self,
            "New Version!",
            f"You have version '{current}', newest version is '{newest}'",
        )


def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon(str(virgui.ASSETS / "miron.png")))

    w = Window()
    sys.stdout = w.redirect
    sys.stderr = w.redirect
    # probably leads to double prints?
    w.redirect.orig_streams = [
        sys.__stdout__,
        sys.__stderr__,
    ]
    w.redirect.text_edits = [w.tab4]
    w.show()
    w.make_version_dialog()

    app.exec()


if __name__ == "__main__":
    main()
