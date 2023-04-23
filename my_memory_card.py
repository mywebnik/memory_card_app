#создай приложение для запоминания информации

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QWidget, QHBoxLayout, QVBoxLayout, QGroupBox, QRadioButton, QPushButton, QLabel, QButtonGroup)
from random import shuffle, randint

#Создадим класс для описания вех вопросов с ответами как объектов
class Question():
    def __init__(self, question, right_answer, wrong1, wrong2, wrong3):
        self.question = question
        self.right_answer = right_answer
        self.wrong1 = wrong1
        self.wrong2 = wrong2
        self.wrong3 = wrong3

#Создадим структуру хранения вопросов — список, добавим в него экземпляры
questions_list = [] 
questions_list.append(Question('Государственный язык Бразилии', 'Португальский', 'Английский', 'Испанский', 'Бразильский'))
questions_list.append(Question('Какого цвета нет на флаге России?', 'Зелёный', 'Красный', 'Белый', 'Синий'))
questions_list.append(Question('Национальная хижина якутов', 'Ураса', 'Юрта', 'Иглу', 'Хата'))

#Cоздание объект-приложения, окна приложения
app = QApplication([])

window = QWidget()
window.setWindowTitle('Memo Card')

'''Введём два накопителя для всех вопросов (total) и верных ответов (score). 
Для обращения к ним из разных функций сделаем их свойствами window:
Обнулим накопители при запуске программы:'''
window.score = 0
window.total = 0

#Cоздание виджет-вопроса и виджета-кнопки «Ответить».
lb_Question = QLabel('В каком году была основана Москва?')
btn_OK = QPushButton('Ответить')

#Создание набора переключателей с вариантами ответов
RadioGroupBox = QGroupBox("Варианты ответов")
rbtn_1 = QRadioButton('1147')
rbtn_2 = QRadioButton('1242')
rbtn_3 = QRadioButton('1861')
rbtn_4 = QRadioButton('1943')

layout_ans1 = QHBoxLayout()   
layout_ans2 = QVBoxLayout() 
layout_ans3 = QVBoxLayout()
layout_ans2.addWidget(rbtn_1) 
layout_ans2.addWidget(rbtn_2)
layout_ans3.addWidget(rbtn_3) 
layout_ans3.addWidget(rbtn_4)

layout_ans1.addLayout(layout_ans2)
layout_ans1.addLayout(layout_ans3)

RadioGroupBox.setLayout(layout_ans1)

#Все переключатели объединяем в специальную группу. Теперь может быть выбран только один из них.
RadioGroup = QButtonGroup() 
RadioGroup.addButton(rbtn_1)
RadioGroup.addButton(rbtn_2)
RadioGroup.addButton(rbtn_3)
RadioGroup.addButton(rbtn_4)

#Создание интерфейс формы правильного ответа
AnsGroupBox = QGroupBox("Результат теста")
lb_Result = QLabel('прав ты или нет?') # здесь размещается надпись "правильно" или "неправильно"
lb_Correct = QLabel('ответ будет тут!') # здесь будет написан текст правильного ответа

layout_res = QVBoxLayout()
layout_res.addWidget(lb_Result, alignment=(Qt.AlignLeft | Qt.AlignTop))
layout_res.addWidget(lb_Correct, alignment=Qt.AlignHCenter, stretch=2)
AnsGroupBox.setLayout(layout_res)

#Расположиv вопрос, группу переключателей и кнопку по лэйаутам
layout_line1 = QHBoxLayout() # вопрос
layout_line2 = QHBoxLayout() # варианты ответов или результат теста
layout_line3 = QHBoxLayout() # кнопка "Ответить"

layout_line1.addWidget(lb_Question, alignment=(Qt.AlignHCenter | Qt.AlignVCenter))
layout_line2.addWidget(RadioGroupBox)
layout_line2.addWidget(AnsGroupBox)

layout_line3.addStretch(1)
layout_line3.addWidget(btn_OK, stretch=2) # кнопка должна быть большой
layout_line3.addStretch(1)

layout_card = QVBoxLayout()

layout_card.addLayout(layout_line1, stretch=2)
layout_card.addLayout(layout_line2, stretch=8)
layout_card.addStretch(1)
layout_card.addLayout(layout_line3, stretch=1)
layout_card.addStretch(1)
layout_card.setSpacing(5) # пробелы между содержимым

