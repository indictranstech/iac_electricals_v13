// Copyright (c) 2021, IAC Electricals and contributors
// For license information, please see license.txt

frappe.ui.form.on('Item Series lavel 1', {
	validate: function(frm) {
		frm.set_value("item_code_name",cur_frm.doc.level_1_item_code);
	}
});
