# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=super-init-not-called
# pylint: disable=unidiomatic-typecount
# pylint: disable=too-many-lines
# pylint: disable=line-too-long


from datetime import datetime
import random
import sys
from tabulate import tabulate

try:
    import pyodide.http
    from js import localStorage  # type: ignore
    HAS_PYODIDE = True
except ImportError:
    HAS_PYODIDE = False
    localStorage = None  # type: ignore


async def main():
    await Welcome()


async def commands():
    print("")
    command = (await input("command: ")).strip()
    print("")

    if not command:
        print("Please enter a command. Type one of: /home, /games, /market, /money, /pv, /exit")
        await commands()
        return

    try:
        if command == "/exit":
            print("\n👋 Thanks for playing! Goodbye.\n")
            return
        elif command == "/home_w":
            await Welcome()
        elif command == "/home":
            await Welcome()
        elif command == "/games_w":
            gamehouse = Gamehouse()
            await gamehouse.welcome()
        elif command == "/games":
            gamehouse = Gamehouse()
            await gamehouse.game()
        elif command == "/market_w":
            market = Market()
            await market.welcome()
        elif command == "/market":
            market = Market()
            await market.option()
        elif command == "/money_w":
            money_market = MoneyMarket()
            await money_market.welcome()
        elif command == "/money":
            money_market = MoneyMarket()
            await money_market.market()
        elif command == "/pv_w":
            profile_viewer = ProfileViewer()
            await profile_viewer.welcome()
        elif command == "/pv":
            profile_viewer = ProfileViewer()
            await profile_viewer.view()
        else:
            print(f"Invalid command: '{command}'")
            print("Valid commands: /home, /games, /market, /money, /pv, /exit")
            await commands()
    except Exception as e:
        print(f"\n\n⚠️ ERROR: {str(e)}")
        print("Returning to main menu...\n")
        await commands()


class MoneyConverter:
    def __init__(self, count=0):
        self.count = count

    async def bitcoin_to_pounds(self):
        if not HAS_PYODIDE:
            raise RuntimeError("This function only works in the browser environment")

        bitcoin = self.count
        response = await pyodide.http.pyfetch("https://api.coindesk.com/v1/bpi/currentprice.json", timeout=10)
        output = await response.json()
        rate_float = output["bpi"]["GBP"]["rate_float"]
        return round(float(bitcoin) * rate_float, 2)

    async def pounds_to_bitcoin(self):
        if not HAS_PYODIDE:
            raise RuntimeError("This function only works in the browser environment")

        if self.count < 1000:
            raise ValueError("minimum spend is £1000")

        pounds = self.count
        response = await pyodide.http.pyfetch("https://api.coindesk.com/v1/bpi/currentprice.json", timeout=10)
        output = await response.json()
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
        self.balance = self.load_balance()

    def load_balance(self):
        try:
            stored = localStorage.getItem("fiat_balance")  # type: ignore
            return float(stored) if stored else 0.0
        except:
            return 0.0

    def save_balance(self):
        localStorage.setItem("fiat_balance", str(self.balance))  # type: ignore

    def deposit(self, amount):
        self.balance += amount
        self.save_balance()

    def withdraw(self, amount):
        if self.balance >= amount:
            self.balance -= amount
            self.save_balance()
            return True
        return False

    def check_balance(self):
        return self.balance

    def add_interest(self):
        self.balance *= 1.10
        self.save_balance()


class CryptoBank:
    def __init__(self):
        self.balance = self.load_balance()

    def load_balance(self):
        try:
            stored = localStorage.getItem("crypto_balance")  # type: ignore
            return float(stored) if stored else 0.0
        except:
            return 0.0

    def save_balance(self):
        localStorage.setItem("crypto_balance", str(self.balance))  # type: ignore

    def deposit(self, amount):
        self.balance += amount
        self.save_balance()

    def withdraw(self, amount):
        if self.balance >= amount:
            self.balance -= amount
            self.save_balance()
            return True
        return False

    def check_balance(self):
        return self.balance


class Wallet:
    def __init__(self):
        self.balance = self.load_balance()

    def load_balance(self):
        try:
            stored = localStorage.getItem("wallet_balance")  # type: ignore
            return float(stored) if stored else 0.0
        except:
            return 0.0

    def save_balance(self):
        localStorage.setItem("wallet_balance", str(self.balance))  # type: ignore

    def deposit(self, amount):
        self.balance += amount
        self.save_balance()

    def withdraw(self, amount):
        if self.balance >= amount:
            self.balance -= amount
            self.save_balance()
            return True
        return False

    def check_balance(self):
        return self.balance


