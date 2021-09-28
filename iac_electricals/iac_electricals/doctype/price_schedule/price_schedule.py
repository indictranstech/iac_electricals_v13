# Copyright (c) 2021, IAC Electricals and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc

class PriceSchedule(Document):
	def validate(self):
		calculate_actual_item_amount(self)
		check_lumpsum_amount_add_or_not(self)
		calculate_item_level_freight_charge(self)
		check_tax_temp_add_or_not_when_apply_charges(self)
		taxes_calculations(self)

		

		for i in self.items:
			if i.freight_charges_type == "Percent" or i.freight_charges_type == "Amount":
				if i.freight_charges == 0 or i.freight_charges == None:
					frappe.throw("Please Enter First Freight Charges for row "+ str(i.idx)+" in Item Table")

			# if i.freight_charges != 0 or i.freight_charges != None:
			# 	print("########################")
			# 	if not i.freight_charges_type:
			# 		frappe.throw("Please Enter First Freight Charges type.........................for row "+ str(i.idx))	

			if i.freight_charges_type_ == "Percent" or i.freight_charges_type_ == "Amount":
				if i.freight_charges_ == 0 or i.freight_charges_ == None:
					frappe.throw("Please Enter Secound Freight Charges for row "+ str(i.idx)+" in Item Table")

			# if i.freight_charges_ != 0 or i.freight_charges_ != None:
			# 	if not i.freight_charges_type_:
			# 		frappe.throw("Please Enter Secound Freight Charges type.........................for row "+ str(i.idx))

