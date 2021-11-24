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

	last_doc = frappe.get_last_doc('File')
	file = open(frappe.utils.get_site_path("private")+"/files/"+last_doc.file_name, "rt")
	csv= file.readlines()
	id_list = []
	variable = None
	for row in csv[1:]:
		li = list(row.split(","))
		id_list.append(li[7])
		if li[7] == self.item_name:
			variable = int(li[0][6:])
			break

	if variable:
		frappe.db.sql("""update tabSeries set current = {0} where name = '{1}'""".format(variable, self.custom_naming_series), debug = 1)
		series = self.custom_naming_series + str(variable).zfill(3)
		self.name = series

	if current is None:
		current = 1
		series = str(self.real_item_code)
		self.name = series
		first_series_to_store = self.custom_naming_series 
		frappe.db.sql("insert into tabSeries (name, current) values (%s, 1)", (first_series_to_store))
	else:
		current = current + 1
		current = current
		series = str(self.real_item_code)
		self.name = series
		frappe.db.sql("""update tabSeries set current = {0} where name = '{1}'""".format(current, self.custom_naming_series))
		pass


@frappe.whitelist()
def update_old_item_custom_naming_series_for_one_time():
	all_item = frappe.get_all('Item')
	cnt = 0
	for item in all_item:
		cnt = cnt + 1
		sql = """ UPDATE `tabItem` SET custom_naming_series = "" where name IN ('{0}')""".format(item.name)
		benificiary_purchase_count = frappe.db.sql(sql,debug=1)

	error_log = frappe.log_error(frappe.get_traceback(), _("All item Updated item count: '{0}' ").format(cnt))		


@frappe.whitelist()
def update_the_series_item_updation(prefix_level_for_item,count1):
	item_updation = frappe.db.sql("""UPDATE `tabSeries` SET current = {0} WHERE name = '{1}' """.format(count1, prefix_level_for_item), debug = 1)
	return "Success"


@frappe.whitelist()
def update_the_series_prefix2_updation(prefix_level_3, count2):
	item_updation = frappe.db.sql("""UPDATE `tabSeries` SET current = {0} WHERE name = '{1}' """.format(count2, prefix_level_3), debug = 1)
	return "Success"


@frappe.whitelist()
def update_the_series_prefix3_updation(prefix_level_2, count3):
	series_3_updation = frappe.db.sql("""UPDATE `tabSeries` SET current = {0} WHERE name = '{1}' """.format(count3, prefix_level_2), debug = 1)
	return "Success"


