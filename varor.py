import datetime as dt


class Varor:
    '''
    Class för att katagolisera varor med dess namn, pris, märke, best-före-datum och lagersaldo. Classen sparar även försäljningshistorik.
    '''

    def __init__(self, name: str, price: float, brand: str):

        self.check_input(name, str)
        self.check_input(price, int, float)
        self.check_input(brand, str)

        self.__name = name
        self.__price = price
        self.__brand = brand
        self.__stock = []  # Kategoriserar varorna på inköpspris och bäst-före-datum
        self.__item_sold = 0  # antal varar sålda
        self.__purchase_price = 0  # Genomsnittligt inköpspris
        self.__profit_margin = 0  # Vinstmarginal ex: 0,5 är 50% vinst
        self.__vinst = 0  # Gjord vinst på varan
        self.__stock_value = 0  # Marknadsvärdet på lagret
        self.__sales_price = []  # Spar hur många varor som är sålda till vilket pris

    @property
    def name(self):
        return self.__name

    @property
    def price(self):
        return self.__price

    @property
    def brand(self):
        return self.__brand

    @property
    def item_sold(self):
        return self.__item_sold

    @property
    def purchase_price(self):
        return self.__purchase_price

    @property
    def profit_margin(self):
        return self.__profit_margin

    @property
    def vinst(self):
        return self.__vinst

    @property
    def stock_value(self):
        return self.__stock_value

    @property
    def sales_price(self):
        return self.__sales_price

    def check_input(self, input, *args):
        if not isinstance(input, (args)):
            raise TypeError(
                f"Wrong input format. Your input '{input}' should be {args}")

    def show_stock(self):
        for element in self.__stock:
            print(
                f"Number of units: {element['number_of_units']}, Purchase price per unit: {element['price_per_unit']}, Best before: {element['best_before']}, Days in stock: {element['days_in_stock']}")

        print(f'Total units: {self.calculate_numbers_in_stock()}')

    def change_price(self, new_price: float) -> None:
        self.check_input(new_price, int, float)
        self.__price = new_price
        self.calculate_stock_value()
        self.calculate_purchase_price()

    def __repr__(self) -> str:
        return f'Namn: {self.name}\nMärke: {self.brand}\nPris: {self.price}'

    def calculate_purchase_price(self) -> None:
        stock_value = sum([element['price_per_unit']*element['number_of_units']
                           for element in self.__stock])
        units_in_stock = sum([element['number_of_units']
                             for element in self.__stock])

        # Beräknar och assignar det genomsnittliga inköpspriset
        self.__purchase_price = stock_value/units_in_stock
        # Beräknar och assignar vinstmarginalen
        self.__profit_margin = self.__price/self.__purchase_price

    def calculate_stock_value(self) -> None:
        self.__stock_value = self.calculate_numbers_in_stock()*self.__price

    def calculate_numbers_in_stock(self):
        return sum([element['number_of_units'] for element in self.__stock])

    def discount(self, discount: float) -> None:
        '''Input discount in %'''
        self.check_input(discount, float, int)
        self.price -= self.price*discount/100

    def sales(self) -> print:
        print(f'Pris:{self.price} kr\nInköpspris: {self.purchase_price} kr\nSålda enheter: {self.item_sold} st\nVinstmarginal: {(self.profit_margin*100):.2f} %\nVinst: {self.vinst:.0f} kr')

    def sales_history(self) -> print:
        for item in self.__sales_price:
            print(item)

    def before_black_friday(self, price_increase: float) -> None:
        '''input price increase in %'''
        self.check_input(price_increase, float, str)
        self.__price += self.__price*(price_increase/100)

    def sell(self, num=1) -> None:
        '''input number of sold items'''
        self.check_input(num, int)

        if num > self.calculate_numbers_in_stock():
            print(
                f'Not enough in stock, current stock is : {self.calculate_numbers_in_stock()}')
        else:
            self.remove_from_stock(num)
            self.__item_sold += num
            self.__vinst += num*self.__price*self.__profit_margin
            self.add_sales_price(num)
            self.calculate_purchase_price()

    def add_sales_price(self, items: int) -> None:
        self.check_input(items, int)

        added_item = False
        for item in self.__sales_price:
            if item['price'] == self.__price:
                item['number_of_sales'] += items
                added_item = True
                break
        if not added_item:
            self.__sales_price.append(
                {'price': self.__price, 'number_of_sales': items})

    def validate_date(self, str: str) -> dt.date:
        try:
            date = dt.date.fromisoformat(str)
        except TypeError:
            raise TypeError(
                "Input format not correct. It should be: 'YYYY-MM-DD'")
        if date < dt.date.today():
            raise ValueError('You can not add items that has already expired.')
        else:
            return date

    def add_to_stock(self, number_of_units: int, price_per_unit: float, best_before: str) -> None:
        '''input best_before as: (YYYY-MM-DD)'''
        self.check_input(number_of_units, int)
        self.check_input(price_per_unit, int, float)
        self.check_input(best_before, str)

        # Kontrollerar så att användares input är i rätt format
        best_before = self.validate_date(best_before)

        added_to_stock = False
        for item in self.__stock:
            # Om varan har samma inköpspris och bäst-före-datum läggs de på befintlig dict, annars skapas en ny
            if price_per_unit == item['price_per_unit'] and best_before == item['best_before']:
                item['number_of_units'] += number_of_units
                added_to_stock = True
                break
        if not added_to_stock:
            self.__stock.append({'number_of_units': number_of_units,
                                 'price_per_unit': price_per_unit, 'best_before': best_before, 'days_in_stock': self.calculate_days_in_stock(dt.date.today())})
        self.__stock = sorted(
            self.__stock, key=lambda d: d['best_before'])  # Sorterar listan efter bäst-före-datum
        self.calculate_purchase_price()  # Uppdaterar inköpspriset
        self.calculate_stock_value()  # Updaterar stock value

    def remove_from_stock(self, num: int) -> None:
        self.check_input(num, int)
        self.__stock = sorted(
            self.__stock, key=lambda d: d['best_before'])  # Sorterar listan efter bäst-före-datum

        # Tar bort lagersaldo från varor med tidigast best-före-datum
        for index, element in enumerate(self.__stock):
            if num >= element['number_of_units'] and num > 0:
                temp = element['number_of_units']
                self.__stock[index]['number_of_units'] = 0
                num -= temp
            elif num > 0:
                temp = element['number_of_units']
                self.__stock[index]['number_of_units'] -= num
                num -= temp
            else:
                break

        # Tar bort alla dicts med 0 items
        self.__stock = [x for x in self.__stock if x['number_of_units'] > 0]
        if len(self.__stock) > 0:
            self.calculate_purchase_price()  # Uppdaterar inköpspriset om lagersaldot inte är 0
        self.calculate_stock_value()  # Updaterar stock value

    def expiers(self, key=''):
        if key == 'all':
            for item in self.__stock:
                print(
                    f"Expires date is in {(item['best_before']-dt.date.today()).days} days")
        else:
            print(
                f"Next expire date is in {(self.__stock[0]['best_before']-dt.date.today()).days} days")

    def calculate_days_in_stock(self, import_date: dt.date):
        return (dt.date.today()-import_date).days
