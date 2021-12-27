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
frappe.ui.form.on("Purchase Invoice Item", "qty_stock", function(frm, cdt, cdn) {
	$.each(frm.doc.items || [], function(i, d) {
	if (d.stock_uom!=d.uom){    
	d.conversion_factor=d.qty_stock/d.qty;
	d.price_list_rate=d.rate_kg*(d.qty_stock/d.qty);
	d.discount_percentage=0;
	d.discount_amount=0;
	d.rate=d.rate_kg*d.conversion_factor;
	d.amount=d.qty_stock*d.rate_kg;
	d.base_amount=d.qty_stock*d.rate_kg;
	}
	else{
	 d.conversion_factor=1;
	 d.qty_stock=d.qty;
	 d.price_list_rate=d.rate_kg*d.conversion_factor;
	d.discount_percentage=0;
	d.discount_amount=0;
	d.rate=d.rate_kg*d.conversion_factor;
	d.amount=d.qty_stock*d.rate_kg;
	d.base_amount=d.qty_stock*d.rate_kg;
	}
	});
	refresh_field("items");
	})
	// frappe.ui.form.on("Purchase Order", "validate", function(frm, cdt, cdn) {
	// $.each(frm.doc.items || [], function(i, d) {
	// if (d.stock_uom!=d.uom){
	// d.conversion_factor=d.qty_stock/d.qty;
	// }
	// else{
	//  d.conversion_factor=1;
	//  d.qty_stock=d.qty;
	// }
	// });
	// refresh_field("items");
	// })
	
	frappe.ui.form.on("Purchase Invoice Item", "rate_kg", function(frm, cdt, cdn) {
	$.each(frm.doc.items || [], function(i, d) {
	d.price_list_rate=d.rate_kg*d.conversion_factor;
	d.discount_percentage=0;
	d.discount_amount=0;
	d.rate=d.rate_kg*d.conversion_factor;
	d.amount=d.stock_qty*d.rate_kg;
	d.base_amount=d.qty_stock*d.rate_kg;
	});
	refresh_field("items");
	})
	frappe.ui.form.on("Purchase Invoice Item", "conversion_factor", function(frm, cdt, cdn) {
	$.each(frm.doc.items || [], function(i, d) {
	d.price_list_rate=d.rate_kg*d.conversion_factor;
	d.discount_percentage=0;
	d.discount_amount=0;
	d.rate=d.rate_kg*d.conversion_factor;
	d.qty_stock=d.qty*d.conversion_factor;
	d.amount=d.stock_qty*d.rate_kg;
	d.base_amount=d.stock_qty*d.rate_kg;
	});
	//refresh_field("items");
	})
	frappe.ui.form.on("Purchase Invoice", "validate", function(frm, cdt, cdn) {
	$.each(frm.doc.items || [], function(i, d) {
	if (d.stock_uom!=d.uom){
	d.conversion_factor=d.qty_stock/d.qty;
	d.price_list_rate=d.rate_kg*d.conversion_factor;
	d.discount_percentage=0;
	d.discount_amount=0;
	d.rate=d.rate_kg*d.conversion_factor;
	
	}
	else{
	 d.conversion_factor=1;
	 d.qty_stock=d.qty;
	 d.price_list_rate=d.rate_kg*d.conversion_factor;
	d.discount_percentage=0;
	d.discount_amount=0;
	d.rate=d.rate_kg*d.conversion_factor;
	
	}
	});    
	
	//});
	refresh_field("items");
	 })
	

frappe.ui.form.on("Purchase Invoice", {
	validate: function(frm) {
	    if (frm.doc.__islocal) {
		frappe.call({
			"method": "frappe.client.get",
			"args": {
				"doctype": "Purchase Invoice",
				fieldname: "lr_no",
				filters: { lr_no: frm.doc.lr_no , docstatus: ["!=", "2"],},
			},
			"callback": function(response) {
				var pinv = response.message;

				if (pinv) {
					frappe.msgprint("LR No Already Exists for this Purchase Invoice: " + pinv.name);
					frappe.validated=false;
				} else {
                    frappe.validated=True;				}
			}
		});
	}
	}
});