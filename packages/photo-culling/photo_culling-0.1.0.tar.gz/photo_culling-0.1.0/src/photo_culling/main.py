import sys
import os
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QFileDialog
from PyQt6.QtGui import QKeyEvent
from PyQt6.QtCore import Qt
from PIL.ImageQt import toqpixmap
from photo_culling.utils import clip, get_subimage
from photo_culling.caching import ImageCache
import threading
import time
import shutil
import pathlib
import argparse


class ImageIndexLabel(QLabel):
    def __init__(self, parent, n_images, fontsize=25):
        super().__init__(parent)
        self.n_images = n_images
        self.colors = {False: "lightgray", True: "green"}
        self.style_template = f"font-size: {fontsize}px;" + "background-color: {color}"
        self.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
        # self.setMinimumSize(300, fontsize + 10)
        self.set_values(0, False, 0)

    def _set_selected(self, selected):
        self.setStyleSheet(self.style_template.format(color=self.colors[selected]))

    def _set_index(self, idx: int, n_selected: int):
        self.setText(f"{idx + 1}/{self.n_images} ({n_selected})")
        self.adjustSize()

    def set_values(self, idx: int, current_selected: bool, n_selected: int):
        self._set_selected(current_selected)
        self._set_index(idx, n_selected)


class ImageViewer(QMainWindow):
    def __init__(self, image_directory, target_directory, windowed=False):
        super().__init__()
        # Initialize image index and display
        self.current_index = 0
        self.image_directory = image_directory
        self.target_directory = target_directory
        self.image_fnames = sorted(pathlib.Path(image_directory).glob("*.jpg", case_sensitive=False))
        self.n_images = len(self.image_fnames)
        self.image_cache = ImageCache(self.image_fnames)
        self.is_selected = [False] * self.n_images
        self.populate_cache_thread = threading.Thread(target=self._populate_cache)
        self.exiting = False

        # Create image label
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setCentralWidget(self.image_label)

        self.pos_label = ImageIndexLabel(self, self.n_images)

        self.setWindowTitle("Fast culling")
        if windowed:
            self.showMaximized()
        else:
            self.showFullScreen()

        # Show first image
        self.populate_cache_thread.start()
        self.show_image()

    def get_target_dir(self):
        directory = str(QFileDialog.getExistingDirectory(self, "Select target directory", self.target_directory))
        return directory

    def _populate_cache(self):
        while not self.exiting:
            self.image_cache.load_next_required_item(self.current_index, self.get_current_resolution())
            self.image_cache.clean_cache(self.current_index, self.get_current_resolution())
            time.sleep(0.01)  # short sleep to reduce thread starvation

    def show_image(self):
        preview = self.image_cache.get_preview(self.current_index, self.get_current_resolution())
        qpm = toqpixmap(preview)
        self.image_label.setPixmap(qpm)

    def navigate(self, step):
        self.current_index = clip(self.current_index + step, 0, self.n_images)
        self.show_image()
        self.pos_label.set_values(self.current_index, self.current_selected, self.n_selected)

    def get_current_resolution(self):
        s = self.image_label.size()
        return s.width(), s.height()

    def copy_selected_images(self, target_dir):
        os.makedirs(target_dir, exist_ok=True)
        n_files_total = 0
        n_unique_photos = 0
        for selected, fname in zip(self.is_selected, self.image_fnames):
            fname = pathlib.Path(fname)
            if not selected:
                continue
            related_files = pathlib.Path(self.image_directory).glob(f"{fname.stem}.*")
            for f in related_files:
                shutil.copy(f, target_dir)
                n_files_total += 1
            n_unique_photos += 1
        print(f"Copied {n_unique_photos} photos, {n_files_total} files in total.")

    @property
    def n_selected(self):
        return sum(self.is_selected)

    @property
    def current_selected(self):
        return self.is_selected[self.current_index]

    def keyPressEvent(self, event: QKeyEvent):
        key = event.key()

        if key in (Qt.Key.Key_Escape, Qt.Key.Key_Q):
            self.exiting = True
            if self.n_selected:
                target_dir = self.get_target_dir()
                if target_dir:
                    self.copy_selected_images(target_dir)
            self.populate_cache_thread.join()
            self.close()
        elif key == Qt.Key.Key_Left:
            self.navigate(-1)  # Go back 1 image
        elif key == Qt.Key.Key_Right:
            self.navigate(1)  # Go forward 1 image
        elif key == Qt.Key.Key_A:
            self.navigate(-10)  # Go back 10 images
        elif key == Qt.Key.Key_D:
            self.navigate(10)  # Go forward 10 images
        elif key == Qt.Key.Key_F11:
            self.toggle_full_screen()
        elif key == Qt.Key.Key_W:
            self.set_selected(True)
        elif key == Qt.Key.Key_S:
            self.set_selected(False)
        elif key == Qt.Key.Key_T:
            self.set_selected(not self.is_selected[self.current_index])

    def set_selected(self, selected):
        self.is_selected[self.current_index] = selected
        self.pos_label.set_values(self.current_index, self.current_selected, self.n_selected)

    def to_fractional(self, pos):
        width, height = self.get_current_resolution()
        return pos.x() / width, pos.y() / height

    def mouseMoveEvent(self, event):
        self.show_zoomed_image(*self.to_fractional(event.pos()))

    def mousePressEvent(self, event):
        self.show_zoomed_image(*self.to_fractional(event.pos()))

    def mouseReleaseEvent(self, event):
        self.show_image()

    def show_zoomed_image(self, frac_x, frac_y):
        sub_img = get_subimage(
            self.image_cache.get_full_image(self.current_index), (frac_x, frac_y), self.get_current_resolution()
        )
        qpm = toqpixmap(sub_img)
        self.image_label.setPixmap(qpm)

    def resizeEvent(self, event):
        self.show_image()

    def toggle_full_screen(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", nargs="?", default=".")
    parser.add_argument("--target", default=None)
    parser.add_argument("--windowed", action="store_true", help="Open in maximized window instead of full screen")
    args = parser.parse_args()
    directory = pathlib.Path(args.directory).resolve()
    if not directory.is_dir():
        print(f"Not a valid directory: {args.directory}")
    elif len(list(directory.glob("*.jpg", case_sensitive=False))) == 0:
        print(f"No jpg files found in {args.directory}")
    else:
        app = QApplication(sys.argv)
        viewer = ImageViewer(directory, args.target, args.windowed)
        sys.exit(app.exec())


if __name__ == "__main__":
    main()
