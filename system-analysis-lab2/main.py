import sys
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QSpinBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QTextEdit,
    QMessageBox,
    QFileDialog,
    QSplitter,
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
import numpy as np


class GraphConverter(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        font = QFont("Segoe UI", 12)
        self.setFont(font)

        self.setStyleSheet(
            """
            QWidget {
                background-color: #1e1e2f;
                color: #ffffff;
                font-family: Segoe UI;
            }
            QLabel {
                color: #a3bffa;
                font-weight: bold;
            }
            QSpinBox, QTextEdit {
                background-color: #2a2a3d;
                color: #ffffff;
                border: 1px solid #3e3e5c;
                border-radius: 5px;
                padding: 5px;
            }
            QTableWidget {
                background-color: #2a2a3d;
                color: #ffffff;
                border: 1px solid #3e3e5c;
                border-radius: 5px;
                gridline-color: #3e3e5c;
            }
            QPushButton {
                background-color: #6366f1;
                color: #ffffff;
                border: none;
                border-radius: 5px;
                padding: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #818cf8;
            }
            QPushButton:pressed {
                background-color: #4f46e5;
            }
            QSpinBox::up-button, QSpinBox::down-button {
                background-color: #3e3e5c;
                border: none;
                width: 20px;
            }
            QSplitter::handle {
                background-color: #3e3e5c;
            }
            QSplitter::handle:hover {
                background-color: #6366f1;
            }
        """
        )

        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        input_layout = QHBoxLayout()
        input_layout.setSpacing(10)

        self.vertex_label = QLabel("Вершины:")
        self.vertex_input = QSpinBox()
        self.vertex_input.setMinimum(1)
        self.vertex_input.setFixedWidth(100)

        self.edge_label = QLabel("Дуги:")
        self.edge_input = QSpinBox()
        self.edge_input.setMinimum(1)
        self.edge_input.setFixedWidth(100)

        input_layout.addWidget(self.vertex_label)
        input_layout.addWidget(self.vertex_input)
        input_layout.addWidget(self.edge_label)
        input_layout.addWidget(self.edge_input)
        input_layout.addStretch()

        layout.addLayout(input_layout)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        self.generate_button = QPushButton("Создать матрицу")
        self.generate_button.clicked.connect(self.create_incidence_matrix)
        self.load_button = QPushButton("Загрузить из файла")
        self.load_button.clicked.connect(self.load_from_file)

        button_layout.addWidget(self.generate_button)
        button_layout.addWidget(self.load_button)
        button_layout.addStretch()

        layout.addLayout(button_layout)

        self.table_label = QLabel("Матрица инцидентности:")
        layout.addWidget(self.table_label)
        self.table = QTableWidget()
        self.table.setMinimumHeight(350)
        layout.addWidget(self.table)

        self.convert_button = QPushButton("Рассчитать уровни и матрицу смежности")
        self.convert_button.clicked.connect(self.calculate_adjacency_and_left_incidence)
        layout.addWidget(self.convert_button)

        splitter = QSplitter(Qt.Orientation.Horizontal)

        left_widget = QWidget()
        left_layout = QVBoxLayout()
        self.left_incidence_label = QLabel("Иерархические уровни:")
        self.result_output = QTextEdit()
        self.result_output.setReadOnly(True)
        self.result_output.setMinimumHeight(150)
        left_layout.addWidget(self.left_incidence_label)
        left_layout.addWidget(self.result_output)
        left_widget.setLayout(left_layout)
        splitter.addWidget(left_widget)

        right_widget = QWidget()
        right_layout = QVBoxLayout()
        self.adjacency_label = QLabel("Новая матрица смежности:")
        self.result_table = QTableWidget()
        self.result_table.setMinimumHeight(150)
        right_layout.addWidget(self.adjacency_label)
        right_layout.addWidget(self.result_table)
        right_widget.setLayout(right_layout)
        splitter.addWidget(right_widget)

        splitter.setSizes([300, 500])
        splitter.setChildrenCollapsible(False)

        layout.addWidget(splitter, stretch=1)

        self.setLayout(layout)
        self.setWindowTitle("Системный анализ • Лабораторная работа №2")
        self.resize(800, 600)

    def create_incidence_matrix(self):
        vertices = self.vertex_input.value()
        edges = self.edge_input.value()

        self.table.setRowCount(vertices)
        self.table.setColumnCount(edges)
        header_labels = [f"e{i+1}" for i in range(edges)]
        self.table.setHorizontalHeaderLabels(header_labels)

        for i in range(vertices):
            for j in range(edges):
                self.table.setItem(i, j, QTableWidgetItem("0"))

    def load_from_file(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Открыть файл", "", "Text Files (*.txt)"
        )
        if file_name:
            try:
                with open(file_name, "r") as file:
                    lines = file.readlines()
                    vertices, edges = map(int, lines[0].strip().split())
                    self.vertex_input.setValue(vertices)
                    self.edge_input.setValue(edges)
                    self.create_incidence_matrix()

                    for i, line in enumerate(lines[1 : vertices + 1]):
                        values = list(map(int, line.strip().split()))
                        for j, value in enumerate(values):
                            self.table.setItem(i, j, QTableWidgetItem(str(value)))
            except Exception as e:
                QMessageBox.critical(
                    self, "Ошибка", f"Не удалось загрузить файл: {str(e)}"
                )

    def calculate_adjacency_and_left_incidence(self):
        vertices = self.vertex_input.value()
        edges = self.edge_input.value()

        incidence_matrix = np.zeros((vertices, edges), dtype=int)

        for i in range(vertices):
            for j in range(edges):
                item = self.table.item(i, j)
                if item is not None:
                    try:
                        value = int(item.text())
                        if value not in (0, 1, -1):
                            raise ValueError("Значение должно быть 0, 1 или -1")
                        incidence_matrix[i, j] = value
                    except ValueError as e:
                        QMessageBox.critical(
                            self,
                            "Ошибка ввода",
                            f"Ошибка в ячейке ({i+1}, {j+1}): {str(e)}",
                        )
                        return
                else:
                    QMessageBox.critical(
                        self, "Ошибка ввода", f"Пустая ячейка ({i+1}, {j+1})."
                    )
                    return

        for j in range(edges):
            col = incidence_matrix[:, j]
            count_pos = np.count_nonzero(col == 1)
            count_neg = np.count_nonzero(col == -1)
            if not (count_pos == 1 and count_neg == 1):
                QMessageBox.critical(
                    self,
                    "Ошибка матрицы",
                    f"В столбце {j+1} должна быть одна 1 и одна -1.\nНайдено: 1 -> {count_pos}, -1 -> {count_neg}.",
                )
                return

        adjacency_matrix = np.zeros((vertices, vertices), dtype=int)
        left_incidence = {i + 1: [] for i in range(vertices)}

        for j in range(edges):
            start = None
            end = None
            for i in range(vertices):
                if incidence_matrix[i, j] == 1:
                    start = i + 1
                elif incidence_matrix[i, j] == -1:
                    end = i + 1
            if start is not None and end is not None:
                adjacency_matrix[start - 1, end - 1] = 1
                left_incidence[end].append(start)

        self.result_table.setRowCount(vertices)
        self.result_table.setColumnCount(vertices)

        levels = []
        while len(left_incidence) != 0:
            level = [key for key, value in left_incidence.items() if not value]
            for vertex in level:
                del left_incidence[vertex]
                for key in left_incidence.keys():
                    if vertex in left_incidence[key]:
                        left_incidence[key].remove(vertex)
            levels.append(level)

        result_text = ""
        for level, vertices_in_level in enumerate(levels):
            result_text += (
                f"Уровень {level}: ({', '.join(map(str, vertices_in_level))})\n"
            )

        self.result_output.setText(result_text)
        swap_vertex = [vertex - 1 for level in levels for vertex in level]

        for i in range(vertices):
            for j in range(vertices):
                self.result_table.setItem(
                    i,
                    j,
                    QTableWidgetItem(
                        str(adjacency_matrix[swap_vertex[i], swap_vertex[j]])
                    ),
                )
        self.result_table.setVerticalHeaderLabels(
            [f"{i + 1}({swap_vertex[i] + 1})" for i in range(vertices)]
        )
        self.result_table.setHorizontalHeaderLabels(
            [f"{i + 1}({swap_vertex[i] + 1})" for i in range(vertices)]
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GraphConverter()
    window.show()
    sys.exit(app.exec())