class MoneyMarket:
    def __init__(self):
        pass

    async def welcome(self):
        welcome_message = (await input(
            """Welcome to the money market!

here we can do many things like deposit and withdraw money
there are three ways to store your money:

.your wallet is temporary storage and it has no perks
.the bank stores money that gains interest over time
.the blockchain stores crypto which is volatile
you can loose or gain money but it is risky!

if you want more information type "help"

"""
        )).strip()
        if welcome_message == "help":
            print("")
            print(
                """.you can only directly deposit money into your bank from your wallet by typing "deposit"
.you can only withdraw money from your bank into your wallet by typing "withdraw"
.you can check your balance of both banks and your wallet by typing "balance"
.you can convert your fiat currency to crypto currency by typing "convert"
.bear in mind the minimum spend on converting money is £1000"
"""
            )
            await self.market()
        else:
            await self.market()

    async def market(self):
        try:
            task = (await input("what would you like to do with your money: ")).strip().lower()
            print("")
            if "deposit" in task:
                await self.deposit()
            elif "withdraw" in task:
                await self.withdraw()
            elif "balance" in task:
                self.balance()
                await commands()
            elif "convert" in task:
                await self.convert()
            else:
                raise ValueError("invalid input")
        except Exception as e:
            print(f"\n⚠️ ERROR: {str(e)}")
            print("Returning to money market...\n")
            await self.market()

    async def deposit(self):
        amount = float(await input(
            "how much money would you like to deposit into your bank account: "
        ))
        wallet = Wallet()
        wallet.withdraw(amount)
        fiat_bank = FiatBank()
        fiat_bank.deposit(amount)
        print(f"you have successfully deposited £{amount} into your bank account")
        await commands()

    async def withdraw(self):
        amount = float(await input(
            "how much money would you like to withdraw from your bank account: "
        ))
        fiat_bank = FiatBank()
        fiat_bank.withdraw(amount)
        wallet = Wallet()
        wallet.deposit(amount)
        print(f"you have successfully withdrawn £{amount} from your bank account")
        await commands()

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

    async def convert(self):
        fiat_bank = FiatBank()
        crypto_bank = CryptoBank()
        currency_input = (await input(
            """if you would like to convert pounds to bitcoin, press "P"
    if you would like to convert bitcoin to pounds, press "B"

    input: """
        )).strip().upper()
        if currency_input == "P":
            pounds = float(await input("how much money would you like to convert: "))
            pound_converter = MoneyConverter(pounds)
            bitcoin = await pound_converter.pounds_to_bitcoin()
            fiat_bank.withdraw(pounds)
            crypto_bank.deposit(bitcoin)
            print(
                f"you have successfully converted £{pounds} into bitcoin which has been deposited into the blockchain"
            )
            await commands()
        elif currency_input == "B":
            bitcoin = float(await input("how much crypto would you like to convert: "))
            bitcoin_converter = MoneyConverter(bitcoin)
            pounds = await bitcoin_converter.bitcoin_to_pounds()
            crypto_bank.withdraw(bitcoin)
            fiat_bank.deposit(pounds)
            print(
                f"you have successfully converted ₿{bitcoin} into pounds which has been deposited into your bank"
            )
            await commands()
        else:
            raise ValueError("invalid input")