def taxes_calculations(self):
	if self.item_charges == "Item Level Freight Charge":
		if self.sales_taxes_and_charges_template:
			try:
				self.sales_taxes_and_charges = []
				tax_items = []
				tx_calculation = 0.0
				total_tax_amount =0.0
				tax_details = frappe.get_doc("Sales Taxes and Charges Template", self.sales_taxes_and_charges_template).taxes
				for taxes in tax_details:
					tx_calculation = float(self.unit_freight_2_item_total_price + self.unit_freight_2_total_item_level_charge)/100*taxes.rate
					if taxes.idx == 1:
						total_tax_amount =float(self.unit_freight_2_item_total_price + self.unit_freight_2_total_item_level_charge) + tx_calculation
					else:
						total_tax_amount = total_tax_amount + tx_calculation


					unit_price_1_tx_calculation = float(self.total+self.unit_freight_1_total_item_level_charge)/100*taxes.rate
					if taxes.idx == 1:
						unit_price_1_total_tax_amount =float(self.total+self.unit_freight_1_total_item_level_charge) + unit_price_1_tx_calculation
					else:
						unit_price_1_total_tax_amount = unit_price_1_total_tax_amount + unit_price_1_tx_calculation	

					temp = {
						'charge_type' : taxes.charge_type,
						'account_head' : taxes.account_head,
						'description' : taxes.description,
						'rate' : taxes.rate,
						'unit_price_2_tax_amount' : tx_calculation,
						'unit_price_2_total':total_tax_amount,
						'unit_price_1_tax_amount' : unit_price_1_tx_calculation,
						'unit_price_1_total':unit_price_1_total_tax_amount
					}
					tax_items.append(temp)

				unit_price_1_sum_tax_amt = 0
				unit_price_2_sum_tax_amt = 0
				for taxes in tax_items:
					unit_price_1_sum_tax_amt += taxes["unit_price_1_tax_amount"]
					unit_price_2_sum_tax_amt += taxes["unit_price_2_tax_amount"]
					itm_tx = self.append('sales_taxes_and_charges')
					itm_tx.charge_type = taxes["charge_type"]
					itm_tx.account_head = taxes["account_head"]
					itm_tx.description = taxes["description"]
					itm_tx.rate = taxes["rate"]

					itm_tx.tax_amount = taxes["unit_price_2_tax_amount"]
					itm_tx.total = taxes["unit_price_2_total"]
					itm_tx.unit_freight_price_1_tax_amount = taxes["unit_price_1_tax_amount"]
					itm_tx.unit_freight_price_1_total = taxes["unit_price_1_total"]

				self.unit_prce_1_total_value = self.total + self.unit_freight_1_total_item_level_charge	
				self.unit_prce_2_total_value =	self.unit_freight_2_item_total_price + self.unit_freight_2_total_item_level_charge
				self.unit_freight_price_1_total_taxes_and_charges = unit_price_1_sum_tax_amt
				self.total_taxes_and_charges = unit_price_2_sum_tax_amt
				self.unit_freight_price_1_grand_total = self.unit_prce_1_total_value + self.unit_freight_price_1_total_taxes_and_charges
				self.grand_total = self.unit_prce_2_total_value + self.total_taxes_and_charges
				self.unit_freight_price_1_rounded_total = round(self.unit_freight_price_1_grand_total)
				self.rounded_total = round(self.grand_total)
				self.unit_freight_price_1_in_words = frappe.utils.money_in_words(self.unit_freight_price_1_rounded_total,self.currency)
				self.in_words = frappe.utils.money_in_words(self.rounded_total,self.currency)				
			except Exception as e:
				raise e

	if self.item_charges == "Lumpsum Amount":
		if self.sales_taxes_and_charges_template:
			try:
				self.sales_taxes_and_charges = []
				tax_items = []
				tx_calculation = 0.0
				total_tax_amount =0.0
				tax_details = frappe.get_doc("Sales Taxes and Charges Template", self.sales_taxes_and_charges_template).taxes
				for taxes in tax_details:
					tx_calculation = float(self.unit_freight_2_item_total_price + self.on_unit_freight_2_lumpsum_amount)/100*taxes.rate
					if taxes.idx == 1:
						total_tax_amount =float(self.unit_freight_2_item_total_price + self.on_unit_freight_2_lumpsum_amount) + tx_calculation
					else:
						total_tax_amount = total_tax_amount + tx_calculation


					unit_price_1_tx_calculation = float(self.total+self.on_unit_freight_1_lumpsum_amount)/100*taxes.rate
					if taxes.idx == 1:
						unit_price_1_total_tax_amount =float(self.total+self.on_unit_freight_1_lumpsum_amount) + unit_price_1_tx_calculation
					else:
						unit_price_1_total_tax_amount = unit_price_1_total_tax_amount + unit_price_1_tx_calculation	

					temp = {
						'charge_type' : taxes.charge_type,
						'account_head' : taxes.account_head,
						'description' : taxes.description,
						'rate' : taxes.rate,
						'unit_price_2_tax_amount' : tx_calculation,
						'unit_price_2_total':total_tax_amount,
						'unit_price_1_tax_amount' : unit_price_1_tx_calculation,
						'unit_price_1_total':unit_price_1_total_tax_amount
					}
					tax_items.append(temp)

				unit_price_1_sum_tax_amt = 0
				unit_price_2_sum_tax_amt = 0
				for taxes in tax_items:
					unit_price_1_sum_tax_amt += taxes["unit_price_1_tax_amount"]
					unit_price_2_sum_tax_amt += taxes["unit_price_2_tax_amount"]
					itm_tx = self.append('sales_taxes_and_charges')
					itm_tx.charge_type = taxes["charge_type"]
					itm_tx.account_head = taxes["account_head"]
					itm_tx.description = taxes["description"]
					itm_tx.rate = taxes["rate"]

					itm_tx.tax_amount = taxes["unit_price_2_tax_amount"]
					itm_tx.total = taxes["unit_price_2_total"]
					itm_tx.unit_freight_price_1_tax_amount = taxes["unit_price_1_tax_amount"]
					itm_tx.unit_freight_price_1_total = taxes["unit_price_1_total"]

				self.unit_prce_1_total_value = self.total + self.on_unit_freight_1_lumpsum_amount	
				self.unit_prce_2_total_value =	self.unit_freight_2_item_total_price + self.on_unit_freight_2_lumpsum_amount
				self.unit_freight_price_1_total_taxes_and_charges = unit_price_1_sum_tax_amt
				self.total_taxes_and_charges = unit_price_2_sum_tax_amt
				self.unit_freight_price_1_grand_total = self.unit_prce_1_total_value + self.unit_freight_price_1_total_taxes_and_charges
				self.grand_total = self.unit_prce_2_total_value + self.total_taxes_and_charges
				self.unit_freight_price_1_rounded_total = round(self.unit_freight_price_1_grand_total)
				self.rounded_total = round(self.grand_total)
				self.unit_freight_price_1_in_words = frappe.utils.money_in_words(self.unit_freight_price_1_rounded_total,self.currency)
				self.in_words = frappe.utils.money_in_words(self.rounded_total,self.currency)				
			except Exception as e:
				raise e

	if self.item_charges == "Not Applicable":
		if self.sales_taxes_and_charges_template:
			try:
				self.sales_taxes_and_charges = []
				tax_items = []
				tx_calculation = 0.0
				total_tax_amount =0.0
				tax_details = frappe.get_doc("Sales Taxes and Charges Template", self.sales_taxes_and_charges_template).taxes
				for taxes in tax_details:
					tx_calculation = float(self.unit_freight_2_item_total_price)/100*taxes.rate
					if taxes.idx == 1:
						total_tax_amount =float(self.unit_freight_2_item_total_price) + tx_calculation
					else:
						total_tax_amount = total_tax_amount + tx_calculation


					unit_price_1_tx_calculation = float(self.total)/100*taxes.rate
					if taxes.idx == 1:
						unit_price_1_total_tax_amount =float(self.total) + unit_price_1_tx_calculation
					else:
						unit_price_1_total_tax_amount = unit_price_1_total_tax_amount + unit_price_1_tx_calculation	

					temp = {
						'charge_type' : taxes.charge_type,
						'account_head' : taxes.account_head,
						'description' : taxes.description,
						'rate' : taxes.rate,
						'unit_price_2_tax_amount' : tx_calculation,
						'unit_price_2_total':total_tax_amount,
						'unit_price_1_tax_amount' : unit_price_1_tx_calculation,
						'unit_price_1_total':unit_price_1_total_tax_amount
					}
					tax_items.append(temp)

				unit_price_1_sum_tax_amt = 0
				unit_price_2_sum_tax_amt = 0
				for taxes in tax_items:
					unit_price_1_sum_tax_amt += taxes["unit_price_1_tax_amount"]
					unit_price_2_sum_tax_amt += taxes["unit_price_2_tax_amount"]
					itm_tx = self.append('sales_taxes_and_charges')
					itm_tx.charge_type = taxes["charge_type"]
					itm_tx.account_head = taxes["account_head"]
					itm_tx.description = taxes["description"]
					itm_tx.rate = taxes["rate"]

					itm_tx.tax_amount = taxes["unit_price_2_tax_amount"]
					itm_tx.total = taxes["unit_price_2_total"]
					itm_tx.unit_freight_price_1_tax_amount = taxes["unit_price_1_tax_amount"]
					itm_tx.unit_freight_price_1_total = taxes["unit_price_1_total"]

				self.unit_prce_1_total_value = self.total	
				self.unit_prce_2_total_value =	self.unit_freight_2_item_total_price
				self.unit_freight_price_1_total_taxes_and_charges = unit_price_1_sum_tax_amt
				self.total_taxes_and_charges = unit_price_2_sum_tax_amt
				self.unit_freight_price_1_grand_total = self.unit_prce_1_total_value + self.unit_freight_price_1_total_taxes_and_charges
				self.grand_total = self.unit_prce_2_total_value + self.total_taxes_and_charges
				self.unit_freight_price_1_rounded_total = round(self.unit_freight_price_1_grand_total)
				self.rounded_total = round(self.grand_total)
				self.unit_freight_price_1_in_words = frappe.utils.money_in_words(self.unit_freight_price_1_rounded_total,self.currency)
				self.in_words = frappe.utils.money_in_words(self.rounded_total,self.currency)				
			except Exception as e:
				raise e	
		else:
			try:
				self.unit_prce_1_total_value = self.total	
				self.unit_prce_2_total_value =	self.unit_freight_2_item_total_price
				self.unit_freight_price_1_total_taxes_and_charges = 0
				self.total_taxes_and_charges = 0
				self.unit_freight_price_1_grand_total = self.unit_prce_1_total_value + self.unit_freight_price_1_total_taxes_and_charges
				self.grand_total = self.unit_prce_2_total_value + self.total_taxes_and_charges
				self.unit_freight_price_1_rounded_total = round(self.unit_freight_price_1_grand_total)
				self.rounded_total = round(self.grand_total)
				self.unit_freight_price_1_in_words = frappe.utils.money_in_words(self.unit_freight_price_1_rounded_total,self.currency)
				self.in_words = frappe.utils.money_in_words(self.rounded_total,self.currency)				
			except Exception as e:
				raise e									

