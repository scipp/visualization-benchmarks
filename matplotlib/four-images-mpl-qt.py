import sys

import matplotlib.pyplot as plt
import numpy as np
import qtawesome as qta
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QSlider,
    QVBoxLayout,
    QWidget,
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up the main widget
        self.setWindowTitle("Matplotlib in PyQt5")
        self.setGeometry(100, 100, 800, 600)
        widget = QWidget(self)
        self.setCentralWidget(widget)

        # Create the matplotlib canvas
        self.fig, self.ax = plt.subplots(ncols=2, nrows=2)
        self.images = [
            ax.imshow(np.random.random((1000, 1000)), origin="lower", aspect="auto")
            for ax in self.ax.ravel()
        ]
        self.canvas = self.fig.canvas

        button_layout = QHBoxLayout()

        # Home button
        home = QPushButton(self)
        home.setIcon(qta.icon("fa.home"))
        home.setFixedWidth(32)
        home.clicked.connect(self.canvas.toolbar.home)
        button_layout.addWidget(home)

        # Zoom button
        zoom = QPushButton(self)
        zoom.setIcon(qta.icon("fa.search"))
        zoom.setFixedWidth(32)
        zoom.setCheckable(True)
        zoom.clicked.connect(self.canvas.toolbar.zoom)
        button_layout.addWidget(zoom)

        # Pan button
        pan = QPushButton(self)
        pan.setIcon(qta.icon("fa.arrows"))
        pan.setFixedWidth(32)
        pan.setCheckable(True)
        pan.clicked.connect(self.canvas.toolbar.pan)
        button_layout.addWidget(pan)

        button_layout.addStretch()

        self.cursor_label = QLabel("x: -, y: -", self)
        self.cursor_label.setMaximumHeight(20)
        self.canvas.mpl_connect("motion_notify_event", self.update_cursor_position)
        button_layout.addWidget(self.cursor_label)

        # Create a slider
        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.setMinimum(1)
        self.slider.setMaximum(100)
        self.slider.valueChanged.connect(self.update_plot)

        # Set up the layout
        layout = QVBoxLayout()
        layout.addLayout(button_layout)
        layout.addWidget(self.canvas)
        layout.addWidget(self.slider)
        widget.setLayout(layout)

    def update_plot(self):
        for im in self.images:
            im.set_data(np.random.random((1000, 1000)))
        self.canvas.draw_idle()

    def update_cursor_position(self, event):
        if event.inaxes:
            x, y = event.xdata, event.ydata
            self.cursor_label.setText(f"x: {x:.2f}, y: {y:.2f}")
        else:
            self.cursor_label.setText("x: -, y: -")


app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
