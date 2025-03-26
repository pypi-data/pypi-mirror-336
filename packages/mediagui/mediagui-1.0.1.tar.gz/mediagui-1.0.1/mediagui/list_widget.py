from PyQt6.QtWidgets import QListWidget, QAbstractItemView
from PyQt6.QtCore import Qt
from pathlib import Path

class CustomListWidget(QListWidget):
    def __init__(self, window, parent=None):
        super().__init__(parent)
        self.window = window
        self.setAcceptDrops(True)
        self.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.DropAction.CopyAction)
            event.accept()
            urls = event.mimeData().urls()
            for url in urls:
                file_path = Path(url.toLocalFile())
                if file_path.suffix.lower() in ['.mp4', '.avi', '.mov', '.mkv']:
                    self.addItem(file_path.name)
                    self.window.video_files.append(file_path)
            # Update the concat button text and enable it
            cbtxt = "Process video" if len(self.window.video_files) == 1 else "Process videos"
            self.window.concat_button.setText(cbtxt)
            self.window.concat_button.setEnabled(True)