class Games:
    def __init__(self):
        self.rank = self.load_rank()

    def load_rank(self):
        try:
            stored = localStorage.getItem("rank")  # type: ignore
            return int(stored) if stored else 0
        except:
            return 0

    def save_rank(self):
        localStorage.setItem("rank", str(self.rank))  # type: ignore

    def choice(self, mode, difficulty):
        mode = mode.lower()
        difficulty = difficulty.lower()
        if difficulty == "easy":
            if mode == "addition":
                return self.addition(difficulty)
            elif mode == "subtraction":
                return self.subtraction(difficulty)
            elif mode == "multiplication":
                return self.multiplication(difficulty)
            elif mode == "division":
                return self.division(difficulty)
        elif difficulty == "medium":
            if mode == "addition":
                return self.addition(difficulty)
            elif mode == "subtraction":
                return self.subtraction(difficulty)
            elif mode == "multiplication":
                return self.multiplication(difficulty)
            elif mode == "division":
                return self.division(difficulty)
        elif difficulty == "hard":
            if mode == "addition":
                return self.addition(difficulty)
            elif mode == "subtraction":
                return self.subtraction(difficulty)
            elif mode == "multiplication":
                return self.multiplication(difficulty)
            elif mode == "division":
                return self.division(difficulty)
        else:
            raise ValueError("Invalid difficulty")
        return 0

    def difficulty_grabber(self, difficulty):
        if difficulty == "easy":
            return random.randint(0, 9)
        elif difficulty == "medium":
            return random.randint(10, 99)
        elif difficulty == "hard":
            return random.randint(100, 999)

    def multiplier(self, difficulty, score, mode):
        mode = mode.lower()
        difficulty = difficulty.lower()
        multipliers = {
            "easy": {"addition": 10, "subtraction": 15, "multiplication": 20, "division": 25},
            "medium": {"addition": 50, "subtraction": 75, "multiplication": 100, "division": 125},
            "hard": {"addition": 200, "subtraction": 300, "multiplication": 400, "division": 500},
        }
        base_multiplier = multipliers.get(difficulty, {}).get(mode, 1)
        rank_multiplier = 1 + (self.rank / 1000)
        return int(score * base_multiplier * rank_multiplier)

    async def addition(self, difficulty):
        score = 0
        for _ in range(10):
            num1 = self.difficulty_grabber(difficulty)
            num2 = self.difficulty_grabber(difficulty)
            try:
                answer = int(await input(f"{num1} + {num2} = "))
                print("")
            except ValueError:
                print("Invalid input, try again")
                continue
            if answer == num1 + num2:
                score += 1
            else:
                print(f"incorrect! the answer was {num1 + num2}")
        self.rank += int(score)
        self.save_rank()
        return score

    async def subtraction(self, difficulty):
        score = 0
        for _ in range(10):
            num1 = self.difficulty_grabber(difficulty)
            num2 = self.difficulty_grabber(difficulty)
            if num1 < num2:
                num1, num2 = num2, num1
            try:
                answer = int(await input(f"{num1} - {num2} = "))
                print("")
            except ValueError:
                print("Invalid input, try again")
                continue
            if answer == num1 - num2:
                score += 1
            else:
                print(f"incorrect! the answer was {num1 - num2}")
        self.rank += score
        self.save_rank()
        return score

    async def multiplication(self, difficulty):
        score = 0
        for _ in range(10):
            num1 = self.difficulty_grabber(difficulty)
            num2 = self.difficulty_grabber(difficulty)
            try:
                answer = int(await input(f"{num1} * {num2} = "))
                print("")
            except ValueError:
                print("Invalid input, try again")
                continue
            if answer == num1 * num2:
                score += 1
            else:
                print(f"incorrect! the answer was {num1 * num2}")
        self.rank += score
        self.save_rank()
        return score

    async def division(self, difficulty):
        print(
            'please type your answer correct to 1 decimal place - if it is an integer, add ".0" after'
        )
        score = 0
        for _ in range(10):
            num1 = self.difficulty_grabber(difficulty)
            num2 = self.difficulty_grabber(difficulty)
            if num1 < num2:
                num1, num2 = num2, num1
            try:
                answer = float(await input(f"{num1} / {num2} = "))
                print("")
            except ValueError:
                print("Invalid input, try again")
                continue
            if answer == round((num1 / num2), 1):
                score += 1
            else:
                print(f"incorrect! the answer was {round(num1 / num2, 1)}")
        self.rank += score
        self.save_rank()
        return score


