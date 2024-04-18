import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, QVBoxLayout, QLabel

from PyQt5.QtCore import QTimer, QTime


class MemoryGame(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Memory Game')
        self.setGeometry(100, 100, 400, 600)

        self.timer = QTimer()
        self.timer.timeout.connect(self.updateTimer)

        self.timeLabel = QLabel()
        self.timerValue = QTime(0, 10, 0)  # Инициализируем таймер на 10 минут
        self.updateTimerLabel()

        self.board = QGridLayout()
        self.initializeBoard()

        layout = QVBoxLayout()
        layout.addLayout(self.board)
        layout.addWidget(self.timeLabel)

        game_board = GameBoard()  # Создаем игровое поле
        layout.addWidget(game_board)

        self.setLayout(layout)

        self.show()
        self.timer.start(1000)  # Таймер обновляется каждую секунду

    def initializeBoard(self):
        # Создайте игровое поле с кнопками (клетками)
        pass  # Добавьте логику инициализации игрового поля здесь

    def updateTimer(self):
        self.timerValue = self.timerValue.addSecs(-1)
        self.updateTimerLabel()

        if self.timerValue.minute() == 0 and self.timerValue.second() == 0:
            self.timer.stop()
            self.timeLabel.setText("Время вышло! Игра окончена.")
            self.close()  # Закрываем окно после окончания времени

    def updateTimerLabel(self):
        self.timeLabel.setText(f"Оставшееся время: {self.timerValue.toString('mm:ss')}")


class GameBoard(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Game Board')
        self.setGeometry(0, 0, 600, 600)  # Устанавливаем размер окна 1920 на 1080

        size = 15  # Размер игрового поля (вы можете поменять на другое значение)

        self.gridLayout = QGridLayout()  # Создаем сетку для размещения кнопок
        self.gridLayout.setSpacing(0)  # Устанавливаем отсутствие отступов между кнопками

        self.buttonMatrix = []  # Матрица для хранения кнопок
        self.valuesMatrix = [[0 for _ in range(size)] for _ in range(size)]  # Матрица для хранения значений кнопок

        for i in range(size):
            for j in range(size):
                button = QPushButton(f'({i}, {j})', self)
                button.setFixedSize(40, 40)  # Устанавливаем фиксированный размер кнопки, делаем ее квадратной
                button.clicked.connect(lambda _, i=i, j=j: self.buttonClicked(i, j))  # Подключаем обработчик клика
                self.buttonMatrix.append(button)
                self.gridLayout.addWidget(button, i, j)

        center_widget = QWidget()
        center_layout = QVBoxLayout()
        spacer_item = QWidget()  # Пространственный элемент для центрирования
        spacer_item.setSizePolicy(1, 1)
        center_layout.addWidget(spacer_item)
        center_layout.addLayout(self.gridLayout)
        center_widget.setLayout(center_layout)

        main_layout = QVBoxLayout(self)
        main_layout.addStretch(1)
        main_layout.addWidget(center_widget)
        main_layout.addStretch(1)

        self.setLayout(main_layout)

        center = size // 2
        index = size * center + center
        self.buttonMatrix[index].setText('1')  # Устанавливаем первое значение 1 в центре
        self.valuesMatrix[center][center] = 1

        self.currentPlayer = -1  # Начинаем с -1 (второй игрок)

    def buttonClicked(self, i, j):
        if self.valuesMatrix[i][j] == 0:  # Проверяем, что клетка пустая
            self.valuesMatrix[i][j] = self.currentPlayer
            index = 15 * i + j
            self.buttonMatrix[index].setText(str(self.currentPlayer))

            self.currentPlayer *= -1  # Смена игрока


if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = MemoryGame()
    sys.exit(app.exec_())
