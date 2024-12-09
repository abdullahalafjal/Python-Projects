from abc import ABC, abstractmethod

# Custom Exception for Invalid Input
class InvalidInputException(Exception):
    pass

# Abstract Base Class 
class Account(ABC):
    def __init__(self, account_number, account_balance):
        if account_number <= 0:
            raise InvalidInputException("Account number must be positive.")
        if account_balance < 0:
            raise InvalidInputException("Account balance cannot be negative.")
        
        self.__account_number = account_number #private 
        self.__account_balance = account_balance #Private

#Create many types of method like,(@account_balance.setterdeposit,withdraw,display)
    @property
    def account_number(self):
        return self.__account_number

    @property
    def account_balance(self):
        return self.__account_balance

    @account_balance.setter
    def account_balance(self, value):
        if value < 0:
            raise InvalidInputException("Account balance cannot be negative.")
        self.__account_balance = value

    @abstractmethod
    def deposit(self, amount):
        pass

    @abstractmethod
    def withdraw(self, amount):
        pass

    @abstractmethod
    def display(self):
        pass


# Single Inheritance: SavingsAccount
class SavingsAccount(Account):
    def __init__(self, account_number, account_balance, interest_rate):
        super().__init__(account_number, account_balance)
        
        if interest_rate < 0:
            raise InvalidInputException("Interest rate cannot be negative.")
        self.__interest_rate = interest_rate #private

    def deposit(self, amount):
        if amount <= 0:
            raise InvalidInputException("Deposit amount must be positive.")
        self.account_balance += amount
        print(f"Deposit successful! New balance: {self.account_balance}")

    def withdraw(self, amount):
        if amount <= 0 or amount > self.account_balance:
            raise InvalidInputException("Invalid withdrawal amount.")
        self.account_balance -= amount
        print(f"Withdrawal successful! New balance: {self.account_balance}")

    def display(self):
        print(f"Savings Account Number: {self.account_number}")
        print(f"Balance: {self.account_balance}")
        print(f"Interest Rate: {self.__interest_rate * 100}%\n")


# Multilevel Inheritance: Premium SavingsAccount
class PremiumSavingsAccount(SavingsAccount):
    def __init__(self, account_number, account_balance, interest_rate, loyalty_bonus):
        super().__init__(account_number, account_balance, interest_rate) 
        
        if loyalty_bonus < 0:
            raise InvalidInputException("Loyalty bonus cannot be negative.")
        self.__loyalty_bonus = loyalty_bonus

    def add_loyalty_bonus(self):
        self.account_balance += self.__loyalty_bonus
        print(f"Loyalty bonus of {self.__loyalty_bonus} added! \nNew balance: {self.account_balance}")

    def display(self):
        super().display()
        print(f"Loyalty Bonus: {self.__loyalty_bonus}\n")


# Hierarchical Inheritance: BusinessAccount
class BusinessAccount(Account):
    def __init__(self, account_number, account_balance, overdraft_limit):
        super().__init__(account_number, account_balance)
        
        if overdraft_limit < 0:
            raise InvalidInputException("Overdraft limit cannot be negative.")
        self.__overdraft_limit = overdraft_limit

    def deposit(self, amount):
        if amount <= 0:
            raise InvalidInputException("Deposit amount must be positive.")
        self.account_balance += amount
        print(f"Deposit successful! \nNew balance: {self.account_balance}")

    def withdraw(self, amount):
        if amount <= 0 or amount > self.account_balance + self.__overdraft_limit:
            raise InvalidInputException("Invalid withdrawal amount.")
        self.account_balance -= amount
        print(f"Withdrawal successful! New balance: {self.account_balance}")

    def display(self):
        print(f"Business Account Number: {self.account_number}")
        print(f"Balance: {self.account_balance}")
        print(f"Overdraft Limit: {self.__overdraft_limit}\n")


# Hybrid Inheritance: LoanAccount
class LoanAccount(Account):
    def __init__(self, account_number, account_balance, loan_amount, interest_rate):
        super().__init__(account_number, account_balance)
        if loan_amount <= 0 or interest_rate < 0:
            raise InvalidInputException("Loan amount and interest rate must be positive.")
        self.__loan_amount = loan_amount
        self.__interest_rate = interest_rate
        self.__repaid_amount = 0

    def repay(self, amount):
        if amount <= 0 or amount > self.__loan_amount - self.__repaid_amount:
            raise InvalidInputException("Invalid repayment amount.")
        self.__repaid_amount += amount
        self.account_balance -= amount
        print(f"Repayment successful! Remaining loan: {self.__loan_amount - self.__repaid_amount}")

    def deposit(self):
        raise InvalidInputException("Deposit is not allowed for Loan Account.")

    def withdraw(self):
        raise InvalidInputException("Withdrawal is not allowed for Loan Account.")

    def display(self):
        print(f"Loan Account Number: {self.account_number}")
        print(f"Balance: {self.account_balance}")
        print(f"Loan Amount: {self.__loan_amount}")
        print(f"Interest Rate: {self.__interest_rate * 100}%")
        print(f"Repaid Amount: {self.__repaid_amount}\n")



        
#create Bill class        
class Bill:
    def __init__(self, bill_type, bill_amount):
        if bill_amount <= 0:
            raise InvalidInputException("Bill amount must be positive.")
        self.__bill_type = bill_type
        self.__bill_amount = bill_amount

    @property
    def bill_type(self):
        return self.__bill_type

    @property
    def bill_amount(self):
        return self.__bill_amount

    def pay_bill(self, account):
        if account.account_balance < self.bill_amount:
            raise InvalidInputException("Insufficient balance to pay the bill.")
        account.account_balance -= self.bill_amount
        print(f"{self.bill_type} bill of amount {self.bill_amount} paid successfully!\nRemaining New balance: {account.account_balance}")
        


