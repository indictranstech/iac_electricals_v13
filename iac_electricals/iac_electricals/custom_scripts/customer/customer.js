frappe.ui.form.on("Customer", {
	refresh: function(frm) {
		$("[data-doctype='Quotation']").hide();
	},
})


cur_frm.cscript.custom_refresh= function(frm){
	cur_frm.add_custom_button(("Price Schedule"), function() {
		frappe.model.open_mapped_doc({
			method: "iac_electricals.iac_electricals.custom_scripts.customer.customer.make_price_schedule",
			frm : cur_frm
		})
	}, __("Create"));
}