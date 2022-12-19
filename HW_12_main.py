import re
from HW_12_contact_book import Record, AddressBook

contacts = AddressBook()  

def input_error(funk):
    def inner(*args,**kwargs):  
        try:
            return funk(*args,**kwargs)
        except KeyError: 
            return "This name does not exist."
        except IndexError:
            return "Did not receive all information."
        except ValueError:
            return "Did not receive a correct format ('%Y-%m-%d' for date or 3-12 items for number)."
        except FileNotFoundError:
            return "Did not find this file"
      
    return inner

@input_error
def add(text):
    phone_number = get_phone(text)
    phone_name = get_name(text)
    if contacts.data.get(phone_name):
        record = contacts[phone_name]
    else:
        record = Record(phone_name)
    record.add(phone_number)
    contacts.add_record(record)
    return "Number added. Something else?"

@input_error
def add_bday(text):
    phone_name = get_name(text)
    birthday = get_birthday(text)

    if  contacts.data.get(phone_name):
        record = contacts[phone_name]
        record.add_birthday(birthday)
        contacts.change_record(record)
    else:
        record = Record(phone_name)
        record.add_birthday(birthday)
        contacts.add_record(record)
    
    return "Birthday added. Something else?"

@input_error
def change(text):
    phone_number = get_phone(text)
    phone_name = get_name(text)
    for name, numbers in contacts.items():
        if name == phone_name:
            old_phone_number = [number.value for number in numbers.phone_numbers]
    record = Record(phone_name)
    record.change(phone_number, old_phone_number)
    contacts.change_record(record)
    result = f"{phone_name}\'s number {old_phone_number} changed to {phone_number}. Something else?"
    return result

@input_error
def days_to_birthday(text):
    name = re.findall(r"[a-z]+", text, flags=re.IGNORECASE)[-1].title()
    days = contacts[name].days_to_birthday()
    if days == None:
        return f"Don't have {name}'s bithday"
    return f"{days} days yet"

@input_error
def delete(text):
    phone_number = get_phone(text)
    phone_name = get_name(text)
    record = contacts[phone_name]
    return record.delete(phone_number)

@input_error
def end(text):
    return "Good bye!"

@input_error
def find(text):
    part = re.findall(r"\w+", text)[1]
    result = ""
    for item in contacts.show_all():
        if bool(re.findall(part, item, flags=re.IGNORECASE)):
            result += item + "\n"
    if result:
        return result.rstrip("\n")
    else:
        return "no matches"


def get_birthday(text):    
    birthday = re.findall(r"\d{4}-\d{2}-\d{2}", text)[0]
    return birthday
    
def get_name(text):
    phone_name = re.findall(r"[a-z]+", text, flags=re.IGNORECASE)[1].title()
    return phone_name

def get_phone(text):
    phone_number = re.findall(r"\d+", text)[-1]
    return phone_number
    
@input_error
def hello(text):
    return "How can I help you?"

@input_error
def iterator(text):
    n = int(re.findall(r"\d+", text)[-1])
    result = ""
    page = 1
    for item in contacts.iterator(n):
        if item:
            result += f"Page №{page} \n"
        for record in item:
            result += f"{record} \n"
        page += 1
        
    return result.rstrip("\n")

@input_error
def load_from_file(text):
    file_name = re.findall(r"\w+", text)[1] + ".bin" 
    contacts.load_from_file(file_name)
    return f"loaded from {file_name}"
    
@input_error
def phone(text):
    phone_name = get_name(text)
    return contacts.find_contact(phone_name)

@input_error
def save_in_file(text):
    file_name = re.findall(r"\w+", text)[1] + ".bin" 
    contacts.save_in_file(file_name)
    return f"saved in {file_name}"

@input_error
def show_all(text):
    result = ""
    for item in contacts.show_all():
        result += item + "\n"
    return result.rstrip("\n")

def main():
    start = True

    while start:

        access = False
        entered_text = input()
        
        for key in user_command.keys():
            if bool(re.search(key, entered_text, flags=re.IGNORECASE)):
                
                access = True
                print(user_command[key](entered_text))

                if key in ["exit","good bye","close"]:
                    start = False  
                break
        if not access:
            print("Option entered incorrectly...")
                     
user_command = {
    "add": add, # додає номер телефону
    "birthday": add_bday, # додає дату народження '%Y-%m-%d'
    "change": change,
    "close": end,
    "days to bday": days_to_birthday,
    "delete": delete,
    "exit": end,
    "find": find, 
    "good bye": end,
    "hello": hello,
    "load": load_from_file, # load [file name]
    "pages": iterator,
    "phone": phone,
    "show all": show_all, 
    "save": save_in_file  # save [file name] 
}

if __name__ == "__main__":
    main()