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

frappe.ui.form.on('Blanket Order', {
	refresh(frm) {
		refresh_field("items");
	},
	hiring_order:function(frm) {
	   if (frm.doc.price_schedule_) {
		frappe.call({
			method: "iac_electricals.iac_electricals.custom_scripts.blanket_order.blanket_order.get_item",
			args: {"price_schedule_":frm.doc.price_schedule_},
			callback: function(r) {console.log('r',r.message[0],'r');
				if (r.message){ console.log('Add Row in Items');
				var a = cur_frm.add_child("items");    
				a.item_code = r.message[0];
				a.item_name = r.message[1];
				a.qty = r.message[2];
				a.rate = r.message[3];

				};
			cur_frm.refresh_fields("items");	
		},
	});

	   
		   
	   
		
	} 
	
	
 }
 
})