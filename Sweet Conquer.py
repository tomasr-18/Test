# Laboration - Sweet Conquer av Tomas Rydenstam
from math import ceil
from random import randint
from time import sleep
from sys import stdout
import matplotlib.pyplot as plt


class Faction:
    """A class to represent a Faction in the game 'Sweet Conquer'"""

    def __init__(self, name: str, apples: int, oranges: int, bananas: int, strawberries: int):
        # kontrollerar användar-input
        self.check_input(name, str)
        self.check_input(apples, int)
        self.check_input(oranges, int)
        self.check_input(bananas, int)
        self.check_input(strawberries, int)

        self.__name = name
        self.__apples = apples
        self.__oranges = oranges
        self.__bananas = bananas
        self.__strawberries = strawberries

    # Kontrollerar användarinput.
    def check_input(self, input, input_type: type, min=0, max=200):
        '''Konttrollerar användarinput'''
        if input_type == int:  # Kom inte på någon bättre lösning på problemet...
            error_messege = 'int'
        elif input_type == str:
            error_messege = 'str'
        elif input_type == Faction:
            error_messege = 'Faction'
        if not isinstance(input, input_type):
            raise TypeError(
                f'Wrong input format. Correct type(s) is : {error_messege}')

        # Om metoden anropas med en int/float i argumentet finns funktionalitet för att kunna sätta min/max
        if type(input) == int or type(input) == float:
            if input > max or input < min:
                raise ValueError(f'Input should be between {min} and {max}')

    def __repr__(self) -> str:
        return f"{__class__.__name__}(name='{self.name}', apples={self.apples}, oranges={self.oranges}, bananas={self.bananas}, strawberries={self.strawberries})"

    # Metod för att snabbt kunna få en dict med frukt_str:frukt_attribut. Metoden är gjord privat för att användaren inte ska kunna komma åt den
    def __fruits_to_dict(self) -> dict:
        '''Skapar en dict 'fruit':self.fruit'''
        return {'apples': self.__apples, 'oranges': self.__oranges,
                'bananas': self.__bananas, 'strawberries': self.__strawberries}

    # Metoden kommer att användas för att få ut lagersaldot för en frukt med hjälp av en string. Metoden är gjord privat för att användaren inte ska kunna komma åt den
    def __get_fruit_amount(self, fruit: str):
        '''Returnerar self.fruit från en string'''
        self.check_input(fruit, str)
        fruits = self.__fruits_to_dict()
        return fruits[fruit]

    @property
    def name(self) -> str:
        return self.__name

    @property
    def apples(self) -> int:
        return self.__apples

    @property
    def bananas(self) -> int:
        return self.__bananas

    @property
    def oranges(self) -> int:
        return self.__oranges

    @property
    def strawberries(self) -> int:
        return self.__strawberries

    # Metod för att räkna ut en factions totala summa frukt
    def inventory(self) -> int:
        '''Returnerar factionens totala antal frukter'''
        total_amount_of_fruits = self.apples+self.bananas+self.oranges+self.strawberries
        return total_amount_of_fruits

    def status(self):
        '''Skriver ut factionens status beroende på antalet frukter som factionen har'''
        if self.inventory() <= 150:
            print(
                f'This aint nothin but a scratch! {self.name} might be struggling for the moment, but will be back with vengance!')
        elif 150 < self.inventory() <= 500:
            print(
                f'The proud {self.name} is VERY eager to toss some apples! Where are the opponents?!')
        else:
            print(f'{self.name} is GODLIKE! Their position is super dominant!')

    # Metod för att ändra factionens antal frukter.
    def alter_stock_value(self, fruit: str, stock: int, add=None):
        '''Choose one of the following fruits: 'apples', 'oranges', 'bananas', 'strawberries'.\n
        Range for stock is 1-200.\n
        if add is True the stock value will be added to the chosen fruits stock.\n
        if add is False the the stock value will be subtracted from the chosen fruits stock.\n
        if add is None (default) the stock will be set to the inputed stock value'''

        # gör input till små bokstäver och tar bort eventuella mellanslag
        fruit = fruit.lower().strip()
        self.check_input(fruit, str)
        self.check_input(stock, int)

        # skapar en dict med {str_fruit : self.fruit}
        fruits = self.__fruits_to_dict()
        # Kontrollerar så att input är en av de aktuella frukterna
        if fruit not in fruits.keys():
            raise ValueError(
                f"fruit has to be one of these: 'apples', 'oranges', 'bananas', 'strawberries'")
        # Adderar stock
        if add:
            if fruit == 'apples':
                self.__apples += stock
            if fruit == 'oranges':
                self.__oranges += stock
            if fruit == 'bananas':
                self.__bananas += stock
            if fruit == 'strawberries':
                self.__strawberries += stock
        # Subtraherar stock
        elif add is False:
            if fruit == 'apples':
                self.__apples -= stock
            if fruit == 'oranges':
                self.__oranges -= stock
            if fruit == 'bananas':
                self.__bananas -= stock
            if fruit == 'strawberries':
                self.__strawberries -= stock
        # Sätter stock
        else:
            if fruit == 'apples':
                self.__apples = stock
            if fruit == 'oranges':
                self.__oranges = stock
            if fruit == 'bananas':
                self.__bananas = stock
            if fruit == 'strawberries':
                self.__strawberries = stock

    def visualize_resources(self):
        '''Metod för att visualisera factionens antal frukter i en barplot. Färgen på staplarna för varje frukt dikteras av dess lagersaldo'''
        fruits = self.__fruits_to_dict()

        plt.ylabel("Number of fruits")
        plt.ylim(0, 210)
        plt.title(f"{self.name}s amount of fruits in stock")

        for str_fruit, fruit_amount in fruits.items():
            # Ändrar färg på staplarna beroende på lagersaldo
            if fruit_amount >= 100:
                bar_color = 'green'
            elif 50 < fruit_amount <= 100:
                bar_color = 'orange'
            else:
                bar_color = 'red'

            plt.bar(str_fruit, fruit_amount, color=bar_color, width=0.5)
            plt.text(str_fruit, fruit_amount,
                     fruit_amount, ha='center')
        plt.show()

    def organical_growth(self):
        '''Metod för att öka faktionens antal frukter med ett slumptal mellan 1-5'''
        # skapar en dict med {str_fruit : self.fruit}
        fruits = self.__fruits_to_dict()

        stock_increase = [randint(1, 5)
                          for _ in range(len(fruits))]  # Gör en lista med en slumpässig ökning med 1-5 för varje frukt

        for str_fruit, fruit_amount, increase in zip(fruits.keys(), fruits.values(), stock_increase):

            if fruit_amount+increase > 200:  # Kontrollerar så inte varje frukt överstiger 200
                self.alter_stock_value(str_fruit, 200)
            else:
                self.alter_stock_value(str_fruit, increase, add=True)

            # Printar ut hur hur mycket antalet frukter har ökat samt den totala summan av alla frukter
            if fruit_amount < 200:
                print(
                    f'Glorius {self.name} has harvested {increase} {str_fruit}, to a new total of {self.__get_fruit_amount(str_fruit)}!')
            else:
                print(
                    f'Glorius {self.name} is already at maximum capacity of {str_fruit}!')

    def delay_print(self, delay: float, messege: str):
        '''Metod för att skriva ut en bokstav i taget för en string.'''
        print()
        for char in messege:
            print(char, end='')
            stdout.flush()
            sleep(0.2)
        print()

    def __mul__(self, other):
        '''Metod som gör att en Faction attackerar en annan Faction'''
        self.check_input(other, Faction)
        if other.inventory() == 0:
            print(
                f'There is no point to attack {other.name}, they have no fruit!')
        else:
            print()
            print(f'{self.name} is attacking {other.name}!')
            sleep(1.5)
            print()
            # Slumpar om attacken ska lyckas eller inte
            success_or_not = randint(1, 10)

            if success_or_not <= 3:  # 3/10 attacker misslyckas
                print(f'{self.name} attack on {other.name} failed!')

            else:  # 7/10 attacker lyckas
                crit = randint(1, 10)  # avgör om det blir en 'crit' 1/10
                if crit == 10:
                    win_str = f'{self.name} attack on {other.name} were VERY successfull and looted '
                    loot_percent = 0.4  # Överför 40% av förlorarens frukt till motståndaren
                else:
                    loot_percent = 0.2  # Överför 20% av förlorarens frukt till motståndaren
                    win_str = f'{self.name} attack on {other.name} were successfull and looted '

                # Gör en lista med antalet frukter som ska tas från förloraren och läggas till vinnaren
                looted_fruits = [
                    ceil(num_fruits*loot_percent) for num_fruits in other.__fruits_to_dict().values()]  # ??????????????????????????????????????

                # Byter alla nollor till resterande antal frukter för respektive frukt från förlorande faction
                looted_fruits = [num if num > 0 else fruit for fruit, num in zip(
                    other.__fruits_to_dict().values(), looted_fruits)]

                # Lägger till de lootade frukterna till anfallande faction
                for fruit, loot in zip(self.__fruits_to_dict().keys(), looted_fruits):
                    win_str += f'{loot} {fruit} '
                    # Kontrollerar så inte antalet av varje frukt överstiger 200
                    if loot+self.__get_fruit_amount(fruit) > 200:
                        self.alter_stock_value(fruit, 200)

                    else:
                        self.alter_stock_value(fruit, loot, add=True)
                    # Tar bort motsvarande loot från förlorande faction
                    if loot == 0:
                        other.alter_stock_value(fruit, loot)
                    else:
                        other.alter_stock_value(fruit, loot, add=False)

                print(win_str+f'from {other.name}')
                sleep(1.5)

                # Kontrollerar om motståndaren har någon frukt kvar
                opponent_is_dead = True
                for fruit_amount in other.__fruits_to_dict().values():
                    if fruit_amount > 0:
                        opponent_is_dead = False
                if opponent_is_dead:
                    end_messege = f'{other.name} is defeated...'.upper()
                    self.delay_print(0.2, end_messege)


fire_nation = Faction('Fire Nation', 100, 100, 100, 100)
earth_kingdom = Faction('Earth Kingdom', 1, 1, 1, 1)
water_tribe = Faction('Water Tribe', 100, 100, 100, 100)
air_nomads = Faction('Air Nomads', 100, 100, 100, 100)

fire_nation.organical_growth()
fire_nation.alter_stock_value('strawberries', 200)
fire_nation.visualize_resources()
