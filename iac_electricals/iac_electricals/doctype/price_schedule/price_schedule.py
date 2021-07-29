# Copyright (c) 2021, IAC Electricals and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc

class PriceSchedule(Document):
	pass

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
	doclist = get_mapped_doc("Price Schedule", source_name, {
		"Price Schedule": {
			"doctype": "Sales Order",
			"field_map": {
					"name":"price_schedule_no",
					"sales_taxes_and_charges_template":"taxes_and_charges",
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
			},
			"Sales Taxes and Charges Table": {
				"doctype": "Sales Taxes and Charges"
			},
		}, target_doc)

	return doclist	


