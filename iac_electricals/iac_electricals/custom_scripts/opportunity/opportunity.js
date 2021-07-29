frappe.ui.form.on("Opportunity", {
	refresh: function(frm) {
		$(".inner-group-button").hide();
		/*cur_frm.remove_custom_button("Quotation", 'Create');*/
		/*$('.btn:contains("Create"):visible').hide();*/
		$("[data-doctype='Quotation']").hide();
		frm.add_custom_button(("Price Schedule"), function() {
			frappe.model.open_mapped_doc({
				method: "iac_electricals.iac_electricals.custom_scripts.opportunity.opportunity.make_price_schedule",
				frm : cur_frm
			})
		}, __("Create New"));
	},
})