import sys
from pathlib import Path
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QFileDialog, QTextEdit
)
from PySide6.QtGui import QPixmap, QDragEnterEvent, QDropEvent
from PySide6.QtCore import Qt

class DropBox(QTextEdit):
    """Simple widget that accepts file drops and shows the dropped file path."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setReadOnly(True)
        self.setPlaceholderText("Drag files here (or click 'Open File')")

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        urls = event.mimeData().urls()
        if not urls:
            return
        # take first file only for this example
        file_path = urls[0].toLocalFile()
        self.setPlainText(file_path)
        # emit a custom signal or call parent method to load image if needed
        if self.parent() and hasattr(self.parent(), "load_image_from_path"):
            self.parent().load_image_from_path(file_path)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PySide6: Image + Drag & Drop + Button")
        self.resize(480, 360)

        self.image_label = QLabel(alignment=Qt.AlignCenter)
        self.image_label.setFixedHeight(220)
        self.image_label.setStyleSheet("border: 1px solid #888; background: #f8f8f8;")
        self.image_label.setText("No image loaded")

        self.drop_box = DropBox(self)

        self.open_btn = QPushButton("Open Image...")
        self.open_btn.clicked.connect(self.open_file_dialog)

        self.clear_btn = QPushButton("Clear")
        self.clear_btn.clicked.connect(self.clear_all)

        layout = QVBoxLayout(self)
        layout.addWidget(self.image_label)
        layout.addWidget(self.drop_box)
        layout.addWidget(self.open_btn)
        layout.addWidget(self.clear_btn)

    def open_file_dialog(self):
        file_filter = "Images (*.png *.jpg *.jpeg *.bmp *.gif);;All Files (*)"
        path, _ = QFileDialog.getOpenFileName(self, "Choose image", str(Path.home()), file_filter)
        if path:
            self.drop_box.setPlainText(path)
            self.load_image_from_path(path)

    def load_image_from_path(self, path: str):
        pix = QPixmap(path)
        if pix.isNull():
            self.image_label.setText("Failed to load image")
            return
        # scale keeping aspect ratio to fit label
        scaled = pix.scaled(self.image_label.width(), self.image_label.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.image_label.setPixmap(scaled)
        self.image_label.setText("")  # clear text

    def clear_all(self):
        self.image_label.clear()
        self.image_label.setText("No image loaded")
        self.drop_box.clear()

    # ensure image resizes with window
    def resizeEvent(self, event):
        if self.image_label.pixmap():
            self.load_image_from_path(self.drop_box.toPlainText() or "")
        super().resizeEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())

