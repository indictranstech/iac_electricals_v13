# Copyright (c) 2021, IAC Electricals and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document

def validate(self,method=None):
	if self.item_charges == "Item Level Freight Charge":
		for d in self.items:
			if d.freight_charges_type == "Percent":
				total_itm_charge  = d.rate*d.freight_charges/100
				d.freight_charge_per_quantity = total_itm_charge
				_on_all_itm_charge = d.qty * d.freight_charge_per_quantity
				d.freight_charges_on_all_quantity = _on_all_itm_charge
				# d.rate = total_itm_charge + d.main_rate

			elif d.freight_charges_type == "Amount":
				total_itm_charge  = d.freight_charges
				d.freight_charge_per_quantity = total_itm_charge
				_on_all_itm_charge = d.qty * d.freight_charge_per_quantity
				d.freight_charges_on_all_quantity = _on_all_itm_charge
				# d.rate = total_itm_charge + d.main_rate
			else:
				d.freight_charges = 0

		freight_ttl = 0
		for d in self.items:
			freight_ttl = freight_ttl + d.freight_charges_on_all_quantity

		self.freight_total = freight_ttl

	if self.item_charges == "Item Level Freight Charge" or self.item_charges == "Lumpsum Amount":
		if not self.taxes_and_charges:
			frappe.throw(_('Please Add Tax Template.'))
		if not self.taxes:
			frappe.throw(_('Please Reselect Tax Template.'))	
			

	if self.item_charges == "Item Level Freight Charge":
		if self.taxes:
			if self.freight_total:
				condition_ = 0
				for d in self.taxes:
					if d.charge_type == "Actual":
						if d.tax_amount <= 0 or d.tax_amount != self.freight_total:
							condition_ = 1

				if condition_ == 1:
					frappe.throw(_('Add This Freight Amount : {0} in Tax Details Table For Row Type Actual.').format(self.freight_total))

	if self.item_charges == "Lumpsum Amount":
		if self.taxes:
			lum_condition_ = 0
			for d in self.taxes:
				if d.charge_type == "Actual":
					if d.tax_amount <= 0:
						lum_condition_ = 1

			if lum_condition_ == 1:
				frappe.throw(_('Please add Lumpsum Amount in Tax Details Table For Row Type Actual.'))				
		

		# if self.taxes_and_charges:
		# 	self.taxes = []
		# 	tax_items = []
		# 	tax_details = frappe.get_doc("Sales Taxes and Charges Template",self.taxes_and_charges).taxes
		# 	tx_calculation = 0.0
		# 	total_tax_amount = 0.0
		# 	for taxes in tax_details:
		# 		if getattr(taxes,'charge_type') == "Actual":
		# 			temp = {
		# 				'charge_type' : taxes.charge_type,
		# 				'account_head' : taxes.account_head,
		# 				'description' : taxes.description,
		# 				'tax_amount' : self.freight_total,
		# 				'rate' : '',
		# 				'total' :self.freight_total+self.total,
		# 				'cost_center' : taxes.cost_center
		# 			}
		# 			tax_items.append(temp)
		# 		else:
		# 			tx_calculation = float(self.freight_total+self.total)*taxes.rate/100
		# 			if taxes.idx == 2:
		# 				total_tax_amount =float(self.freight_total+self.total) + tx_calculation
		# 			else:
		# 				total_tax_amount = total_tax_amount + tx_calculation
		# 			temp = {
		# 				'charge_type' : taxes.charge_type,
		# 				'account_head' : taxes.account_head,
		# 				'description' : taxes.description,
		# 				'rate' : taxes.rate,
		# 				'tax_amount' : tx_calculation,
		# 				'total' : total_tax_amount,
		# 				'cost_center' : taxes.cost_center
		# 			}
		# 			tax_items.append(temp)

		# 	for freight_taxes in tax_items:
		# 		lum_itm_tx = self.append('taxes')
		# 		lum_itm_tx.charge_type = freight_taxes["charge_type"]
		# 		if freight_taxes["charge_type"] != "Actual":
		# 			lum_itm_tx.row_id = 1
		# 		lum_itm_tx.account_head = freight_taxes["account_head"]
		# 		lum_itm_tx.description = freight_taxes["description"]
		# 		lum_itm_tx.tax_amount = freight_taxes["tax_amount"]
		# 		lum_itm_tx.rate = freight_taxes["rate"]
		# 		lum_itm_tx.total = freight_taxes["total"]
		# 		lum_itm_tx.cost_center = freight_taxes["cost_center"]
			
	for i in self.items:
		if i.freight_charges_type == "Percent" or i.freight_charges_type == "Amount":
			if i.freight_charges == 0 or i.freight_charges == None:
				frappe.throw("Please Enter Freight Charges for row "+ str(i.idx)+" in Item Table")