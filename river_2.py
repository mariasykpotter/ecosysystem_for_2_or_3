import random
from animal_2 import Animal, Fish, Bear
from config import ANIMAL_FILL, BEAR_PERCENTAGE, BORN_NEW, KILLED, BROTHER_KILLED


class River:
    '''This class represents river'''
    THE_END = 0

    def __init__(self, n=20):
        '''
        Initialises River
        :param n: int
        '''
        self.__cells = [None] * n
        self.potential_positions = {}
        self.tuple = ()

    def random_generation(self, n=20):
        '''
        Creates reandom_generation of ecosystem.
        :param n: int
        :return: list
        '''
        # Creation of animals
        num_of_animals = int(n * ANIMAL_FILL)
        positions = random.sample(range(n), num_of_animals)
        for position in positions:
            rand_const = random.random()
            if rand_const < BEAR_PERCENTAGE:
                self.__cells[position] = Bear()
            else:
                self.__cells[position] = Fish()
        return self.__cells

    def find_indexes(self):
        '''
        Finds indexes where the 2 parents are.
        :return: list
        '''
        lst = []
        for el in self.potential_positions.keys():
            if len(self.potential_positions[el]) == 4:
                if self.potential_positions[el][0].meet(self.potential_positions[el][2]) != 1:
                    lst.append(self.potential_positions[el][1])
                    lst.append(self.potential_positions[el][3])
        return lst

    def add_animals(self, lst_animals):
        '''
        Adds animals to an ecosystem
        :param lst_animals: list of tuples
        :return: list
        '''
        if lst_animals:
            for tup in lst_animals:
                if self.tuple[0].get(tup[1]):
                    self.tuple[0][tup[1]].append(tup[0])
                    self.tuple[0][tup[1]].append(tup[1])
                else:
                    self.tuple[0][tup[1]] = list(tup)
            self.potential_positions = self.tuple[0]
        # print("in add_animals", self.tuple)
        # print("in add_animals", self.potential_positions)
        return self.potential_positions

    def create_dict(self, lst=[]):
        '''
        Creates a dictionary where a key is a position to which goes an animal and value is an animal and a position on which was an animal.
        :return: dict
        '''
        self.potential_positions = {}
        for i, animal in enumerate(self.__cells):
            if animal is None:
                continue
            new_positions = filter(lambda x: 0 <= x < len(self.__cells), [i - 1, i, i + 1])
            new_position = random.sample(list(new_positions), 1)[0]
            self.potential_positions[new_position] = self.potential_positions.get(new_position, []) + ([animal, i])
        if lst:
            self.add_animals(lst)
            print("Adding {}".format(lst))
        return self.potential_positions

    def give_a_birth(self, lst=[]):
        lst_new_born = []
        new_cells = [None] * len(self.__cells)
        # print("new cells before a birth",new_cells)
        self.potential_positions = self.create_dict(lst)
        # print("pot in give_a_birth", self.potential_positions)
        # print("potential_positions",self.potential_positions)
        for position in list(self.potential_positions.keys()):
            if len(self.potential_positions[position]) == 4:
                status = self.potential_positions[position][0].meet(self.potential_positions[position][2])
                if status == BORN_NEW:
                    print("Congratulations!!!One more baby {0}".format(self.potential_positions[position][0].__str__()))
                    lst_indexes2 = []
                    for j in range(len(new_cells)):
                        if j not in self.find_indexes() and j not in self.potential_positions.keys() and j not in lst_new_born:
                            lst_indexes2.append(j)
                    # print("lst_indexes:", lst_indexes2)
                    if lst_indexes2 == []:
                        "Fish survive anyway."
                    else:
                        rand_index = random.choice(lst_indexes2)
                        lst_new_born.append(rand_index)
                        print("The index where baby was born:", rand_index)
                        # Filling new_cells in case a baby was born
                        new_cells[rand_index] = self.potential_positions[position][0]
                        # print("changed new_cells",new_cells)
                        lst_parents_positions = [self.potential_positions[position][0],
                                                 self.potential_positions[position][1],
                                                 self.potential_positions[position][2],
                                                 self.potential_positions[position][3]]
                        # print("a", a)
                        if self.potential_positions.get(lst_parents_positions[1]) and lst_parents_positions[
                            1] != position:
                            self.potential_positions[lst_parents_positions[1]].append(lst_parents_positions[0])
                            self.potential_positions[lst_parents_positions[1]].append(lst_parents_positions[1])
                        else:
                            self.potential_positions[lst_parents_positions[1]] = [lst_parents_positions[0],
                                                                                  lst_parents_positions[1]]
                        if self.potential_positions.get(lst_parents_positions[3]) and lst_parents_positions[
                            3] != position:
                            self.potential_positions[lst_parents_positions[3]].append(lst_parents_positions[2])
                            self.potential_positions[lst_parents_positions[3]].append(lst_parents_positions[3])
                        else:
                            self.potential_positions[lst_parents_positions[3]] = [lst_parents_positions[2],
                                                                                  lst_parents_positions[3]]
                    # print("new_cells",new_cells)
        return self.potential_positions, new_cells

    def killed(self, lst=[]):
        self.potential_positions, new_cells = self.give_a_birth(lst)
        self.tuple = self.potential_positions, new_cells
        # print("pot in killed", self.potential_positions)
        lst_keys = list(self.potential_positions.keys())
        # print("new_cells after a birth", new_cells)
        for position in lst_keys:
            if len(self.potential_positions[position]) == 4:
                status = self.potential_positions[position][0].meet(self.potential_positions[position][2])
                if status == KILLED:
                    print("OOOPS, Bear ate a fish")
                    if isinstance(self.potential_positions[position][0], Bear):
                        # The case when a bear kills a fish
                        new_cells[position] = self.potential_positions[position][0]
                    else:
                        new_cells[position] = self.potential_positions[position][2]
        return new_cells

    def brother_killed(self, lst=[]):
        new_cells = self.killed(lst)
        # print("new_cells after killed",new_cells)
        self.potential_positions = self.tuple[0]
        # print("pot in brother_killed",self.potential_positions)
        lst_keys = list(self.potential_positions.keys())
        for position in lst_keys:
            if len(self.potential_positions[position]) == 4:
                status = self.potential_positions[position][0].meet(self.potential_positions[position][2])
                if status == BROTHER_KILLED:
                    # Filling new cells in case one animal kills another of the same type
                    print("One {0} kills another {1}".format(self.potential_positions[position][0].__str__(),
                                                             self.potential_positions[position][2].__str__()))
                    if self.potential_positions[position][0].power > self.potential_positions[position][2].power:
                        new_cells[position] = self.potential_positions[position][0]
                    else:
                        new_cells[position] = self.potential_positions[position][2]
        # print("new_cells after brother killed",new_cells)
        return new_cells

    def random_update(self, lst=[]):
        '''
        Shows the ecosystem state after everybody went somewhere
        :param: lst of tuples of animals which an animal wants to add to an ecosystem
        :return: the ecosystem after everybody went on 1 position
        '''
        self.brother_killed(lst)
        self.potential_positions = self.tuple[0]
        # print("on the start", self.potential_positions)
        new_cells = self.tuple[1]
        # print("positions:",self.potential_positions)
        # print("new_cells at the beginning",new_cells)
        lst_keys = list(self.potential_positions.keys())
        for position in lst_keys:
            if len(self.potential_positions[position]) == 2:
                # The case when animals do not meet
                new_cells[position] = self.potential_positions[position][0]
            elif len(self.potential_positions[position]) == 6:
                print("WOW!Three animals are fighting.Only one will survive")
                # In case 3 animals go into the same cell, if there is at least one bear, then the bear stays in the position
                # If no bear is there, then a fish is in the cell.
                # In the fight between 3 only one can stay alive!!!1
                b_count = 0
                lst_power = []
                for el in self.potential_positions[position]:
                    if isinstance(el, Bear):
                        b_count += 1
                        new_cells[position] = el
                    if b_count == 0:
                        if isinstance(el, Fish):
                            lst_power.append(el.power)
                            if el.power == max(lst_power):
                                new_cells[position] = el
            # print("new_cells", new_cells)
        self.__cells = new_cells
        return self.__cells

    def __str__(self):
        '''
        Description of class River
        :return: str
        '''
        animals = ""
        for i in range(len(self.__cells)):
            if self.__cells[i]:
                if self.__cells[i].sex == True:
                    sex = "F"
                else:
                    sex = "M"
                if isinstance(self.__cells[i], Bear):
                    animals += "🐻" + str(self.__cells[i].power) + sex
                elif isinstance(self.__cells[i], Fish):
                    animals += "🐟" + str(self.__cells[i].power) + sex
            else:
                animals += "      "
        return animals

    def count_animals(self):
        '''
        Counts animals
        :return: str
        '''
        b_counter = 0
        f_counter = 0
        for i in range(len(self.__cells)):
            if isinstance(self.__cells[i], Bear):
                b_counter += 1
            elif isinstance(self.__cells[i], Fish):
                f_counter += 1
        text = "There is {0} bears, {1} fish".format(b_counter, f_counter)
        return text


if __name__ == "__main__":
    r = River()
    print(r.random_generation())
    print(r)
    print(r.count_animals())
    f_count = 5
    while f_count != 0:
        f_count = 0
        lst = r.random_update()
        for el in lst:
            if isinstance(el, Fish):
                f_count += 1
        print(r)
        print(r.count_animals())
    r.random_update([(Fish(), 4)])
    print(r)
    print(r.count_animals())
    f_count = 5
    while f_count != 0:
        f_count = 0
        lst = r.random_update()
        for el in lst:
            if isinstance(el, Fish):
                f_count += 1
        print(r)
        print(r.count_animals())
