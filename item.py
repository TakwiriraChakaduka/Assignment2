class Item(object):

	def __init__(self, name, description, price, status):
		self.name = name
		self.description = description
		self.price = price
		self.status = status

	def return_as_string(self):
		return '{0},{1},{2},{3}'.format(self.name, self.description, self.price, self.status)