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
				name,DATE_FORMAT(creation,"%d/%m/%Y") as eng_recvd_date,lead_type,country_name,company_name,source,lead_owner,DATE_FORMAT(tender_due_date,"%d/%m/%Y") as tdr_due_date,
				tender_name,offer_no,DATE_FORMAT(off_date,"%d/%m/%Y") as off_date,DATE_FORMAT(off_validity,"%d/%m/%Y") as off_validity,price_basis,unit,price,value_in_lakhs,
				lead_name
			from `tabLead` where {0} """.format(get_filters_codition(filters)), as_dict = True)

	query_data = []
	for data in query:
		contact_details = frappe.get_all('Dynamic Link', filters={'link_doctype': 'Lead', 'link_name': data.name, 'parenttype': 'Contact'}, fields=['parent'])
		contact_doc = frappe.get_doc("Contact",contact_details[0].parent)
		cnt = 0
		for phone in contact_doc.phone_nos:
			cnt = cnt + 1
			if cnt == 1:
				data['mobile_no'] = phone.get('phone')

		cont = 0
		for phone in contact_doc.email_ids:
			cont = cont + 1
			if cont == 1:
				data['email_id'] = phone.get('email_id')		
		
		query_data.append(data)
	return query_data

# Filters conditions
def get_filters_codition(filters):
	conditions = "1=1"
	if filters.get("from_date"):
		conditions += " and creation >= '{0}'".format(filters.get('from_date'))
	if filters.get("to_date"):
		conditions += " and creation <= '{0}'".format(filters.get('to_date'))
	if filters.get("lead_type"):
		conditions += " and lead_type = '{0}'".format(filters.get('lead_type'))	

	return conditions

def get_columns(filters):
	columns = []
	columns.append({
		'fieldname': 'name',
		'label': 'Lead Id',
		'fieldtype': 'Link',
		'options': 'Lead',
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
		'fieldname': 'lead_type',
		'label': 'Lead Type',
		'fieldtype': 'Data',
		'options': '',
		'width': 120
		})
	columns.append({
		'fieldname': 'country_name',
		'label': 'Country',
		'fieldtype': 'Data',
		'options': '',
		'width': 120
		})
	columns.append({
		'fieldname': 'company_name',
		'label': 'Customer',
		'fieldtype': 'Data',
		'options': '',
		'width': 180
		})
	columns.append({
		'fieldname': 'source',
		'label': 'Source',
		'fieldtype': 'Data',
		'options': '',
		'width': 120
		})
	columns.append({
		'fieldname': 'lead_owner',
		'label': 'Owner',
		'fieldtype': 'Data',
		'options': '',
		'width': 150
		})
	columns.append({
		'fieldname': 'tdr_due_date',
		'label': 'Tender Due Date',
		'fieldtype': 'Data',
		'width': 95
		})
	columns.append({
		'fieldname': 'tender_name',
		'label': 'Tender/Project /Name',
		'fieldtype': 'Data',
		'width': 180
		})
	columns.append({
		'fieldname': 'offer_no',
		'label': 'Offer No',
		'fieldtype': 'Data',
		'width': 140
		})
	columns.append({
		'fieldname': 'off_date',
		'label': 'Offer Date',
		'fieldtype': 'Data',
		'width': 100
		})
	columns.append({
		'fieldname': 'off_validity',
		'label': 'Offer Validity',
		'fieldtype': 'Data',
		'width': 105
		})
	columns.append({
		'fieldname': 'price_basis',
		'label': 'Price Basis',
		'fieldtype': 'Data',
		'width': 95
		})
	columns.append({
		'fieldname': 'unit',
		'label': 'Unit',
		'fieldtype': 'Data',
		'width': 75
		})
	columns.append({
		'fieldname': 'price',
		'label': 'Price',
		'fieldtype': 'Currency',
		'width': 180
		})
	columns.append({
		'fieldname': 'value_in_lakhs',
		'label': 'Value In Lakhs',
		'fieldtype': 'Currency',
		'width': 180
		})
	columns.append({
		'fieldname': 'lead_name',
		'label': 'Contact Person',
		'fieldtype': 'Data',
		'width': 180
		})
	columns.append({
		'fieldname': 'mobile_no',
		'label': 'Contact No',
		'fieldtype': 'Data',
		'width': 180
		})
	columns.append({
		'fieldname': 'email_id',
		'label': 'Mail Id',
		'fieldtype': 'Data',
		'width': 180
		})
	return columns