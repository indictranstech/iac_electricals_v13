// Copyright (c) 2016, IAC Electricals and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Enquiry Tracker"] = {
	"filters": [
		{
			"label": __("From Date"),
			"fieldname":"from_date",
			"fieldtype": "Date",
			"default": frappe.datetime.add_months(frappe.datetime.month_start())
		},
		{
			"label": __("To Date"),
			"fieldname":"to_date",
			"fieldtype": "Date",
			"default": frappe.datetime.add_days(frappe.datetime.month_end())
		},
		{
			"fieldname": "sale_type",
			"label": __("Lead Type"),
			"fieldtype": "Select",
			"options": "\nDomestic Tender\nDomestic Purchase\nExport Tender\nExport Purchase"
		}
	]
};
