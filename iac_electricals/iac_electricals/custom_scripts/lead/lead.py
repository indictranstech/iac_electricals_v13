# Copyright (c) 2021, IAC Electricals and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc

class Lead(Document):
	pass

@frappe.whitelist()
def make_price_schedule(source_name, target_doc=None, ignore_permissions=False):
	doclist = get_mapped_doc("Lead", source_name, {
		"Lead": {
			"doctype": "Price Schedule",
			"field_map": {
					"name":"party_name",
					"doctype":"quotation_to",
					"lead_name":"customer_name"
				},
			"validation": {
					"docstatus": ["=", 0]
				}
			}
		}, target_doc)

	return doclist	