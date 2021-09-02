# Copyright (c) 2021, IAC Electricals and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document

def validate(self,method=None):			
	for i in self.items:
		if i.freight_charges_type == "Percent" or i.freight_charges_type == "Amount":
			if i.freight_charges == 0 or i.freight_charges == None:
				frappe.throw("Please Enter Freight Charges for row "+ str(i.idx)+" in Item Table")