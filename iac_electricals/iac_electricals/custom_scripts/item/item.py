# Copyright (c) 2021, IAC Electricals and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc

def before_insert(self,method=None):
	self.flags.name_set = 1

	current = frappe.db.sql("""select MAX(current) AS current from `tabSeries` where name = '{0}'""".format(self.custom_naming_series),as_dict=1)
	for row in current:
		current = row.current

	if current is None:
		current = 1
		series = self.custom_naming_series + str(current).zfill(4)
		self.name = series
		first_series_to_store = self.custom_naming_series 
		frappe.db.sql("insert into tabSeries (name, current) values (%s, 1)", (first_series_to_store))
	else:
		current = current + 1
		current = current
		series = self.custom_naming_series + str(current).zfill(4)
		self.name = series
		frappe.db.sql("""update tabSeries set current = {0} where name = '{1}'""".format(current, self.custom_naming_series))