import random


class Animal:
    '''Abstract class to present Animal'''
    BORN_NEW = 0
    KILLED = 1
    BROTHER_KILLED = 2

    def __init__(self):
        self.sex = random.sample([True, False], 1)[0]
        self.power = round(random.uniform(10, 20), 1)

    def meet(self, animal):
        '''Meeting'''
        raise NotImplementedError

    def __repr__(self):
        '''
        Representation of string
        :return: str
        '''
        return self.__class__.__name__[0].upper()


class Bear(Animal):
    '''Represents a bear'''

    def meet(self, animal):
        '''
        Represents meetings
        :param animal: Animal
        :return: int
        '''
        if animal == None:
            return Animal.COULD_BE_PLACED
        elif isinstance(animal, Bear):
            if animal.sex != self.sex:
                return Animal.BORN_NEW
            else:
                return Animal.BROTHER_KILLED
        else:
            return Animal.KILLED


class Fish(Animal):
    '''Represents a fish'''

    def meet(self, animal):
        '''
        Represents meetings
        :param animal: Animal
        :return: int
        '''
        if isinstance(animal, Fish):
            if animal.sex != self.sex:
                return Animal.BORN_NEW
            else:
                return Animal.BROTHER_KILLED
        else:
            return Animal.KILLED
