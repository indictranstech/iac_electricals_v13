// Copyright (c) 2016, IAC Electricals and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Sales Order Report"] = {
	"filters": [
		{
			"fieldname": "sales_order_no",
			"label": __("Sales Order No"),
			"fieldtype": "Link",
			"options": "Sales Order"
		},
		{
			"fieldname": "customer",
			"label": __("Customer"),
			"fieldtype": "Link",
			"options": "Customer"
		},
		{
			"fieldname": "project",
			"label": __("Project"),
			"fieldtype": "Link",
			"options": "Project"
		},
		{
			"fieldname": "item_code",
			"label": __(" Item Code"),
			"fieldtype": "Link",
			"options": "Item"
		},
	]
};