@frappe.whitelist()
def all_reset_series(level, count4):
	#item series level 1 counter reset
	item_updation = frappe.db.sql("""UPDATE `tabSeries` SET current = {0} WHERE name = '{1}' """.format(count4,level), debug = 1)

	#item series level 2 counter reset
	level2_name = frappe.db.sql("""SELECT l2.name from `tabItem Series lavel 2` l2 join `tabItem Series lavel 1` l1 on l1.name = l2.lavel_2_item_code where l1.name = '{0}' """.format(level), debug = 1, as_dict = 1)

	level_2_name_list = [item.name for item in level2_name]
	if len(level_2_name_list)> 1:
		item_updation2 = frappe.db.sql("""UPDATE `tabSeries` SET current = {0} WHERE name in {1} """.format(count4,tuple(level_2_name_list)), debug = 1)

		level3_name = frappe.db.sql("""SELECT l3.name from `tabItem Series lavel 3` l3 join `tabItem Series lavel 2` l2 on l2.name = l3.level_3_item_code where l2.name in {0} """.format(tuple(level_2_name_list)), debug = 1, as_dict = 1)

		level_3_name_list = [item.name for item in level3_name]

		if len(level_3_name_list) > 1:
	 		item_updation3 = frappe.db.sql("""UPDATE `tabSeries` SET current = {0} WHERE name in {1}""".format(count4,tuple(level_3_name_list)), debug = 1)

	 		item_name = frappe.db.sql("""SELECT item.name from `tabItem` item join `tabItem Series lavel 3` l3 on l3.name = item.item_name where l3.name in {0} """.format(tuple(level_3_name_list)), debug = 1, as_dict = 1)
	 		
	 		item_name_list = tuple([item.name for item in item_name])

	 		if len(item_name_list) > 1:
	 			item_updation4 = frappe.db.sql("""UPDATE `tabSeries` SET current = {0} WHERE name in {1}""".format(count4,tuple(item_name_list)), debug = 1)
	 			item_deletion = frappe.db.sql("""DELETE from `tabItem` where name in {0}""".format(tuple(item_name_list)), debug = 1)
	 		elif len(item_name_list) == 1:
	 			item_updation4 = frappe.db.sql("""UPDATE `tabSeries` SET current = {0} WHERE name = '{1}' """.format(count4,item_name_list[0]), debug = 1)
	 			item_deletion = frappe.db.sql("""DELETE from `tabItem` where name = '{0}' """.format(item_name_list[0]), debug = 1)
	 		else:
	 			pass

	if len(level_2_name_list)> 1:
		item_updation2 = frappe.db.sql("""UPDATE `tabSeries` SET current = {0} WHERE name in {1} """.format(count4,tuple(level_2_name_list)), debug = 1)

		level3_name = frappe.db.sql("""SELECT l3.name from `tabItem Series lavel 3` l3 join `tabItem Series lavel 2` l2 on l2.name = l3.level_3_item_code where l2.name in {0} """.format(tuple(level_2_name_list)), debug = 1, as_dict = 1)

		level_3_name_list = [item.name for item in level3_name]
		if len(level_3_name_list) == 1:
	 		item_updation3 = frappe.db.sql("""UPDATE `tabSeries` SET current = {0} WHERE name = '{1}' """.format(count4,level_3_name_list[0]), debug = 1)
	 		item_name = frappe.db.sql("""SELECT item.name from `tabItem` item join `tabItem Series lavel 3` l3 on l3.name = item.item_name where l3.name = '{0}' """.format(level_3_name_list[0]), debug = 1, as_dict = 1)

	 		item_name_list = tuple([item.name for item in item_name])
	 		if len(item_name_list) > 1:
	 			item_updation4 = frappe.db.sql("""UPDATE `tabSeries` SET current = {0} WHERE name in {1}""".format(count4,tuple(item_name_list)), debug = 1)
	 			item_deletion = frappe.db.sql("""DELETE from `tabItem` where name in {0}""".format(tuple(item_name_list)), debug = 1)
	 		elif len(item_name_list) == 1:
	 			item_updation4 = frappe.db.sql("""UPDATE `tabSeries` SET current = {0} WHERE name = '{1}' """.format(count4,item_name_list[0]), debug = 1)
	 			item_deletion = frappe.db.sql("""DELETE from `tabItem` where name = '{0}' """.format(item_name_list[0]), debug = 1)
	 		else:
	 			pass
	 	

	if len(level_2_name_list) == 1:
		item_updation2 = frappe.db.sql("""UPDATE `tabSeries` SET current = {0} WHERE name = '{1}' """.format(count4,level_2_name_list[0]), debug = 1)

		level3_name = frappe.db.sql("""SELECT l3.name from `tabItem Series lavel 3` l3 join `tabItem Series lavel 2` l2 on l2.name = l3.level_3_item_code where l2.name = '{0}' """.format(level_2_name_list[0]), debug = 1, as_dict = 1)

		level_3_name_list = [item.name for item in level3_name]

		if len(level_3_name_list) > 1:
	 		item_updation3 = frappe.db.sql("""UPDATE `tabSeries` SET current = {0} WHERE name in {1}""".format(count4,tuple(level_3_name_list)), debug = 1)
	 		item_name = frappe.db.sql("""SELECT item.name from `tabItem` item join `tabItem Series lavel 3` l3 on l3.name = item.item_name where l3.name in {0} """.format(tuple(level_3_name_list)), debug = 1, as_dict = 1)
	 		
	 		item_name_list = tuple([item.name for item in item_name])
	 		if len(item_name_list) > 1:
	 			item_updation4 = frappe.db.sql("""UPDATE `tabSeries` SET current = {0} WHERE name in {1}""".format(count4,tuple(item_name_list)), debug = 1)
	 			item_deletion = frappe.db.sql("""DELETE from `tabItem` where name in {0}""".format(tuple(item_name_list)), debug = 1)
	 		elif len(item_name_list) == 1:
	 			item_updation4 = frappe.db.sql("""UPDATE `tabSeries` SET current = {0} WHERE name = '{1}' """.format(count4,item_name_list[0]), debug = 1)
	 			item_deletion = frappe.db.sql("""DELETE from `tabItem` where name = '{0}' """.format(item_name_list[0]), debug = 1)
	 		else:
	 			pass


	if len(level_2_name_list) == 1:
		item_updation2 = frappe.db.sql("""UPDATE `tabSeries` SET current = {0} WHERE name = '{1}' """.format(count4,level_2_name_list[0]), debug = 1)

		level3_name = frappe.db.sql("""SELECT l3.name from `tabItem Series lavel 3` l3 join `tabItem Series lavel 2` l2 on l2.name = l3.level_3_item_code where l2.name = '{0}' """.format(level_2_name_list[0]), debug = 1, as_dict = 1)

		level_3_name_list = [item.name for item in level3_name]
		if len(level_3_name_list) == 1:
			item_updation3 = frappe.db.sql("""UPDATE `tabSeries` SET current = {0} WHERE name = '{1}' """.format(count4,level_3_name_list[0]), debug = 1)
			item_name = frappe.db.sql("""SELECT item.name from `tabItem` item join `tabItem Series lavel 3` l3 on l3.name = item.item_name where l3.name = '{0}' """.format(level_3_name_list[0]), debug = 1, as_dict = 1)
			item_name_list = tuple([item.name for item in item_name])
			if len(item_name_list) > 1:
				item_updation4 = frappe.db.sql("""UPDATE `tabSeries` SET current = {0} WHERE name in {1}""".format(count4,tuple(item_name_list)), debug = 1)
				item_deletion = frappe.db.sql("""DELETE from `tabItem` where name in {0}""".format(tuple(item_name_list)), debug = 1)
			elif len(item_name_list) == 1:
				item_updation4 = frappe.db.sql("""UPDATE `tabSeries` SET current = {0} WHERE name = '{1}' """.format(count4,item_name_list[0]), debug = 1)
				item_deletion = frappe.db.sql("""DELETE from `tabItem` where name = '{0}' """.format(item_name_list[0]), debug = 1)
			else:
				pass


	return "Success"


