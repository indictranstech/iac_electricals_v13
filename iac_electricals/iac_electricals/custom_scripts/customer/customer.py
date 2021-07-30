# Copyright (c) 2021, IAC Electricals and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc

class Customer(Document):
	pass

@frappe.whitelist()
def make_price_schedule(source_name, target_doc=None, ignore_permissions=False):
	doclist = get_mapped_doc("Customer", source_name, {
		"Customer": {
			"doctype": "Price Schedule",
			"field_map": {
					"doctype":"quotation_to",
					"name":"customer",
					"customer_name":"customer_name"
				},
			"validation": {
					"docstatus": ["=", 0]
				}
			}
		}, target_doc)

	return doclist	