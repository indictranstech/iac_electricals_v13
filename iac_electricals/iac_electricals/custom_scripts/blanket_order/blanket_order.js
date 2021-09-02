frappe.ui.form.on("Blanket Order", {
	refresh: function(frm) {
		$("[data-doctype='Quotation']").hide();
		
	}
})

frappe.ui.form.on('Blanket Order Item',{
	freight_charges_type :function(frm,cdt,cdn){
		var d  = locals[cdt][cdn];
		if(d.freight_charges_type == ""){
			frappe.model.set_value(d.doctype, d.name, "freight_charges", 0)
		}
	}
});

cur_frm.cscript.custom_refresh= function(frm){
	$('.inner-group-button').find("[data-label='Quotation']").hide();
}