from pprint import pprint
import csv
import re
with open("phonebook_raw.csv", encoding='utf-8') as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)


formatted_contacts_list = list()

# Паттерны для регулярных выражений
patterns = {
    'name': r'[а-яА-ЯёЁ]+',
    'split': r'[,\s]',
    'phone': r'(\+7|8)[\s\(]*(\d{3})[\s\)]*[-\s]*(\d{3})[-\s]*(\d{2})[-\s]*(\d{2})[\s\(]*' \
                    r'(доб[\.]*)*[\s]*(\d{4})*[\s\)]*',
    'phone_replace': r'+7(\2)\3-\4-\5 \6\7'
}


for contact in contacts_list[1:]:

    # Добавление имени
    full_name = ' '.join(contact[0:3])
    formatted_name = re.split(pattern=patterns['split'], string=full_name)
    formatted_contact = formatted_name[0:3]

    # Добавление организации
    organization = contact[3]
    formatted_contact.append(organization)

    # Добавление должности
    position = contact[4]
    formatted_contact.append(position)

    # Добавление телефона
    phone = contact[5]
    formatted_phone = re.sub(pattern=patterns['phone'], repl=patterns['phone_replace'], string=phone)
    if formatted_phone:
        if formatted_phone[-1] == ' ':
            formatted_phone = formatted_phone[0:-1]
    formatted_contact.append(formatted_phone)

    # Добавление почты
    email = contact[6]
    formatted_contact.append(email)

    # Проверка совпадений записи
    found = False
    for cont in formatted_contacts_list:
        if formatted_name[0:2] == cont[0:2]:
            found = True
            for i, value in enumerate(formatted_contact):
                if value and not cont[i]:
                    cont[i] = value
    if not found:
        formatted_contacts_list.append(formatted_contact)

# Добавление строки с заголовками
formatted_contacts_list.insert(0, contacts_list[0])

with open("phonebook.csv", "w", encoding='utf-8', newline='') as f:
    datawriter = csv.writer(f, delimiter=',')
    # Вместо contacts_list подставьте свой список
    datawriter.writerows(formatted_contacts_list)