import sys

from PyQt5.QtWidgets import (
    QApplication,
    QFileDialog,
    QLabel,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)
from PyQt5.QtCore import Qt

from NIST_tests import *


class BitSequenceAnalyzer(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()


    def init_ui(self):
        self.setWindowTitle("Bit Sequence Analyzer")

        layout = QVBoxLayout()

        self.text_edit = QTextEdit(self)
        self.text_edit.setPlaceholderText("Upload a text file with a bit sequence...")
        layout.addWidget(self.text_edit)

        self.load_button = QPushButton("Upload a file", self)
        self.load_button.clicked.connect(self.load_file)
        layout.addWidget(self.load_button)

        self.analyze_button = QPushButton("Analyse", self)
        self.analyze_button.clicked.connect(self.analyze_sequence)
        layout.addWidget(self.analyze_button)

        self.save_button = QPushButton("Save the results", self)
        self.save_button.clicked.connect(self.save_results)
        layout.addWidget(self.save_button)

        self.result_label = QLabel("", self)
        self.result_label.setAlignment(Qt.AlignTop)
        layout.addWidget(self.result_label)

        self.setLayout(layout)


    def load_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open the file", "", "Text Files (*.txt);;All Files (*)")
        if file_path:
            sequence = read_txt_file(file_path)
            self.text_edit.setPlainText(sequence)


    def analyze_sequence(self):
        sequence = self.text_edit.toPlainText().strip()
        if not sequence:
            self.result_label.setText("Please download the bit sequence.")
            return
        frequency_p_value = frequency_test(sequence)
        consecutive_bits_p_value = consecutive_bits_test(sequence)
        block_statistic_values = block_statistic(sequence)
        identical_bits_p_value = test_identical_consecutive_bits(block_statistic_values)
        results = (
            f"Frequency bitwise test: {frequency_p_value:.4f}\n"
            f"A test for identical consecutive bits: {consecutive_bits_p_value:.4f}\n"
            f"Test for the longest sequence of units in a block: {identical_bits_p_value:.4f}"
        )
        self.results_to_save = results


    def save_results(self):
        if hasattr(self, 'results_to_save'):
            file_path, _ = QFileDialog.getSaveFileName(self, "Save the results", "", "Text Files (*.txt);;All Files (*)")
            if file_path:
                write_txt_file(self.results_to_save, file_path)
                self.result_label.setText(f"The results were successfully saved in {file_path}")
                self.results_to_save = None
                self.result_label.clear()
        else:
            self.result_label.setText("First, perform the analysis.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    analyzer = BitSequenceAnalyzer()
    analyzer.resize(400, 300)
    analyzer.show()
    sys.exit(app.exec_())
