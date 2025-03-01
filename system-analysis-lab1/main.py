import sys
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QSpinBox,
    QTableWidget,
    QTableWidgetItem,
    QPushButton,
    QTextEdit,
    QHeaderView,
    QMessageBox,
    QFileDialog,
)
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QColor
import matplotlib.pyplot as plt
import networkx as nx


class AnimatedButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self._animation = QPropertyAnimation(self, b"color")
        self._animation.setDuration(200)
        self.normal_color = QColor(100, 149, 237)
        self.hover_color = QColor(65, 105, 225)
        self.setStyleSheet(
            f"""
            QPushButton {{
                background-color: {self.normal_color.name()};
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-size: 14px;
                font-weight: 500;
            }}
            QPushButton:hover {{
                background-color: {self.hover_color.name()};
            }}
        """
        )

    def enterEvent(self, event):
        self._animate_color(self.normal_color, self.hover_color)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._animate_color(self.hover_color, self.normal_color)
        super().leaveEvent(event)

    def _animate_color(self, start, end):
        self._animation.stop()
        self._animation.setStartValue(start)
        self._animation.setEndValue(end)
        self._animation.setEasingCurve(QEasingCurve.InOutQuad)
        self._animation.start()


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setStyleSheet(self.get_styles())
        self.resize(1280, 800)

    def get_styles(self):
        return """
            QWidget {
                background-color: #f8f9fa;
                font-family: 'Segoe UI', sans-serif;
            }
            QLabel {
                color: #495057;
                font-size: 14px;
                font-weight: 500;
            }
            QSpinBox {
                padding: 5px;
                border: 1px solid #ced4da;
                border-radius: 4px;
                background: white;
            }
            QTableWidget {
                background-color: white;
                border: 1px solid #dee2e6;
                border-radius: 4px;
                gridline-color: #e9ecef;
                font-size: 14px;
            }
            QHeaderView::section {
                background-color: #6c757d;
                color: white;
                padding: 8px;
                border: none;
                font-weight: 500;
            }
            QTextEdit {
                background: white;
                border: 1px solid #ced4da;
                border-radius: 4px;
                padding: 5px;
                font-size: 14px;
            }
        """

    def initUI(self):
        self.setWindowTitle("Системный анализ • Лабораторная работа №1")

        self.vertices_spin = QSpinBox()
        self.vertices_spin.setMinimum(1)
        self.vertices_spin.setValue(2)

        self.edges_spin = QSpinBox()
        self.edges_spin.setMinimum(1)
        self.edges_spin.setValue(1)

        self.update_b_button = AnimatedButton("🔄 Обновить таблицу")
        self.update_b_button.clicked.connect(self.update_b_table)

        self.load_button = AnimatedButton("📂 Загрузить из файла")
        self.load_button.clicked.connect(self.load_from_file)

        self.clear_button = AnimatedButton("🧹 Очистить всё")
        self.clear_button.clicked.connect(self.clear_all)

        self.convert_button = AnimatedButton("⚡ Преобразовать")
        self.convert_button.clicked.connect(self.convert)

        self.b_table = QTableWidget()
        self.b_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.a_table = QTableWidget()
        self.a_table.setFixedHeight(250)

        self.g_plus_text = QTextEdit()
        self.g_plus_text.setReadOnly(True)

        controls_layout = QHBoxLayout()
        controls_layout.addWidget(QLabel("Число вершин:"))
        controls_layout.addWidget(self.vertices_spin)
        controls_layout.addWidget(QLabel("Число ребер:"))
        controls_layout.addWidget(self.edges_spin)
        controls_layout.addStretch()

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.update_b_button)
        buttons_layout.addWidget(self.load_button)
        buttons_layout.addWidget(self.clear_button)
        buttons_layout.addWidget(self.convert_button)
        buttons_layout.addStretch()

        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.addLayout(controls_layout)
        main_layout.addWidget(QLabel("Матрица инциденций B:"))
        main_layout.addWidget(self.b_table)
        main_layout.addLayout(buttons_layout)
        main_layout.addWidget(QLabel("Матрица смежности A:"))
        main_layout.addWidget(self.a_table)
        main_layout.addWidget(QLabel("Множество правых инциденций G+:"))
        main_layout.addWidget(self.g_plus_text)

        self.setLayout(main_layout)
        self.update_b_table()

    def clear_all(self):
        self.vertices_spin.setValue(2)
        self.edges_spin.setValue(1)
        self.update_b_table()
        self.a_table.clear()
        self.a_table.setRowCount(0)
        self.a_table.setColumnCount(0)
        self.g_plus_text.clear()

    def update_b_table(self):
        m = self.vertices_spin.value()
        n = self.edges_spin.value()
        self.b_table.setRowCount(m)
        self.b_table.setColumnCount(n)
        self.b_table.setHorizontalHeaderLabels([f"Ребро {i+1}" for i in range(n)])
        self.b_table.setVerticalHeaderLabels([f"Вершина {i+1}" for i in range(m)])
        for i in range(m):
            for j in range(n):
                if self.b_table.item(i, j) is None:
                    item = QTableWidgetItem("0")
                    item.setTextAlignment(Qt.AlignCenter)
                    self.b_table.setItem(i, j, item)
                else:
                    self.b_table.item(i, j).setText("0")
        self.b_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def load_from_file(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Выберите файл", "", "Text Files (*.txt);;All Files (*)"
        )
        if not file_name:
            return

        try:
            with open(file_name, "r") as file:
                lines = file.readlines()
                if not lines:
                    raise ValueError("Файл пустой")

                header = lines[0].strip().split()
                if len(header) != 2:
                    raise ValueError(
                        "Первая строка должна содержать два числа: вершины и ребра"
                    )
                m, n = map(int, header)
                if m < 1 or n < 1:
                    raise ValueError("Число вершин и ребер должно быть положительным")

                self.vertices_spin.setValue(m)
                self.edges_spin.setValue(n)
                self.update_b_table()

                if len(lines) - 1 != m:
                    raise ValueError(
                        f"Ожидалось {m} строк матрицы, найдено {len(lines)-1}"
                    )
                for i in range(m):
                    row = lines[i + 1].strip().split()
                    if len(row) != n:
                        raise ValueError(f"Строка {i+1} должна содержать {n} значений")
                    for j, val in enumerate(row):
                        if val not in {"0", "1", "-1"}:
                            raise ValueError(
                                f"Недопустимое значение '{val}' в строке {i+1}, столбце {j+1}"
                            )
                        item = QTableWidgetItem(val)
                        item.setTextAlignment(Qt.AlignCenter)
                        self.b_table.setItem(i, j, item)

        except Exception as e:
            QMessageBox.critical(
                self, "Ошибка", f"Ошибка при загрузке файла:\n{str(e)}", QMessageBox.Ok
            )

    def convert(self):
        try:
            m = self.vertices_spin.value()
            n = self.edges_spin.value()

            B = []
            for i in range(m):
                row = []
                for j in range(n):
                    item = self.b_table.item(i, j)
                    if item is None:
                        val = 0
                    else:
                        text = item.text().strip()
                        if text == "1":
                            val = 1
                        elif text == "-1":
                            val = -1
                        elif text == "0":
                            val = 0
                        else:
                            raise ValueError(
                                f"Неверное значение '{text}' в вершине {i+1}, ребро {j+1}"
                            )
                    row.append(val)
                B.append(row)

            A, G_plus = self.convert_incidence(B)

            self.a_table.setRowCount(m)
            self.a_table.setColumnCount(m)
            self.a_table.setHorizontalHeaderLabels([str(i + 1) for i in range(m)])
            self.a_table.setVerticalHeaderLabels([str(i + 1) for i in range(m)])
            for i in range(m):
                for j in range(m):
                    item = QTableWidgetItem(str(A[i][j]))
                    item.setTextAlignment(Qt.AlignCenter)
                    self.a_table.setItem(i, j, item)

            text = ""
            for vertex in sorted(G_plus.keys()):
                end_vertices = (
                    ", ".join(map(str, sorted(set(G_plus[vertex]))))
                    if G_plus[vertex]
                    else "0"
                )
                text += f"Вершина {vertex+1}: {end_vertices}\n"
            self.g_plus_text.setText(text)

            self.draw_graph(A)

        except Exception as e:
            QMessageBox.critical(
                self, "Ошибка", f"Произошла ошибка:\n{str(e)}", QMessageBox.Ok
            )

    def convert_incidence(self, B):
        m = len(B)
        n = len(B[0]) if m > 0 else 0
        A = [[0] * m for _ in range(m)]
        G_plus = {i: set() for i in range(m)}
        existing_edges = set()

        for edge_idx in range(n):
            start = None
            end = None
            for vertex in range(m):
                val = B[vertex][edge_idx]
                if val == 1:
                    if start is not None:
                        raise ValueError(
                            f"В ребре {edge_idx+1} несколько начальных вершин"
                        )
                    start = vertex
                elif val == -1:
                    if end is not None:
                        raise ValueError(
                            f"В ребре {edge_idx+1} несколько конечных вершин"
                        )
                    end = vertex
                elif val != 0:
                    raise ValueError(
                        f"Недопустимое значение {val} в ребре {edge_idx+1}, вершина {vertex+1}"
                    )
            if start is None:
                raise ValueError(f"В ребре {edge_idx+1} нет начальной вершины (1)")
            if end is None:
                raise ValueError(f"В ребре {edge_idx+1} нет конечной вершины (-1)")
            if (start, end) in existing_edges:
                raise ValueError(
                    f"Ребро между вершинами {start+1} и {end+1} уже существует"
                )
            existing_edges.add((start, end))
            A[start][end] += 1

            if start is not None:
                G_plus[start].add(end + 1)

        G_plus = {k: sorted(list(v)) for k, v in G_plus.items()}
        return A, G_plus

    def draw_graph(self, A):
        G = nx.DiGraph()
        m = len(A)
        for i in range(m):
            G.add_node(i + 1)
        for i in range(m):
            for j in range(m):
                if A[i][j] > 0:
                    G.add_edge(i + 1, j + 1)
        plt.figure(figsize=(8, 6))
        pos = nx.spring_layout(G)
        nx.draw(
            G,
            pos,
            with_labels=True,
            node_color="lightblue",
            node_size=500,
            font_size=12,
            font_weight="bold",
            arrows=True,
            edge_color="gray",
        )
        plt.title("Визуализация графа")
        plt.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
