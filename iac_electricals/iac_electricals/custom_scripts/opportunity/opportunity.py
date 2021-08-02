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
					"customer_name":"customer"
				},
			"validation": {
					"docstatus": ["=", 0]
				}
			}
		}, target_doc)
	opp_doc = frappe.get_doc("Opportunity", source_name)
	print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!22222222222222",opp_doc)
	if (not frappe.db.exists('Customer',{'name': opp_doc.customer_name})):
		cus_name = create_customer(opp_doc)
		
	return doclist	




def create_customer(opp_doc):
	try:
		customer = frappe.new_doc("Customer")
		customer.customer_name = opp_doc.customer_name
		customer.insert(ignore_permissions=True)
		if customer.name:
			if opp_doc.customer_address:
				add_doc = frappe.get_doc("Address", opp_doc.customer_address)
				if add_doc:
					add_doc.append("links", {
						"link_doctype": "Customer",
						"link_name": customer.name,
						"link_title": opp_doc.customer_name
					})
					add_doc.save()
			if opp_doc.contact_person:
				con_doc = frappe.get_doc("Contact", opp_doc.contact_person)
				if con_doc:
					con_doc.append("links", {
						"link_doctype": "Customer",
						"link_name": customer.name,
						"link_title": opp_doc.customer_name
					})
					con_doc.save()
		return customer.name	
	except Exception as e:
		raise e
