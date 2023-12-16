from collections import UserDict
from datetime import datetime, timedelta

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        while not isinstance(value, str) or not value.isdigit() or len(value) != 10:
            print("Invalid phone number format. Please enter a 10-digit phone number.")
            value = input("Enter the contact number: ")
        super().__init__(value)

class Birthday(Field):
    def __init__(self, value):
        try:
            datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            print("Invalid birthday format. Please enter a date in DD.MM.YYYY format.")
            value = input("Enter the birthday: ")
        super().__init__(value)

    def display_with_weekday(self):
        date_obj = datetime.strptime(self.value, "%d.%m.%Y")
        day_of_week = date_obj.strftime("%A")
        return f"{self.value} ({day_of_week})"

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        for p in self.phones:
            if p.value == old_phone:
                p.value = new_phone
                break

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def __str__(self):
        phones_str = '; '.join(str(p) for p in self.phones)
        return f"Contact name: {self.name}, phones: {phones_str}, birthday: {self.birthday.display_with_weekday()}" if self.birthday else f"Contact name: {self.name}, phones: {phones_str}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def get_birthdays_per_week(self):
        today = datetime.now()
        next_week = today + timedelta(days=7)
        upcoming_birthdays = []

        for record in self.data.values():
            if record.birthday:
                birthdate = datetime.strptime(record.birthday.value, "%d.%m.%Y").replace(year=today.year)
                if today <= birthdate <= next_week:
                    upcoming_birthdays.append(record)

        return upcoming_birthdays

def load_contacts(address_book):
    # Function to load contacts, if needed
    pass

def main():
    address_book = AddressBook()
    load_contacts(address_book)
    print('=' * 30 + '\nMain commands:\n'
                     'add - add new contact\\contact number\n'
                     'change - change contact number\n'
                     'phone - show phone number\n'
                     'all - show all contacts\n'
                     'add-birthday - add birthday\n'
                     'show-birthday - show birthday\n'
                     'birthdays - upcoming birthdays\n'
                     'close or exit - close the program\n' + '=' * 30)

    while True:
        command = input("Enter a command: ").lower()

        if command == 'add':
            name = input("Enter the contact name: ")
            phone = input("Enter the contact number: ")
            record = address_book.find(name)
            if not record:
                record = Record(name)
                address_book.add_record(record)
            record.add_phone(phone)
            print(f"Contact {name} added successfully.")
        elif command == 'change':
            name = input("Enter the contact name: ")
            record = address_book.find(name)
            if record:
                print(f"Current contact numbers: {', '.join(str(p) for p in record.phones)}")
                old_phone = input("Enter the contact number to change: ")
                if record.find_phone(old_phone):
                    new_phone = input("Enter the new contact number: ")
                    record.edit_phone(old_phone, new_phone)
                    print(f"Contact number for {name} changed successfully.")
                else:
                    print(f"Contact number {old_phone} not found for {name}.")
            else:
                print(f"Contact {name} not found.")
        elif command == 'phone':
            name = input("Enter the contact name: ")
            record = address_book.find(name)
            if record:
                print(f"Contact {name} numbers: {', '.join(str(p) for p in record.phones)}")
            else:
                print(f"Contact {name} not found.")
        elif command == 'all':
            if not address_book.data:
                print("Address book is empty.")
            else:
                for name, record in address_book.data.items():
                    print(record)
        elif command == 'add-birthday':
            name = input("Enter the contact name: ")
            record = address_book.find(name)
            if record:
                birthday = input("Enter the birthday in DD.MM.YYYY format: ")
                record.add_birthday(birthday)
                print(f"Birthday added for {name} successfully.")
            else:
                print(f"Contact {name} not found.")
        elif command == 'show-birthday':
            name = input("Enter the contact name: ")
            record = address_book.find(name)
            if record and record.birthday:
                print(f"Birthday for {name}: {record.birthday.display_with_weekday()}")
            elif record:
                print(f"No birthday found for {name}.")
            else:
                print(f"Contact {name} not found.")
        elif command == 'birthdays':
            upcoming_birthdays = address_book.get_birthdays_per_week()
            if upcoming_birthdays:
                print("Upcoming birthdays:")
                for record in upcoming_birthdays:
                    print(f"{record.name}: {record.birthday.display_with_weekday()}")
            else:
                print("No upcoming birthdays.")
        elif command == 'close' or command == 'exit':
            print("Goodbye!")
            break
        else:
            print("Invalid command. Please try again.")

if __name__ == "__main__":
    main()
