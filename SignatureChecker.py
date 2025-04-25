import os
import subprocess
import csv
import requests
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QGridLayout, QLabel, QLineEdit, QPushButton,
    QFileDialog, QTableWidget, QTableWidgetItem, QMessageBox, QAction
)
from PyQt5.QtCore import Qt
import zipfile
import io

SIGCHECK_URL = "https://download.sysinternals.com/files/Sigcheck.zip"
SIGCHECK_EXE = "sigcheck.exe"


def download_sigcheck():
    if not os.path.exists(SIGCHECK_EXE):
        response = requests.get(SIGCHECK_URL)
        with zipfile.ZipFile(io.BytesIO(response.content)) as z:
            z.extract(SIGCHECK_EXE)


def parse_sigcheck_output(output):
    data = {}
    for line in output.splitlines():
        if ':' in line:
            key, val = line.split(':', 1)
            data[key.strip()] = val.strip()
    return {
        "Verified": data.get("Verified", ""),
        "Signing Date": data.get("Signing date", ""),
        "Publisher": data.get("Publisher", ""),
        "Company": data.get("Company", ""),
        "Description": data.get("Description", ""),
        "Product": data.get("Product", ""),
        "Prod Version": data.get("Product version", ""),
        "File Version": data.get("File version", ""),
        "MachineType": data.get("MachineType", ""),
    }


class SigcheckApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sigcheck GUI")
        self.setGeometry(100, 100, 1200, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QGridLayout(self.central_widget)

        self.selected_files = []

        self.create_menu()

        # File selection
        self.file_entry = QLineEdit()
        self.file_button = QPushButton("Select Files")
        self.file_button.clicked.connect(self.select_files)

        # Folder selection
        self.folder_entry = QLineEdit()
        self.folder_button = QPushButton("Select Folder")
        self.folder_button.clicked.connect(self.select_folder)

        # Run button
        self.run_button = QPushButton("Run Sigcheck")
        self.run_button.clicked.connect(self.run_sigcheck)

        # Save button
        self.save_button = QPushButton("Save to CSV")
        self.save_button.clicked.connect(self.save_to_csv)

        # Table
        self.table = QTableWidget(0, 10)
        headers = ["File Name", "Verified", "Signing Date", "Publisher", "Company",
                   "Description", "Product", "Prod Version", "File Version", "MachineType"]
        self.table.setHorizontalHeaderLabels(headers)

        # Layout setup
        self.layout.addWidget(QLabel("Files:"), 0, 0)
        self.layout.addWidget(self.file_entry, 0, 1)
        self.layout.addWidget(self.file_button, 0, 2)

        self.layout.addWidget(QLabel("Folder:"), 1, 0)
        self.layout.addWidget(self.folder_entry, 1, 1)
        self.layout.addWidget(self.folder_button, 1, 2)

        self.layout.addWidget(self.run_button, 2, 1)
        self.layout.addWidget(self.save_button, 2, 2)

        self.layout.addWidget(self.table, 3, 0, 1, 3)

    def create_menu(self):
        menu_bar = self.menuBar()

        # File Menu
        file_menu = menu_bar.addMenu("File")
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Help Menu
        help_menu = menu_bar.addMenu("Help")

        doc_action = QAction("Doc", self)
        doc_action.triggered.connect(self.show_doc)
        help_menu.addAction(doc_action)

        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def show_doc(self):
        doc_text = (
            "Sigcheck is a command-line utility from Microsoft Sysinternals.\n"
            "It shows file version, signing info, timestamp, and much more.\n"
            "Official site: https://learn.microsoft.com/en-us/sysinternals/downloads/sigcheck"
        )
        QMessageBox.information(self, "Documentation", doc_text)

    def show_about(self):
        QMessageBox.information(self, "About", "Version: 1.0\nDeveloper: Vaibhav Patil")

    def select_files(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Select Files", "", "All Files (*.*)")
        if files:
            self.selected_files = files
            self.file_entry.setText("; ".join(files))

    def select_folder(self):
        path = QFileDialog.getExistingDirectory(self, "Select Folder")
        if path:
            self.folder_entry.setText(path)

    def run_sigcheck(self):
        try:
            download_sigcheck()
        except Exception as e:
            QMessageBox.critical(self, "Download Error", f"Failed to download sigcheck: {e}")
            return

        file_paths = list(self.selected_files)

        folder_path = self.folder_entry.text().strip()
        if folder_path and os.path.isdir(folder_path):
            for root, _, files in os.walk(folder_path):
                for f in files:
                    file_paths.append(os.path.join(root, f))

        self.table.setRowCount(0)

        for file in file_paths:
            try:
                result = subprocess.run(
                    [SIGCHECK_EXE, "-nobanner", file],
                    capture_output=True, text=True, check=True
                )
                parsed = parse_sigcheck_output(result.stdout)
                row = self.table.rowCount()
                self.table.insertRow(row)
                self.table.setItem(row, 0, QTableWidgetItem(file))
                for col, key in enumerate(parsed.keys(), start=1):
                    self.table.setItem(row, col, QTableWidgetItem(parsed[key]))
            except subprocess.CalledProcessError as e:
                QMessageBox.warning(
                    self,
                    "Sigcheck Error",
                    f"Failed to process file:\n{file}\n\nReturn Code: {e.returncode}\n\n"
                    f"Output:\n{e.stdout}\n\nError:\n{e.stderr}"
                )
            except Exception as e:
                QMessageBox.critical(self, "Unexpected Error", f"Error processing {file}:\n{e}")

    def save_to_csv(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save Output to CSV", "", "CSV Files (*.csv)")
        if not path:
            return

        with open(path, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([self.table.horizontalHeaderItem(i).text() for i in range(self.table.columnCount())])
            for row in range(self.table.rowCount()):
                writer.writerow([
                    self.table.item(row, col).text() if self.table.item(row, col) else ""
                    for col in range(self.table.columnCount())
                ])
        QMessageBox.information(self, "Success", "Data saved to CSV.")


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = SigcheckApp()
    window.show()
    sys.exit(app.exec_())
