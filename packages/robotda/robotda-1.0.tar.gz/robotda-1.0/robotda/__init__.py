__author__ = 'DavidYdin'
__version__ = '1.0'
__email__ = 'David.2280@yandex.ru'
class robot :
    def __init__(self, vertical, horizontal, robot_symbol, no_robot_symbol, fol_symdol):
        self.vertical = vertical
        self.horizontal = horizontal
        self.robot_symbol = robot_symbol
        self.no_robot_symbol = no_robot_symbol
        self.fol_symdol = fol_symdol
        a = []
        for i in range(vertical):
            b = f"{no_robot_symbol} "*horizontal
            b = b[:-1]
            a += [b.split(' ')]
        self.matrix = a
        self.matrix[0][0] = robot_symbol
    def show_robot(self):
        for i in self.matrix:
            print(*i)
    def moving(self, direction, fol=False):
        a = 0
        b = 0
        a_1 = 0
        b_1 = 0
        a_2 = 0
        b_2 = 0
        for x in self.matrix:
            a_1 += 1
            for y in x:
                b_1 += 1
                if y == self.robot_symbol:
                    a = a_1-1
                    b = b_1-1
            b_1 = 0
        a_2 = a + 0
        b_2 = b + 0
        self.matrix[a][b] = self.no_robot_symbol
        #up down right left
        if direction == 'up':
            a -= 1
        elif direction == 'down':
            a += 1
        elif direction == 'right':
            b += 1
        elif direction == 'left':
            b -= 1
        else:
            print('Such a stand is not suitable for moving sides')
        if fol == True:
            self.matrix[a_2][b_2] = self.fol_symdol
        self.matrix[a][b] = self.robot_symbol