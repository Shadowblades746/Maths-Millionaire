
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=super-init-not-called
# pylint: disable=unidiomatic-typecheck
# pylint: disable=too-many-lines
# pylint: disable=line-too-long


from datetime import datetime
import random
import csv
import sys
from tabulate import tabulate
import requests



def main():
    Welcome()


def commands():
    print("")
    command = input("command: ")
    print("")
    if command == "/exit":
        sys.exit()
    elif command == "/home_w":
        Welcome()
    elif command == "/home":
        Welcome()
    elif command == "/games_w":
        gamehouse = Gamehouse()
        gamehouse.welcome()
    elif command == "/games":
        gamehouse = Gamehouse()
        gamehouse.game()
    elif command == "/market_w":
        market = Market()
        market.welcome()
    elif command == "/market":
        market = Market()
        market.option()
    elif command == "/money_w":
        money_market = MoneyMarket()
        money_market.welcome()
    elif command == "/money":
        money_market = MoneyMarket()
        money_market.market()
    elif command == "/pv_w":
        profile_viewer = ProfileViewer()
        profile_viewer.welcome()
    elif command == "/pv":
        profile_viewer = ProfileViewer()
        profile_viewer.view()
    else:
        raise ValueError("invalid command")


class MoneyConverter:
    def __init__(self, count=0):
        self.count = count

    def bitcoin_to_pounds(self):
        bitcoin = self.count
        response = requests.get("https://api.coindesk.com/v1/bpi/currentprice.json", timeout=10)
        output = response.json()
        rate_float = output["bpi"]["GBP"]["rate_float"]
        return round(float(bitcoin) * rate_float, 2)

    def pounds_to_bitcoin(self):
        if self.count < 1000:
            raise ValueError("minimum spend is £1000")
        else:
            pounds = self.count
            response = requests.get("https://api.coindesk.com/v1/bpi/currentprice.json", timeout=10)
            output = response.json()
            rate_float = output["bpi"]["GBP"]["rate_float"]
            return round(float(pounds) / rate_float, 2)

    @property
    def count(self):
        return self._count

    @count.setter
    def count(self, count):
        if count < 0 or type(count) is not float:
            raise ValueError("invalid count")
        self._count = count


