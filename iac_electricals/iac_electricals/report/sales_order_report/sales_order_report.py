# Copyright (c) 2013, IAC Electricals and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
import json
from erpnext.accounts.utils import flt
from datetime import datetime

def execute(filters=None):
	columns = get_columns(filters)
	data = get_data(filters)
	return columns, data
	
def get_data(filters):
	conditions = get_filters_codition(filters)
	customer_dict = frappe.db.sql("""SELECT * from `tabCustomer` """, as_dict=1)
	customer_list = tuple([row.get("name") for row in customer_dict])
	blanket_order_dict1 = "SELECT name as blanket_order from `tabBlanket Order` where customer in {0}".format(customer_list)
	blanket_order_dict = frappe.db.sql(blanket_order_dict1,as_dict=1)
	blanket_order_list = tuple([row.get("blanket_order") for row in blanket_order_dict])

	sales_order_list = "SELECT  so.name as sales_order, so.customer as customer_name, so.project, soi.item_code, soi.item_name , soi.qty , soi.rate, soi.amount, soi.blanket_order from `tabSales Order` so join `tabSales Order Item` soi on soi.parent = so.name where soi.blanket_order in {0} and {1}".format(blanket_order_list,conditions)
	sales_order_dict = frappe.db.sql(sales_order_list,as_dict=1)
	sales_order = tuple([row.get("sales_order") for row in sales_order_dict])
	
	if not len(list(sales_order)) == 0 :
		if len(list(sales_order)) == 1 :
			sales_list_single = list(sales_order)[0]
			delivery_note_list = "SELECT  dn.name as delivery_note , dni.item_code, dni.item_name, dni.qty , dni.against_sales_order from `tabDelivery Note` dn join `tabDelivery Note Item` dni on dni.parent = dn.name where dni.against_sales_order = '{0}' ".format(sales_list_single)
		else:
			delivery_note_list = "SELECT  dn.name as delivery_note , dni.item_code, dni.item_name, dni.qty , dni.against_sales_order from `tabDelivery Note` dn join `tabDelivery Note Item` dni on dni.parent = dn.name where dni.against_sales_order in {0}".format(sales_order)
		delivery_note_dict = frappe.db.sql(delivery_note_list,as_dict=1)
		delivery_note = tuple([row.get("delivery_note") for row in delivery_note_dict])


		if not len(list(delivery_note)) == 0:
			if len(list(delivery_note)) == 1:
				delivery_list_single = list(delivery_note)[0]
				sales_invoice_list = "SELECT  si.name as sales_invoice , sii.item_code, sii.item_name, sii.qty, sii.delivery_note , sii.sales_order from `tabSales Invoice` si join `tabSales Invoice Item` sii on sii.parent = si.name where sii.delivery_note = '{0}' ".format(delivery_list_single)
				
			else:
				sales_invoice_list = "SELECT  si.name as sales_invoice , sii.item_code, sii.item_name, sii.qty, sii.delivery_note , sii.sales_order from `tabSales Invoice` si join `tabSales Invoice Item` sii on sii.parent = si.name where sii.delivery_note in {0}".format(delivery_note)
			sales_invoice_dict = frappe.db.sql(sales_invoice_list,as_dict=1)
			sales_invoice = tuple([row.get("sales_invoice") for row in sales_invoice_dict])


			for row in sales_order_dict:
				for row1 in delivery_note_dict:
					if row.get('sales_order') == row1.get('against_sales_order'):
						row['delivery_note'] = (row1.get('delivery_note'))
				
			for row in sales_order_dict:
				for row2 in sales_invoice_dict:
						if row.get('sales_order') == row2.get('sales_order'):
							row['sales_invoice'] = (row2.get('sales_invoice'))

		else:
			delivery_note_list = "SELECT  dn.name as delivery_note , dni.item_code, dni.item_name, dni.qty , dni.against_sales_order from `tabDelivery Note` dn join `tabDelivery Note Item` dni on dni.parent = dn.name where dni.against_sales_order in {0}".format(sales_order)
			delivery_note_dict = frappe.db.sql(delivery_note_list,as_dict=1)
			delivery_note = tuple([row.get("delivery_note") for row in delivery_note_dict])


			if not len(list(delivery_note)) == 0:
				sales_invoice_list = "SELECT  si.name as sales_invoice , sii.item_code, sii.item_name, sii.qty, sii.delivery_note , sii.sales_order from `tabSales Invoice` si join `tabSales Invoice Item` sii on sii.parent = si.name where sii.delivery_note in {0}".format(delivery_note)
				sales_invoice_dict = frappe.db.sql(sales_invoice_list,as_dict=1)
				sales_invoice = tuple([row.get("sales_invoice") for row in sales_invoice_dict])
				
				for row in sales_order_dict:
					for row1 in delivery_note_dict:
						if row.get('sales_order') == row1.get('against_sales_order'):
							row['delivery_note'] = (row1.get('delivery_note'))
					
				for row in sales_order_dict:
					for row2 in sales_invoice_dict:
							if row.get('sales_order') == row2.get('sales_order'):
								row['sales_invoice'] = (row2.get('sales_invoice'))

	return sales_order_dict
	


# Filters conditions
def get_filters_codition(filters):
	conditions = "1=1"
	if filters.get("sales_order_no"):
		conditions += " and so.name = '{0}'".format(filters.get('sales_order_no'))
	if filters.get("customer"):
		conditions += " and customer = '{0}'".format(filters.get('customer'))
	if filters.get("project"):
		conditions += " and project = '{0}'".format(filters.get('project'))	
	if filters.get("item_code"):
		conditions += " and item_code = '{0}'".format(filters.get('item_code'))	
	return conditions


def get_columns(filters):
	columns = []
	columns.append({
		'fieldname': 'customer_name',
		'label': 'Customer Id',
		'fieldtype': 'Link',
		'options': 'Customer',
		'width': 180
		})
	columns.append({
		'fieldname': 'item_code',
		'label': 'Item Code',
		'fieldtype': 'Link',
		'options': 'Item',
		'width': 180
		})
	columns.append({
		'fieldname': 'item_name',
		'label': 'Item Name',
		'fieldtype': 'Data',
		# 'options': '',
		'width': 180
		})
	columns.append({
		'fieldname': 'qty',
		'label': 'Quantity',
		'fieldtype': 'Int',
		# 'options': 'Item',
		'width': 180
		})
	columns.append({
		'fieldname': 'rate',
		'label': 'Rate',
		'fieldtype': 'Currency',
		# 'options': 'Item',
		'width': 180
		})
	columns.append({
		'fieldname': 'amount',
		'label': 'Amount',
		'fieldtype': 'Currency',
		# 'options': 'Item',
		'width': 180
		})
	columns.append({
		'fieldname': 'project',
		'label': 'Project',
		'fieldtype': 'Link',
		'options': 'Project',
		'width': 180
		})
	columns.append({
		'fieldname': 'blanket_order',
		'label': 'Blanket Order',
		'fieldtype': 'Link',
		'options': 'Blanket Order',
		'width': 120
		})
	columns.append({
		'fieldname': 'sales_order',
		'label': 'Sales Order',
		'fieldtype': 'Link',
		'options': 'Sales Order',
		'width': 120
		})
	columns.append({
		'fieldname': 'delivery_note',
		'label': 'Delivery Note',
		'fieldtype': 'Link',
		'options': 'Delivery Note',
		'width': 120
		})
	columns.append({
		'fieldname': 'sales_invoice',
		'label': 'Sales Invoice',
		'fieldtype': 'Link',
		'options': 'Sales Invoice',
		'width': 120
		})
	return columns