def calculate_item_level_freight_charge(self):
	try:
		if self.item_charges == "Item Level Freight Charge":
			itm_1_freight_total = 0
			itm_2_freight_total = 0
			for i in self.items:
				itm_1_freight_total += i.freight_charges_on_all_quantity
				itm_2_freight_total += i.freight_charges_on_all_quantity_

			self.unit_freight_1_total_item_level_charge = itm_1_freight_total
			self.unit_freight_2_total_item_level_charge = itm_2_freight_total
		else:
			self.unit_freight_1_total_item_level_charge = 0
			self.unit_freight_2_total_item_level_charge = 0
	except Exception as e:
		raise e


def calculate_actual_item_amount(self):
	try:
		itm_1_total = 0
		itm_2_total = 0
		for i in self.items:
			itm_1_total += i.total_value
			itm_2_total += i.total

		self.total = itm_1_total
		self.unit_freight_2_item_total_price = itm_2_total
	except Exception as e:
		raise e

def check_lumpsum_amount_add_or_not(self):
	try:
		if self.item_charges == "Lumpsum Amount":
			if not self.on_unit_freight_1_lumpsum_amount:
				frappe.throw("Please Enter Lumpsum Amount for Unit Freight 1.")
			# if not self.on_unit_freight_2_lumpsum_amount::
			# 	frappe.throw("Please Enter Lumpsum Amount for Unit Freight 2.")	
		else:
			self.on_unit_freight_1_lumpsum_amount = 0
			self.on_unit_freight_2_lumpsum_amount = 0
	except Exception as e:
		raise e