class Gamehouse:
    def __init__(self):
        pass

    async def welcome(self):
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
        await self.game()

    async def game(self):
        mode = await input("what mode would you like to choose: \n")
        difficulty = await input("what difficulty would you like to choose: \n")
        game = Games()
        score = await game.choice(mode, difficulty)
        prize = game.multiplier(difficulty, score, mode)
        print(f"well done, you scored {score} points, winning £{prize}!")
        wallet = Wallet()
        wallet.deposit(prize)
        await commands()


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
                raise ValueError(f"Item '{item}' not found")
            return item
        raise ValueError(f"Item number {item} out of range")

    def get_price(self, item, quantity):
        if type(quantity) != int:
            raise ValueError("Quantity must be an integer.")

        try:
            item_number = int(item)
            if item_number in range(1, len(self.item_names) + 1):
                item = self.item_names[item_number - 1]
        except ValueError:
            if item not in self.item_names:
                raise ValueError(f"Item '{item}' not found")
        return self.item_prices[item] * quantity

    def load_inventory(self):
        try:
            from js import JSON  # type: ignore
            stored = localStorage.getItem("inventory")  # type: ignore
            return JSON.parse(stored) if stored else []
        except:
            return []

    def save_inventory(self, inventory):
        try:
            from js import JSON  # type: ignore
            localStorage.setItem("inventory", JSON.stringify(inventory))  # type: ignore
        except:
            pass

    def sales(self, item, quantity):
        if type(quantity) != int:
            raise ValueError("Quantity must be an integer.")

        try:
            item_number = int(item)
            if item_number in range(1, len(self.item_names) + 1):
                item = self.item_names[item_number - 1]
        except ValueError:
            if item not in self.item_names:
                raise ValueError(f"Item '{item}' not found")

        inventory = self.load_inventory()
        item_found = False
        for i in inventory:
            if i["item"] == item:
                i["quantity"] = str(int(i["quantity"]) + quantity)
                item_found = True
        if not item_found:
            inventory.append({"item": item, "quantity": str(quantity)})
        self.save_inventory(inventory)

    def shop_buy(self, item, quantity, price):
        wallet = Wallet()
        bank = FiatBank()
        wallet_balance = wallet.check_balance()
        if wallet_balance - price < 0:
            bank_balance = bank.check_balance()
            if bank_balance - price < 0:
                raise ValueError("Insufficient funds")
            bank.withdraw(price)
            print(f"you have successfully bought {quantity} {item} for £{price}")
        else:
            wallet.withdraw(price)
            print(f"you have successfully bought {quantity} {item} for £{price}")
        self.sales(item, quantity)

    def shop_sell(self, item, quantity, price):
        wallet = Wallet()
        wallet.deposit(price)
        print(f"you have successfully sold {quantity} {item} for £{price}")
        self.remove_from_inventory(item, quantity)

    def black_market_buy(self, item, quantity, price):
        crypto_bank = CryptoBank()
        crypto_balance = crypto_bank.check_balance()
        if crypto_balance - price < 0:
            raise ValueError("Insufficient crypto funds")
        crypto_bank.withdraw(price)
        print(f"you have successfully bought {quantity} {item} for ₿{price}")
        self.sales(item, quantity)

    def black_market_sell(self, item, quantity, price):
        crypto_bank = CryptoBank()
        crypto_bank.deposit(price)
        print(f"you have successfully sold {quantity} {item} for ₿{price}")
        self.remove_from_inventory(item, quantity)

    def remove_from_inventory(self, item, quantity):
        inventory = self.load_inventory()
        for i in inventory:
            if i["item"] == item:
                i["quantity"] = str(int(i["quantity"]) - quantity)
        self.save_inventory(inventory)

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
            ["item no.5", "lamborghini 🏎", "£250000"],
            ["item no.6", "house 🏠", "£1000000"],
            ["item no.7", "bugatti 🏎️", "£3000000"],
            ["item no.8", "mansion 🏘️", "£5000000"],
            ["item no.9", "yacht 🛳️", "£25000000"],
            ["item no.10", "private jet ✈️", "£100000000"],
        ]
        print(tabulate(items, headers=["item", "name", "price"], tablefmt="pretty"))

    def black_market_info(self):
        print(
            """Welcome to the black market!

below are the items we sell and the prices per item

"""
        )
        items = [
            ["item no.11", "definitely not drugs 🍃", "₿1 - 3"],
            ["item no.12", "definitely not guns 🔫", "₿4 - 7"],
            ["item no.13", "definitely not classified documents 🗎", "₿10 - 25"],
            ["item no.14", "definitely not apache helicopter 🚁", "₿2500 - 5000"],
            ["item no.15", "definately not military jet 🛦", "₿5000 - 10000"],
            ["item no.16", "definately not aircraft carrier 🚢", "₿250000 - 500000"],
            ["item no.17", "definately not the US govenment 🕶️", "₿1000000 - 5000000"],
            ["item no.18", "definately not earth 🌎", "₿25000000 - 30000000"],
            ["item no.19", "definately not a black hole 🕳️", "₿100000000 - 250000000"],
            ["item no.20", "definately not the universe 🌌", "₿1000000000"],
        ]
        print(tabulate(items, headers=["item", "name", "price"], tablefmt="pretty"))


