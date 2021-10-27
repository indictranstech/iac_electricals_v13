// Copyright (c) 2021, IAC Electricals and contributors
// For license information, please see license.txt

frappe.ui.form.on('Update the series',{
	update_button_1: function(frm) {
		frappe.call({
			method: "iac_electricals.iac_electricals.custom_scripts.item.item.update_the_series_item_updation",
			args:{prefix_level_for_item:frm.doc.prefix_level_for_item, count1 : frm.doc.count_1},
			callback:function(r){
				console.log(r.message)
			}
		});
	},
	update_button_2: function(frm) {
		frappe.call({
			method: "iac_electricals.iac_electricals.custom_scripts.item.item.update_the_series_prefix2_updation",
			args:{prefix_level_3:frm.doc.prefix_level_3, count2 : frm.doc.count_2},
			callback:function(r){
				console.log(r.message)
			}
		});
	},
	update_button_3: function(frm) {
		frappe.call({
			method: "iac_electricals.iac_electricals.custom_scripts.item.item.update_the_series_prefix3_updation",
			args:{prefix_level_2:frm.doc.prefix_level_2, count3 : frm.doc.count_3},
			callback:function(r){
				console.log(r.message)
			}
		})
	}
});
