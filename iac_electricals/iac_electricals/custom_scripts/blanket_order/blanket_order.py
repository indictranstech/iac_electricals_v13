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



@frappe.whitelist()
def get_item(price_schedule):
	a=price_schedule
	z=frappe.db.get_value("Price Schedule Items",{'parent':a},['item_code','item_name','total_quantity','unit_price'])
	if z:
		return z
		print('z',z,'z')


# class PriceSchedule(Document):
def validate1(self):
	check_tax_temp_add_or_not_when_apply_charges(self)
	taxes_calculations(self)	


def check_tax_temp_add_or_not_when_apply_charges(self):
	try:
		if self.item_charges == "Item Level Freight Charge" or self.item_charges == "Lumpsum Amount":
			if not self.taxes_and_charges:
				frappe.throw(_('Please Add Tax Template.'))
			# if not self.taxes:
			# 	frappe.throw(_('Please Reselect Tax Template.'))
	except Exception as e:
		raise e	

def taxes_calculations(self,method=None):
	# if self.item_charges == "Item Level Freight Charge":
	# 	if self.taxes_and_charges:
	# 		try:
	# 			self.taxes = []
	# 			tax_items = []
	# 			tx_calculation = 0.0
	# 			total_tax_amount =0.0
	# 			tax_details = frappe.get_doc("Sales Taxes and Charges Template", self.taxes_and_charges).taxes
	# 			for taxes in tax_details:
	# 				tx_calculation = float(self.unit_freight_2_item_total_price + self.unit_freight_2_total_item_level_charge)/100*taxes.rate
	# 				if taxes.idx == 1:
	# 					total_tax_amount =float(self.unit_freight_2_item_total_price + self.unit_freight_2_total_item_level_charge) + tx_calculation
	# 				else:
	# 					total_tax_amount = total_tax_amount + tx_calculation


	# 				unit_price_1_tx_calculation = float(self.total+self.unit_freight_1_total_item_level_charge)/100*taxes.rate
	# 				if taxes.idx == 1:
	# 					unit_price_1_total_tax_amount =float(self.total+self.unit_freight_1_total_item_level_charge) + unit_price_1_tx_calculation
	# 				else:
	# 					unit_price_1_total_tax_amount = unit_price_1_total_tax_amount + unit_price_1_tx_calculation	

	# 				temp = {
	# 					'charge_type' : taxes.charge_type,
	# 					'account_head' : taxes.account_head,
	# 					'description' : taxes.description,
	# 					'rate' : taxes.rate,
	# 					'unit_price_2_tax_amount' : tx_calculation,
	# 					'unit_price_2_total':total_tax_amount,
	# 					'unit_price_1_tax_amount' : unit_price_1_tx_calculation,
	# 					'unit_price_1_total':unit_price_1_total_tax_amount
	# 				}
	# 				tax_items.append(temp)

	# 			unit_price_1_sum_tax_amt = 0
	# 			unit_price_2_sum_tax_amt = 0
	# 			for taxes in tax_items:
	# 				unit_price_1_sum_tax_amt += taxes["unit_price_1_tax_amount"]
	# 				unit_price_2_sum_tax_amt += taxes["unit_price_2_tax_amount"]
	# 				itm_tx = self.append('taxes')
	# 				itm_tx.charge_type = taxes["charge_type"]
	# 				itm_tx.account_head = taxes["account_head"]
	# 				itm_tx.description = taxes["description"]
	# 				itm_tx.rate = taxes["rate"]

	# 				itm_tx.tax_amount = taxes["unit_price_2_tax_amount"]
	# 				itm_tx.total = taxes["unit_price_2_total"]
	# 				itm_tx.unit_freight_price_1_tax_amount = taxes["unit_price_1_tax_amount"]
	# 				itm_tx.unit_freight_price_1_total = taxes["unit_price_1_total"]

	# 			self.unit_prce_1_total_value = self.total + self.unit_freight_1_total_item_level_charge	
	# 			self.unit_prce_2_total_value =	self.unit_freight_2_item_total_price + self.unit_freight_2_total_item_level_charge
	# 			self.unit_freight_price_1_total_taxes_and_charges = unit_price_1_sum_tax_amt
	# 			self.total_taxes_and_charges = unit_price_2_sum_tax_amt
	# 			self.unit_freight_price_1_grand_total = self.unit_prce_1_total_value + self.unit_freight_price_1_total_taxes_and_charges
	# 			self.grand_total = self.unit_prce_2_total_value + self.total_taxes_and_charges
	# 			self.unit_freight_price_1_rounded_total = round(self.unit_freight_price_1_grand_total)
	# 			self.rounded_total = round(self.grand_total)
	# 			self.unit_freight_price_1_in_words = frappe.utils.money_in_words(self.unit_freight_price_1_rounded_total,self.currency)
	# 			self.in_words = frappe.utils.money_in_words(self.rounded_total,self.currency)				
	# 		except Exception as e:
	# 			raise e

	# # if self.item_charges == "Lumpsum Amount":
	# 	if self.taxes_and_charges:
	# 		try:
	# 			self.taxes = []
	# 			tax_items = []
	# 			tx_calculation = 0.0
	# 			total_tax_amount =0.0
	# 			tax_details = frappe.get_doc("Sales Taxes and Charges Template", self.taxes_and_charges).taxes
	# 			for taxes in tax_details:
	# 				tx_calculation = float(self.unit_freight_2_item_total_price + self.on_unit_freight_2_lumpsum_amount)/100*taxes.rate
	# 				if taxes.idx == 1:
	# 					total_tax_amount =float(self.unit_freight_2_item_total_price + self.on_unit_freight_2_lumpsum_amount) + tx_calculation
	# 				else:
	# 					total_tax_amount = total_tax_amount + tx_calculation


	# 				unit_price_1_tx_calculation = float(self.total+self.on_unit_freight_1_lumpsum_amount)/100*taxes.rate
	# 				if taxes.idx == 1:
	# 					unit_price_1_total_tax_amount =float(self.total+self.on_unit_freight_1_lumpsum_amount) + unit_price_1_tx_calculation
	# 				else:
	# 					unit_price_1_total_tax_amount = unit_price_1_total_tax_amount + unit_price_1_tx_calculation	

	# 				temp = {
	# 					'charge_type' : taxes.charge_type,
	# 					'account_head' : taxes.account_head,
	# 					'description' : taxes.description,
	# 					'rate' : taxes.rate,
	# 					'unit_price_2_tax_amount' : tx_calculation,
	# 					'unit_price_2_total':total_tax_amount,
	# 					'unit_price_1_tax_amount' : unit_price_1_tx_calculation,
	# 					'unit_price_1_total':unit_price_1_total_tax_amount
	# 				}
	# 				tax_items.append(temp)

	# 			unit_price_1_sum_tax_amt = 0
	# 			unit_price_2_sum_tax_amt = 0
	# 			for taxes in tax_items:
	# 				unit_price_1_sum_tax_amt += taxes["unit_price_1_tax_amount"]
	# 				unit_price_2_sum_tax_amt += taxes["unit_price_2_tax_amount"]
	# 				itm_tx = self.append('taxes')
	# 				itm_tx.charge_type = taxes["charge_type"]
	# 				itm_tx.account_head = taxes["account_head"]
	# 				itm_tx.description = taxes["description"]
	# 				itm_tx.rate = taxes["rate"]

	# 				itm_tx.tax_amount = taxes["unit_price_2_tax_amount"]
	# 				itm_tx.total = taxes["unit_price_2_total"]
	# 				itm_tx.unit_freight_price_1_tax_amount = taxes["unit_price_1_tax_amount"]
	# 				itm_tx.unit_freight_price_1_total = taxes["unit_price_1_total"]

	# 			self.unit_prce_1_total_value = self.total + self.on_unit_freight_1_lumpsum_amount	
	# 			self.unit_prce_2_total_value =	self.unit_freight_2_item_total_price + self.on_unit_freight_2_lumpsum_amount
	# 			self.unit_freight_price_1_total_taxes_and_charges = unit_price_1_sum_tax_amt
	# 			self.total_taxes_and_charges = unit_price_2_sum_tax_amt
	# 			self.unit_freight_price_1_grand_total = self.unit_prce_1_total_value + self.unit_freight_price_1_total_taxes_and_charges
	# 			self.grand_total = self.unit_prce_2_total_value + self.total_taxes_and_charges
	# 			self.unit_freight_price_1_rounded_total = round(self.unit_freight_price_1_grand_total)
	# 			self.rounded_total = round(self.grand_total)
	# 			self.unit_freight_price_1_in_words = frappe.utils.money_in_words(self.unit_freight_price_1_rounded_total,self.currency)
	# 			self.in_words = frappe.utils.money_in_words(self.rounded_total,self.currency)				
	# 		except Exception as e:
	# 			raise e

	# if self.item_charges == "Not Applicable":
	if self.taxes_and_charges:
		try:
			self.taxes = []
			tax_items = []
			# qty=[]
			rate=[]
			freight=[]
			tx_calculation = 0.0
			total_tax_amount =0.0
			tax_details = frappe.get_doc("Sales Taxes and Charges Template", self.taxes_and_charges).taxes
			for i in self.items:
				# qty.append(int(i.qty))
				rate.append(float(i.rate)*i.qty)
				if i.freight_charges:
					freight.append(float(i.freight_charges)* i.qty)
			# qty = sum(qty)
			# rate = sum(rate)
			amount = sum(rate)	
			freight = sum(freight)
			total= amount + freight
			for taxes in tax_details:
			# 	tx_calculation = float(self.unit_freight_2_item_total_price)/100*taxes.rate
			# 	if taxes.idx == 1:
			# 		total_tax_amount =float(self.unit_freight_2_item_total_price) + tx_calculation
			# 	else:
			# 		total_tax_amount = total_tax_amount + tx_calculation


				unit_price_1_tx_calculation = float(total)/100*taxes.rate

				# if taxes.idx == 1:
				# 	unit_price_1_total_tax_amount =float(amount) + unit_price_1_tx_calculation
				# 	print('unit_price_1_total_tax_amount',unit_price_1_total_tax_amount,'unit_price_1_total_tax_amount')
				# else:
				# 	unit_price_1_total_tax_amount = unit_price_1_total_tax_amount + unit_price_1_tx_calculation	
				# 	print('unit_price_1_total_tax_amount',unit_price_1_total_tax_amount,'unit_price_1_total_tax_amount')

				temp = {
					'charge_type' : taxes.charge_type,
					'account_head' : taxes.account_head,
					'description' : taxes.description,
					'rate' : taxes.rate,
					'tax_amount':unit_price_1_tx_calculation
				}
				tax_items.append(temp)

			unit_price_1_sum_tax_amt = 0
			unit_price_2_sum_tax_amt = 0
			for taxes in tax_items:
				unit_price_1_sum_tax_amt += taxes["tax_amount"]
				
				itm_tx = self.append('taxes')
				itm_tx.charge_type = taxes["charge_type"]
				itm_tx.account_head = taxes["account_head"]
				itm_tx.description = taxes["description"]
				itm_tx.rate = taxes["rate"]

				itm_tx.tax_amount = taxes["tax_amount"]
				# itm_tx.total = taxes["unit_price_2_total"]
				# itm_tx.unit_freight_price_1_tax_amount = taxes["unit_price_1_tax_amount"]
				# itm_tx.unit_freight_price_1_total = taxes["unit_price_1_total"]

	# 		self.unit_prce_1_total_value = self.total	
	# 		self.unit_prce_2_total_value =	self.unit_freight_2_item_total_price
	# 		self.unit_freight_price_1_total_taxes_and_charges = unit_price_1_sum_tax_amt
	# 		self.total_taxes_and_charges = unit_price_2_sum_tax_amt
	# 		self.unit_freight_price_1_grand_total = self.unit_prce_1_total_value + self.unit_freight_price_1_total_taxes_and_charges
	# 		self.grand_total = self.unit_prce_2_total_value + self.total_taxes_and_charges
	# 		self.unit_freight_price_1_rounded_total = round(self.unit_freight_price_1_grand_total)
	# 		self.rounded_total = round(self.grand_total)
	# 		self.unit_freight_price_1_in_words = frappe.utils.money_in_words(self.unit_freight_price_1_rounded_total,self.currency)
	# 		self.in_words = frappe.utils.money_in_words(self.rounded_total,self.currency)				
		except Exception as e:
			raise e	
	# else:
	# 	try:
	# 		self.unit_prce_1_total_value = self.total	
	# 		self.unit_prce_2_total_value =	self.unit_freight_2_item_total_price
	# 		self.unit_freight_price_1_total_taxes_and_charges = 0
	# 		self.total_taxes_and_charges = 0
	# 		self.unit_freight_price_1_grand_total = self.unit_prce_1_total_value + self.unit_freight_price_1_total_taxes_and_charges
	# 		self.grand_total = self.unit_prce_2_total_value + self.total_taxes_and_charges
	# 		self.unit_freight_price_1_rounded_total = round(self.unit_freight_price_1_grand_total)
	# 		self.rounded_total = round(self.grand_total)
	# 		self.unit_freight_price_1_in_words = frappe.utils.money_in_words(self.unit_freight_price_1_rounded_total,self.currency)
	# 		self.in_words = frappe.utils.money_in_words(self.rounded_total,self.currency)				
	# 	except Exception as e:
	# 		raise e									

		