frappe.ui.form.on("Purchase Invoice", {
	project: function(frm, cdt, cdn) {
		if(!frm.doc.delivery_date) {
			erpnext.utils.copy_value_in_all_rows(frm.doc, cdt, cdn, "items", "project");
		}
	},
	delivery_address: function(frm) {
		erpnext.utils.get_address_display(frm, "delivery_address", "delivery_address_display");
	}
})