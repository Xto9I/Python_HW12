from collections import UserDict
from datetime import datetime
import pickle

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record
  
    def change_record(self, record):
        self.data.update({record.name.value: record})

    def find_contact(self, name):
        for phone_name, numbers in self.data.items():
            if phone_name == name:
                return [number.value for number in numbers.phone_numbers]
        return "Contact not found!!!"

    def show_all(self):
        result = []
        for item in self.data.values():
            if not item.birthday:
                birthday = "no info"
            else:
                birthday = item.birthday.value
            if not item.phone_numbers:
                phone_list = "no info"
            else:
                phone_list = [number.value for number in item.phone_numbers]
            result.append(f"{item.name.value} : phones - {phone_list}, birthday - {birthday}")
        return result


    def iterator(self, n):
        result = [] 
        i = 0
        if n > len(self.data):
            n = len(self.data) 
        
        all_info = self.show_all()
        
        for record_item in all_info:
            result.append(record_item)
            i += 1
            if i == n:
                yield result
                result = [] 
                i = 0
        
        yield result
 
    def load_from_file(self, file_name):
        with open(file_name, "rb") as fh:
            self.data = pickle.load(fh)
        
    def save_in_file(self, file_name):
        with open(file_name, "wb") as fh:
            pickle.dump(self.data, fh)
    
class Field:
    def __init__(self, value):
        self._value = None
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

class Birthday(Field):
    
    @Field.value.setter
    def value(self, value):
        row_format = "%Y-%m-%d" 
        value = datetime.strptime(value, row_format).date()
        today = datetime.today().date()
        if value > today:
            raise ValueError
        self._value = value

class Name(Field):
    pass

class Phone(Field):
    
    @Field.value.setter
    def value(self, value):
        if len(value) < 3 or len(value) > 12:
            raise ValueError
        self._value = value

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phone_numbers = []
        self.birthday = None
    
    def add(self, phone):    
        self.phone_numbers.append(Phone(phone))

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def change(self, phone, old_phone):
        self.delete(old_phone)
        self.add(phone)

    def days_to_birthday(self):
        if self.birthday:
            today = datetime.today().date()
            b_day = self.birthday.value.replace(year=today.year)
            if b_day < today:
                b_day = b_day.replace(year=today.year + 1)

            time_to_birthday = abs(b_day - today).days 
            return time_to_birthday

    def delete(self, phone):
        for item in self.phone_numbers:
            if item.value == phone:
                self.phone_numbers.remove(item)
                return f"Number {phone} deleted."
        return "Phone number not found!!!"    
