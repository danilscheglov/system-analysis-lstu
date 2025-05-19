import sys
import numpy as np
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QSpinBox,
    QGroupBox,
    QTextEdit,
    QMessageBox,
    QComboBox,
    QSplitter,
    QFrame,
    QSizePolicy,
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QColor, QPalette, QIcon, QPixmap


class ModernButton(QPushButton):
    def __init__(self, text, primary=False):
        super().__init__(text)
        self.setMinimumHeight(32)
        if primary:
            self.setStyleSheet(
                """
                QPushButton {
                    background-color: #3498db;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    padding: 8px 16px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #2980b9;
                }
                QPushButton:pressed {
                    background-color: #1c6ea4;
                }
            """
            )
        else:
            self.setStyleSheet(
                """
                QPushButton {
                    background-color: #f0f0f0;
                    border: 1px solid #dcdcdc;
                    border-radius: 4px;
                    padding: 8px 16px;
                }
                QPushButton:hover {
                    background-color: #e0e0e0;
                }
                QPushButton:pressed {
                    background-color: #d0d0d0;
                }
            """
            )


class ModernSpinBox(QSpinBox):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(
            """
            QSpinBox {
                border: 1px solid #dcdcdc;
                border-radius: 4px;
                padding: 4px;
                background-color: white;
                min-width: 60px;
                min-height: 28px;
            }
            QSpinBox::up-button, QSpinBox::down-button {
                width: 20px;
                border: none;
                background-color: #f0f0f0;
            }
            QSpinBox::up-button:hover, QSpinBox::down-button:hover {
                background-color: #e0e0e0;
            }
        """
        )


class ModernComboBox(QComboBox):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(
            """
            QComboBox {
                border: 1px solid #dcdcdc;
                border-radius: 4px;
                padding: 4px 8px;
                background-color: white;
                min-height: 28px;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
                border-left: 1px solid #dcdcdc;
                background-color: #f0f0f0;
            }
            QComboBox QAbstractItemView {
                border: 1px solid #dcdcdc;
                selection-background-color: #3498db;
            }
        """
        )


