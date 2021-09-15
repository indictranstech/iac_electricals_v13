// Copyright (c) 2021, IAC Electricals and contributors
// For license information, please see license.txt

frappe.ui.form.on('Inspection Call', {
	setup: function(frm) {
		frm.set_query('customer_address', function(doc) {
			return {
				filters: {
					'link_doctype': 'Customer',
					'link_name': doc.customer_name
				}
			}
		})

	}
	
});