def check_tax_temp_add_or_not_when_apply_charges(self):
	try:
		if self.item_charges == "Item Level Freight Charge" or self.item_charges == "Lumpsum Amount":
			if not self.sales_taxes_and_charges_template:
				frappe.throw(_('Please Add Tax Template.'))
			# if not self.sales_taxes_and_charges:
			# 	frappe.throw(_('Please Reselect Tax Template.'))
	except Exception as e:
		raise e		


@frappe.whitelist()
def address_query(name):
	if name:
		address_lists = frappe.db.get_all("Address",{'name':name},["name","address_line1","address_line2","city","state","country","pincode"])
		if address_lists:
			return address_lists

@frappe.whitelist()
def contact_query(name):
	if name:
		contact_info = {
			'mobile_no' :'',
			'email' :'',
			'first_name':'',
			'middle_name':'',
			'last_name':'' 
		}
		contact_doc = frappe.get_doc("Contact",name)
		if contact_doc:		
			contact_info['first_name'] = contact_doc.get('first_name')
			contact_info['middle_name'] = contact_doc.get('middle_name')
			contact_info['last_name'] = contact_doc.get('last_name')
			for phone in contact_doc.phone_nos:
				if phone.get('is_primary_mobile_no'):
					contact_info['mobile_no'] = phone.get('phone')
			for email in contact_doc.email_ids:
				if email.get('is_primary'):
					contact_info['email'] = email.get('email_id')		
			return contact_info		


@frappe.whitelist()
def fetch_address_contact_name(name):
	if name:
		address_contact_name = {
			'address_name' :'',
			'contact_name' :'' 
		}
		add_name = frappe.get_all('Dynamic Link', filters={'link_doctype': 'Customer', 'link_name': name, 'parenttype': 'Address'}, fields=['parent'])
		con_name = frappe.get_all('Dynamic Link', filters={'link_doctype': 'Customer', 'link_name': name, 'parenttype': 'Contact'}, fields=['parent'])
		if add_name:
			address_contact_name['address_name'] = add_name[0].get('parent')
		if con_name:
			address_contact_name['contact_name'] = con_name[0].get('parent')
		return address_contact_name