class Market:
    def __init__(self):
        pass

    async def welcome(self):
        print(
            """Welcome to the market!

here we can buy or sell goods!

.you can use either fiat currency or crypto currency
.the money will be taken from your wallet or the blockchain
.if there is not enough money in your wallet you may use your bank
"""
        )
        await self.option()

    async def option(self):
        try:
            markets = Shops()
            choice = (await input("would you like to go to the shop or the black market: \n")).strip().lower()
            print("")

            if choice == "/exit":
                await commands()
                return

            if "shop" in choice:
                markets.shop_info()
                print("")
                buy_or_sell = (await input("would you like to buy or sell items: \n")).strip().lower()
                print("")

                if buy_or_sell == "/exit":
                    await commands()
                    return

                if "buy" in buy_or_sell:
                    item = await input("which item would you like to buy (number or name): \n")
                    print("")

                    if item == "/exit":
                        await commands()
                        return

                    try:
                        quantity = int(await input("how many would you like to buy: \n"))
                        print("")
                    except ValueError:
                        print("Invalid quantity")
                        await self.option()
                        return
                    try:
                        if item.isdigit() and (int(item) < 1 or int(item) > 10):
                            raise ValueError("Item number must be between 1 and 10 for the shop")
                        item_name = markets.get_item_name(item)
                    except Exception as error:
                        print(f"Error: {error}")
                        await self.option()
                        return
                    try:
                        price = markets.get_price(item, quantity)
                    except Exception as error:
                        print(f"Error: {error}")
                        await self.option()
                        return
                    print(f"that will cost £{price}")
                    proceed = (await input("do you want to proceed? (yes/no): \n")).strip().lower()
                    print("")

                    if proceed == "/exit":
                        await commands()
                        return

                    if proceed == "yes":
                        try:
                            markets.shop_buy(item, quantity, price)
                            await commands()
                        except ValueError as e:
                            print(f"Error: {e}")
                            await self.option()
                    else:
                        await self.option()

                elif "sell" in buy_or_sell:
                    item = await input("which item would you like to sell (number or name): \n")
                    print("")

                    if item == "/exit":
                        await commands()
                        return

                    try:
                        quantity = int(await input("how many would you like to sell: \n"))
                        print("")
                    except ValueError:
                        print("Invalid quantity")
                        await self.option()
                        return
                    try:
                        if item.isdigit() and (int(item) < 1 or int(item) > 10):
                            raise ValueError("Item number must be between 1 and 10 for the shop")
                        item_name = markets.get_item_name(item)
                    except Exception as error:
                        print(f"Error: {error}")
                        await self.option()
                        return
                    try:
                        price = markets.get_price(item, quantity)
                    except Exception as error:
                        print(f"Error: {error}")
                        await self.option()
                        return
                    print(f"that will sell for £{price}")
                    proceed = (await input("do you want to proceed? (yes/no): \n")).strip().lower()
                    print("")

                    if proceed == "/exit":
                        await commands()
                        return

                    if proceed == "yes":
                        try:
                            markets.shop_sell(item, quantity, price)
                            await commands()
                        except ValueError as e:
                            print(f"Error: {e}")
                            await self.option()
                    else:
                        await self.option()

                else:
                    raise ValueError("invalid action")

            elif "black market" in choice:
                markets.black_market_info()
                print("")
                buy_or_sell = (await input("would you like to buy or sell items: \n")).strip().lower()
                print("")

                if buy_or_sell == "/exit":
                    await commands()
                    return

                if "buy" in buy_or_sell:
                    item = await input("which item would you like to buy (number or name): \n")
                    print("")

                    if item == "/exit":
                        await commands()
                        return

                    try:
                        quantity = int(await input("how many would you like to buy: \n"))
                        print("")
                    except ValueError:
                        print("Invalid quantity")
                        await self.option()
                        return
                    try:
                        if item.isdigit() and (int(item) < 11 or int(item) > 20):
                            raise ValueError("Item number must be between 11 and 20 for the black market")
                        item_name = markets.get_item_name(item)
                    except Exception as error:
                        print(f"Error: {error}")
                        await self.option()
                        return
                    try:
                        price = markets.get_price(item, quantity)
                    except Exception as error:
                        print(f"Error: {error}")
                        await self.option()
                        return
                    print(f"that will cost ₿{price}")
                    proceed = (await input("do you want to proceed? (yes/no): \n")).strip().lower()
                    print("")

                    if proceed == "/exit":
                        await commands()
                        return

                    if proceed == "yes":
                        try:
                            markets.black_market_buy(item, quantity, price)
                            await commands()
                        except ValueError as e:
                            print(f"Error: {e}")
                            await self.option()
                    else:
                        await self.option()

                elif "sell" in buy_or_sell:
                    item = await input("which item would you like to sell (number or name): \n")
                    print("")

                    if item == "/exit":
                        await commands()
                        return

                    try:
                        quantity = int(await input("how many would you like to sell: \n"))
                        print("")
                    except ValueError:
                        print("Invalid quantity")
                        await self.option()
                        return
                    try:
                        if item.isdigit() and (int(item) < 11 or int(item) > 20):
                            raise ValueError("Item number must be between 11 and 20 for the black market")
                        item_name = markets.get_item_name(item)
                    except Exception as error:
                        print(f"Error: {error}")
                        await self.option()
                        return
                    try:
                        price = markets.get_price(item, quantity)
                    except Exception as error:
                        print(f"Error: {error}")
                        await self.option()
                        return
                    print(f"that will sell for ₿{price}")
                    proceed = (await input("do you want to proceed? (yes/no): \n")).strip().lower()
                    print("")

                    if proceed == "/exit":
                        await commands()
                        return

                    if proceed == "yes":
                        try:
                            markets.black_market_sell(item, quantity, price)
                            await commands()
                        except ValueError as e:
                            print(f"Error: {e}")
                            await self.option()
                    else:
                        await self.option()

                else:
                    raise ValueError("invalid action")

            else:
                raise ValueError("invalid action")
        except Exception as e:
            print(f"\n⚠️ ERROR: {str(e)}")
            print("Returning to market...\n")
            await self.option()


