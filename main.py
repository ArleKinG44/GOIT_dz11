from collections import UserDict
from datetime import datetime


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        if len(value) != 10 or not value.isdigit():
            raise ValueError("Phone number must be 10 digits.")
        super().__init__(value)


class Birthday(Field):
    def __init__(self, value):
        if not isinstance(value, datetime):
            raise ValueError("Birthday must be a datetime object.")
        super().__init__(value)


class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday) if birthday else None

    def add_phone(self, phone_number):
        self.phones.append(Phone(phone_number))

    def remove_phone(self, phone_number):
        for phone in self.phones:
            if phone.value == phone_number:
                self.phones.remove(phone)
                break

    def edit_phone(self, old_phone_number, new_phone_number):
        for phone in self.phones:
            if phone.value == old_phone_number:
                phone.value = new_phone_number
                break
        else:
            raise ValueError("The old phone number does not exist.")

    def find_phone(self, phone_number):
        for phone in self.phones:
            if phone.value == phone_number:
                return phone

    def days_to_birthday(self):
        if not self.birthday:
            return None
        now = datetime.now()
        next_birthday = datetime(now.year, self.birthday.value.month,
                                 self.birthday.value.day)
        if now > next_birthday:
            next_birthday = datetime(now.year + 1, self.birthday.value.month,
                                     self.birthday.value.day)
        return (next_birthday - now).days

    def __str__(self):
        return f"""Contact name: {self.name.value},
                    phones: {'; '.join(p.value for p in self.phones)}"""


class AddressBook(UserDict):
    def __init__(self):
        super().__init__()
        self.current_page = 0

    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def iterator(self, n):
        self.current_page = 0
        self.page_size = n

    def __iter__(self):
        return self

    def __next__(self):
        if self.current_page * self.page_size >= len(self.data):
            raise StopIteration
        data_slice = dict(list(self.data.items())
                          [self.current_page * self.page_size:
                           (self.current_page + 1) * self.page_size])
        self.current_page += 1
        return data_slice
