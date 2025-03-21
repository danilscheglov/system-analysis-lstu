import sys
import networkx as nx
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QLabel,
    QTextEdit,
    QPushButton,
    QHBoxLayout,
    QFileDialog,
    QMessageBox,
    QGridLayout,
    QFrame,
)
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QFont, QPalette, QColor, QPixmap, QIcon
from PyQt5.QtWidgets import QGraphicsDropShadowEffect


class GraphDecompositionApp(QMainWindow):
    """Главное окно приложения для топологической декомпозиции графа с современным UI."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Топологическая декомпозиция графа")
        self.setGeometry(100, 100, 900, 700)

        self.set_dark_theme()

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        title_label = QLabel("Системный анализ • Лабораторная работа №3")
        title_label.setFont(QFont("Segoe UI", 18, QFont.Bold))
        title_label.setStyleSheet("color: #ffffff; margin-bottom: 10px;")
        main_layout.addWidget(title_label, alignment=Qt.AlignCenter)

        control_frame = QFrame()
        control_frame.setStyleSheet(
            """
            QFrame {
                background-color: #2a2a2a;
                border-radius: 10px;
                padding: 15px;
            }
        """
        )
        control_layout = QGridLayout(control_frame)
        control_layout.setSpacing(10)

        self.input_label = QLabel("Введите матрицу смежности:")
        self.input_label.setFont(QFont("Segoe UI", 12))
        self.input_label.setStyleSheet("color: #d3d3d3;")
        control_layout.addWidget(self.input_label, 0, 0, 1, 2)

        self.matrix_input = QTextEdit()
        self.matrix_input.setFont(QFont("Consolas", 11))
        self.matrix_input.setPlaceholderText("Пример:\n0 1 0\n0 0 1\n0 0 0")
        self.matrix_input.setStyleSheet(
            """
            QTextEdit {
                background-color: #333333;
                color: #ffffff;
                border: 1px solid #555555;
                border-radius: 5px;
                padding: 10px;
            }
        """
        )
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 160))
        shadow.setOffset(0, 2)
        self.matrix_input.setGraphicsEffect(shadow)
        control_layout.addWidget(self.matrix_input, 1, 0, 1, 2)

        self.load_button = QPushButton("📂 Загрузить из файла")
        self.load_button.setFont(QFont("Segoe UI", 11))
        self.load_button.setStyleSheet(
            """
            QPushButton {
                background-color: #4a90e2;
                color: white;
                border-radius: 5px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #357abd;
            }
            QPushButton:pressed {
                background-color: #2a5d91;
            }
        """
        )
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setColor(QColor(0, 0, 0, 100))
        shadow.setOffset(0, 2)
        self.load_button.setGraphicsEffect(shadow)
        self.load_button.clicked.connect(self.load_from_file)
        control_layout.addWidget(self.load_button, 2, 0, 1, 1)

        self.analyze_button = QPushButton("🔍 Анализировать")
        self.analyze_button.setFont(QFont("Segoe UI", 11))
        self.analyze_button.setStyleSheet(
            """
            QPushButton {
                background-color: #28a745;
                color: white;
                border-radius: 5px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
            QPushButton:pressed {
                background-color: #1c6d30;
            }
        """
        )
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setColor(QColor(0, 0, 0, 100))
        shadow.setOffset(0, 2)
        self.analyze_button.setGraphicsEffect(shadow)
        self.analyze_button.clicked.connect(self.analyze_graph)
        control_layout.addWidget(self.analyze_button, 2, 1, 1, 1)

        self.instruction_label = QLabel(
            "Граф должен быть ациклическим (дуги направлены в одну сторону)."
        )
        self.instruction_label.setFont(QFont("Segoe UI", 10, QFont.StyleItalic))
        self.instruction_label.setStyleSheet("color: #aaaaaa; margin-top: 5px;")
        control_layout.addWidget(self.instruction_label, 3, 0, 1, 2)

        main_layout.addWidget(control_frame)

        self.result_text = QTextEdit()
        self.result_text.setFont(QFont("Consolas", 11))
        self.result_text.setReadOnly(True)
        self.result_text.setStyleSheet(
            """
            QTextEdit {
                background-color: #333333;
                color: #ffffff;
                border: 1px solid #555555;
                border-radius: 5px;
                padding: 10px;
            }
        """
        )
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 160))
        shadow.setOffset(0, 2)
        self.result_text.setGraphicsEffect(shadow)
        main_layout.addWidget(self.result_text)

        self.adjacency = None
        self.matrix = None

    def set_dark_theme(self):
        """Устанавливает темную тему для приложения."""
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(34, 34, 34))
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.Base, QColor(51, 51, 51))
        palette.setColor(QPalette.AlternateBase, QColor(34, 34, 34))
        palette.setColor(QPalette.Text, Qt.white)
        palette.setColor(QPalette.Button, QColor(74, 144, 226))
        palette.setColor(QPalette.ButtonText, Qt.white)
        palette.setColor(QPalette.BrightText, Qt.red)
        palette.setColor(QPalette.Highlight, QColor(40, 167, 69))
        palette.setColor(QPalette.HighlightedText, Qt.white)
        self.setPalette(palette)
        self.setStyleSheet("background-color: #222222;")

    def load_from_file(self):
        """Загружает матрицу смежности из файла."""
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Выберите файл", "", "Text Files (*.txt)"
        )
        if file_name:
            try:
                with open(file_name, "r", encoding="utf-8") as file:
                    matrix_str = file.read().strip()
                    self.matrix_input.setText(matrix_str)
            except Exception as e:
                self.result_text.setText(f"Ошибка при чтении файла: {str(e)}")

    def parse_matrix(self, matrix_str):
        """Парсит текстовый ввод в матрицу смежности."""
        try:
            rows = [
                list(map(int, row.split()))
                for row in matrix_str.strip().split("\n")
                if row.strip()
            ]
            if not rows or not all(len(row) == len(rows[0]) for row in rows):
                raise ValueError(
                    "Некорректная матрица! Все строки должны иметь одинаковое количество элементов."
                )
            self.matrix = rows
            n = len(rows)
            adjacency = {i + 1: [] for i in range(n)}
            for i in range(n):
                for j in range(len(rows[i])):
                    if rows[i][j] == 1 and i != j:
                        adjacency[i + 1].append(j + 1)
            return adjacency
        except Exception as e:
            self.result_text.setText(f"Ошибка парсинга: {str(e)}")
            return None

    def build_graph(self, edges):
        """Создает ориентированный граф на основе списка ребер."""
        G = nx.DiGraph()
        G.add_edges_from(edges)
        return G

    def get_subsystem_edges(self, subsystem):
        """Находит дуги внутри заданной подсистемы."""
        edges = []
        n = len(self.matrix)
        for i in range(n):
            for j in range(n):
                if (
                    self.matrix[i][j] == 1
                    and i != j
                    and (i + 1) in subsystem
                    and (j + 1) in subsystem
                ):
                    edges.append((i + 1, j + 1))
        return edges

    def get_subsystem_right_incidence(self, subsystem_graph, num_subsystems):
        """Определяет множества правых инциденций для подсистем."""
        right_incidence = {i + 1: set() for i in range(num_subsystems)}
        for i in range(num_subsystems):
            for j in range(num_subsystems):
                if subsystem_graph.has_edge(j + 1, i + 1):
                    right_incidence[i + 1].add(j + 1)
        return right_incidence

    def check_acyclic(self, G):
        """Проверяет, является ли граф ациклическим (DAG)."""
        try:
            nx.topological_sort(G)
            return True
        except nx.NetworkXUnfeasible:
            return False

    def find_cycles(self, G):
        """Находит все простые циклы в графе."""
        try:
            cycles = list(nx.simple_cycles(G))
            return cycles
        except nx.NetworkXNoCycle:
            return []

    def analyze_graph(self):
        """Выполняет анализ графа и визуализацию результатов."""
        matrix_str = self.matrix_input.toPlainText().strip()
        if not matrix_str:
            self.result_text.setText("Введите матрицу смежности!")
            return

        self.adjacency = self.parse_matrix(matrix_str)
        if not self.adjacency or not self.matrix:
            return

        all_edges = []
        n = len(self.matrix)
        for i in range(n):
            for j in range(n):
                if self.matrix[i][j] == 1 and i != j:
                    all_edges.append((i + 1, j + 1))

        G_original = self.build_graph(all_edges)

        if not self.check_acyclic(G_original):
            cycles = self.find_cycles(G_original)
            cycle_str = "\n".join(
                [
                    f"Цикл: {' -> '.join(map(str, cycle + [cycle[0]]))}"
                    for cycle in cycles
                ]
            )
            QMessageBox.warning(
                self,
                "Ошибка",
                f"Граф содержит циклы, что недопустимо для ациклического графа!\n{cycle_str}\n"
                "Пожалуйста, исправьте матрицу, удалив одно из ребер в каждом цикле.",
            )
            return

        subsystems = list(nx.strongly_connected_components(G_original))

        all_nodes = set(range(1, n + 1))
        used_nodes = set().union(*subsystems)
        isolated_nodes = all_nodes - used_nodes
        for node in isolated_nodes:
            subsystems.append({node})
        subsystems_with_edges = [
            (subsystem, self.get_subsystem_edges(subsystem)) for subsystem in subsystems
        ]

        color_map = [
            "skyblue",
            "lightcoral",
            "lightgreen",
            "gold",
            "violet",
            "cyan",
            "magenta",
            "yellow",
            "orange",
        ]
        legend_labels = []
        for idx, subsystem in enumerate(subsystems):
            legend_labels.append(f"Подсистема {idx + 1}")

        plt.figure(figsize=(8, 6))
        pos = nx.spring_layout(G_original, seed=42, scale=1.0, center=(0, 0))
        nx.draw_networkx_nodes(
            G_original,
            pos,
            node_color="white",
            node_size=800,
            edgecolors="black",
            linewidths=1.5,
        )
        nx.draw_networkx_edges(
            G_original,
            pos,
            edge_color="navy",
            arrows=True,
            arrowsize=25,
            width=1.5,
            alpha=0.7,
        )
        nx.draw_networkx_labels(
            G_original, pos, font_size=12, font_weight="bold", font_color="black"
        )
        plt.title("Исходный граф", fontsize=14, pad=20)
        plt.axis("off")
        plt.savefig("original_graph.png", dpi=300, bbox_inches="tight")
        plt.close()

        G_subsystems = nx.DiGraph()
        for i in range(len(subsystems)):
            G_subsystems.add_node(i + 1, label=f"Подсистема {i+1}")

        subsystem_colors = [
            color_map[i % len(color_map)] for i in range(len(subsystems))
        ]
        subsystem_edges = []
        for i in range(len(subsystems)):
            for j in range(len(subsystems)):
                if i != j:
                    for u in subsystems[i]:
                        for v in subsystems[j]:
                            if (u, v) in G_original.edges:
                                G_subsystems.add_edge(i + 1, j + 1)
                                subsystem_edges.append((i + 1, j + 1))
                                break
                        else:
                            continue
                        break

        plt.figure(figsize=(8, 6))
        pos_sub = nx.spring_layout(G_subsystems, seed=42, scale=1.0, center=(0, 0))
        nx.draw_networkx_nodes(
            G_subsystems,
            pos_sub,
            node_color=subsystem_colors,
            node_size=1200,
            edgecolors="black",
            linewidths=1.5,
        )
        nx.draw_networkx_edges(
            G_subsystems,
            pos_sub,
            edgelist=subsystem_edges,
            edge_color="darkgreen",
            arrows=True,
            arrowsize=25,
            width=2,
            alpha=0.8,
        )
        nx.draw_networkx_labels(
            G_subsystems,
            pos_sub,
            labels={n: G_subsystems.nodes[n]["label"] for n in G_subsystems.nodes},
            font_size=12,
            font_weight="bold",
            font_color="black",
        )
        plt.title("Граф подсистем", fontsize=14, pad=20)
        plt.legend(
            handles=[
                plt.Line2D(
                    [0],
                    [0],
                    marker="o",
                    color="w",
                    markerfacecolor=color,
                    markersize=10,
                    label=label,
                )
                for color, label in zip(subsystem_colors, legend_labels)
            ],
            loc="best",
            frameon=True,
            edgecolor="black",
        )
        plt.axis("off")
        plt.savefig("subsystem_graph.png", dpi=300, bbox_inches="tight")
        plt.close()

        result_text = "Подсистемы (связные компоненты):\n\n"
        for i, (subsystem, edges) in enumerate(subsystems_with_edges, 1):
            result_text += f"Подсистема {i}:\n"
            result_text += f"Вершины: {', '.join(map(str, sorted(list(subsystem))))}\n"
            result_text += f"Дуги: {', '.join([f'{u}--{v}' for u, v in edges]) if edges else 'Нет дуг'}\n\n"

        right_incidence = self.get_subsystem_right_incidence(
            G_subsystems, len(subsystems)
        )
        result_text += "Множества правых инциденций для подсистем:\n"
        for s, inc_set in right_incidence.items():
            result_text += f"Подсистема {s}: {sorted(list(inc_set)) if inc_set else 'Нет входящих связей'}\n"

        self.result_text.setText(result_text)
        self.show_graphs()

    def show_graphs(self):
        """Отображает графики в отдельном окне."""
        graph_window = QWidget()
        graph_window.setWindowTitle("Графики")
        graph_window.setStyleSheet("background-color: #222222;")
        graph_layout = QHBoxLayout(graph_window)
        graph_layout.setContentsMargins(10, 10, 10, 10)

        original_label = QLabel(graph_window)
        original_pixmap = QPixmap("original_graph.png")
        original_label.setPixmap(original_pixmap.scaled(400, 300, Qt.KeepAspectRatio))
        original_label.setStyleSheet(
            "background-color: #333333; border-radius: 5px; padding: 5px;"
        )
        graph_layout.addWidget(original_label)

        subsystem_label = QLabel(graph_window)
        subsystem_pixmap = QPixmap("subsystem_graph.png")
        subsystem_label.setPixmap(subsystem_pixmap.scaled(400, 300, Qt.KeepAspectRatio))
        subsystem_label.setStyleSheet(
            "background-color: #333333; border-radius: 5px; padding: 5px;"
        )
        graph_layout.addWidget(subsystem_label)

        graph_window.setGeometry(200, 200, 800, 300)
        graph_window.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GraphDecompositionApp()
    window.show()
    sys.exit(app.exec_())
