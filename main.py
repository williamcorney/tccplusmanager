import sys
import subprocess
from pathlib import Path
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton,
    QComboBox, QMessageBox
)
from PyQt6.QtCore import Qt

PERMISSIONS = [
    "All", "Accessibility", "AddressBook", "AppleEvents", "Calendar", "Camera", 
    "ContactsFull", "ContactsLimited", "DeveloperTool", "Facebook", "LinkedIn", 
    "ListenEvent", "Liverpool", "Location", "MediaLibrary", "Microphone", "Motion", 
    "Photos", "PhotosAdd", "PostEvent", "Reminders", "ScreenCapture", "ShareKit", 
    "SinaWeibo", "Siri", "SpeechRecognition", "SystemPolicyAllFiles", 
    "SystemPolicyDesktopFolder", "SystemPolicyDeveloperFiles", "SystemPolicyDocumentsFolder", 
    "SystemPolicyDownloadsFolder", "SystemPolicyNetworkVolumes", 
    "SystemPolicyRemovableVolumes", "SystemPolicySysAdminFiles", "TencentWeibo", 
    "Twitter", "Ubiquity", "Willow"
]

class TCCManager(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TCC Permission Manager")
        self.setAcceptDrops(True)
        self.setFixedSize(300, 250)

        self.app_path = None
        self.bundle_id = None

        self.layout = QVBoxLayout()

        self.info_label = QLabel("Drag and drop an app (.app) here")
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.info_label)

        self.bundle_label = QLabel("Bundle ID: ")
        self.layout.addWidget(self.bundle_label)

        self.permission_combo = QComboBox()
        self.permission_combo.addItems(PERMISSIONS)
        self.layout.addWidget(self.permission_combo)

        self.add_button = QPushButton("Add Permission")
        self.add_button.clicked.connect(self.add_permission)
        self.layout.addWidget(self.add_button)

        self.remove_button = QPushButton("Remove Permission")
        self.remove_button.clicked.connect(self.remove_permission)
        self.layout.addWidget(self.remove_button)

        self.setLayout(self.layout)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        if urls:
            dropped_path = Path(urls[0].toLocalFile()).resolve()
            if dropped_path.is_dir() and dropped_path.suffix == ".app":
                self.app_path = str(dropped_path)
                self.get_bundle_id(self.app_path)
            else:
                QMessageBox.warning(
                    self, "Invalid File", f"The dropped item is not a valid .app bundle:\n{dropped_path}"
                )

    def get_bundle_id(self, path):
        try:
            result = subprocess.run(
                ["mdls", "-name", "kMDItemCFBundleIdentifier", path],
                capture_output=True, text=True, check=True
            )
            line = result.stdout.strip()
            if "=" in line:
                self.bundle_id = line.split("=")[1].strip().strip('"')
                self.bundle_label.setText(f"Bundle ID: {self.bundle_id}")
            else:
                self.bundle_label.setText("Bundle ID: Not found")
                self.bundle_id = None
        except subprocess.CalledProcessError as e:
            QMessageBox.critical(self, "Error", f"Failed to get bundle ID:\n{e}")

    def run_tccplus(self, action):
        if not self.bundle_id:
            QMessageBox.warning(self, "No Bundle ID", "Please drop a valid .app bundle first.")
            return

        permission = self.permission_combo.currentText()
        tccplus_path = Path(__file__).parent / "tccplus"
        cmd = [str(tccplus_path), action, permission, self.bundle_id]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            QMessageBox.information(self, f"{action.title()} Success", result.stdout.strip())
        except subprocess.CalledProcessError as e:
            QMessageBox.critical(self, f"{action.title()} Failed", e.stderr.strip())

    def add_permission(self):
        self.run_tccplus("add")

    def remove_permission(self):
        self.run_tccplus("reset")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TCCManager()
    window.show()
    sys.exit(app.exec())
