import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, QVBoxLayout, QLabel, QDialog
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt


class TieForm(QDialog):
    def __init__(self, main_form):
        super().__init__()
        self.main_form = main_form
        self.setWindowTitle("Результат игры")
        self.setGeometry(800, 400 , 500, 250)
        self.setFixedSize(500, 250)
        self.label = QLabel("Ничья", self)
        self.label.setGeometry(50, 50, 400, 50)

        self.button = QPushButton("Продолжить", self)
        self.button.setGeometry(150, 150, 200, 50)
        self.button.clicked.connect(self.returnToMainForm)

    def returnToMainForm(self):
        self.close()
        self.main_form.show()


class WinnerForm(QDialog):
    def __init__(self, main_form, winner):
        super().__init__()
        self.main_form = main_form
        self.setWindowTitle("Результат игры")
        self.setGeometry(800, 400, 500, 250)
        self.setFixedSize(500, 250)

        self.label = QLabel(f"Победил: {winner} игрок", self)
        self.label.setGeometry(50, 50, 400, 50)

        self.button = QPushButton("Продолжить", self)
        self.button.setGeometry(150, 150, 200, 50)
        self.button.clicked.connect(self.returnToMainForm)

    def returnToMainForm(self):
        self.close()
        self.main_form.show()

class GameBoard(QWidget):
    def __init__(self, main_form):
        super().__init__()
        self.main_form = main_form
        self.initUI()


    def initUI(self):
        self.setWindowTitle('Game Board')
        self.setGeometry(500, 32, 600, 600)  # Устанавливаем размер окна 600 на 600
        self.setFixedSize(1000, 1000)
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
                button.setText('')
                button.clicked.connect(lambda _, i=i, j=j: self.buttonClicked(i, j))  # Подключаем обработчик клика
                self.buttonMatrix.append(button)
                self.gridLayout.addWidget(button, i, j)

        self.setLayout(self.gridLayout)  # Добавляем сетку кнопок в саму форму

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

    def openTieForm(self):
        self.close()  # Закрываем текущую форму
        tie_form = TieForm()
        tie_form.display_tie()


    def checkWin(self, row, col):
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
                if self.currentPlayer == 1:
                    self.winner = "Белый"
                if self.currentPlayer == -1:
                    self.winner = "Черный"
                self.openWinnerForm()

        # Проверка на ничью (если все клетки заполнены, но нет победителя)
        if all(all(cell != 0 for cell in row) for row in self.valuesMatrix):
            self.openTieForm()


    def openWinnerForm(self):
        winner_form = WinnerForm(self.main_form, self.winner)
        winner_form.exec_()
        self.close()

    def openTieForm(self):
        tie_form = TieForm(self.main_form)
        tie_form.exec_()
        self.close()

class TutorialForms(QDialog):
    def __init__(self, main_form):
        super().__init__()
        self.main_form = main_form
        self.setWindowTitle("Обучение")
        self.setGeometry(500, 32, 1000, 1000)
        self.setFixedSize(1000, 1000)

        self.imagelable = QLabel(self)
        pixmap = QPixmap('board.png') 
        self.imagelable.setPixmap(pixmap)
        self.imagelable.resize(1000, 1000)

        self.button = QPushButton("Продолжить", self)
        self.button.setGeometry(600, 850, 300, 100)
        self.button.clicked.connect(self.returnToMainForm)

    def returnToMainForm(self):
        self.main_form.show()
        self.close()


class MainForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Main Form')
        self.setGeometry(500, 32, 600, 600)
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
        start_game_button.clicked.connect(self.openGameForm)
        layout.addWidget(start_game_button)

        training_button = QPushButton('Обучение', self)
        training_button.setFixedHeight(250)
        training_button.setFont(QFont("Arial", 36))
        training_button.clicked.connect(self.openTutorialForms)
        layout.addWidget(training_button)

        exit_button = QPushButton('Выход', self)
        exit_button.setFixedHeight(250)
        exit_button.setFont(QFont("Arial", 36))
        exit_button.clicked.connect(self.close)
        layout.addWidget(exit_button)

        self.setLayout(layout)

    def openGameForm(self):
        game_form = GameBoard(self)
        game_form.show()
        self.hide()  # Скрываем текущую форму, чтобы показать форму игры


    def openTutorialForms(self):
        self.hide()
        Tutorial_Forms = TutorialForms(self)
        Tutorial_Forms.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_form = MainForm()
    main_form.show()
    sys.exit(app.exec_())
