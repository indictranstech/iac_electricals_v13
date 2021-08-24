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
	query = frappe.db.sql("""SELECT 
				opp.name,DATE_FORMAT(opp.creation,"%d/%m/%Y") as eng_recvd_date,opp.sale_type,opp.country,opp.customer_name,opp.source,l.lead_owner,DATE_FORMAT(opp.tender_due_date,"%d/%m/%Y") as tdr_due_date,
				opp.tender_name,l.request_type,l.product_category,opp.offer_no,DATE_FORMAT(opp.offer_date,"%d/%m/%Y") as off_date,DATE_FORMAT(opp.offer_validity,"%d/%m/%Y") as off_validity,opp.price_basis,opp.currency,opp.price,opp.currency_in_lakhs,
				opp.contact_display,opp.contact_mobile,opp.contact_email
			from `tabOpportunity` opp
			LEFT OUTER JOIN `tabLead` l ON l.name = opp.party_name
			where {0} """.format(get_filters_codition(filters)), as_list = True)

	# query_data = []
	# for data in query:
	# 	contact_details = frappe.get_all('Dynamic Link', filters={'link_doctype': 'Lead', 'link_name': data.name, 'parenttype': 'Contact'}, fields=['parent'])
	# 	contact_doc = frappe.get_doc("Contact",contact_details[0].parent)
	# 	cnt = 0
	# 	for phone in contact_doc.phone_nos:
	# 		cnt = cnt + 1
	# 		if cnt == 1:
	# 			data['mobile_no'] = phone.get('phone')

	# 	cont = 0
	# 	for phone in contact_doc.email_ids:
	# 		cont = cont + 1
	# 		if cont == 1:
	# 			data['email_id'] = phone.get('email_id')		
		
	# 	query_data.append(data)
	return query

# Filters conditions
def get_filters_codition(filters):
	conditions = "1=1"
	if filters.get("from_date"):
		conditions += " and opp.creation >= '{0}'".format(filters.get('from_date'))
	if filters.get("to_date"):
		conditions += " and opp.creation <= '{0}'".format(filters.get('to_date'))
	if filters.get("sale_type"):
		conditions += " and opp.sale_type = '{0}'".format(filters.get('sale_type'))	

	return conditions

def get_columns(filters):
	columns = []
	columns.append({
		'fieldname': 'opp.name',
		'label': 'Opportunity Id',
		'fieldtype': 'Link',
		'options': 'Opportunity',
		'width': 180
		})
	columns.append({
		'fieldname': 'eng_recvd_date',
		'label': 'Enquiry Receievd Date',
		'fieldtype': 'Data',
		'options': '',
		'width': 120
		})
	columns.append({
		'fieldname': 'opp.sale_type',
		'label': 'Lead Type',
		'fieldtype': 'Data',
		'options': '',
		'align':'Left',
		'width': 120
		})
	columns.append({
		'fieldname': 'opp.country',
		'label': 'Country',
		'fieldtype': 'Data',
		'options': '',
		'align':'Left',
		'width': 120
		})
	columns.append({
		'fieldname': 'opp.customer_name',
		'label': 'Customer',
		'fieldtype': 'Data',
		'options': '',
		'width': 180
		})
	columns.append({
		'fieldname': 'opp.source',
		'label': 'Source',
		'fieldtype': 'Data',
		'options': '',
		'align':'Left',
		'width': 120
		})
	columns.append({
		'fieldname': 'l.lead_owner',
		'label': 'Owner',
		'fieldtype': 'Data',
		'options': '',
		'width': 150
		})
	columns.append({
		'fieldname': 'tdr_due_date',
		'label': 'Tender Due Date',
		'fieldtype': 'Data',
		'align':'Left',
		'width': 95
		})
	columns.append({
		'fieldname': 'opp.tender_name',
		'label': 'Tender/Project /Name',
		'fieldtype': 'Data',
		'align':'Left',
		'width': 180
		})
	columns.append({
		'fieldname': 'l.request_type',
		'label': 'KV Rating',
		'fieldtype': 'Data',
		'width': 180
		})
	columns.append({
		'fieldname': 'l.product_category',
		'label': 'Category of Items',
		'fieldtype': 'Data',
		'width': 180
		})
	columns.append({
		'fieldname': 'opp.offer_no',
		'label': 'Offer No',
		'fieldtype': 'Data',
		'align':'Left',
		'width': 140
		})
	columns.append({
		'fieldname': 'opp.off_date',
		'label': 'Offer Date',
		'fieldtype': 'Data',
		'align':'Left',
		'width': 100
		})
	columns.append({
		'fieldname': 'opp.off_validity',
		'label': 'Offer Validity',
		'fieldtype': 'Data',
		'align':'Left',	
		'width': 105
		})
	columns.append({
		'fieldname': 'opp.price_basis',
		'label': 'Price Basis',
		'fieldtype': 'Data',
		'align':'Left',
		'width': 95
		})
	columns.append({
		'fieldname': 'opp.currency',
		'label': 'Unit',
		'fieldtype': 'Data',
		'width': 75
		})
	columns.append({
		'fieldname': 'opp.price',
		'label': 'Price',
		'fieldtype': 'Currency',
		'width': 180
		})
	columns.append({
		'fieldname': 'opp.currency_in_lakhs',
		'label': 'Value In Lakhs',
		'fieldtype': 'Currency',
		'width': 180
		})
	columns.append({
		'fieldname': 'opp.contact_display',
		'label': 'Contact Person',
		'fieldtype': 'Data',
		'align':'Left',
		'width': 180
		})
	columns.append({
		'fieldname': 'opp.contact_mobile',
		'label': 'Contact No',
		'fieldtype': 'Data',
		'align':'Left',
		'width': 180
		})
	columns.append({
		'fieldname': 'opp.contact_email',
		'label': 'Mail Id',
		'fieldtype': 'Data',
		'align':'Left',
		'width': 180
		})
	return columns