import sys
import os
import subprocess
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QFileDialog, QMessageBox
)

class OpenModelicaRunner(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('OpenModelica Simulation Runner')
        self.setMinimumWidth(450)
        self.setMinimumHeight(200)

        layout = QVBoxLayout()

        # Executable Selection
        exe_layout = QHBoxLayout()
        self.exe_label = QLabel('Executable Path:')
        self.exe_input = QLineEdit()
        self.exe_input.setReadOnly(True)
        self.browse_btn = QPushButton('Browse')
        self.browse_btn.clicked.connect(self.browse_executable)
        exe_layout.addWidget(self.exe_label)
        exe_layout.addWidget(self.exe_input)
        exe_layout.addWidget(self.browse_btn)
        layout.addLayout(exe_layout)

        # Start Time
        start_layout = QHBoxLayout()
        self.start_label = QLabel('Start Time (Integer):')
        self.start_input = QLineEdit()
        start_layout.addWidget(self.start_label)
        start_layout.addWidget(self.start_input)
        layout.addLayout(start_layout)

        # Stop Time
        stop_layout = QHBoxLayout()
        self.stop_label = QLabel('Stop Time (Integer):')
        self.stop_input = QLineEdit()
        stop_layout.addWidget(self.stop_label)
        stop_layout.addWidget(self.stop_input)
        layout.addLayout(stop_layout)

        # Run Button
        self.run_btn = QPushButton('Run Simulation')
        self.run_btn.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold; padding: 8px;")
        self.run_btn.clicked.connect(self.run_simulation)
        layout.addWidget(self.run_btn)

        self.setLayout(layout)

    def browse_executable(self):
        file_filter = "Executables (*.exe);;All Files (*)" if os.name == 'nt' else "All Files (*)"
        file_path, _ = QFileDialog.getOpenFileName(self, 'Select Executable', '', file_filter)
        if file_path:
            self.exe_input.setText(file_path)

    def validate_inputs(self) -> tuple:
        exe_path = self.exe_input.text().strip()
        start_str = self.start_input.text().strip()
        stop_str = self.stop_input.text().strip()

        if not exe_path or not os.path.isfile(exe_path):
            raise ValueError("Please select a valid executable file.")

        try:
            start_time = int(start_str)
            stop_time = int(stop_str)
        except ValueError:
            raise ValueError("Start time and Stop time must be valid integers.")

        if not (0 <= start_time < stop_time < 5):
            raise ValueError("Time constraints not met.\nEnsure that: 0 <= Start Time < Stop Time < 5")

        return exe_path, start_time, stop_time

    def run_simulation(self):
        try:
            exe_path, start_time, stop_time = self.validate_inputs()
        except ValueError as ve:
            QMessageBox.warning(self, 'Validation Error', str(ve))
            return

        override_args = f'startTime={start_time},stopTime={stop_time}'
        command = [exe_path, '-override', override_args]

        try:
            self.run_btn.setText("Running...")
            self.run_btn.setEnabled(False)
            QApplication.processEvents() 

            exe_dir = os.path.dirname(exe_path)
            process = subprocess.run(command, capture_output=True, text=True, check=True, cwd=exe_dir)
            
            QMessageBox.information(
                self, 
                'Simulation Success', 
                f'Simulation completed successfully!\n\nParameters: {override_args}'
            )

        except subprocess.CalledProcessError as e:
            error_text = e.stderr if e.stderr else e.stdout
            QMessageBox.critical(
                self, 
                'Execution Error', 
                f'Simulation failed (Exit Code: {e.returncode}).\n\nError Output:\n{error_text}'
            )
        except Exception as e:
            QMessageBox.critical(self, 'System Error', f'An unexpected error occurred:\n{str(e)}')
        finally:
            self.run_btn.setText("Run Simulation")
            self.run_btn.setEnabled(True)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    runner = OpenModelicaRunner()
    runner.show()
    sys.exit(app.exec())