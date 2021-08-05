frappe.ui.form.on("Blanket Order", {
	refresh: function(frm) {
		$("[data-doctype='Quotation']").hide();
		
	}
})

cur_frm.cscript.custom_refresh= function(frm){
	$('.inner-group-button').find("[data-label='Quotation']").hide();
}