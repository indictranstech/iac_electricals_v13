frappe.ui.form.on("Item", {
	refresh: function(frm) {
		cur_frm.set_df_property("item_code", "hidden", 1);
		if(frm.doc.__islocal !=1) {
			cur_frm.set_df_property("custom_naming_series", "read_only", 1);
			/*cur_frm.set_df_property("item_code", "hidden", 1);*/
		}
	},
	custom_naming_series:function(frm){
		frm.set_value("item_code",frm.doc.custom_naming_series);
		frm.refresh_field("item_code");
	}
})