import sys
import numpy as np
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QLabel, QPushButton, QTableWidget, 
                            QTableWidgetItem, QSpinBox, QMessageBox, QGroupBox,
                            QSplitter, QFileDialog, QCheckBox, QGridLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor, QIcon
import random

class ShortestPathFinder:
    def __init__(self):
        self.distances = None
        self.n = 0
        
    def set_distances(self, distances):
        self.distances = distances
        self.n = len(distances)
    
    def find_shortest_paths(self):
        # Инициализация матрицы кратчайших путей и предшественников
        shortest_paths = [[float('inf') for _ in range(self.n)] for _ in range(self.n)]
        path = [[-1 for _ in range(self.n)] for _ in range(self.n)]
        
        for i in range(self.n):
            for j in range(self.n):
                shortest_paths[i][j] = self.distances[i][j]
                if self.distances[i][j] != float('inf') and i != j:
                    path[i][j] = i
                else:
                    path[i][j] = -1
        
        for k in range(self.n):
            for i in range(self.n):
                for j in range(self.n):
                    if shortest_paths[i][k] != float('inf') and shortest_paths[k][j] != float('inf'):
                        new_dist = shortest_paths[i][k] + shortest_paths[k][j]
                        if new_dist < shortest_paths[i][j]:
                            shortest_paths[i][j] = new_dist
                            path[i][j] = path[k][j]
        
        return shortest_paths, path
    
    def get_path(self, source, target, path_matrix):
        if source == target:
            return [source]
            
        if path_matrix[source][target] == -1:
            return []
        
        result = []
        current = target
        
        while current != source:
            result.append(current)
            current = path_matrix[source][current]
            if current == -1:
                return []
            
        result.append(source)
        
        return result[::-1]

class ShortestPathApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.path_finder = ShortestPathFinder()
        self.shortest_paths = None
        self.path_matrix = None
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle('Поиск кратчайших путей в графе без контуров')
        self.setGeometry(100, 100, 1000, 800)
        
        # Основной виджет и лэйаут
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        
        # Создаем разделитель для верхней и нижней частей интерфейса
        splitter = QSplitter(Qt.Vertical)
        
        # Верхняя часть - настройка и ввод данных
        top_widget = QWidget()
        top_layout = QVBoxLayout()
        
        # Группа настройки размера графа
        size_group = QGroupBox("Настройки графа")
        size_layout = QHBoxLayout()
        
        self.size_label = QLabel("Количество вершин:")
        self.size_label.setFont(QFont("Arial", 10))
        self.size_spinbox = QSpinBox()
        self.size_spinbox.setRange(2, 20)
        self.size_spinbox.setValue(5)
        self.size_spinbox.setFont(QFont("Arial", 10))
        self.size_spinbox.setStyleSheet("QSpinBox { padding: 5px; }")
        
        self.create_matrix_btn = QPushButton("Создать матрицу")
        self.create_matrix_btn.setFont(QFont("Arial", 10))
        self.create_matrix_btn.setIcon(QIcon("icons/create.png"))
        self.create_matrix_btn.setToolTip("Создать новую матрицу расстояний")
        self.create_matrix_btn.clicked.connect(self.create_distance_matrix)
        
        size_layout.addWidget(self.size_label)
        size_layout.addWidget(self.size_spinbox)
        size_layout.addWidget(self.create_matrix_btn)
        size_layout.addStretch(1)
        size_group.setLayout(size_layout)
        
        # Панель инструментов для матрицы расстояний
        matrix_tools_layout = QHBoxLayout()
        
        self.example_btn = QPushButton("Заполнить примером")
        self.example_btn.setFont(QFont("Arial", 10))
        self.example_btn.setIcon(QIcon("icons/example.png"))
        self.example_btn.setToolTip("Заполнить матрицу примером")
        self.example_btn.clicked.connect(self.fill_example_matrix)
        
        self.random_btn = QPushButton("Случайный граф")
        self.random_btn.setFont(QFont("Arial", 10))
        self.random_btn.setIcon(QIcon("icons/random.png"))
        self.random_btn.setToolTip("Сгенерировать случайный ациклический граф")
        self.random_btn.clicked.connect(self.fill_random_matrix)
        
        matrix_tools_layout.addWidget(self.example_btn)
        matrix_tools_layout.addWidget(self.random_btn)
        matrix_tools_layout.addStretch(1)
        
        # Группа для матрицы расстояний
        self.distance_group = QGroupBox("Матрица расстояний")
        distance_layout = QVBoxLayout()
        
        self.distance_table = QTableWidget()
        self.distance_table.setFont(QFont("Arial", 10))
        self.distance_table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #cccccc;
                gridline-color: #e0e0e0;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QHeaderView::section {
                background-color: #f0f0f0;
                padding: 5px;
                border: 1px solid #cccccc;
                font: 10pt Arial;
            }
        """)
        
        distance_layout.addWidget(self.distance_table)
        self.distance_group.setLayout(distance_layout)
        
        # Кнопки действий
        actions_layout = QHBoxLayout()
        
        self.calculate_btn = QPushButton("Найти кратчайшие пути")
        self.calculate_btn.setFont(QFont("Arial", 10))
        self.calculate_btn.setIcon(QIcon("icons/calculate.png"))
        self.calculate_btn.setToolTip("Вычислить кратчайшие пути между всеми вершинами")
        self.calculate_btn.clicked.connect(self.calculate_shortest_paths)
        
        self.clear_btn = QPushButton("Очистить")
        self.clear_btn.setFont(QFont("Arial", 10))
        self.clear_btn.setIcon(QIcon("icons/clear.png"))
        self.clear_btn.setToolTip("Очистить матрицу и результаты")
        self.clear_btn.clicked.connect(self.clear_tables)
        
        self.export_btn = QPushButton("Экспорт результатов")
        self.export_btn.setFont(QFont("Arial", 10))
        self.export_btn.setIcon(QIcon("icons/export.png"))
        self.export_btn.setToolTip("Сохранить результаты в файл")
        self.export_btn.clicked.connect(self.export_results)
        
        actions_layout.addWidget(self.calculate_btn)
        actions_layout.addWidget(self.clear_btn)
        actions_layout.addWidget(self.export_btn)
        
        # Добавляем элементы в верхний лэйаут
        top_layout.addWidget(size_group)
        top_layout.addLayout(matrix_tools_layout)
        top_layout.addWidget(self.distance_group)
        top_layout.addLayout(actions_layout)
        
        top_widget.setLayout(top_layout)
        
        # Нижняя часть - результаты
        bottom_widget = QWidget()
        bottom_layout = QVBoxLayout()
        
        # Группа для матрицы кратчайших путей
        self.result_group = QGroupBox("Матрица кратчайших путей")
        result_layout = QVBoxLayout()
        
        self.result_table = QTableWidget()
        self.result_table.setFont(QFont("Arial", 10))
        self.result_table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #cccccc;
                gridline-color: #e0e0e0;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QHeaderView::section {
                background-color: #f0f0f0;
                padding: 5px;
                border: 1px solid #cccccc;
                font: 10pt Arial;
            }
        """)
        
        result_layout.addWidget(self.result_table)
        self.result_group.setLayout(result_layout)
        
        # Отображение пути
        self.path_group = QGroupBox("Кратчайший путь между вершинами")
        path_layout = QVBoxLayout()
        
        path_selection_layout = QHBoxLayout()
        self.from_label = QLabel("От вершины:")
        self.from_label.setFont(QFont("Arial", 10))
        self.from_spinbox = QSpinBox()
        self.from_spinbox.setFont(QFont("Arial", 10))
        self.from_spinbox.setStyleSheet("QSpinBox { padding: 5px; }")
        self.to_label = QLabel("К вершине:")
        self.to_label.setFont(QFont("Arial", 10))
        self.to_spinbox = QSpinBox()
        self.to_spinbox.setFont(QFont("Arial", 10))
        self.to_spinbox.setStyleSheet("QSpinBox { padding: 5px; }")
        self.show_path_btn = QPushButton("Показать путь")
        self.show_path_btn.setFont(QFont("Arial", 10))
        self.show_path_btn.setIcon(QIcon("icons/path.png"))
        self.show_path_btn.setToolTip("Показать кратчайший путь между выбранными вершинами")
        self.show_path_btn.clicked.connect(self.show_path)
        
        path_selection_layout.addWidget(self.from_label)
        path_selection_layout.addWidget(self.from_spinbox)
        path_selection_layout.addWidget(self.to_label)
        path_selection_layout.addWidget(self.to_spinbox)
        path_selection_layout.addWidget(self.show_path_btn)
        
        self.path_label = QLabel("Выберите вершины и нажмите 'Показать путь'")
        self.path_label.setAlignment(Qt.AlignCenter)
        self.path_label.setFont(QFont("Arial", 11, QFont.Bold))
        self.path_label.setStyleSheet("QLabel { color: #333333; padding: 10px; background-color: #f9f9f9; border-radius: 5px; }")
        
        path_layout.addLayout(path_selection_layout)
        path_layout.addWidget(self.path_label)
        self.path_group.setLayout(path_layout)
        
        # Добавляем элементы в нижний лэйаут
        bottom_layout.addWidget(self.result_group)
        bottom_layout.addWidget(self.path_group)
        
        bottom_widget.setLayout(bottom_layout)
        
        # Добавляем виджеты в сплиттер
        splitter.addWidget(top_widget)
        splitter.addWidget(bottom_widget)
        
        # Добавляем сплиттер в основной лэйаут
        main_layout.addWidget(splitter)
        
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
        
        # Применяем общие стили
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QGroupBox {
                font: 12pt Arial;
                color: #333333;
                border: 1px solid #cccccc;
                border-radius: 5px;
                margin-top: 15px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 5px 10px;
                background-color: #e0e0e0;
                border-radius: 5px;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 8px 15px;
                border: none;
                border-radius: 5px;
                font: 10pt Arial;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
            QLabel {
                color: #333333;
            }
        """)
        
        # Начальная настройка
        self.create_distance_matrix()
    
    def create_distance_matrix(self):
        n = self.size_spinbox.value()
        
        # Настраиваем таблицу расстояний
        self.distance_table.setRowCount(n)
        self.distance_table.setColumnCount(n)
        
        # Заполняем заголовки (нумерация с 1)
        labels = [str(i + 1) for i in range(n)]
        self.distance_table.setHorizontalHeaderLabels(labels)
        self.distance_table.setVerticalHeaderLabels(labels)
        
        # Заполняем значениями по умолчанию
        for i in range(n):
            for j in range(n):
                if i == j:
                    item = QTableWidgetItem("0")
                    item.setBackground(QColor(220, 255, 220))  # Зелёный для диагонали
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                else:
                    item = QTableWidgetItem("∞")
                self.distance_table.setItem(i, j, item)
        
        # Настраиваем спинбоксы выбора вершин (нумерация с 1)
        self.from_spinbox.setRange(1, n)
        self.to_spinbox.setRange(1, n)
        
        # Очищаем результаты
        self.shortest_paths = None
        self.path_matrix = None
        self.result_table.setRowCount(0)
        self.result_table.setColumnCount(0)
        self.path_label.setText("Выберите вершины и нажмите 'Показать путь'")
        
        # Подгоняем размер таблицы
        self.distance_table.resizeColumnsToContents()
    
    def fill_example_matrix(self):
        n = self.size_spinbox.value()
        if n < 5:
            QMessageBox.warning(self, "Предупреждение", "Для примера требуется минимум 5 вершин. Установите размер графа не менее 5.")
            return
        
        # Пример из задания (нумерация с 1, но индексы с 0)
        example = [
            [0, 10, 30, 50, 10],
            [float('inf'), 0, float('inf'), float('inf'), float('inf')],
            [float('inf'), float('inf'), 0, float('inf'), 10],
            [float('inf'), 40, 20, 0, float('inf')],
            [10, float('inf'), 10, 30, 0]
        ]
        
        # Заполняем таблицу примером
        for i in range(n):
            for j in range(n):
                if i == j:
                    item = QTableWidgetItem("0")
                    item.setBackground(QColor(220, 255, 220))
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                else:
                    if i < 5 and j < 5:
                        value = example[i][j]
                        item = QTableWidgetItem("∞" if value == float('inf') else str(int(value)))
                    else:
                        item = QTableWidgetItem("∞")
                self.distance_table.setItem(i, j, item)
    
    def fill_random_matrix(self):
        n = self.size_spinbox.value()
        
        # Очищаем матрицу
        for i in range(n):
            for j in range(n):
                if i == j:
                    item = QTableWidgetItem("0")
                    item.setBackground(QColor(220, 255, 220))
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                else:
                    item = QTableWidgetItem("∞")
                self.distance_table.setItem(i, j, item)
        
        # Заполняем случайные элементы (только для i < j, чтобы гарантировать ацикличность)
        edge_probability = 0.4  # Вероятность существования ребра
        
        for i in range(n):
            for j in range(i + 1, n):  # Только рёбра i → j, где i < j
                if random.random() < edge_probability:
                    weight = random.randint(1, 10)  # Положительный вес
                    self.distance_table.setItem(i, j, QTableWidgetItem(str(weight)))
    
    def calculate_shortest_paths(self):
        try:
            n = self.distance_table.rowCount()
            
            # Считываем матрицу расстояний
            distances = []
            for i in range(n):
                row = []
                for j in range(n):
                    item_text = self.distance_table.item(i, j).text()
                    if item_text == "∞":
                        row.append(float('inf'))
                    else:
                        row.append(float(item_text))
                distances.append(row)
            
            # Устанавливаем матрицу расстояний в алгоритм
            self.path_finder.set_distances(distances)
            
            # Находим кратчайшие пути
            self.shortest_paths, self.path_matrix = self.path_finder.find_shortest_paths()
            
            # Настраиваем таблицу результатов
            self.result_table.setRowCount(n)
            self.result_table.setColumnCount(n)
            
            # Заполняем заголовки (нумерация с 1)
            labels = [str(i + 1) for i in range(n)]
            self.result_table.setHorizontalHeaderLabels(labels)
            self.result_table.setVerticalHeaderLabels(labels)
            
            # Заполняем значениями (только целые числа)
            for i in range(n):
                for j in range(n):
                    if self.shortest_paths[i][j] == float('inf'):
                        item = QTableWidgetItem("∞")
                    else:
                        item = QTableWidgetItem(str(int(self.shortest_paths[i][j])))
                    
                    # Выделяем диагональ другим цветом
                    if i == j:
                        item.setBackground(QColor(220, 255, 220))
                    
                    self.result_table.setItem(i, j, item)
            
            # Разбираем таблицу результатов по размеру ячеек
            self.result_table.resizeColumnsToContents()
            
            QMessageBox.information(self, "Успех", "Кратчайшие пути найдены!")
            
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось найти кратчайшие пути: {str(e)}")
    
    def show_path(self):
        if self.path_matrix is None:
            QMessageBox.warning(self, "Предупреждение", "Сначала найдите кратчайшие пути!")
            return
        
        # Преобразуем номера вершин в индексы (нумерация с 1 → индексы с 0)
        source = self.from_spinbox.value() - 1
        target = self.to_spinbox.value() - 1
        
        path = self.path_finder.get_path(source, target, self.path_matrix)
        
        if source == target:
            self.path_label.setText(f"Путь от {source + 1} до {target + 1}: это одна и та же вершина")
            return
            
        if not path:
            self.path_label.setText(f"Путь от {source + 1} до {target + 1} не существует")
            return
            
        # Преобразуем индексы в номера вершин (добавляем 1)
        path_str = " → ".join(str(v + 1) for v in path)
        
        # Добавляем информацию о длине пути
        path_length = int(self.shortest_paths[source][target])
        self.path_label.setText(f"Путь от {source + 1} до {target + 1}: {path_str} (длина: {path_length})")
        
        # Подсвечиваем в таблице результатов соответствующую ячейку
        self.highlight_cell(source, target)
    
    def highlight_cell(self, row, col):
        # Сбрасываем цвета всех ячеек
        for i in range(self.result_table.rowCount()):
            for j in range(self.result_table.columnCount()):
                item = self.result_table.item(i, j)
                if i == j:
                    item.setBackground(QColor(220, 255, 220))  # Зелёный для диагонали
                else:
                    item.setBackground(QColor(255, 255, 255))  # Белый для остальных
        
        # Выделяем выбранную ячейку
        item = self.result_table.item(row, col)
        item.setBackground(QColor(255, 235, 156))  # Жёлтый для выбранной ячейки
    
    def clear_tables(self):
        self.create_distance_matrix()
        
        # Очищаем таблицу результатов
        self.result_table.setRowCount(0)
        self.result_table.setColumnCount(0)
        
        # Сбрасываем метку пути
        self.path_label.setText("Выберите вершины и нажмите 'Показать путь'")
        
        # Сбрасываем матрицу путей
        self.shortest_paths = None
        self.path_matrix = None
    
    def export_results(self):
        if self.result_table.rowCount() == 0:
            QMessageBox.warning(self, "Предупреждение", "Нет результатов для экспорта!")
            return
        
        try:
            filename, _ = QFileDialog.getSaveFileName(self, "Сохранить результаты", "", "Текстовые файлы (*.txt);;Все файлы (*)")
            
            if filename:
                with open(filename, 'w', encoding='utf-8') as f:
                    # Записываем размерность
                    n = self.result_table.rowCount()
                    f.write(f"Матрица кратчайших путей ({n}x{n}):\n\n")
                    
                    # Записываем заголовок столбцов (нумерация с 1)
                    f.write("   ")
                    for j in range(n):
                        f.write(f"{j + 1:4}")
                    f.write("\n")
                    
                    # Записываем матрицу
                    for i in range(n):
                        f.write(f"{i + 1:2} ")
                        for j in range(n):
                            item_text = self.result_table.item(i, j).text()
                            if item_text == "∞":
                                f.write("  ∞ ")
                            else:
                                f.write(f"{int(float(item_text)):4}")
                        f.write("\n")
                    
                    # Добавляем информацию о путях
                    if self.path_matrix is not None:
                        f.write("\n\nКратчайшие пути между вершинами:\n")
                        for i in range(n):
                            for j in range(n):
                                if i != j and self.shortest_paths[i][j] != float('inf'):
                                    path = self.path_finder.get_path(i, j, self.path_matrix)
                                    path_str = " → ".join(str(v + 1) for v in path)  # Нумеруем с 1
                                    f.write(f"Путь от {i + 1} до {j + 1}: {path_str} (длина: {int(self.shortest_paths[i][j])})\n")
                
                QMessageBox.information(self, "Успех", f"Результаты сохранены в {filename}")
        
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить результаты: {str(e)}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ShortestPathApp()
    ex.show()
    sys.exit(app.exec_())