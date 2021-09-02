# Copyright (c) 2021, IAC Electricals and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document

def validate(self,method=None):
	for d in self.items:
		if d.freight_charges_type == "Percent":
			total_itm_charge  = d.rate*d.freight_charges/100 * d.qty
			_total_qty = d.qty*d.rate+total_itm_charge
			d.amount = _total_qty
		elif d.freight_charges_type == "Amount":
			total_itm_charge  = d.freight_charges
			_total_qty = d.qty*d.rate+ total_itm_charge
			d.amount = _total_qty
		else:
			d.freight_charges = 0
			d.amount = d.qty*d.rate
			
	for i in self.items:
		if i.freight_charges_type == "Percent" or i.freight_charges_type == "Amount":
			if i.freight_charges == 0 or i.freight_charges == None:
				frappe.throw("Please Enter Freight Charges for row "+ str(i.idx)+" in Item Table")