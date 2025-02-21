from datetime import datetime

class Bkash:
    def __init__(self, account_number, pin, balance):
        self.account_number = account_number
        self.pin = pin
        self.balance = balance
        self.transaction_history = []
        self.daily_transaction_limit = 25000
        self.daily_transaction_total = 0
        self.failed_attempts = 0
        self.locked = False

    def log_transaction(self, transaction_type, amount, recipient=None):
        """Logs a transaction with type, amount, recipient, and timestamp."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if recipient:
            self.transaction_history.append({
                "type": transaction_type,
                "amount": amount,
                "recipient": recipient,
                "date": timestamp
            })
        else:
            self.transaction_history.append({
                "type": transaction_type,
                "amount": amount,
                "date": timestamp
            })

    def validate_user(self, account_number, pin):
        if self.locked:
            print("Account is locked due to multiple failed login attempts.")
            return False
        if self.account_number == account_number and self.pin == pin:
            self.failed_attempts = 0
            return True
        else:
            self.failed_attempts += 1
            if self.failed_attempts >= 3:
                self.locked = True
                print("Too many failed attempts! Account is now locked.")
            return False

    def validate_transaction(self, amount):
        if amount <= 0:
            print("Invalid amount!")
            return False
        if amount > self.balance:
            print("Insufficient balance!")
            return False
        if self.daily_transaction_total + amount > self.daily_transaction_limit:
            print("Transaction limit exceeded!")
            return False
        return True

    def send_money(self, recipient, amount):
        if self.validate_transaction(amount):
            self.balance -= amount
            self.daily_transaction_total += amount
            self.log_transaction("Send Money", amount, recipient)
            print(f"Successfully sent {amount} to {recipient}.")
        else:
            print("Transaction failed!")

    def cash_out(self, amount):
        if amount < 50:
            print("Amount is low. Minimum cash out is 50 taka.")
        elif self.validate_transaction(amount):
            self.balance -= amount
            self.daily_transaction_total += amount
            self.log_transaction("Cash Out", amount)
            print(f"Successfully cashed out {amount}.")
        else:
            print("Transaction failed!")

    def mobile_recharge(self, phone_number, amount):
        if amount < 20:
            print("Amount is low. Minimum recharge is 20 taka.")
        elif self.validate_transaction(amount):
            self.balance -= amount
            self.daily_transaction_total += amount
            self.log_transaction("Mobile Recharge", amount, phone_number)
            print(f"Successfully recharged {amount} to {phone_number}.")
        else:
            print("Transaction failed!")

    def change_pin(self):
        current_pin = input("Enter your current PIN: ")
        if current_pin == self.pin:
            new_pin = input("Enter your new PIN: ")
            confirm_pin = input("Confirm your new PIN: ")
            if new_pin == confirm_pin:
                self.pin = new_pin
                print("PIN changed successfully!")
            else:
                print("PIN confirmation failed!")
        else:
            print("Incorrect current PIN!")

    def check_balance(self):
        print(f"Your current balance is {self.balance}")

    def my_bkash(self):
        while True:
            print("\n=== My bKash ===")
            print("1. View Transaction History")
            print("2. Change PIN")
            print("3. Back to Main Menu")
            choice = input("Enter your choice: ")

            if choice == "1":
                self.view_transaction_history()
            elif choice == "2":
                self.change_pin()
            elif choice == "3":
                break
            else:
                print("Invalid choice! Please try again.")

    def view_transaction_history(self):
        if not self.transaction_history:
            print("No transactions to display.")
        else:
            print("\n=== Transaction History ===")
            for transaction in self.transaction_history:
                details = f"{transaction['date']} - {transaction['type']} - {transaction['amount']} Taka"
                if "recipient" in transaction:
                    details += f" (Recipient: {transaction['recipient']})"
                print(details)

    def donation(self, cause, amount):
        if self.validate_transaction(amount):
            self.balance -= amount
            self.daily_transaction_total += amount
            self.log_transaction("Donation", amount, cause)
            print(f"Successfully donated {amount} to {cause}.")
        else:
            print("Transaction failed!")

    def request_money(self, sender, amount):
        print(f"Requesting {amount} from {sender}...")
        # Placeholder for sender's response
        print(f"Request sent to {sender}.")

# Create a bKash account
account = Bkash(account_number="01712121212", pin="213", balance=5000)

# Login Validation
while True:
    print("=== bKash Login ===")
    input_account = input("Enter your account number: ")
    input_pin = input("Enter your PIN: ")

    if account.validate_user(input_account, input_pin):
        print("Login successful!")
        break
    else:
        print("Invalid account number or PIN. Please try again.")

# Main menu
while True:
    print("\n=== bKash Menu ===")
    print("1. Send Money")
    print("2. Cash Out")
    print("3. Mobile Recharge")
    print("4. Donations")
    print("5. Request Money")
    print("6. Check Balance")
    print("7. My bKash")
    print("8. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        recipient = input("Enter recipient's account number: ")
        amount = float(input("Enter amount to send: "))
        account.send_money(recipient, amount)
    elif choice == "2":
        amount = float(input("Enter amount to cash out: "))
        account.cash_out(amount)
    elif choice == "3":
        phone_number = input("Enter phone number: ")
        amount = float(input("Enter amount to recharge: "))
        account.mobile_recharge(phone_number, amount)
    elif choice == "4":
        cause = input("Enter donation cause: ")
        amount = float(input("Enter amount to donate: "))
        account.donation(cause, amount)
    elif choice == "5":
        sender = input("Enter sender's account number: ")
        amount = float(input("Enter amount to request: "))
        account.request_money(sender, amount)
    elif choice == "6":
        account.check_balance()
    elif choice == "7":
        account.my_bkash()
    elif choice == "8":
        print("Thank you for using bKash. Goodbye!")
        break
    else:
        print("Invalid choice! Please try again.")
