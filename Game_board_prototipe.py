import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, QVBoxLayout, QLabel, QDialog
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import QTimer, QTime, Qt

class MainForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Main Form')
        self.setGeometry(100, 100, 300, 200)
        self.setFixedSize(1000, 1000)
        layout = QVBoxLayout()

        gomoku_label = QLabel('Gomoku', self)
        gomoku_label.setFont(QFont("Arial", 36, QFont.Bold))
        gomoku_label.setAlignment(Qt.AlignCenter)
        gomoku_label.setStyleSheet("border: none")  # убираем контур
        layout.addWidget(gomoku_label)

        start_game_button = QPushButton('Начало игры', self)
        start_game_button.setFixedHeight(250)
        start_game_button.setFont(QFont("Arial", 36))
        start_game_button.clicked.connect(self.openNewGameForm)
        layout.addWidget(start_game_button)

        training_button = QPushButton('Обучение', self)
        training_button.setFixedHeight(250)
        training_button.setFont(QFont("Arial", 36))
        training_button.clicked.connect(self.openTrainingForm)
        layout.addWidget(training_button)

        exit_button = QPushButton('Выход', self)
        exit_button.setFixedHeight(250)
        exit_button.setFont(QFont("Arial", 36))
        exit_button.clicked.connect(self.close)
        layout.addWidget(exit_button)

        self.setLayout(layout)

    def openNewGameForm(self):
        self.hide()  # Закрываем текущую форму
        main_form = GameBoard()
        main_form.show()

    def openTrainingForm(self):
        self.hide()
        training_form = TrainingForm()
        training_form.show()


class NewGameForm(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Memory Game')
        self.setGeometry(100, 100, 600, 600)
        self.setFixedSize(1000, 1000)
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateTimer)
        self.timeLabel = QLabel()
        self.timerValue = QTime(0, 10, 0)  # Инициализируем таймер на 10 минут
        self.updateTimerLabel()
        self.board = QGridLayout()
        layout = QVBoxLayout()
        layout.addLayout(self.board)
        layout.addWidget(self.timeLabel)
        game_board = GameBoard()  # Создаем игровое поле
        layout.addWidget(game_board)
        self.setLayout(layout)
        self.show()
        self.timer.start(1000)  # Таймер обновляется каждую секунду

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

    def buttonClicked(self, i, j):
        self.buttonClickedSignal.emit(i, j)
        if self.valuesMatrix[i][j] == 0:  # Проверяем, что клетка пустая
            self.valuesMatrix[i][j] = self.currentPlayer
            index = 15 * i + j
            if self.currentPlayer == 1:
                self.buttonMatrix[index].setStyleSheet(
                    '''QPushButton {border: none; margin: 0px; padding: 0px; border-image: url(board_white.png);}''')
            else:
                self.buttonMatrix[index].setStyleSheet(
                    '''QPushButton {border: none; margin: 0px; padding: 0px; border-image: url(board_black.png);}''')

            if self.checkWin(i, j):
                self.timeLabel.setText(f"Победитель: Игрок {self.currentPlayer}")  # Вывод победителя
                self.timer.stop()  # Останавливаем таймер после победы
                self.disableButtons()  # Деактивируем кнопки после победы
            else:
                self.currentPlayer *= -1  # Смена игрока, если нет победителя

    def initUI(self):
        self.setWindowTitle('Game Board')
        self.setGeometry(0, 0, 600, 600)  # Устанавливаем размер окна 600 на 600

        self.gridLayout = QGridLayout()  # Создаем сетку для размещения кнопок
        self.gridLayout.setSpacing(0)  # Устанавливаем отсутствие отступов между кнопками

        self.buttonMatrix = []  # Матрица для хранения кнопок
        self.valuesMatrix = [[0 for _ in range(15)] for _ in range(15)]  # Матрица для хранения значений кнопок

        for i in range(15):
            for j in range(15):
                button = QPushButton(f'({i}, {j})', self)
                button.setFixedSize(64, 64)  # Устанавливаем фиксированный размер кнопки, делаем ее квадратной
                button.collate = QPushButton("Collate")
                button.setStyleSheet(
                    '''QPushButton {border: none; margin: 0px; padding: 0px; border-image: url(board.png);}''')
                button.clicked.connect(lambda _, i=i, j=j: self.buttonClicked(i, j))  # Подключаем обработчик клика
                self.buttonMatrix.append(button)
                self.gridLayout.addWidget(button, i, j)
                self.setLayout(self.gridLayout)
                button.setText('')

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

        self.currentPlayer = 1  # Начинаем с -1 (второй игрок)

    def buttonClicked(self, i, j):
        if self.valuesMatrix[i][j] == 0:  # Проверяем, что клетка пустая
            self.valuesMatrix[i][j] = self.currentPlayer
            index = 15 * i + j
            if self.currentPlayer == 1:
                self.buttonMatrix[index].setStyleSheet(
                    '''QPushButton {border: none; margin: 0px; padding: 0px; border-image: url(board_white.png);}''')
                self.buttonMatrix[index].setText('')
            else:
                self.buttonMatrix[index].setStyleSheet(
                    '''QPushButton {border: none; margin: 0px; padding: 0px; border-image: url(board_black.png);}''')
                self.buttonMatrix[index].setText('')

            if self.checkWin(i, j):
                self.disableButtons()  # Деактивируем кнопки после победы

            self.currentPlayer *= -1  # Смена игрока

    def checkWin(self, row, col):
        # Проверка на заполнение всего поля
        if all(all(cell != 0 for cell in row) for row in self.valuesMatrix):
            return None  # Ничья

        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

        for d in directions:
            count = 1
            for i in range(1, 5):
                r = row + i * d[0]
                c = col + i * d[1]
                if 0 <= r < 15 and 0 <= c < 15 and self.valuesMatrix[r][c] == self.currentPlayer:
                    count += 1
                else:
                    break

            for i in range(1, 5):
                r = row - i * d[0]
                c = col - i * d[1]
                if 0 <= r < 15 and 0 <= c < 15 and self.valuesMatrix[r][c] == self.currentPlayer:
                    count += 1
                else:
                    break

            if count >= 5:
                winner = "Белые" if self.currentPlayer == 1 else "Черные"
                return winner

        return None

class WinnerForm:
    def __init__(self, winner):
        self.winner = winner

    def display_winner(self):
        print(f"Победитель: {self.winner}")

# Класс для формы с выводом ничьей
class TieForm:
    def __init__(self):
        pass

    def display_tie(self):
        print("Ничья")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_form = MainForm()
    main_form.show()
    sys.exit(app.exec_())
