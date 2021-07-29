# Copyright (c) 2021, IAC Electricals and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc

class Opportunity(Document):
	pass


@frappe.whitelist()
def make_price_schedule(source_name, target_doc=None, ignore_permissions=False):
	doclist = get_mapped_doc("Opportunity", source_name, {
		"Opportunity": {
			"doctype": "Price Schedule",
			"field_map": {
					"opportunity_from":"quotation_to",
				},
			"validation": {
					"docstatus": ["=", 0]
				}
			}
		}, target_doc)

	return doclist	