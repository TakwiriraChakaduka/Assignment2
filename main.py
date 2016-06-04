""" CP5632 Assignment 1 - 2016
    Items for Hire - Solution
    Takwirira Chakaduka
    18/02/2014

Pseudocode:



function main()
	load items from file
	display welcome msg
	display menu
	get choice
	while choice not
		if choice is
			call load items()
		else if choice is
			call item hire()
		else if choice is
			return items
			display item returned
		else
			display error message (invalid choice)
		display menu
		get choice
	print farewell message

function loading_items ()
function save(items)
function hire_items()
function return_items(items)
"""


class Storage(object):

    def __init__(self, filename):
        super(Storage, self).__init__()
        self.filename = filename
        self.items = {}

    def load(self):
        with open(self.filename, "r") as fd:
            for idx, line in enumerate(fd.readlines()):
                record = line.split(',')
                record = [ value.rstrip() for value in record ]
                self.items[idx] = record

    def save(self):
        with open(self.filename, "w") as fd:
            for x in range(len(self.items)):
                record = self.items[x]
                fd.write(','.join(record) + "\n")

    def hire_items(self, items_index):
        for item_index in items_index:
            record = self.items[item_index]
            if record[-1] == 'out':
                return False
        return True

    def can_hire_items(self, item_index):
        assert self.can_hire_items(item_index)

        for item_index in items_index:
            record = self.items[item_index]
            record[-1] = 'out'
            self.items[item_index] = record
        self.save()
        return True

    def can_return_items(self, items_index):
        for item_index in items_index:
            record = self.items[item_index]
            if record[-1] == 'in':
                return False
        return True

    def return_items(self, items_index):
        assert self.can_return_items(item_index)
        for item_index in items_index:
            record = self.items[item_index]
            record[-1] = 'in'
            self.items[item_index] = record
        self.save()
        return True

    def add_item(self, name, description, price):
        self.items[len(self.items)] = (description, name, price, "in")
        self.save()

import csv
Menu = "\nMenu:\n(L)ist all items\n(H)ire an item\n(R)eturn an item\n(A)dd new item to the stock\n(Q)uit"
welcome_message = "Items for Hire written by: Takwirira Chakaduka"
def main():
    print(welcome_message)
    print(Menu)
    choice = input(">>> ").upper()
    while choice != 'Q':
        if choice == "L":
            loading_items()
        elif choice == "H":
            loading_items()
            hire_items()
        elif choice == "R":
            return_items()
        elif choice == "A":
            items_list = []
            item_name = input("Item name: ")
            if item_name == "":
                print("please enter name of item")
            else:
                items_list.append(item_name)
                pass
            item_description = input("Description: ")
            if item_description == "":
                print("Please enter description")
            else:
                items_list.append(item_description)
                pass
            item_charges = float(input("Price per day: $"))
            if item_charges == "" or item_charges <=0:
                print("Please enter valid amount")
            else:
                items_list.append(item_charges)
                pass
            items_list.append("in")
            writefile = open("items.csv", "a")
            writer = csv.writer(writefile)
            writer.writerow(items_list)
            writefile.close()
            print(item_name + "\t Added")

        else:
            print("Invalid menu choice.")
        print(Menu)
        choice = input(">>> ").upper()
    print("Have a nice day:) ")

def loading_items():
    print("All items  on file ( '*' indicates item is currently out):")
    items = load()
    for key in sorted(items.keys()):
        item = items[key]
        itemstatus = item[-1]
        if itemstatus == "out":
            string_tail = "*"
        else:
            string_tail = ""
        name = item[0]
        print(str(key) + "-" + name + "(" + item[1] + ")" + "\t=" + "\t$ " + item[2] + string_tail)
    print(str(key+1) + " - items loaded from items.csv")


def save(items):
    with open("items.csv", "w") as fd:
        for x in range(len(items)):
            record = items[x]
            fd.write(','.join(record) + "\n")
def load():
    items = {}

    with open("items.csv", "r") as fd:
        for idx, line in enumerate(fd.readlines()):
            record = line.split(',')
            record = [ value.rstrip() for value in record ]
            items[idx] = record

    return items

def hire_items():
    items = load()
    item_index = get_user_value("Enter the number of item to hire", len(items))
    item_line = items[item_index]
    item_properties = item_line
    print( " ".join(item_properties) + " hired ")
    record = items[item_index]
    if record[-1] == 'out':
        print( " That item is already been hired")
        return

    record[-1] = 'out'
    items[item_index] = record
    save(items)

def items_that_are_out(items):
    result = {}
    for k,i in items.items():
        if i[-1] == 'out':
            result[k] = i
    return result

def get_user_value(msg, max_num):
    while True:
        try:
            value = input(msg)
            return int(value)
        except:
            print("Invalid number. Please enter a number between 0 and %d" % max_num)

def return_items():
    items = load()

    items_out = items_that_are_out(items)

    for key in sorted(items_out.keys()):
        print(key, " ".join(items_out[key]))

    item_index = get_user_value("Enter the number of item to return", len(items))
    item_line = items_out[item_index]
    print( " ".join(item_line) + " returned ")
    record = items_out[item_index]
    if record[-1] == 'in':
        print( " That item is already been returned")
        return

    record[-1] = 'in'
    items[item_index] = record
    save(items)

if __name__ == '__main__':
	main()
