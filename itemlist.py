from item import Item

class ItemList(object):

    def __init__(self, filename):
        super(ItemList, self).__init__()
        self.filename = filename
        self.items = {}

    def load(self):
        with open(self.filename, "r") as fd:
            for idx, line in enumerate(fd.readlines()):
                record = line.split(',')
                record = [ value.rstrip() for value in record ]
                self.items[idx] = Item(name=record[0], description=record[1], price=record[2], status=record[3])
        return self.items

    def save(self):
        with open(self.filename, "w") as fd:
            for x in range(len(self.items)):
                record = self.items[x].return_as_string()
                fd.write(record + "\n")


    def add_item(self, name, description, price):
        self.items[len(self.items)] = Item(name=name, price=price, description=description, status="in")
        self.save()