
frappe.ui.form.on("Quotation", {
	sale_type: function(frm) {
		if (frm.doc.sale_type == "Domestic Sale") {
			frm.set_df_property('freight_basis', 'options', [
					"Ex Works",
					"FORD"
			]);
		} else if (frm.doc.sale_type == "Export Sale") {
			frm.set_df_property('freight_basis', 'options', [
					"Ex-Works",
					"FOB",
					"CIF",
					"CFR",
					"CIP",
					"DDP",
					"DDU"
			]);
		}else{
			frm.set_df_property('freight_basis', 'options', []);
		}
	}
})