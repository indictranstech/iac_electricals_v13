import frappe
from frappe import _
from frappe.model.document import Document

# According To Reading Value Avrage_value calculate
# Formula Total Reading value by count of reading
def before_save(self,method=None):	
	
	for i in self.readings:
		count = 0
		avrage_total = 0	
		if i.reading_1:
			count = count+1
			avrage_total = avrage_total + float(i.reading_1)
		if i.reading_2:
			count = count+1
			avrage_total = avrage_total + float(i.reading_2)
		if i.reading_3:
			count = count+1
			avrage_total = avrage_total + float(i.reading_3)
		if i.reading_4:
			count = count+1
			avrage_total = avrage_total + float(i.reading_4)
		if i.reading_5:
			count = count+1
			avrage_total = avrage_total + float(i.reading_5)
		if i.reading_6:
			count = count+1
			avrage_total = avrage_total + float(i.reading_6)
		if i.reading_7:
			count = count+1
			avrage_total = avrage_total + float(i.reading_7)
		if i.reading_8:
			count = count+1
			avrage_total = avrage_total + float(i.reading_8)
		if i.reading_9:
			count = count+1
			avrage_total = avrage_total + float(i.reading_9)
		if i.reading_10:
			count = count+1
			avrage_total = avrage_total + float(i.reading_10)
		if not count == 0:
			i.average_value = float(avrage_total)/float(count)
		