class ModernTableWidget(QTableWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(
            """
            QTableWidget {
                border: 1px solid #dcdcdc;
                border-radius: 4px;
                gridline-color: #e0e0e0;
                background-color: white;
                selection-background-color: #3498db33;
                selection-color: black;
            }
            QTableWidget::item {
                padding: 6px;
            }
            QHeaderView::section {
                background-color: #f0f0f0;
                border: none;
                border-right: 1px solid #dcdcdc;
                border-bottom: 1px solid #dcdcdc;
                padding: 6px;
                font-weight: bold;
            }
        """
        )
        self.setAlternatingRowColors(True)


class ModernTextEdit(QTextEdit):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(
            """
            QTextEdit {
                border: 1px solid #dcdcdc;
                border-radius: 4px;
                background-color: white;
                selection-background-color: #3498db33;
                padding: 8px;
                font-family: 'Segoe UI', Arial, sans-serif;
                line-height: 1.5;
            }
        """
        )


class ModernFrame(QFrame):
    def __init__(self):
        super().__init__()
        self.setFrameShape(QFrame.StyledPanel)
        self.setStyleSheet(
            """
            QFrame {
                background-color: white;
                border-radius: 6px;
                border: 1px solid #dcdcdc;
            }
        """
        )


class StructuralAnalysisApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Анализ качества структуры системы")
        self.setGeometry(100, 100, 1200, 800)
        self.setMinimumSize(1000, 700)

        self.setStyleSheet(
            """
            QMainWindow {
                background-color: #f8f9fa;
            }
            QGroupBox {
                font-weight: bold;
                border: 1px solid #dcdcdc;
                border-radius: 6px;
                margin-top: 12px;
                padding-top: 12px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
            QLabel {
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QSplitter::handle {
                background-color: #dcdcdc;
            }
        """
        )

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(15, 15, 15, 15)
        self.main_layout.setSpacing(12)

        control_frame = ModernFrame()
        control_layout = QVBoxLayout(control_frame)
        control_layout.setContentsMargins(15, 15, 15, 15)

        header_label = QLabel("Анализ связности структуры системы")
        header_label.setFont(QFont("Segoe UI", 14, QFont.Bold))
        header_label.setStyleSheet("color: #2c3e50;")
        control_layout.addWidget(header_label)

        settings_layout = QHBoxLayout()
        settings_layout.setSpacing(15)

        size_group = QGroupBox("Размер матрицы")
        size_group.setStyleSheet("QGroupBox { padding-top: 15px; }")
        size_layout = QHBoxLayout(size_group)
        size_layout.setContentsMargins(15, 10, 15, 10)

        size_label = QLabel("Размер:")
        size_label.setFont(QFont("Segoe UI", 10))

        self.size_spinbox = ModernSpinBox()
        self.size_spinbox.setRange(2, 15)
        self.size_spinbox.setValue(5)

        self.create_matrix_button = ModernButton("Создать матрицу", primary=True)
        self.create_matrix_button.clicked.connect(self.create_adjacency_matrix)

        size_layout.addWidget(size_label)
        size_layout.addWidget(self.size_spinbox)
        size_layout.addWidget(self.create_matrix_button)
        settings_layout.addWidget(size_group)

        examples_group = QGroupBox("Тестовые примеры")
        examples_group.setStyleSheet("QGroupBox { padding-top: 15px; }")
        examples_layout = QHBoxLayout(examples_group)
        examples_layout.setContentsMargins(15, 10, 15, 10)

        self.examples_combo = ModernComboBox()
        self.examples_combo.addItem("Выберите пример...")
        self.examples_combo.addItem("Пример 1: Сильно связный граф")
        self.examples_combo.addItem("Пример 2: Слабо связный граф")
        self.examples_combo.addItem("Пример 3: Несвязный граф")
        self.examples_combo.addItem("Пример 4: Цепь")
        self.examples_combo.addItem("Пример 5: Цикл")

        self.load_example_button = ModernButton("Загрузить")
        self.load_example_button.clicked.connect(self.load_example)

        examples_layout.addWidget(self.examples_combo)
        examples_layout.addWidget(self.load_example_button)
        settings_layout.addWidget(examples_group)

        control_layout.addLayout(settings_layout)
        self.main_layout.addWidget(control_frame)

        splitter = QSplitter(Qt.Horizontal)
        splitter.setHandleWidth(2)
        self.main_layout.addWidget(splitter, 1)

        left_splitter = QSplitter(Qt.Vertical)
        splitter.addWidget(left_splitter)

        matrix_frame = ModernFrame()
        matrix_layout = QVBoxLayout(matrix_frame)
        matrix_layout.setContentsMargins(15, 15, 15, 15)

        matrix_header = QLabel("Матрица смежности (A)")
        matrix_header.setFont(QFont("Segoe UI", 12, QFont.Bold))
        matrix_header.setStyleSheet("color: #2c3e50;")
        matrix_layout.addWidget(matrix_header)

        self.matrix_table = ModernTableWidget()
        matrix_layout.addWidget(self.matrix_table)

        left_splitter.addWidget(matrix_frame)

        results_frame = ModernFrame()
        results_layout = QVBoxLayout(results_frame)
        results_layout.setContentsMargins(15, 15, 15, 15)

        results_header_layout = QHBoxLayout()

        results_header = QLabel("Результаты анализа")
        results_header.setFont(QFont("Segoe UI", 12, QFont.Bold))
        results_header.setStyleSheet("color: #2c3e50;")
        results_header_layout.addWidget(results_header)

        self.calculate_button = ModernButton("Рассчитать показатели", primary=True)
        self.calculate_button.clicked.connect(self.calculate_metrics)
        results_header_layout.addWidget(self.calculate_button)

        results_layout.addLayout(results_header_layout)

        self.results_text = ModernTextEdit()
        self.results_text.setReadOnly(True)
        font = QFont("Consolas", 10)
        self.results_text.setFont(font)
        results_layout.addWidget(self.results_text)

        left_splitter.addWidget(results_frame)
        left_splitter.setSizes([400, 300])

        asigma_frame = ModernFrame()
        asigma_layout = QVBoxLayout(asigma_frame)
        asigma_layout.setContentsMargins(15, 15, 15, 15)

        asigma_header = QLabel("Матрица суммарной связности (AΣ)")
        asigma_header.setFont(QFont("Segoe UI", 12, QFont.Bold))
        asigma_header.setStyleSheet("color: #2c3e50;")
        asigma_layout.addWidget(asigma_header)

        self.asigma_table = ModernTableWidget()
        asigma_layout.addWidget(self.asigma_table)

        splitter.addWidget(asigma_frame)
        splitter.setSizes([600, 400])

        self.create_adjacency_matrix()

    def create_adjacency_matrix(self):
        size = self.size_spinbox.value()
        self.matrix_table.setRowCount(size)
        self.matrix_table.setColumnCount(size)

        headers = [str(i + 1) for i in range(size)]
        self.matrix_table.setHorizontalHeaderLabels(headers)
        self.matrix_table.setVerticalHeaderLabels(headers)

        for i in range(size):
            for j in range(size):
                item = QTableWidgetItem("0")
                item.setTextAlignment(Qt.AlignCenter)
                if i == j:
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                    item.setBackground(QColor("#f0f0f0"))
                else:
                    item.setBackground(QColor("white"))
                self.matrix_table.setItem(i, j, item)

        for i in range(size):
            self.matrix_table.setColumnWidth(i, 40)
            self.matrix_table.setRowHeight(i, 40)

    def load_example(self):
        example_index = self.examples_combo.currentIndex()
        if example_index == 0:
            return

        if example_index == 1:
            size = 5
            matrix = np.ones((size, size), dtype=int) - np.eye(size, dtype=int)
        elif example_index == 2:
            size = 5
            matrix = np.zeros((size, size), dtype=int)
            matrix[0, 1] = 1
            matrix[0, 2] = 1
            matrix[1, 3] = 1
            matrix[2, 4] = 1
        elif example_index == 3:
            size = 6
            matrix = np.zeros((size, size), dtype=int)
            matrix[0, 1] = 1
            matrix[1, 2] = 1
            matrix[2, 0] = 1
            matrix[3, 4] = 1
            matrix[4, 5] = 1
            matrix[5, 3] = 1
        elif example_index == 4:
            size = 5
            matrix = np.zeros((size, size), dtype=int)
            for i in range(size - 1):
                matrix[i, i + 1] = 1
        elif example_index == 5:
            size = 5
            matrix = np.zeros((size, size), dtype=int)
            for i in range(size - 1):
                matrix[i, i + 1] = 1
            matrix[size - 1, 0] = 1

        self.size_spinbox.setValue(size)
        self.create_adjacency_matrix()

        for i in range(size):
            for j in range(size):
                if i != j:
                    item = self.matrix_table.item(i, j)
                    item.setText(str(matrix[i, j]))
                    if matrix[i, j] == 1:
                        item.setBackground(QColor("#e3f2fd"))
                    else:
                        item.setBackground(QColor("white"))

        example_descriptions = [
            "",
            "Сильно связный граф (полный ориентированный граф). Каждая вершина связана со всеми остальными.",
            "Слабо связный граф (дерево). Если игнорировать направление рёбер, то граф связный.",
            "Несвязный граф с двумя независимыми компонентами связности.",
            "Цепь (линейная структура). Последовательность вершин, соединенных направленными рёбрами.",
            "Цикл. Замкнутая цепь вершин.",
        ]

        result_text = f"<h3>Загружен {self.examples_combo.currentText()}</h3>"
        result_text += f"<p style='line-height: 1.5; margin-top: 10px;'>{example_descriptions[example_index]}</p>"
        result_text += "<p style='margin-top: 15px;'>Нажмите <b>Рассчитать показатели</b> для анализа связности.</p>"

        self.results_text.setHtml(result_text)

    def calculate_metrics(self):
        size = self.matrix_table.rowCount()

        if size == 0:
            QMessageBox.warning(
                self, "Предупреждение", "Сначала создайте матрицу смежности!"
            )
            return

        adjacency_matrix = np.zeros((size, size), dtype=int)
        for i in range(size):
            for j in range(size):
                try:
                    value = int(self.matrix_table.item(i, j).text())
                    if value not in [0, 1]:
                        QMessageBox.warning(
                            self,
                            "Ошибка ввода",
                            f"Некорректное значение в ячейке ({i+1}, {j+1}). Используйте только 0 или 1.",
                        )
                        return
                    adjacency_matrix[i, j] = value
                except ValueError:
                    QMessageBox.warning(
                        self,
                        "Ошибка ввода",
                        f"Некорректное значение в ячейке ({i+1}, {j+1}). Используйте только 0 или 1.",
                    )
                    return

        # Расчет матрицы AΣ
        a_sigma_matrix = self.calculate_asigma_matrix(adjacency_matrix)

        # Обновление таблицы AΣ
        self.asigma_table.setRowCount(size)
        self.asigma_table.setColumnCount(size)
        headers = [str(i + 1) for i in range(size)]
        self.asigma_table.setHorizontalHeaderLabels(headers)
        self.asigma_table.setVerticalHeaderLabels(headers)

        for i in range(size):
            for j in range(size):
                item = QTableWidgetItem(str(a_sigma_matrix[i][j]))
                item.setTextAlignment(Qt.AlignCenter)
                self.asigma_table.setItem(i, j, item)
                if a_sigma_matrix[i][j] > 0:
                    item.setBackground(QColor("#e3f2fd"))
                else:
                    item.setBackground(QColor("white"))
            self.asigma_table.setColumnWidth(i, 60)
            self.asigma_table.setRowHeight(i, 40)

        result_text = self.calculate_connectivity(adjacency_matrix)
        self.results_text.setHtml(result_text)

    def calculate_asigma_matrix(self, adjacency_matrix):
        n = len(adjacency_matrix)
        a_sigma = np.eye(n, dtype=int)
        current_power = np.eye(n, dtype=int)

        for _ in range(n):
            current_power = np.matmul(current_power, adjacency_matrix)
            a_sigma += current_power

        return a_sigma

    def calculate_connectivity(self, adjacency_matrix):
        n = len(adjacency_matrix)
        absolute_connectivity = np.sum(adjacency_matrix)
        max_connections = n * (n - 1)
        relative_connectivity = absolute_connectivity / max_connections if max_connections > 0 else 0

        reachability_matrix = self.calculate_reachability_matrix(adjacency_matrix)
        is_strongly_connected = np.all(reachability_matrix > 0)

        undirected_matrix = adjacency_matrix | adjacency_matrix.T
        undirected_reachability = self.calculate_reachability_matrix(undirected_matrix)
        is_weakly_connected = np.all(np.logical_or(undirected_reachability, np.eye(n, dtype=int)))

        result = f"""
        <h3>Результаты анализа структуры системы</h3>
        <div style='margin-top: 15px;'>
            <table cellspacing='0' cellpadding='5' style='border-collapse: collapse; width: 100%;'>
                <tr style='background-color: #f8f9fa;'>
                    <td style='padding: 8px; border: 1px solid #ddd; font-weight: bold;'>Размер графа:</td>
                    <td style='padding: 8px; border: 1px solid #ddd;'>{n}x{n}</td>
                </tr>
                <tr>
                    <td style='padding: 8px; border: 1px solid #ddd; font-weight: bold;'>Абсолютная связность (A):</td>
                    <td style='padding: 8px; border: 1px solid #ddd;'>{absolute_connectivity}</td>
                </tr>
                <tr style='background-color: #f8f9fa;'>
                    <td style='padding: 8px; border: 1px solid #ddd; font-weight: bold;'>Максимально возможное количество связей:</td>
                    <td style='padding: 8px; border: 1px solid #ddd;'>{max_connections}</td>
                </tr>
                <tr>
                    <td style='padding: 8px; border: 1px solid #ddd; font-weight: bold;'>Относительная связность (C):</td>
                    <td style='padding: 8px; border: 1px solid #ddd;'>{relative_connectivity:.4f}</td>
                </tr>
                <tr style='background-color: #f8f9fa;'>
                    <td style='padding: 8px; border: 1px solid #ddd; font-weight: bold;'>Сильная связность:</td>
                    <td style='padding: 8px; border: 1px solid #ddd;'>{"Да" if is_strongly_connected else "Нет"}</td>
                </tr>
                <tr>
                    <td style='padding: 8px; border: 1px solid #ddd; font-weight: bold;'>Слабая связность:</td>
                    <td style='padding: 8px; border: 1px solid #ddd;'>{"Да" if is_weakly_connected else "Нет"}</td>
                </tr>
            </table>
        </div>
        
        <h4 style='margin-top: 20px;'>Матрица достижимости:</h4>
        <div style='margin-top: 10px; font-family: Consolas, monospace; background-color: #f8f9fa; padding: 10px; border: 1px solid #dcdcdc; border-radius: 4px;'>
        """

        result += "<table cellspacing='0' cellpadding='5' style='border-collapse: collapse;'>"
        result += "<tr><td style='width: 30px;'></td>"
        for i in range(n):
            result += f"<td style='width: 30px; text-align: center; font-weight: bold;'>{i+1}</td>"
        result += "</tr>"

        for i in range(n):
            result += f"<tr><td style='font-weight: bold; text-align: center;'>{i+1}</td>"
            for j in range(n):
                color = "#e3f2fd" if reachability_matrix[i, j] == 1 else "white"
                result += f"<td style='width: 30px; text-align: center; background-color: {color};'>{reachability_matrix[i, j]}</td>"
            result += "</tr>"
        result += "</table></div>"

        result += f"""
        <div style='margin-top: 20px;'>
            <h4>Интерпретация результатов:</h4>
            <ul style='line-height: 1.5;'>
                <li>Граф <b>{'' if is_strongly_connected else 'не '}является сильно связным</b>. 
                    {{
                        'Из любой вершины можно достичь любую другую вершину, следуя по направленным рёбрам.' 
                        if is_strongly_connected else 
                        'Существуют вершины, из которых невозможно достичь некоторых других вершин, следуя по направленным рёбрам.'
                    }}
                </li>
                <li>Граф <b>{'' if is_weakly_connected else 'не '}является слабо связным</b>. 
                    {{
                        'Если игнорировать направление рёбер, то граф образует связную структуру.' 
                        if is_weakly_connected else 
                        'Даже если игнорировать направление рёбер, граф всё равно содержит не связанные между собой компоненты.'
                    }}
                </li>
                <li>Относительная связность (C={relative_connectivity:.4f}) показывает, насколько граф близок к полносвязному графу.
                    {{
                        ' Значение близко к 1, что указывает на высокую связность структуры.' 
                        if relative_connectivity > 0.7 else 
                        ' Значение среднее, что указывает на умеренную связность структуры.' 
                        if relative_connectivity > 0.3 else
                        ' Значение низкое, что указывает на слабую связность структуры.'
                    }}
                </li>
            </ul>
        </div>
        """

        return result

    def calculate_reachability_matrix(self, adjacency_matrix):
        n = len(adjacency_matrix)
        reachability = np.eye(n, dtype=int) | adjacency_matrix

        for k in range(n):
            for i in range(n):
                for j in range(n):
                    if reachability[i, k] == 1 and reachability[k, j] == 1:
                        reachability[i, j] = 1

        return reachability


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = StructuralAnalysisApp()
    window.show()
    sys.exit(app.exec_())