class ProfileViewer:
    def __init__(self):
        pass

    async def welcome(self):
        print(
            """Welcome to the profile viewer where you can view your stats

-what you can view-

.your bank balance
.your inventory
.your rank
"""
        )
        await self.view()

    async def view(self):
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

        print(rank)
        print("=" * len(rank))
        for i in range(max_lines):
            print(f"{inventory_lines[i]:<20s}   {funds_lines[i]:<20s}")
        await commands()

    def rank_getter(self):
        try:
            stored = localStorage.getItem("rank")  # type: ignore
            rank = int(stored) if stored else 0
        except:
            rank = 0

        if rank in range(0, 9):
            return f"=== Level {rank} Civilian ==="
        elif rank in range(10, 24):
            return f"=== Level {rank} Merchant ==="
        elif rank in range(25, 49):
            return f"=== Level {rank} Officer ==="
        elif rank in range(50, 99):
            return f"=== Level {rank} Knight ==="
        elif rank in range(100, 149):
            return f"=== Level {rank} Noble ==="
        elif rank in range(150, 249):
            return f"=== Level {rank} Sir ==="
        elif rank in range(250, 499):
            return f"=== Level {rank} Lord ==="
        elif rank in range(500, 999):
            return f"=== Level {rank} Baron ==="
        elif rank in range(999, 1499):
            return f"=== Level {rank} Duke ==="
        elif rank in range(1500, 2499):
            return f"=== Level {rank} Prince ==="
        elif rank in range(2500, 4999):
            return f"=== Level {rank} King ==="
        elif rank in range(5000, 9999):
            return f"=== Level {rank} Emperor ==="
        elif rank > 10000:
            return f"=== Level {rank} Overlord ==="

    def inventory_getter(self):
        try:
            from js import JSON  # type: ignore
            stored = localStorage.getItem("inventory")  # type: ignore
            inventory = JSON.parse(stored) if stored else []
            table = []
            for row in inventory:
                table.append([row["item"], row["quantity"]])
            return tabulate(table, headers=["item", "quantity"], tablefmt="pretty")
        except:
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


async def Welcome():
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
    await commands()


if __name__ == "__main__":
    pass