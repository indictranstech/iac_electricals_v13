
frappe.ui.form.on("Product Bundle", {
	new_item_code: function(frm) {
		if(frm.doc.new_item_code != null){			
			frappe.call({
				method: "frappe.client.get",
				args:{
					doctype: "Item",
					filters: {'name': frm.doc.new_item_code}
				},
				callback: function(r) {
					if (r.message){ 
						var item_data = r.message
						frm.set_value("description",item_data.description)
	        		}
				}
			});
		}
	}
})

cur_frm.fields_dict['items'].grid.get_field("item_code").get_query = function(doc, cdt, cdn) {
	return{
		filters:{
			'item_group': 'FG',
			'is_stock_item': 1,
			'is_sales_item':1
		}
	};
};