from collections import UserDict
from datetime import date
import json


class Field:
    def __init__(self, value) -> None:
        self._value = None
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value: str):
        self._value = new_value

    def __str__(self) -> str:
        return f"{self.value}"

    def __eq__(self, new_value) -> bool:
        if isinstance(new_value, self.__class__):
            return self.value == new_value.value


class Name(Field):
    @Field.value.setter
    def value(self, name: str):
        if not name.isalpha():
            raise ValueError("not valid name only alpha")
        Field.value.fset(self, name)
        # super(Name, Name).value.fset(self, name) # decorator call


class Phone(Field):
    def __valid_phone(self, phone: str) -> None:
        if not isinstance(phone, str):
            raise ValueError("only str for number")
        if not phone.isdigit():
            raise ValueError("Error... Phone number must be digit")

    @Field.value.setter
    def value(self, phone: str):
        self.__valid_phone(phone)
        Field.value.fset(self, phone)


class Birthday(Field):
    def __valid_date(self, birthday: str) -> None:
        try:
            date.fromisoformat(birthday)
        except ValueError:
            raise ValueError("invalid format date, only ISO format yyyy-mm-dd")

    @Field.value.setter
    def value(self, birthday):
        self.__valid_date(birthday)
        Field.value.fset(self, birthday)

    def get_date(self):
        return date.fromisoformat(self.value)


class Record:
    def __init__(self, name: Name, phone: Phone, birthday: Birthday = None) -> None:
        self.name = name
        self.phones = [phone] if phone else []
        self.birthday = birthday

    def add_phone(self, phone: Phone):
        if phone not in self.phones:
            self.phones.append(phone)

    def del_phone(self, phone: Phone):
        if phone in self.phones:
            self.phones.remove(phone)

    def edit_phone(self, old_phone: Phone, new_phone: Phone):
        if old_phone not in self.phones:
            # перевірка на входження (порівнюемо строку зі строками - все коректно без додаткових магічних методів)
            raise ValueError(f"old...{old_phone}")
        if new_phone not in self.phones:
            raise ValueError(f"new {new_phone}")
        index = self.phones.index(old_phone)
        # знаходимо індекс..індекси у списку обьектів і у списку строк відповідні
        self.phones[index] = new_phone

    # змінюемо значення обьекту при цьому комірка памьяті залишаеться та сама у обьекту Phone

    def days_to_birthday(self) -> int:
        today = date.today()
        b_day = self.birthday.get_date().replace(year=today.year)
        if b_day < today:
            b_day = b_day.replace(year=today.year + 1)
        return (b_day - today).days

    def __str__(self):  # реалізуємо магічний метод для виводу контактів
        return f"{self.name.value} {[(ph.value) for ph in self.phones]} {self.birthday.value}"


class AddressBook(UserDict):
    N = 2  # додамо змінну классу, для контролю паггінації, по замовчюванню 2 записи на 1 сторінку

    def save_to_file(self):
        data_for_json = {}
        # for v in self.data.values():
        #     data_for_json.append(f"{v}")
        for self.k, self.v in self.data.items():
            data_for_json[self.k] = str(self.v).split(" ")[1:]

        with open("contacts.json", "w") as f:
            json.dump(data_for_json, f, indent=4)

    def read_from_file(self):
        with open("contacts.json", "r") as f:
            return json.load(f)

    def add_record(self, record):
        if not isinstance(record, Record):
            raise ValueError("Record must be an instance of the Record class")
        # if type(record) != Record:
        #     raise TypeError("")
        self.data[record.name.value] = record

    def find_record(self, search: str):
        # return self.data.get(value)
        val_record = []
        search = search.lower()
        for record in self.data.values():
            str_val_record = f"{record.name} -> {' '.join([str(ph)for ph in record.phones])}: {record.birthday}"
            if search in record.name.value.lower():
                val_record.append(str_val_record)
            else:
                for phone in record.phones:
                    if search in phone.value:
                        val_record.append(str_val_record)
        return val_record

    def iterator(self, n) -> list[dict]:
        contact_list = []  # список записів контактів
        if n:
            AddressBook.N = n
        # for record in self.data.values():
        #     contact_list.append(record)

        return self.__next__()

    def __iter__(self):
        n_list = []
        counter = 0
        for contact in self.data.values():
            n_list.append(contact)
            counter += 1
            if (
                counter >= AddressBook.N
            ):  # якщо вже створено список із заданої кількості записів
                yield n_list
                n_list.clear()
                counter = 0
        yield n_list

    def __next__(self):
        generator = self.__iter__()
        page = 1
        while True:
            user_input = input("Press ENTER")
            if user_input == "":
                try:
                    result = next(generator)
                    if result:
                        print(f"{'*' * 20} Page {page} {'*' * 20}")
                        page += 1
                    for var in result:
                        print(var)
                except StopIteration:
                    print(f"{'*' * 20} END {'*' * 20}")
                    break
            else:
                break


if __name__ == "__main__":
    name = Name("Bill")
    phone = Phone("39447509105")
    bday = Birthday("1234-12-27")

    name_1 = Name("Tom")
    phone_1 = Phone("39447509105")
    bday_1 = Birthday("1234-12-12")

    name_2 = Name("Ket")
    phone_2 = Phone("39447509105")
    bday_2 = Birthday("1234-12-12")

    name_3 = Name("Gim")
    phone_3 = Phone("7654689")
    bday_3 = Birthday("1298-10-17")

    name_4 = Name("Gim")
    phone_4 = Phone("11111")
    bday_4 = Birthday("1298-10-17")

    record = Record(name, phone, bday)
    record_1 = Record(name_1, phone_1, bday_1)
    record_2 = Record(name_2, phone_2, bday_2)
    record_3 = Record(name_3, phone_3, bday_3)
    record_4 = Record(name_4, phone_4, bday_4)

    # print(record.name, [p.value for p in record.phones], record.birthday)

    ab = AddressBook()
    ab.add_record(record)
    ab.add_record(record_1)
    ab.add_record(record_2)
    ab.add_record(record_3)
    ab.add_record(record_4)

    print(
        ab.iterator(2)
    )  # викликаємо метод ітератор, та можемо передати n - число записів
    print(record.days_to_birthday())

    print(ab.find_record("et"))

    # print(ab.data.keys(), ab.data.values())
    ab.save_to_file()
    ab.read_from_file()
    # print(ab.read_from_file)