@frappe.whitelist()
def number_to_word(amount):
	def get_word(n):
		words={ 0:"", 1:"One", 2:"Two", 3:"Three", 4:"Four", 5:"Five", 6:"Six", 7:"Seven", 8:"Eight", 9:"Nine", 10:"Ten", 11:"Eleven", 12:"Twelve", 13:"Thirteen", 14:"Fourteen", 15:"Fifteen", 16:"Sixteen", 17:"Seventeen", 18:"Eighteen", 19:"Nineteen", 20:"Twenty", 30:"Thirty", 40:"Forty", 50:"Fifty", 60:"Sixty", 70:"Seventy", 80:"Eighty", 90:"Ninty" }
		if n<=20:
			return words[n]
		else:
			ones=n%10
			tens=n-ones
			return words[tens]+" "+words[ones]

	def get_all_word(n):
		d=[100,10,100,100]
		v=["","Hundred And","Thousand","lakh"]
		w=[]
		for i,x in zip(d,v):
			t=get_word(n%i)
			if t!="":
				t+=" "+x
			w.append(t.rstrip(" "))
			n=n//i
		w.reverse()
		w=' '.join(w).strip()
		if w.endswith("And"):
			w=w[:-3]
		return w

	arr=str(amount).split(".")
	amount=int(arr[0])
	crore=amount//10000000
	amount=amount%10000000
	word=""
	if crore>0:
		word+=get_all_word(crore)
		word+=" crore "
	word+=get_all_word(amount).strip()+" only."
	if len(arr)>1:
		if len(arr[1])==1:
			arr[1]+="0"
		word+=" and "+get_all_word(int(arr[1]))+" paisa"
	
	return word


@frappe.whitelist()
def calculate_taxes(tax_temlet_name,total_amount,unit_price_1_total_amount):
	try:
		tax_items = []
		tx_calculation = 0.0
		total_tax_amount =0.0
		tax_details = frappe.get_doc("Sales Taxes and Charges Template", tax_temlet_name).taxes
		for taxes in tax_details:
			tx_calculation = float(total_amount)/100*taxes.rate
			if taxes.idx == 1:
				total_tax_amount =float(total_amount) + tx_calculation
			else:
				total_tax_amount = total_tax_amount + tx_calculation


			unit_price_1_tx_calculation = float(unit_price_1_total_amount)/100*taxes.rate
			if taxes.idx == 1:
				unit_price_1_total_tax_amount =float(unit_price_1_total_amount) + unit_price_1_tx_calculation
			else:
				unit_price_1_total_tax_amount = unit_price_1_total_tax_amount + unit_price_1_tx_calculation	

			temp = {
				'charge_type' : taxes.charge_type,
				'account_head' : taxes.account_head,
				'description' : taxes.description,
				'rate' : taxes.rate,
				'unit_price_2_tax_amount' : tx_calculation,
				'unit_price_2_total':total_tax_amount,
				'unit_price_1_tax_amount' : unit_price_1_tx_calculation,
				'unit_price_1_total':unit_price_1_total_tax_amount
			}
			tax_items.append(temp)
		return tax_items
	except Exception as e:
		raise e


@frappe.whitelist()
def make_blanket_order(source_name, target_doc=None, ignore_permissions=False):
	frappe.log_error(frappe.get_traceback(), _("Blanket order Button clicked....(Error_log)"))
	doclist = get_mapped_doc("Price Schedule", source_name, {
		"Price Schedule": {
			"doctype": "Blanket Order",
			"field_map": {
					"name": "Price Schedule",
					"name":"price_schedule_no",
					"terms":"tc_name",
					"term_details":"terms"
				},
			"validation": {
					"docstatus": ["=", 1]
				}
			},
			"Price Schedule Items": {
				"doctype": "Blanket Order Item",
				"field_map": {
					"total_quantity": "qty"
				},
			},
		}, target_doc)

	return doclist


@frappe.whitelist()
def make_sales_order(source_name, target_doc=None, ignore_permissions=False):
	def set_missing_values(source, target):
		target.against_price_schedule = 1
	def update_item(source_doc, target_doc, source_parent):
		target_doc.against_price_schedule = 1
		target_doc.price_schedule = source_name

	doclist = get_mapped_doc("Price Schedule", source_name, {
		"Price Schedule": {
			"doctype": "Sales Order",
			"field_map": {
					"name":"price_schedule_no",
					# "sales_taxes_and_charges_template":"taxes_and_charges",
					"contact_person_mobile_no":"contact_mobile",
					"terms":"tc_name",
					"term_details":"terms"
				},
			"validation": {
					"docstatus": ["=", 1]
				}
			},
			"Price Schedule Items": {
				"doctype": "Sales Order Item",
				"field_map": {
					"total_quantity": "qty"
				},
				"postprocess": update_item
			},
			# "Sales Taxes and Charges Table": {
			# 	"doctype": "Sales Taxes and Charges"
			# },
		}, target_doc, set_missing_values)

	return doclist	


