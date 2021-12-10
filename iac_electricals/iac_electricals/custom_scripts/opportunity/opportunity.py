# Copyright (c) 2021, IAC Electricals and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc


from frappe.utils import flt, add_days
from frappe.utils import get_datetime_str, nowdate
from erpnext import get_default_company

def validate(doc,method=None):
	doc.offer_no = doc.name
	if doc.exchange_rate == 0:
		default_company = frappe.db.get_single_value('Global Defaults', 'default_company')
		company_default_currency = frappe.db.get_value("Company", default_company, 'default_currency')
		frappe.throw(_('Unable to find exchange rate for '+doc.currency+' to '+company_default_currency +'. Please create a Currency Exchange record manually.'))

	if not doc.currency:
		frappe.throw(_(' Please select Currency.'))

def after_insert(doc,method=None):
	doc.offer_no = doc.name


@frappe.whitelist()
def make_price_schedule(source_name, target_doc=None, ignore_permissions=False):
	doclist = get_mapped_doc("Opportunity", source_name, {
		"Opportunity": {
			"doctype": "Price Schedule",
			"field_map": {
					"opportunity_from":"quotation_to",
					"customer_name":"customer",
					"name":"opportunity"
				},
			"validation": {
					"docstatus": ["=", 0]
				}
			}
		}, target_doc)
	opp_doc = frappe.get_doc("Opportunity", source_name)
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

@frappe.whitelist()
def get_exchange_rate_(from_currency, transaction_date=None, args=None):

	default_company = frappe.db.get_single_value('Global Defaults', 'default_company')
	to_currency = frappe.db.get_value("Company", default_company, 'default_currency')

	if not (from_currency and to_currency):
		# manqala 19/09/2016: Should this be an empty return or should it throw and exception?
		return
	if from_currency == to_currency:
		return 1

	if not transaction_date:
		transaction_date = nowdate()
	currency_settings = frappe.get_doc("Accounts Settings").as_dict()
	allow_stale_rates = currency_settings.get("allow_stale")

	filters = [
		["date", "<=", get_datetime_str(transaction_date)],
		["from_currency", "=", from_currency],
		["to_currency", "=", to_currency]
	]

	if args == "for_buying":
		filters.append(["for_buying", "=", "1"])
	elif args == "for_selling":
		filters.append(["for_selling", "=", "1"])

	if not allow_stale_rates:
		stale_days = currency_settings.get("stale_days")
		checkpoint_date = add_days(transaction_date, -stale_days)
		filters.append(["date", ">", get_datetime_str(checkpoint_date)])

	# cksgb 19/09/2016: get last entry in Currency Exchange with from_currency and to_currency.
	entries = frappe.get_all(
		"Currency Exchange", fields=["exchange_rate"], filters=filters, order_by="date desc",
		limit=1)
	if entries:
		return flt(entries[0].exchange_rate)

	try:
		cache = frappe.cache()
		key = "currency_exchange_rate_{0}:{1}:{2}".format(transaction_date,from_currency, to_currency)
		value = cache.get(key)

		if not value:
			import requests
			api_url = "https://frankfurter.app/{0}".format(transaction_date)
			response = requests.get(api_url, params={
				"base": from_currency,
				"symbols": to_currency
			})
			# expire in 6 hours
			response.raise_for_status()
			value = response.json()["rates"][to_currency]

			cache.set_value(key, value, expires_in_sec=6 * 60 * 60)
		return flt(value)
	except:
		frappe.log_error(title="Get Exchange Rate")
		return 0.0


