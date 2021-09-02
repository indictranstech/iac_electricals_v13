frappe.ui.form.on("Sales Invoice", {
	refresh: function(frm) {
	}
})

frappe.ui.form.on('Sales Invoice Item',{
	freight_charges_type :function(frm,cdt,cdn){
		var d  = locals[cdt][cdn];
		calculate_total(d);
	},
	freight_charges :function(frm,cdt,cdn){
		var d  = locals[cdt][cdn];
		calculate_total(d);
	},
	rate :function(frm,cdt,cdn){
		var d  = locals[cdt][cdn];
		calculate_total(d);
	},
	qty :function(frm,cdt,cdn){
		var d  = locals[cdt][cdn];
		calculate_total(d);
	},
});	

var calculate_total = function(d) {
	if(d.freight_charges_type == "Percent"){
		var total_itm_charge  = d.rate*d.freight_charges/100 * d.qty
		var _total_qty = d.qty*d.rate+ total_itm_charge
		frappe.model.set_value(d.doctype, d.name, "amount", _total_qty)
	}else if(d.freight_charges_type == "Amount"){
		var total_itm_charge  = d.freight_charges
		var _total_qty = d.qty*d.rate+ total_itm_charge
		frappe.model.set_value(d.doctype, d.name, "amount", _total_qty)
	}else{
		frappe.model.set_value(d.doctype, d.name, "freight_charges", 0)
		frappe.model.set_value(d.doctype, d.name, "amount", d.qty*d.rate)
	}

}