class FiatBank:
    def __init__(self):
        try:
            with open("fiat_balance.csv", "r", newline='', encoding="utf-8") as file:
                reader = csv.reader(file)
                self.balance = float(next(reader)[0])
                self.last_added_at = datetime.strptime(next(reader)[0], "%Y-%m-%d")
        except FileNotFoundError:
            with open("fiat_balance.csv", "w", newline='', encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow([0])
                writer.writerow([datetime.now().strftime("%Y-%m-%d")])
                self.balance = 0
                self.last_added_at = datetime.now()

    def deposit(self, amount):
        try:
            amount = float(amount)
        except ValueError:
            print("invalid amount")
        if amount > 0:
            self.balance += amount
            self.save_balance()
        else:
            raise ValueError("invalid amount")

    def withdraw(self, amount):
        try:
            amount = float(amount)
        except ValueError:
            print("invalid amount")
        if amount > 0 and self.balance >= amount:
            self.balance -= amount
            self.save_balance()
        else:
            raise ValueError("Insufficient funds.")

    def check_balance(self):
        return f"£{self.balance}"

    def check_int_balance(self):
        return self.balance

    def add_interest(self):
        today = datetime.now().date()
        last_added_date = self.last_added_at.date()
        if today > last_added_date:
            days_since_last_added = (datetime.now() - self.last_added_at).days
            interest_rate = 1.1**days_since_last_added
            balance_before = self.balance
            self.balance *= round(interest_rate, 2)
            self.balance = round(self.balance, 2)
            self.save_balance()
            self.last_added_at = datetime.now()
            interest_added = self.balance - balance_before
            print(f"Interest added: £{interest_added:.2f}")

    def save_balance(self):
        with open("fiat_balance.csv", "w", newline='', encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([self.balance])
            writer.writerow([self.last_added_at.strftime("%Y-%m-%d")])


class CryptoBank(FiatBank):
    def __init__(self):
        try:
            with open("crypto_balance.csv", "r", newline='', encoding="utf-8") as file:
                reader = csv.reader(file)
                self.balance = float(next(reader)[0])
                self.last_added_at = datetime.strptime(next(reader)[0], "%Y-%m-%d")
        except FileNotFoundError:
            with open("crypto_balance.csv", "w", newline='', encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow([0])
                writer.writerow([datetime.now().strftime("%Y-%m-%d")])
                self.balance = 0
                self.last_added_at = datetime.now()

    def check_balance(self):
        return f"₿{self.balance}"

    def save_balance(self):
        with open("crypto_balance.csv", "w", newline='', encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([self.balance])
            writer.writerow([self.last_added_at.strftime("%Y-%m-%d")])


class Wallet(FiatBank):
    def __init__(self):
        try:
            with open("wallet_balance.csv", "r", newline='', encoding="utf-8") as file:
                reader = csv.reader(file)
                self.balance = float(next(reader)[0])
                self.last_added_at = datetime.strptime(next(reader)[0], "%Y-%m-%d")
        except FileNotFoundError:
            with open("wallet_balance.csv", "w", newline='', encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow([0])
                writer.writerow([datetime.now().strftime("%Y-%m-%d")])
                self.balance = 0
                self.last_added_at = datetime.now()

    def save_balance(self):
        with open("wallet_balance.csv", "w", newline='', encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([self.balance])
            writer.writerow([self.last_added_at.strftime("%Y-%m-%d")])


class MoneyMarket:
    def __init__(self):
        pass

    def welcome(self):
        welcome_message = input(
            """Welcome to the money market!

here we can do many things like deposit and withdraw money
there are three ways to store your money:

.your wallet is temporary storage and it has no perks
.the bank stores money that gains interest over time
.the blockchain stores crypto which is volatile
you can loose or gain money but it is risky!

if you want more information type "help"

"""
        )
        if welcome_message == "help":
            print("")
            print(
                """.you can only directly deposit money into your bank from your wallet by typing "deposit"
.you can only withdraw money from your bank into your wallet by typing "withdraw"
.you can check your balance of both banks and your wallet by typing "balance"
.you can convert your fiat currency to crypto currency by typing "convert
.bear in mind the minimum spend on converting money is £1000"
"""
            )
            self.market()
        else:
            self.market()

    def market(self):
        task = input("what would you like to do with your money: ").strip().lower()
        print("")
        if "deposit" in task:
            self.deposit()
        if "withdraw" in task:
            self.withdraw()
        if "balance" in task:
            self.balance()
        if "convert" in task:
            self.convert()
        else:
            raise ValueError("invalid input")

    def deposit(self):
        amount = input(
            "how much money would you like to deposit into your bank account: "
        )
        wallet = Wallet()
        wallet.withdraw(amount)
        fiat_bank = FiatBank()
        fiat_bank.deposit(amount)
        print(f"you have successfully deposited £{amount} into your bank account")
        commands()

    def withdraw(self):
        amount = input(
            "how much money would you like to withdraw from your bank account: "
        )
        fiat_bank = FiatBank()
        fiat_bank.withdraw(amount)
        wallet = Wallet()
        wallet.deposit(amount)
        print(f"you have successfully withdrawn £{amount} from your bank account")
        commands()

    def balance(self):
        wallet = Wallet()
        fiat_bank = FiatBank()
        crypto_bank = CryptoBank()
        wallet_balance = wallet.check_balance()
        fiat_balance = fiat_bank.check_balance()
        crypto_balance = crypto_bank.check_balance()
        balances = [
            ["wallet", wallet_balance],
            ["bank", fiat_balance],
            ["blockchain", crypto_balance],
        ]
        print(tabulate(balances, tablefmt="grid"))
        commands()

    def convert(self):
        fiat_bank = FiatBank()
        crypto_bank = CryptoBank()
        currency_input = input(
            """if you would like to convert pounds to bitcoin, press "P"
if you would like to convert bitcoin to pounds, press "B"

input: """
        )
        if currency_input == "P" or "p":
            pounds = float(input("how much money would you like to convert: "))
            pound_converter = MoneyConverter(pounds)
            bitcoin = pound_converter.pounds_to_bitcoin()
            fiat_bank.withdraw(pounds)
            crypto_bank.deposit(bitcoin)
            print(
                f"you have successfully converted £{pounds} into bitcoin which has been deposited into the blockchain"
            )
            commands()
        elif currency_input == "B" or "b":
            bitcoin = float(input("how much crypto would you like to convert: "))
            bitcoin_converter = MoneyConverter(bitcoin)
            pounds = bitcoin_converter.bitcoin_to_pounds()
            crypto_bank.withdraw(bitcoin)
            fiat_bank.deposit(pounds)
            print(
                f"you have successfully converted ₿{bitcoin} into pounds which has been deposited into your bank"
            )
            commands()
        else:
            raise ValueError("invalid input")


class Games:
    def __init__(self):
        try:
            with open("rank.csv", "r", newline='', encoding="utf-8") as file:
                reader = csv.reader(file)
                self.rank = int(next(reader)[0])
        except FileNotFoundError:
            with open("rank.csv", "w", newline='', encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow([0])
                self.rank = 0

    def choice(self, mode, difficulty):
        if difficulty == "easy":
            if mode == "addition":
                score = self.addition("easy")
            elif mode == "subtraction":
                score = self.subtraction("easy")
            elif mode == "multiplication":
                score = self.multiplication("easy")
            elif mode == "division":
                score = self.division("easy")
        elif difficulty == "medium":
            if mode == "addition":
                score = self.addition("medium")
            elif mode == "subtraction":
                score = self.subtraction("medium")
            elif mode == "multiplication":
                score = self.multiplication("medium")
            elif mode == "division":
                score = self.division("medium")
        elif difficulty == "hard":
            if mode == "addition":
                score = self.addition("hard")
            elif mode == "subtraction":
                score = self.subtraction("hard")
            elif mode == "multiplication":
                score = self.multiplication("hard")
            elif mode == "division":
                score = self.division("hard")
        else:
            raise ValueError
        return score

    def difficulty_grabber(self, difficulty):
        if difficulty == "easy":
            return random.randint(0, 9)
        elif difficulty == "medium":
            return random.randint(10, 99)
        elif difficulty == "hard":
            return random.randint(100, 999)

    def multiplier(self, difficulty, score, mode):
        if difficulty == "easy":
            if mode == "addition":
                return score * 100 * self.rank
            elif mode == "subtraction":
                return score * 200 * self.rank
            elif mode == "multiplication":
                return score * 300 * self.rank
            elif mode == "division":
                return score * 400 * self.rank
        elif difficulty == "medium":
            if mode == "addition":
                return score * 200 * self.rank
            elif mode == "subtraction":
                return score * 400 * self.rank
            elif mode == "multiplication":
                return score * 600 * self.rank
            elif mode == "division":
                return score * 800 * self.rank
        elif difficulty == "hard":
            if mode == "addition":
                return score * 300 * self.rank
            elif mode == "subtraction":
                return score * 600 * self.rank
            elif mode == "multiplication":
                return score * 900 * self.rank
            elif mode == "division":
                return score * 1200 * self.rank

    def save_rank(self):
        with open("rank.csv", "w", newline='', encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([self.rank])

    def addition(self, difficulty):
        score = 0
        for _ in range(10):
            num1 = self.difficulty_grabber(difficulty)
            num2 = self.difficulty_grabber(difficulty)
            answer = int(input(f"{num1} + {num2} = "))
            if answer == num1 + num2:
                score += 1
            else:
                errors = 0
                while answer != num1 + num2:
                    errors += 1
                    print("incorrect, try again")
                    if errors == 3:
                        print(f"the answer was {num1 + num2}")
                        break
                    answer = int(input(f"{num1} + {num2} = "))
                    if answer == num1 + num2:
                        score += 1
        self.rank += int(score)
        self.save_rank()
        return score

    def subtraction(self, difficulty):
        score = 0
        for _ in range(10):
            num1 = self.difficulty_grabber(difficulty)
            num2 = self.difficulty_grabber(difficulty)
            if num1 < num2:
                before1 = num1
                before2 = num2
                num1 = before2
                num2 = before1
            answer = int(input(f"{num1} - {num2} = "))
            if answer == num1 - num2:
                score += 1
            else:
                errors = 0
                while answer != num1 - num2:
                    errors += 1
                    print("incorrect, try again")
                    if errors == 3:
                        print(f"the answer was {num1 - num2}")
                        break
                    answer = int(input(f"{num1} - {num2} = "))
                    if answer == num1 - num2:
                        score += 1
        self.rank += score
        self.save_rank()
        return score

    def multiplication(self, difficulty):
        score = 0
        for _ in range(10):
            num1 = self.difficulty_grabber(difficulty)
            num2 = self.difficulty_grabber(difficulty)
            answer = int(input(f"{num1} * {num2} = "))
            if answer == num1 * num2:
                score += 1
            else:
                errors = 0
                while answer != num1 * num2:
                    errors += 1
                    print("incorrect, try again")
                    if errors == 3:
                        print(f"the answer was {num1 * num2}")
                        break
                    answer = int(input(f"{num1} * {num2} = "))
                    if answer == num1 * num2:
                        score += 1
        self.rank += score
        self.save_rank()
        return score

    def division(self, difficulty):
        print(
            'please type your answer correct to 1 decimal place - if it is an integer, add ".0" after'
        )
        score = 0
        for _ in range(10):
            num1 = self.difficulty_grabber(difficulty)
            num2 = self.difficulty_grabber(difficulty)
            if num1 < num2:
                before1 = num1
                before2 = num2
                num1 = before2
                num2 = before1
            answer = float(input(f"{num1} / {num2} = "))
            if answer == round((num1 / num2), 1):
                score += 1
            else:
                errors = 0
                while answer != round((num1 / num2), 1):
                    errors += 1
                    print("incorrect, try again")
                    if errors == 3:
                        print(f"the answer was {(round(num1 / num2, 1))}")
                        break
                    answer = float(input(f"{num1} / {num2} = "))
                    if answer == round((num1 / num2), 1):
                        score += 1
        self.rank += score
        self.save_rank()
        return score


class Gamehouse:
    def __init__(self):
        pass

    def welcome(self):
        print(
            """Welcome to the gamehouse!

here we can play many maths games with various difficulties
there are four different modes with three difficulties:

-modes-
.addition mode allows you to solve addition problems
.subtraction mode allows you to solve subtraction problems
.multiplication mode allows you to solve multiplication problems
.division mode allows you to solve division problems

-difficulties-
.easy difficuly chooses 2 random single digit numbers
.medium difficulty chooses 2 random double digit numbers
.hard difficulty chooses 2 random triple digit numbers

-prizes-
.you earn money based on the game mode and the difficulty
.the harder the mode and higher the difficulty, the more you win!
.the minimum prize is £0 with the highest being £12,000!
.the prize money will be deposited directly into your wallet
"""
        )
        self.game()

    def game(self):
        mode = input("what mode would you like to choose: ")
        difficulty = input("what difficulty would you like to choose: ")
        game = Games()
        score = game.choice(mode, difficulty)
        prize = game.multiplier(difficulty, score, mode)
        print(f"well done, you scored {score} points, winning £{prize}!")
        wallet = Wallet()
        wallet.deposit(prize)
        commands()


class Shops:
    def __init__(self):
        self.item_prices = {
            "vr headset": 350,
            "ps5": 500,
            "i phone": 1000,
            "gaming pc": 2000,
            "lamborghini": 250000,
            "house": 1000000,
            "bugatti": 3000000,
            "mansion": 5000000,
            "yacht": 25000000,
            "private jet": 100000000,
            "definitely not drugs": random.randint(1, 3),
            "definitely not guns": random.randint(4, 7),
            "definitely not classified documents": random.randint(10, 25),
            "definitely not apache helicopter": random.randint(2500, 5000),
            "definately not military jet": random.randint(5000, 10000),
            "definately not aircraft carrier": random.randint(250000, 500000),
            "definately not the US govenment": random.randint(1000000, 5000000),
            "definately not earth": random.randint(25000000, 30000000),
            "definately not a black hole": random.randint(100000000, 250000000),
            "definately not the universe": 1000000000,
        }
        self.item_names = list(self.item_prices.keys())
        self.item_nice_names = [
            "vr headset 🥽",
            "ps5 🎮",
            "i phone 📱",
            "gaming pc 🖥️",
            "lamborghini 🏎",
            "house 🏠",
            "bugatti 🏎️",
            "mansion 🏘️",
            "yacht 🛳️",
            "private jet ✈️",
            "definitely not drugs 🍃",
            "definitely not guns 🔫",
            "definitely not classified documents 🗎",
            "definitely not apache helicopter 🚁",
            "definately not military jet 🛦",
            "definately not aircraft carrier 🚢",
            "definately not the US govenment 🕶️",
            "definately not earth 🌎",
            "definately not a black hole 🕳️",
            "definately not the universe 🌌",
        ]

    def get_item_name(self, item):
        try:
            item_number = int(item)
            if item_number in range(1, len(self.item_nice_names) + 1):
                return self.item_nice_names[item_number - 1]
        except ValueError:
            if item not in self.item_names:
                print(f"{item} not found in item list.")
                return
            else:
                return item

    def get_price(self, item, quantity):
        if type(quantity) != int:
            raise ValueError("Quantity must be an integer.")

        try:
            item_number = int(item)
            if item_number in range(1, len(self.item_names) + 1):
                item = self.item_names[item_number - 1]
        except ValueError:
            if item not in self.item_names:
                print(f"{item} not found in item list.")
                return
        return self.item_prices[item] * quantity

    def sales(self, item, quantity):
        if type(quantity) != int:
            raise ValueError("Quantity must be an integer.")

        try:
            item_number = int(item)
            if item_number in range(1, len(self.item_names) + 1):
                item = self.item_names[item_number - 1]
        except ValueError:
            if item not in self.item_names:
                print(f"{item} not found in item list.")
                return

        try:
            with open("inventory.csv", "r", newline='', encoding="utf-8") as file:
                reader = csv.DictReader(file)
                inventory = list(reader)
        except FileNotFoundError:
            with open("inventory.csv", "w", newline='', encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=["item", "quantity"])
                writer.writeheader()
                writer.writerow({"item": item, "quantity": quantity})
            return

        item_found = False
        for i in inventory:
            if i["item"] == item:
                i["quantity"] = str(int(i["quantity"]) + quantity)
                item_found = True
                break
        if not item_found:
            inventory.append({"item": item, "quantity": quantity})
        with open("inventory.csv", "w", newline='', encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=["item", "quantity"])
            writer.writeheader()
            for i in inventory:
                writer.writerow(i)

    def shop_buy(self, item, quantity, price):
        wallet = Wallet()
        bank = FiatBank()
        wallet_balance = wallet.check_int_balance()
        if wallet_balance - price < 0:
            bank_balance = wallet.check_int_balance()
            if bank_balance - price < 0:
                raise ValueError(
                    "there were insufficient funds in your wallet and bank acount so we canceled the transaction"
                )
            print(
                "there were insufficient funds in our purse so we took money from your bank acount"
            )
            bank.withdraw(price)
            print(f"you have successfully bought {quantity} {item} for £{price}")
        wallet.withdraw(price)
        print(f"you have successfully bought {quantity} {item} for £{price}")

    def shop_sell(self, item, quantity, price):
        wallet = Wallet()
        wallet.deposit(price)
        print(f"you have successfully sold {quantity} {item} for £{price}")

    def black_market_buy(self, item, quantity, price):
        crypto_bank = CryptoBank()
        crypto_balance = crypto_bank.check_int_balance()
        if crypto_balance - price < 0:
            raise ValueError(
                "there were insufficient funds in the blockchain so we canceled the transaction"
            )
        crypto_bank.withdraw(price)
        print(f"you have successfully bought {quantity} {item} for ₿{price}")

    def black_market_sell(self, item, quantity, price):
        crypto_bank = CryptoBank()
        crypto_bank.deposit(price)
        print(f"you have successfully sold {quantity} {item} for ₿{price}")

    def shop_info(self):
        print(
            """Welcome to the shop!

below are the items we sell and the prices per item
"""
        )
        items = [
            ["item no.1", "vr headset 🥽", "£350"],
            ["item no.2", "ps5 🎮", "£500"],
            ["item no.3", "i phone 📱", "£1000"],
            ["item no.4", "gaming pc 🖥️", "£2000"],
            ["item no.5", "lamborghini 🏎", "£250,000"],
            ["item no.6", "house 🏠", "£1,000,000"],
            ["item no.7", "bugatti 🏎️", "£3,000,000"],
            ["item no.8", "mansion 🏘️", "£5,000,000"],
            ["item no.9", "yacht 🛳️", "£25,000,000"],
            ["item no.10", "private jet ✈️", "£100,000,000"],
        ]
        print(tabulate(items, headers=["item", "price"], tablefmt="pretty"))

    def black_market_info(self):
        print(
            """Welcome to the black market!

below are the items we sell and the prices per item

"""
        )
        items = [
            ["item no.11 - definitely not drugs 🍃", "₿1 - 3"],
            ["item no.13 - definitely not guns 🔫", "₿4 - 7"],
            ["item no.12 - definitely not classified documents 🗎", "₿10 - 25"],
            ["item no.14 - definitely not apache helicopter 🚁", "₿2500 - 5000"],
            ["item no.15 - definately not military jet 🛦", "₿5000 - 10,000"],
            ["item no.16 - definately not aircraft carrier 🚢", "₿250,000 - 500,000"],
            [
                "item no.17 - definately not the US govenment 🕶️",
                "₿1,000,000 - 5,000,000",
            ],
            ["item no.18 - definately not earth 🌎", "₿25,000,000 - 30,000,000"],
            [
                "item no.19 - definately not a black hole 🕳️",
                "₿100,000,000 - 250,000,000",
            ],
            ["item no.20 - definately not the universe 🌌", "₿1,000,000,000"],
        ]
        print(tabulate(items, headers=["item", "price"], tablefmt="pretty"))


class Market:
    def __init__(self):
        pass

    def welcome(self):
        print(
            """Welcome to the market!

here we can buy or sell goods!

.you can use either fiat currency or crypto currency
.the money will be taken from your wallet or the blockchain
.if there is not enough money in your wallet you may use your bank
"""
        )
        self.option()

    def option(self):
        markets = Shops()
        choice = input("would you like to go to the shop or the black market: ")

        if "shop" in choice:
            markets.shop_info()
            print("")
            buy_or_sell = input("would you like to buy or sell items: ")
            if "buy" in buy_or_sell:
                item = input(
                    "type in the item or item number of the item you would like to buy: "
                )
                try:
                    quantity = int(
                        input("how much of this item would you like to buy: ")
                    )
                except Exception as error:
                    raise ValueError from error
                item_name = markets.get_item_name(item)
                try:
                    price = markets.get_price(item, quantity)
                except Exception as error:
                    raise ValueError from error
                print(f"that will cost £{price}")
                proceed = input(
                    'if you would like to proceed with the purchase, type "yes" otherwise type "no": '
                )
                if proceed == "yes":
                    markets.shop_buy(item_name, quantity, price)
                    markets.sales(item, quantity)
                    commands()
                else:
                    print("purchase canceled")
                    commands()

            elif "sell" in buy_or_sell:
                item = input(
                    "type in the item or item number of the item you would like to sell: "
                )
                try:
                    quantity = int(
                        input("how much of this item would you like to sell: ")
                    )
                except Exception as error:
                    raise ValueError from error
                item_name = markets.get_item_name(item)
                try:
                    price = markets.get_price(item, quantity)
                except Exception as error:
                    raise ValueError from error
                price = markets.get_price(item, quantity)
                print(f"that will sell for £{price}")
                proceed = input(
                    'if you would like to proceed with the sale, type "yes" otherwise type "no": '
                )
                if proceed == "yes":
                    markets.sales(item, -quantity)
                    markets.shop_sell(item_name, quantity, price)
                    commands()
                else:
                    print("purchase canceled")
                    commands()

            else:
                raise ValueError("invalid action")

        elif "black market" in choice:
            markets.black_market_info()
            buy_or_sell = input("would you like to buy or sell items: ")
            if "buy" in buy_or_sell:
                item = input(
                    "type in the item or item number of the item you would like to buy: "
                )
                try:
                    quantity = int(
                        input("how much of this item would you like to buy: ")
                    )
                except Exception as error:
                    raise ValueError from error
                item_name = markets.get_item_name(item)
                try:
                    price = markets.get_price(item, quantity)
                except Exception as error:
                    raise ValueError from error
                print(f"that will cost ₿{price}")
                proceed = input(
                    'if you would like to proceed with the purchase, type "yes" otherwise type "no": '
                )
                if proceed == "yes":
                    markets.black_market_buy(item_name, quantity, price)
                    markets.sales(item, quantity)
                    commands()
                else:
                    print("purchase canceled")
                    commands()

            elif "sell" in buy_or_sell:
                item = input(
                    "type in the item or item number of the item you would like to sell: "
                )
                try:
                    quantity = int(
                        input("how much of this item would you like to sell: ")
                    )
                except Exception as error:
                    raise ValueError from error
                item_name = markets.get_item_name(item)
                try:
                    price = markets.get_price(item, quantity)
                except Exception as error:
                    raise ValueError from error
                price = markets.get_price(item, quantity)
                print(f"that will sell for ₿{price}")
                proceed = input(
                    'if you would like to proceed with the sale, type "yes" otherwise type "no": '
                )
                if proceed == "yes":
                    markets.sales(item, -quantity)
                    markets.black_market_sell(item_name, quantity, price)
                    commands()
                else:
                    print("purchase canceled")
                    commands()

            else:
                raise ValueError("invalid action")

        else:
            raise ValueError("invalid action")


class ProfileViewer:
    def __init__(self):
        pass

    def welcome(self):
        print(
            """Welcome to the profile viewer where you can view your stats

-what you can view-

.your bank balance
.your inventory
.your rank
"""
        )
        self.view()

    def view(self):
        rank = self.rank_getter()
        inventory_string = self.inventory_getter()
        funds_string = self.banks_getter()

        inventory_lines = inventory_string.split("\n")
        funds_lines = funds_string.split("\n")
        max_lines = max(len(inventory_lines), len(funds_lines))
        if len(inventory_lines) < max_lines:
            inventory_lines += [""] * (max_lines - len(inventory_lines))
        if len(funds_lines) < max_lines:
            funds_lines += [""] * (max_lines - len(funds_lines))
        string = f"{rank}"
        print(f"\033[1m{rank}\033[0m")
        print("=" * len(string))
        for i in range(max_lines):
            print(f"{inventory_lines[i]:<20s}   {funds_lines[i]:<20s}")
        commands()

    def rank_getter(self):
        try:
            with open("rank.csv", "r", newline='', encoding="utf-8") as file:
                reader = csv.reader(file)
                rank = int(next(reader)[0])
        except FileNotFoundError:
            with open("rank.csv", "w", newline='', encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow([0])
                rank = 0
        if rank in range(0, 9):
            return f"-Level {rank} Civilian-"
        elif rank in range(10, 24):
            return f"-Level {rank} Merchant-"
        elif rank in range(25, 49):
            return f"-Level {rank} Officer-"
        elif rank in range(50, 99):
            return f"-Level {rank} Knight-"
        elif rank in range(100, 149):
            return f"-Level {rank} Noble-"
        elif rank in range(150, 249):
            return f"-Level {rank} Sir-"
        elif rank in range(250, 499):
            return f"-Level {rank} Lord-"
        elif rank in range(500, 999):
            return f"-Level {rank} Baron-"
        elif rank in range(999, 1499):
            return f"-Level {rank} Duke-"
        elif rank in range(1500, 2499):
            return f"-Level {rank} Prince-"
        elif rank in range(2500, 4999):
            return f"-Level {rank} King-"
        elif rank in range(5000, 9999):
            return f"-Level {rank} Emperor-"
        elif rank > 10000:
            return f"-Level {rank} Overlord-"

    def inventory_getter(self):
        try:
            with open("inventory.csv", "r", newline='', encoding="utf-8") as file:
                reader = csv.DictReader(file)
                inventory = list(reader)
            table = []
            for row in inventory:
                table.append([row["item"], row["quantity"]])
            return tabulate(table, headers=["item", "quantity"], tablefmt="pretty")
        except FileNotFoundError:
            items = [["N/A", "N/A"]]
            return tabulate(items, headers=["item", "quantity"], tablefmt="pretty")

    def banks_getter(self):
        wallet = Wallet()
        fiat_bank = FiatBank()
        crypto_bank = CryptoBank()
        wallet_balance = wallet.check_balance()
        fiat_balance = fiat_bank.check_balance()
        crypto_balance = crypto_bank.check_balance()
        balances = [
            ["wallet", wallet_balance],
            ["bank", fiat_balance],
            ["blockchain", crypto_balance],
        ]
        return tabulate(balances, headers=["funds", "balance"], tablefmt="pretty")


class Welcome:
    def __init__(self):
        print(
            """Welcome to my project!

-brief description-

.In this program, there is one simple goal: to get as rich as possible!

-commands-

.commands allow you to choose where you want to go
.you can go to the welcome screen by suffixing _w
.below are all the commands that you need:
.ps they start with a forward slash

./home - this brings you back home
./games - this brings you to the games
./market - this brings you to the market
./money - this brings you to the money market
./pv - this brings you to the profile viewer

-you have three funds namely-

.your wallet: which should be seen as temporary storage as it has no perks
.your bank: which gains interest at a rate of 10% per day! so ensure to use it
.the blockchain: which stores bitcoin so if you like the idea of crypto then go use it

-games-

.there are maths games which allow you to earn money by solving simple math problems
.there are three main difficulties so ensure to choose wislely based on your skill level
.you can try your luck at either addition, subtraction, multiplication or division

-rank system-

.you get a higher rank based on how good you do in the games which depends on your score
.your score is added to your rank level every time you complete one of the games
.when playing games, the higher your rank level, the more money you earn per game

-market-

.there is a market which allows you to buy and sell items to add to your collection
.you can even go to the black market which allows you to buy and sell special items

-money market-
here you can do things like:

.deposit money from your wallet to your bank account
.withdraw money from your bank account
.convert money from your bank to the blockchain
.check all of your balances

-profile viewer-

.you can check all of your stats here
.your bank balance
.your inventory
.your rank
"""
        )
        fiat_bank = FiatBank()
        fiat_bank.add_interest()
        commands()


def good_morning(good):
    if good == "good":
        return "good morning"


def good_afternoon(good):
    if good == "good":
        return "good afternoon"


def good_evening(good):
    if good == "good":
        return "good evening"


if __name__ == "__main__":
    main()
