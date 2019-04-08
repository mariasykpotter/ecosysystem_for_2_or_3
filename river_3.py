import random
import time

from animal_3 import NONE, Animal, Bear, Fish, Otter


class River:
    '''This is a class for a river representation.'''

    def __init__(self, len=40):
        '''
        Initialises a River class.
        :param len: int
        '''
        self.river = [random.choice([Bear(), Fish(), Otter(), NONE()]) for _ in range(len)]
        self.display_river()
        self.set_position()

    def add_animal(self, dictionary):
        position = random.choice(range(len(self.river)))
        for i in dictionary:
            for j in range(dictionary[i]):
                eval(i.capitalize() + '()').move(position)

    def display_river(self):
        '''
        Prints the river state.
        :return: None
        '''
        for i in self.river:
            print(i, end=' ')
        print('\n')

    def set_position(self):
        '''
        Sets an animal to a certain position.
        :return: None
        '''
        for i in self.river:
            i.position = self.river.index(i)
        Animal.river_map = self.river

    def add_age(self):
        '''
        Counts the age of the animal.
        :return: None
        '''
        for animal in self.river:
            if not isinstance(animal, NONE):
                animal.age += 1
            else:
                continue

    def check_age(self):
        '''
        Checks whether the age is less than max_age, else kills.
        :return:None
        '''
        death_animals = 0
        for animal in self.river:
            if not isinstance(animal, NONE):
                if animal.age > animal.max_age:
                    animal.death()
                    death_animals += 1
            else:
                continue
        if death_animals > 0:
            print('At this year {} old animals have died'.format(death_animals))

    def check_ratio(self):
        '''
        Checks the number of animals of each type.
        :return: dict
        '''
        count = {"Bear": 0, "Fish": 0, "Otter": 0}
        for i in self.river:
            if isinstance(i, Bear):
                count["Bear"] += 1
            elif isinstance(i, Fish):
                count["Fish"] += 1
            elif isinstance(i, Otter):
                count["Otter"] += 1
            else:
                continue
        for i in count:
            if count[i] / sum(count.values()) > 0.6:
                over_limit = int((count[i] / sum(count.values()) - 0.6) * sum(count.values()))
                for j in range(over_limit):
                    for animal in self.river:
                        if isinstance(animal, type(count[i])):
                            print('{}{} over limit death'.format(animal, animal.position))
                            animal.death()
                        else:
                            continue
        return count

    def character(self):
        '''
        Returns a character which represents an animal.
        :return: str
        '''
        character = random.choice(self.river)
        if isinstance(character, NONE):
            return self.character()
        else:
            return character

    def update_river(self):
        '''
        Updates a river
        :return: None
        '''
        self.check_age()
        character = self.character()
        character.select = True
        self.display_river()
        character.move()
        character.select = False
        self.add_age()
        self.set_position()
        self.check_ratio()


if __name__ == '__main__':
    x = River()
    while True:
        try:
            x.update_river()
            time.sleep(0.5)
            print(x.check_ratio())
        except RecursionError:
            print('GAME OVER')
            break
