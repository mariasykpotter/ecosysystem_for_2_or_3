import random
from abc import abstractmethod

class NONE():
    '''A class for an empty cell representation.'''

    def __init__(self):
        '''
        Initialises a NONE clas
        '''
        self.position = None

    def __repr__(self):
        '''A description of NONE class'''
        return '       '


class Animal:
    '''A class for an Animal representation'''
    river_map = None

    def __init__(self):
        '''
        Initialises an Animal class.
        :return: None
        '''
        self.position = None
        self.sex = random.choice(['male', 'female'])
        self.power = round(random.uniform(1, 10), 2)
        self.age = 0
        self.max_age = None
        self.children_count = None
        self.select = False

    @abstractmethod
    def __repr__(self):
        '''An abstract method'''
        pass

    def death(self):
        '''
        Used when animal dies
        :return: None
        '''
        self.river_map[self.position] = NONE()

    def choice(self, new_pos):
        '''
        Makes a choice whether to fight or make kids.
        :param new_pos: int
        :return: str
        '''
        opponent = self.river_map[new_pos]
        if self.sex == opponent.sex:
            # finish him
            self.fight(new_pos)
        else:
            # "make love, not war"
            children = self.love()
            print('{}{} have {} children with the {}{}'.format(self, self.position, children, opponent,
                                                               opponent.position))

    def love(self):
        '''
        Represents a process of breeding.Counts the number of kids.
        :return: int
        '''
        new_child = 0
        child = type(self)()
        for i in range(self.children_count):
            for j in self.river_map:
                if isinstance(j, NONE):
                    try:
                        self.river_map[j.position] = child
                    except TypeError:
                        continue
                    new_child += 1
                    break
        return new_child

    def set_position(self):
        self.position = self.river_map.index(self)

    def fight(self, new_pos):
        '''
        Makes a conclusion on who defeated whom
        :param new_pos: int
        :return: None
        '''
        opponent = self.river_map[new_pos]
        if self.power > opponent.power:
            opponent.death()
            print('More powerful {}{} killed the {}{}'.format(self, self.position, opponent, opponent.position))
            self.change_position(new_pos)
        elif self.power < opponent.power:
            self.death()
            print('Weak {}{} was killed by the {}{}'.format(self, self.position, opponent, opponent.position))
        else:
            if self.age < opponent.age:
                opponent.death()
                print('Younger {}{} killed the {}{}'.format(self, self.position, opponent, opponent.position))
                self.change_position(new_pos)
            elif self.age > opponent.age:
                self.death()
                print('Older {}{} was killed by the {}{}'.format(self, self.position, opponent, opponent.position))
            else:
                print('{}{} ignored the {}{} because it was the same.'.format(self, self.position, opponent,
                                                                              opponent.position))

    def change_position(self, new_pos):
        '''
        Represents movements of animals
        :param new_pos: int
        :return: None
        '''
        print('{}{} moved to position [{}]'.format(self, self.position, new_pos))
        old_position = self.position
        self.river_map[new_pos] = self
        self.river_map[old_position] = NONE()


class Bear(Animal):
    '''Class for a bear representation'''

    def __init__(self):
        '''
        Initialises a class Bear.
        :return: None
        '''
        super().__init__()
        self.max_age = 10
        self.children_count = 2

    def __repr__(self):
        '''
        String representation of class Bear
        :return: str
        '''
        if self.select:
            return '[' + u'\U0001F43B' + ']' + str(self.power) + self.sex[0] + str(self.age)
        else:
            return u'\U0001F43B' + str(self.power) + self.sex[0] + str(self.age)

    def move(self, new_pos=None):
        '''
        Makes a desicion what do to do.
        :return: None
        '''
        if new_pos == None:
            new_position = self.position + random.choice([1, -1])
        else:
            new_position = new_pos
        if new_position == len(self.river_map):
            new_position = len(self.river_map) - 2
        elif new_position < 0:
            new_position = 0
        opponent = self.river_map[new_position]
        if isinstance(opponent, NONE):
            self.change_position(new_position)
        elif isinstance(opponent, type(self)):
            self.choice(new_position)
        elif isinstance(opponent, Fish):
            opponent.death()
            print('{}{} killed the {}{}'.format(self, self.position, opponent, opponent.position))
            self.change_position(new_position)
        elif isinstance(opponent, Otter):
            opponent.death()
            print('{}{} killed the {}{}'.format(self, self.position, opponent, opponent.position))
            self.change_position(new_position)


class Fish(Animal):
    '''
    This is a class for a Fish representation.
    '''

    def __init__(self):
        '''
        Initialises a Fish
        :return: None
        '''
        super().__init__()
        self.max_age = 5
        self.children_count = 7

    def __repr__(self):
        '''
        Returns a string representation of a Fish
        :return: str
        '''
        if self.select:
            return '[' + u'\U0001F41F' + ']' + str(self.power) + self.sex[0] + str(self.age)
        else:
            return u'\U0001F41F' + str(self.power) + self.sex[0] + str(self.age)

    def move(self, new_pos=None):
        '''
        Makes a decision on what to do
        :return: None
        '''
        if new_pos == None:
            new_position = self.position + random.choice([1, -1])
        else:
            new_position = new_pos
        new_position = self.position + random.choice([1, -1])
        if new_position == len(self.river_map):
            new_position = len(self.river_map) - 2
        elif new_position < 0:
            new_position = 0
        opponent = self.river_map[new_position]
        if isinstance(opponent, NONE):
            self.change_position(new_position)
        elif isinstance(opponent, type(self)):
            self.choice(new_position)
        elif isinstance(opponent, Bear):
            self.death()
            print('{}{} was killed by the {}{}'.format(self, self.position, opponent, opponent.position))
        elif isinstance(opponent, Otter):
            self.death()
            print('{}{} was killed by the {}{}'.format(self, self.position, opponent, opponent.position))


class Otter(Animal):
    '''This is a class for Otter representation'''

    def __init__(self):
        '''
        Initialises a class Otter
        :return: None
        '''
        super().__init__()
        self.max_age = 12
        self.children_count = 3

    def __repr__(self):
        '''
        String representation of Otter
        :return: str
        '''
        if self.select:
            return '[' + u'\U0001F400' + ']' + str(self.power) + self.sex[0] + str(self.age)
        else:
            return u'\U0001F400' + str(self.power) + self.sex[0] + str(self.age)

    def move(self, new_pos=None):
        '''
        Makes a decision on what to do during movements
        :return: None
        '''
        if new_pos == None:
            new_position = self.position + random.choice([1, -1])
        else:
            new_position = new_pos
        new_position = self.position + random.choice([1, -1])
        if new_position == len(self.river_map):
            new_position = len(self.river_map) - 2
        elif new_position < 0:
            new_position = 0
        opponent = self.river_map[new_position]
        if isinstance(opponent, NONE):
            self.change_position(new_position)
        elif isinstance(opponent, type(self)):
            self.choice(new_position)
        elif isinstance(opponent, Fish):
            opponent.death()
            print('{}{} killed the {}{}'.format(self, self.position, opponent, opponent.position))
            self.change_position(new_position)
        elif isinstance(opponent, Bear):
            self.death()
            print('{}{} was killed by the {}{}'.format(self, self.position, opponent, opponent.position))
