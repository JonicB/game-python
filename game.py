''' Игра "Сапер" '''

import PySimpleGUI as sg
import random
from dataclasses import dataclass

@dataclass
class Table:
    '''Класс содержания поля.
    table - массив с наполнением клеток поля (наличие мины или количество мин рядом)
    layout - описание окна игры'''

    table = []
    layout = []

    def MinesPlaces(self, n, m, cmines):
        '''Возвращает список координат, в которых находятся мины.
        На вход подаются:
        n - длина поля.
        m - ширина поля.
        cmines - количество мин.'''

        mines = []
        for i in range(cmines):
            a = random.randint(0,n * m -1)
            a = (a % n, a // n)
            while a in mines:
                a = random.randint(0,n*m - 1)
                a = (a % n, a // n)
            mines.append(a)
        return mines


    def TableCells(self, n, m, mines):
        '''Возвращает массив с наполнением клеток поля.
        На вход подаются:
        n - длина поля.
        m - ширина поля.
        mines - массив координат, в которых находятся мины.'''

        arr = [[i for i in range(n)] for j in range(m)]
        for i in range(n):
            for j in range(m):
                if (i, j) in mines:
                    arr[j][i] = '*'
                    continue
                count = 0
                if (i - 1, j - 1) in mines:
                    count += 1
                if (i - 1, j) in mines:
                    count += 1
                if (i - 1, j + 1) in mines:                        
                    count += 1
                if (i, j + 1) in mines:
                    count += 1
                if (i + 1, j + 1) in mines:
                    count += 1
                if (i + 1, j) in mines:
                    count += 1
                if (i + 1, j - 1) in mines:
                    count += 1
                if (i, j - 1) in mines:
                    count += 1
                arr[j][i] = count
        return arr


    def __init__(self, n , m, cmines):
        '''Конструктор значений переменных класса.
        На вход подаются:
        n - длина поля
        m - ширина поля
        cmines - количество мин на поле'''

        self.layout = [[sg.Button('', key = j * n + i, size = (2,1),button_color = [None,'blue']) for i in range(n)] for j in range(m)]
        self.layout.append([sg.Button('New game',key = 'restart', button_color = ['white','blue']),
                          sg.Button('Options',button_color = ['white','blue']),
                          sg.Button('Mark mines', button_color = ['white','blue'],key = 'mark'),
                          sg.Text('Mines: {}'.format(cmines),key = 'count',font = ('Arial',10))])
        self.layout.append([sg.Text('You lost!', font = ('Arial', 15), visible = False, key = 'lost')])
        self.layout.append([sg.Text('You win!', font = ('Arial', 15), visible = False, key = 'win')])

        mines = self.MinesPlaces(n, m, cmines)

        self.table = self.TableCells(n, m, mines)



def Minesweeper(optionsWindow, n , m, mines):
    '''Описание и работа окна игры.
    На вход подаются:
    optionWindow - окно, которое надо закрыть.
    n - длина поля.
    m - ширина поля.
    mines - количество мин на поле'''

    optionsWindow.close()

    layout = Table(n, m, mines)

    window = sg.Window('Minesweeper',layout.layout)
    win = True
    count = 0
    uses = []
    flags = []
    mark = False

    while True:
        event, value = window.read()
        if event == None:
            break
        if (event in [i for i in range(n*m)]) and win:
            if mark:
                if event not in flags:
                    window[event].Update(button_color = [None,'green'])
                    flags.append(event)
                else:
                    window[event].Update(button_color = [None,'blue'])
                    flags.remove(event)
                window['count'].Update('Mines: {}'.format(mines - len(flags)))
            else:
                if event not in flags:
                    if layout.table[event // n][event % n] == '*':
                        window['lost'].Update(visible = True)
                        window[event].Update(button_color = [None,'red'])
                        win = False
                    else:
                        if event not in uses:
                            window[event].Update(layout.table[event // n][event % n], button_color = ['black','white'])
                            count += 1
                            uses.append(event)
                            if count == n * m - mines:
                                window['win'].Update(visible = True)
                                win = False
        if event == 'Options':
            Option(window)
            break
        if event == 'restart':
            Minesweeper(window, n, m, mines)
            break
        if (event == 'mark') and win:
            mark = not mark
            if mark:
                window['mark'].Update('Return')
            else:
                window['mark'].Update('Mark mines')
        
    window.close()


def Option(window):
    '''Работа и описание окна настроек.
    На вход подается:
    window - окно, которое надо закрыть'''

    window.close()

    optionsLayout = [[sg.Text('Choose the size of the field')],
                [sg.Radio('10 * 10','Radio1', key = 'many1',default = True)],
                [sg.Radio('16 * 16','Radio1',key = 'many3')],
                [sg.Radio('30 * 16','Radio1',key = 'many2')],
                [sg.Button('Ok',button_color = ['white', 'blue'], key = 'ok')]]
    optionsWindow = sg.Window('Options',optionsLayout)

    while True:
        event, value = optionsWindow.read()
        if event == None:
            break
        if event == 'ok':
            if optionsWindow['many1'].Get():
                n = 10
                m = 10
                mines = 10
            elif optionsWindow['many2'].Get():
                n = 30
                m = 16
                mines = 99
            elif optionsWindow['many3'].Get():
                n = 16
                m = 16
                mines = 40
            Minesweeper(optionsWindow, n , m , mines)
            break
    optionsWindow.close()

window = sg.Window('',[])
Option(window)
