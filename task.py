from collections import UserDict
from datetime import datetime, timedelta

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    # реалізація класу
		pass

class Phone(Field):
    def __init__(self, value:str):         
            if value.isdigit() and len(value)==10:
                super().__init__(value)
            else:
                raise ValueError(f"Phone is too short:{value}.Please put in 10 number")

class Birthday(Field):
    def __init__(self, value):
        try:
           self.value = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY") 

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday=None

    def __str__(self):
        phones = '; '.join(p.value for p in self.phones)
        birthday = f", birthday: {self.birthday}" if self.birthday else ""
        return f"Contact name: {self.name}, phones: {phones}{birthday}"
    
    def add_phone(self,phone):
        try:
            self.phones.append(Phone(phone))
        except ValueError as e:
            print(e)

    def add_birthday(self,date):
        try:
            self.birthday = Birthday(date)
        except ValueError as e:
            print(e)

    def edit_phone(self, old_phone, new_phone):
        try:
            for phone in self.phones:
                if phone.value == old_phone:
                    phone.value = Phone(new_phone).value
                    break
                else:
                    raise ValueError('Phone is not find')
        except ValueError as e:
            print(e)
             
    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
            else:"phone isn't find"
    
    def delete_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

class AddressBook(UserDict):

    def __str__(self):
        return '\n'.join(str(contact) for contact in self.data.values())
    
    def add_record(self,contact):
           self.data[contact.name.value]=contact

    def find(self, name):
        return self.data.get(name, None)
    
    def delete(self, name):
        self.data=[c for c in self.data if self.data[name] != name]

    def get_upcoming_birthdays(self):
        today = datetime.today().date()
        upcoming_birthdays = []
        print(self.data)

        for item in self.data.values():
            if item.birthday:
                year = item.birthday.value.replace(year=today.year)
                birthday = (year - today).days
                
                if 0 <= birthday <= 7:
                    if year.weekday() == 5:  
                        year += timedelta(days=2)
                    elif year.weekday() == 6:
                        year += timedelta(days=1)

                    upcoming_birthdays.append({
                        "name": item.name.value,
                        "birthday": year
                    })

        return upcoming_birthdays

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (IndexError, ValueError) as e:
            return str(e)
    return wrapper

@input_error
def add_contact(args, contacts):
    name, phone,*_ = args
    print(contact)

    if name in contacts:
        user=input("Do you want re-record contact? (yes/no):").strip().lower()

        if user == "yes":
            contacts.add_record(Record(name))
            contacts[name].add_phone(phone)
            return "contact update"
        elif user == "no":
            return "contact not added"
        else:
            return "Invalid command."
    else: 
        contact = Record(name)
        contact.add_phone(phone)
        contacts.add_record(contact)
        return "Contact added."

@input_error   
def change_number(args, contacts):
    name, old_phone, new_phone = args
    record = contacts.find(name)
    if record:
        record.edit_phone(old_phone, new_phone)
        return "number is change"
    else:
        return f"{name} is not found"

@input_error
def print_phone(args, contacts):
    name,*ar = args
    record = contacts.find(name)
    if record:
        return '; '.join(phone.value for phone in record.phones)
    else:
        return f"{name} is not found"
    
@input_error
def add_birthday(args, contacts):
    name, date = args
    record = contacts.find(name)
    if record:
        record.add_birthday(date)
        return f"Birthday added for {name}."
    else:
        return f"{name} not found."

@input_error
def show_birthday(args, contacts):
    name, *ar = args
    record = contacts.find(name)
    if record:
        return str(record.birthday.value) if record.birthday else "Birthday not set."
    else:
        return f"{name} not found."

@input_error
def birthdays(args, contacts):
    upcoming_birthdays = contacts.get_upcoming_birthdays()
    if not upcoming_birthdays:
        return "No upcoming birthdays in the next week."
    return "\n".join(f"{contact['name']}: {contact['birthday']}" for contact in upcoming_birthdays)

    
def main():
    contacts=AddressBook()
    print("Welcome to the assistant bot!")
    print("Available commands:\nheloo\nadd\nall\nchange\nphone\nclose or exit")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, contacts))
        elif command == "all":
            print(contacts)
        elif command == "change":
            print(change_number(args, contacts))
        elif command == "phone":
            print(print_phone(args, contacts))
        elif command == "add-birthday":
            print(add_birthday(args, contacts))
        elif command == "show-birthday":
            print(show_birthday(args, contacts))
        elif command == "birthdays":
            print(birthdays(args, contacts))
        else:
            print("Invalid command.")

    
if __name__ == "__main__":
    try:
        main()
    except ValueError as error:
        print(f"error:{error}")
