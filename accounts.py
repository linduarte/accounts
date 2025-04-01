import json

# File to store account data
DATA_FILE = 'accounts.json'

def load_accounts():
    try:
        with open(DATA_FILE, 'r') as file:
            accounts = json.load(file)
            # print("Loaded accounts:", accounts)  # Debug: Print loaded accounts
            return accounts
    except FileNotFoundError:
        print("No accounts file found. Starting fresh.")  # Debug: File not found
        return {}

def save_accounts(accounts):
    with open(DATA_FILE, 'w') as file:
        json.dump(accounts, file, indent=4)
    print("Accounts saved to file.")  # Debug: Confirm save

def add_account(accounts):
    service = input("Enter the service name (e.g., OneDrive, Apple TV, Medium): ")
    username = input("Enter the username/email: ")
    recurring_billing = input("Enter the recurring billing period (e.g., monthly, yearly): ")
    payment_method = input("Enter the payment method (e.g., Visa, MasterCard, PayPal): ")
    currency = input("Enter the currency (e.g., USD, BRL): ")  # New field for currency
    accounts[service] = {
        'username': username,
        'recurring_billing': recurring_billing,
        'payment_method': payment_method,
        'currency': currency  # Add currency to the account details
    }
    save_accounts(accounts)
    print(f"Account for {service} added successfully!")

def edit_account(accounts):
    service = input("Enter the service name to edit: ")
    if service in accounts:
        print(f"Editing account for {service}. Leave fields blank to keep current values.")
        current_details = accounts[service]
        
        username = input(f"Enter the username/email [{current_details['username']}]: ").strip()
        recurring_billing = input(f"Enter the recurring billing period (e.g., monthly, yearly) [{current_details['recurring_billing']}]: ").strip()
        payment_method = input(f"Enter the payment method (e.g., Visa, MasterCard, PayPal) [{current_details['payment_method']}]: ").strip()
        currency = input(f"Enter the currency (e.g., USD, BRL) [{current_details.get('currency', 'Not specified')}]: ").strip()
        
        # Update only the fields that are not blank
        accounts[service] = {
            'username': username if username else current_details['username'],
            'recurring_billing': recurring_billing if recurring_billing else current_details['recurring_billing'],
            'payment_method': payment_method if payment_method else current_details['payment_method'],
            'currency': currency if currency else current_details.get('currency', 'Not specified')
        }
        
        save_accounts(accounts)
        print(f"Account for {service} updated successfully!")
    else:
        print(f"No account found for {service}.")   

def view_accounts(accounts):
    if not accounts:
        print("No accounts found.")
        return
    for service, details in accounts.items():
        print(f"Service: {service}")
        print(f"  Username: {details['username']}")
        print(f"  Recurring Billing: {details['recurring_billing']}")
        print(f"  Payment Method: {details['payment_method']}")
        print(f"  Currency: {details.get('currency', 'Not specified')}")  # Use .get() to avoid KeyError
        print()


def delete_account(accounts):
    service = input("Enter the service name to delete: ")
    if service in accounts:
        del accounts[service]
        save_accounts(accounts)
        print(f"Account for {service} deleted successfully!")
    else:
        print(f"No account found for {service}.")

def main():
    accounts = load_accounts()
    while True:
        print("\nAccount Manager")
        print("1. Add Account")
        print("2. View Accounts")
        print("3. Delete Account")
        print("4. Edit Account")  # Added Edit Account option
        print("5. Exit")
        choice = input("Enter your choice: ").strip()  # Strip whitespace
        if choice == '1':
            add_account(accounts)
        elif choice == '2':
            view_accounts(accounts)
        elif choice == '3':
            delete_account(accounts)
        elif choice == '4':
            edit_account(accounts)  # Call the edit_account function
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()