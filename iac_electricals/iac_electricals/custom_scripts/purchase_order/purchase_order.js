frappe.ui.form.on("Purchase Order", {
	project: function(frm, cdt, cdn) {
		if(!frm.doc.delivery_date) {
			erpnext.utils.copy_value_in_all_rows(frm.doc, cdt, cdn, "items", "project");
		}
	}
})

frappe.ui.form.on("Purchase Order Item", "qty_stock", function(frm, cdt, cdn) {
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
	
	frappe.ui.form.on("Purchase Order Item", "rate_kg", function(frm, cdt, cdn) {
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
	frappe.ui.form.on("Purchase Order Item", "conversion_factor", function(frm, cdt, cdn) {
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
	frappe.ui.form.on("Purchase Order", "validate", function(frm, cdt, cdn) {
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