window.setLayout(layout_card)

#Функция show_result(), обрабатывающую нажатие на кнопку «Ответить»
def show_result():
    ''' показать панель ответов '''
    RadioGroupBox.hide()
    AnsGroupBox.show()
    btn_OK.setText('Следующий вопрос')

#Функция-обработчик show_question(), обрабатывающую нажатие на «Следующий вопрос»
def show_question():
    ''' показать панель вопросов '''
    RadioGroupBox.show()
    AnsGroupBox.hide()
    btn_OK.setText('Ответить')
    RadioGroup.setExclusive(False) # сняли ограничения, чтобы можно было сбросить выбор радиокнопки
    rbtn_1.setChecked(False)
    rbtn_2.setChecked(False)
    rbtn_3.setChecked(False)
    rbtn_4.setChecked(False)
    RadioGroup.setExclusive(True) # вернули ограничения, теперь только одна радиокнопка может быть выбрана

#Создаем список кнопок
answers = [rbtn_1, rbtn_2, rbtn_3, rbtn_4]

#Функция перемешивает список кнопок answers, заменяет тексты виджетов на нужные в  форме вопросов и ответов, и показывает форму вопросов
def ask(q):
    shuffle(answers)
    answers[0].setText(q.right_answer)
    answers[1].setText(q.wrong1)
    answers[2].setText(q.wrong2)
    answers[3].setText(q.wrong3)
    lb_Question.setText(q.question)
    lb_Correct.setText(q.right_answer)
    show_question() 

#Функция check_answer() должна проверять правильность данного ответа при нажатии на «Ответить» – если выбран переключатель answers[0], то вызывать функцию show_correct с аргументом «Правильно», в другом случае с аргументом «Неверно»
def check_answer():
    ''' если выбран какой-то вариант ответа, то надо проверить и показать панель ответов'''
    if answers[0].isChecked():
        show_correct('Правильно!')
        window.score += 1 #увеличиваем счетчик правильных ответов на 1
        #После проверки ответа пользователя отобразим изменённую статистику и рейтинг.
        print('Статистика\n-Всего вопросов: ', window.total, '\n-Правильных ответов: ', window.score)
        print('Рейтинг: ', (window.score/window.total*100), '%')

    else:
        if answers[1].isChecked() or answers[2].isChecked() or answers[3].isChecked():
            show_correct('Неверно!')
            ##После проверки ответа пользователя отобразим изменённую статистику и рейтинг.
            print('Статистика\n-Всего вопросов: ', window.total, '\n-Правильных ответов: ', window.score)
            print('Рейтинг: ', (window.score/window.total*100), '%')


#Функция show_correct() должна – устанавливать текст-результат в форме ответа,  отображать форму ответа.
def show_correct(res):
    ''' показать результат - установим переданный текст в надпись "результат" и покажем нужную панель '''
    lb_Result.setText(res)
    show_result()

#функция next_question() для последовательного перехода между вопросами
def next_question():
    ''' задает следующий вопрос из списка '''
    window.total += 1 #увеличиваем счетчик вопросов на 1
    #напечатаем текущую статистику вопросов и правильных ответов
    print('Статистика\n-Всего вопросов: ', window.total, '\n-Правильных ответов: ', window.score)
    # этой функции нужна переменная, в которой будет указываться номер текущего вопроса
    # эту переменную можно сделать глобальной, либо же сделать свойством "глобального объекта" (app или window)
    # мы заведем локальную переменную и присвоим ей случайно сгенерированное число
    cur_question = randint(0, len(questions_list) - 1) # переходим к следующему вопросу
    q = questions_list[cur_question] # взяли вопрос из списка по индексу
    ask(q) # спросили

#функцию-посредник click_ok() для переключения между формами вопроса и ответа и функциями next_question() и check_answer()
def click_OK():
    if btn_OK.text() == 'Ответить':
        check_answer() # проверка ответа
    else:
        next_question() # следующий вопрос

next_question() #сразу увеличиваем счетчик до 0 и отображаем первый вопрос с ответами из списка вопросов

# Обработка события при нажатии на кнопку
btn_OK.clicked.connect(click_OK)

AnsGroupBox.hide()
window.show()

app.exec()