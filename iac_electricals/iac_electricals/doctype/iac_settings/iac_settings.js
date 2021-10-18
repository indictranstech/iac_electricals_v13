// Copyright (c) 2021, IAC Electricals and contributors
// For license information, please see license.txt

frappe.ui.form.on('IAC Settings', {
	update_old_item: function(frm) {
		frappe.call({
			method: "iac_electricals.iac_electricals.custom_scripts.item.item.update_old_item_custom_naming_series_for_one_time"
		});
	}
});
