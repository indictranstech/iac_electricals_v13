frappe.ui.form.on("Sales Order", {
	refresh: function(frm) {
	},
	validate: function(frm) {
		if(frm.doc.item_charges == "Item Level Freight Charge"){
			var freight_total_on_itm = 0
			frm.doc.items.forEach(d => {
				freight_total_on_itm = freight_total_on_itm + d.freight_charges_on_all_quantity
			})
			frm.set_value("freight_total", freight_total_on_itm);
		}else{
			frm.set_value("freight_total", 0);
		}
	},
	item_charges:function(frm){
		frm.set_value("freight_total", 0);
		frm.set_value("taxes_and_charges", "");
		cur_frm.clear_table("taxes");
		cur_frm.refresh_fields();
	}
})

frappe.ui.form.on('Sales Order Item',{
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
		var total_itm_charge  = d.rate*d.freight_charges/100
		frappe.model.set_value(d.doctype, d.name, "freight_charge_per_quantity", total_itm_charge)
		var _on_all_itm_charge = d.qty * d.freight_charge_per_quantity
		frappe.model.set_value(d.doctype, d.name, "freight_charges_on_all_quantity", _on_all_itm_charge)
	}else if(d.freight_charges_type == "Amount"){
		var total_itm_charge  = d.freight_charges
		frappe.model.set_value(d.doctype, d.name, "freight_charge_per_quantity", total_itm_charge)
		var _on_all_itm_charge = d.qty * d.freight_charge_per_quantity
		frappe.model.set_value(d.doctype, d.name, "freight_charges_on_all_quantity", _on_all_itm_charge)
	}else{
		frappe.model.set_value(d.doctype, d.name, "freight_charges", 0)
		frappe.model.set_value(d.doctype, d.name, "freight_charge_per_quantity", 0)
		frappe.model.set_value(d.doctype, d.name, "freight_charges_on_all_quantity", 0)
	}

}