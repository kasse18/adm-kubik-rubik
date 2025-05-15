colorsPair = [[1, 2], [3, 6], [4, 5]]
colorsThree = [[6, 5, 1], [6, 2, 5], [6, 4, 2], [6, 1, 4],
               [5, 1, 6], [2, 5, 6], [4, 2, 6], [1, 4, 6],
               [1, 6, 5], [5, 6, 2], [2, 6, 4], [4, 6, 1],
               [3, 4, 1], [3, 4, 2], [3, 5, 2], [3, 1, 5],
               [4, 1, 3], [4, 2, 3], [5, 2, 3], [1, 5, 3],
               [1, 3, 4], [2, 3, 4], [2, 3, 5], [5, 3, 1]]


class Shape3:
    def __init__(self, x, y, z):
        self.colors = [0, 0, 0]
        self.pos = [x, y, z]

    def send(self, color, pos):
        self.colors[pos] = color

    def check(self):
        # if self.colors not in colorsThree:
        #     return False
        # return True
        return self.colors in colorsThree

    def complete(self):
        if self.colors.count(0) == 1:
            j = self.colors.index(0)
            colors = self.colors
            for i in range(1, 7):
                colors[j] = i
                if colors in colorsThree:
                    return i
        return 0


class Shape2:
    def __init__(self, x, y):
        self.colors = [0, 0]
        self.pos = [x, y]

    def send(self, color, pos):
        self.colors[pos] = color

    def check(self):
        # if self.colors in colorsPair:
        #     return False
        # if self.colors[0] == self.colors[1]:
        #     return False
        # return True
        return self.colors not in colorsPair and self.colors[0] != self.colors[1]