# Bank System for Managing Accounts
class BankSystem:
    def __init__(self):
        self.accounts = []
        self.users = {"admin": "admin123"}  # Default admin user

    #Login Function
    def login(self):
        username = input("Enter username: ")
        password = input("Enter password: ")
        if username in self.users and self.users[username] == password:
            print("Login successful!")
            return True
        else:
            print("Invalid username or password!")
            return False
        
    #Register User function (Set Username,password)
    def register_user(self, username, password):
        if username in self.users:
            raise InvalidInputException("Username already exists!")
        self.users[username] = password
        print("User registered successfully!")

    def add_account(self, account):
        if any(acc.account_number == account.account_number for acc in self.accounts):
            raise InvalidInputException("Account number already exists.")
        self.accounts.append(account)
        print("Account added successfully!")

    def find_account(self, account_number):
        for account in self.accounts:
            if account.account_number == account_number:
                return account
        raise InvalidInputException("Account not found.")

    def remove_account(self, account_number):
        account = self.find_account(account_number)
        self.accounts.remove(account)
        print(f"Account {account_number} removed successfully!")

    def display_accounts(self):
        if not self.accounts:
            print("No accounts found.")
        else:
            for account in self.accounts:
                account.display()



# Menu System
def banking_menu():
    bank = BankSystem()

    while True:
        print("\n1. Login")
        print("2. Register")
        print("3. Exit")
        login_choice = int(input("Enter your choice: "))

        if login_choice == 1:  #Login
            if bank.login():
                
                while True:
                    try:
                        print("\n1. Add Savings Account")
                        print("2. Add Premium Savings Account")
                        print("3. Add Business Account")
                        print("4. Add Loan Account")
                        print("5. Deposit Amount")
                        print("6. Withdraw Amount")
                        print("7. Pay Bill")
                        print("8. Display Accounts")
                        print("9. Remove Account")
                        print("10. Logout")
                        print("------------------------")
                        choice = int(input("Enter your choice: "))

                        if choice == 1:  #Saving Account
                            acc_no = int(input("Enter Account Number: "))
                            balance = float(input("Enter Balance: "))
                            interest_rate = float(input("Enter Interest Rate (0.05 for 5%): "))
                            account = SavingsAccount(acc_no, balance, interest_rate)
                            bank.add_account(account)
                            print("------------------------")
                            
                        elif choice == 2:  #Premium Saving Account
                            acc_no = int(input("Enter Account Number: "))
                            balance = float(input("Enter Balance: "))
                            interest_rate = float(input("Enter Interest Rate (0.05 for 5%): "))
                            loyalty_bonus = float(input("Enter Loyalty Bonus: "))
                            account = PremiumSavingsAccount(acc_no, balance, interest_rate, loyalty_bonus)
                            bank.add_account(account)
                            print("------------------------")
                                
                        elif choice == 3:  #Bussiness Account
                            acc_no = int(input("Enter Account Number: "))
                            balance = float(input("Enter Balance: "))
                            overdraft = float(input("Enter Overdraft Limit: "))
                            account = BusinessAccount(acc_no, balance, overdraft)
                            bank.add_account(account) 
                            print("------------------------") 
                            
                            
                        elif choice == 4: #Loan Account
                            acc_no = int(input("Enter Account Number: "))
                            balance = float(input("Enter Balance: "))
                            loan_amount = float(input("Enter Loan Amount: "))
                            interest_rate = float(input("Enter Interest Rate (0.1 for 10%): "))
                            account = LoanAccount(acc_no, balance, loan_amount, interest_rate)
                            bank.add_account(account)
                            print("------------------------")
   
                                
                        elif choice == 5:  # Deposit Amount
                            acc_no = int(input("Enter Account Number: "))
                            account = bank.find_account(acc_no)
                            amount = float(input("Enter Deposit Amount: "))
                            account.deposit(amount)
                            print("------------------------")

                        elif choice == 6:  # Withdraw Amount
                            acc_no = int(input("Enter Account Number: "))
                            account = bank.find_account(acc_no)
                            amount = float(input("Enter Withdrawal Amount: "))
                            account.withdraw(amount)
                            print("------------------------")

                        elif choice == 7:  # Pay Bill
                            acc_no = int(input("Enter Account Number: "))
                            account = bank.find_account(acc_no)
                            bill_type = input("Enter Bill Type (Electricity, Water,Wi-fi,loan): ")
                            bill_amount = float(input("Enter Bill Amount: "))
                            bill = Bill(bill_type, bill_amount)
                            bill.pay_bill(account)
                            print("------------------------")

                        elif choice == 8:  # Display Accounts
                            bank.display_accounts()
                            print("------------------------")

                        elif choice == 9:  # Remove Account
                            acc_no = int(input("Enter Account Number to Remove: "))
                            bank.remove_account(acc_no)
                            print("------------------------")

                        elif choice == 1:  # Logout
                            print("Logged out successfully!")
                            break

                        else:
                            print("Invalid choice! Please try again.")

                    except InvalidInputException as e:
                        print(f"Error: {e}")
                    except ValueError:
                        print("Invalid input! Please enter valid numbers.")
                    except Exception as e:
                        print(f"An unexpected error occurred: {e}")

        elif login_choice == 2:  # Register
            try:
                username = input("Enter username: ")
                password = input("Enter password: ")
                bank.register_user(username, password)
                print("------------------------")
            except InvalidInputException as e:
                print(f"Error: {e}")

        elif login_choice == 3:  # Exit
            print("Exiting....")
            break

        else:
            print("Invalid choice! Please try again.")


# Run the menu
banking_menu()
