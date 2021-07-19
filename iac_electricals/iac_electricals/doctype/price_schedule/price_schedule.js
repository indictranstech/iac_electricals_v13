// Copyright (c) 2021, IAC Electricals and contributors
// For license information, please see license.txt

frappe.ui.form.on('Price Schedule', {
	onload: function(frm) {
		if(frm.doc.__islocal ==1) {
			cur_frm.clear_table("items");
			cur_frm.refresh_fields();
		}
	},
	validate:function(frm){
		var unit_prce_1_item_total_amt = 0;
		var unit_prce_2_item_total_amt = 0;
		var item_total_amt = 0;
		var ttl_qty = 0.0;
		frm.doc.items.forEach(d => {
			unit_prce_1_item_total_amt = unit_prce_1_item_total_amt + d.total_value
			unit_prce_2_item_total_amt = unit_prce_2_item_total_amt + d.total
			ttl_qty = ttl_qty + d.total_quantity
		})
		frm.set_value("unit_prce_1_total_value", unit_prce_1_item_total_amt);
		frm.set_value("unit_prce_2_total_value", unit_prce_2_item_total_amt);
		item_total_amt = unit_prce_1_item_total_amt + unit_prce_2_item_total_amt
		frm.set_value("total", item_total_amt);
		frm.set_value("total_quantity", ttl_qty);


		if(frm.doc.total != null){
			frm.set_value("grand_total", "");
			frm.set_value("rounded_total", "");
			frm.set_value("in_words","")
			frm.set_value("total_taxes_and_charges","")
			if(frm.doc.sales_taxes_and_charges_template != null){
				frappe.call({
					method:"iac_electricals.iac_electricals.doctype.price_schedule.price_schedule.calculate_taxes",
					args: {
						"tax_temlet_name":frm.doc.sales_taxes_and_charges_template,
						"total_amount": frm.doc.total	
					},
					async: false,
					callback:function(r){
						if(r.message){
							frm.clear_table("sales_taxes_and_charges");
							frm.refresh_fields("sales_taxes_and_charges");
							var sum_tax_amt = 0.0
							r.message.forEach(d => {
								sum_tax_amt+=d.tax_amount
								var childTable = cur_frm.add_child("sales_taxes_and_charges");
								childTable.charge_type = d.charge_type
								childTable.account_head = d.account_head
								childTable.description = d.description
								childTable.rate = d.rate
								childTable.tax_amount = d.tax_amount
								childTable.total = d.total
								frm.refresh_fields("sales_taxes_and_charges");
							})
							frm.set_value("total_taxes_and_charges", sum_tax_amt);
							frm.set_value("grand_total", sum_tax_amt+frm.doc.total);
							var rount_ttl = Math.round(sum_tax_amt+frm.doc.total)
							frm.set_value("rounded_total", rount_ttl);
							if(frm.doc.rounded_total != null){
								frappe.call({
									method:"iac_electricals.iac_electricals.doctype.price_schedule.price_schedule.number_to_word",
									args: {
										"amount":frm.doc.rounded_total,	
									},
									async: false,
									callback:function(r){
										if(r.message){
											frm.set_value("in_words",r.message)
										}
									}
								});
							}
						}
					}
				});
			}else{
				frm.clear_table("sales_taxes_and_charges");
				frm.refresh_fields("sales_taxes_and_charges");
				frm.set_value("grand_total", "");
				frm.set_value("rounded_total", "");
				frm.set_value("in_words","")
				frm.set_value("total_taxes_and_charges", "")

				frm.set_value("grand_total", frm.doc.total);
				var rount_ttl = Math.round(frm.doc.total)
				frm.set_value("rounded_total", rount_ttl);
				if(frm.doc.rounded_total != null){
					frappe.call({
						method:"iac_electricals.iac_electricals.doctype.price_schedule.price_schedule.number_to_word",
						args: {
							"amount":frm.doc.rounded_total,	
						},
						async: false,
						callback:function(r){
							if(r.message){
								frm.set_value("in_words",r.message)
							}
						}
					});
				}
			}
		}

	},
	refresh: function(frm) {
		frm.fields_dict['sales_taxes_and_charges'].grid.wrapper.find('.grid-add-row').hide();
		/*if(frm.doc.sales_taxes_and_charges_template == null){
			frm.clear_table("sales_taxes_and_charges");
			frm.refresh_fields("sales_taxes_and_charges");
		}*/
		if(frm.doc.docstatus == 0){
			frm.fields_dict["items"].grid.add_custom_button(__('Add Product Bundle Item'),() =>{
				var d = new frappe.ui.Dialog({
				'fields': [
					{'fieldname': 'select_item',
					 'fieldtype': 'Link',
					 "options":  "Product Bundle", 
					 "label": __("Select Item"),
					 "reqd": 1,
					 "get_query": function () {
					    },
					}
					],
				});
				d.set_primary_action(__('Get Data'), function() {
					if(cur_frm.doc.sale_type == ""){
						frappe.throw(__("Please add Sale Type"));
					}
				   	var data = d.get_values();
				   	this.data = [];
					const inner_dialog = new frappe.ui.Dialog({

		             	fields: [
						   {
								"fieldname":"selected_item",
								"fieldtype": "Link",
								"options": "Product Bundle",
								"default" :data.select_item ,
								"read_only":1,
						    },
						    {
								fieldname: "price_schedule_items", fieldtype: "Table",
								cannot_add_rows: 1,
								data: this.data,						
								get_data: () => {
									return this.data;
								},
								fields: [
									{
										fieldtype:'Link',
										fieldname:"item_code",
										options: 'Item',
										in_list_view: 1,
										label: __('Item Code'),
										columns:2,
										"read_only":1,						
									},
									{
										fieldtype:'Link',
										fieldname:"selected_item",
										options: 'Product Bundle',
										in_list_view: 1,
										label: __('Product Bundle Item'),
										columns:2						
									},
									{fieldtype:"Column Break"},
									{
										fieldtype:'Text',
										fieldname:"description",
										in_list_view: 0,
										label: __('Description'),
										columns : 2,
										"read_only":1,
									},
									{fieldtype:"Section Break",label: __("Add Packages")},
									{
										fieldtype:'Int',
										fieldname:"pkg_line1_main",
										in_list_view: 1,
										label: __('Pkg/Line 1 Main'),
										columns : 2,
									},
									{
										fieldtype:'Int',
										fieldname:"pkg_line2_main",
										in_list_view: 1,
										label: __('Pkg/Line 2 Main'),
										columns : 2,
									},
									{
										fieldtype:'Int',
										fieldname:"pkg_line3_main",
										in_list_view: 1,
										label: __('Pkg/Line 3 Main'),
										columns : 2,
									},
									{
										fieldtype:'Int',
										fieldname:"pkg_line4_main",
										in_list_view: 1,
										label: __('Pkg/Line 4 Main'),
										columns : 2,
									},
									{
										fieldtype:'Int',
										fieldname:"pkg_line5_main",
										in_list_view: 1,
										label: __('Pkg/Line 5 Main'),
										columns : 2,
									},
									{fieldtype:"Column Break"},
									{
										fieldtype:'Int',
										fieldname:"pkg_line1_spares",
										in_list_view: 1,
										label: __('Pkg/Line 1 Spares'),
										columns : 2,
									},
									{
										fieldtype:'Int',
										fieldname:"pkg_line2_spares",
										in_list_view: 1,
										label: __('Pkg/Line 2 Spares'),
										columns : 2,
									},
									{
										fieldtype:'Int',
										fieldname:"pkg_line3_spares",
										in_list_view: 1,
										label: __('Pkg/Line 3 Spares'),
										columns : 2,
									},
									{
										fieldtype:'Int',
										fieldname:"pkg_line4_spares",
										in_list_view: 1,
										label: __('Pkg/Line 4 Spares'),
										columns : 2,
									},
									{
										fieldtype:'Int',
										fieldname:"pkg_line5_spares",
										in_list_view: 1,
										label: __('Pkg/Line 5 Spares'),
										columns : 2,
									},
									{fieldtype:"Section Break",label: __("Add Additional Packages")},
									{
										fieldtype:'Int',
										fieldname:"pkg_line6_main",
										in_list_view: 1,
										label: __('Pkg/Line 6 Main'),
										columns : 2,
									},
									{
										fieldtype:'Int',
										fieldname:"pkg_line7_main",
										in_list_view: 1,
										label: __('Pkg/Line 7 Main'),
										columns : 2,
									},
									{
										fieldtype:'Int',
										fieldname:"pkg_line8_main",
										in_list_view: 1,
										label: __('Pkg/Line 8 Main'),
										columns : 2,
									},
									{
										fieldtype:'Int',
										fieldname:"pkg_line9_main",
										in_list_view: 1,
										label: __('Pkg/Line 9 Main'),
										columns : 2,
									},
									{
										fieldtype:'Int',
										fieldname:"pkg_line10_main",
										in_list_view: 1,
										label: __('Pkg/Line 10 Main'),
										columns : 2,
									},
									{fieldtype:"Column Break"},
									{
										fieldtype:'Int',
										fieldname:"pkg_line6_spares",
										in_list_view: 1,
										label: __('Pkg/Line 6 Spares'),
										columns : 2,
									},
									{
										fieldtype:'Int',
										fieldname:"pkg_line7_spares",
										in_list_view: 1,
										label: __('Pkg/Line 7 Spares'),
										columns : 2,
									},
									{
										fieldtype:'Int',
										fieldname:"pkg_line8_spares",
										in_list_view: 1,
										label: __('Pkg/Line 8 Spares'),
										columns : 2,
									},
									{
										fieldtype:'Int',
										fieldname:"pkg_line9_spares",
										in_list_view: 1,
										label: __('Pkg/Line 9 Spares'),
										columns : 2,
									},
									{
										fieldtype:'Int',
										fieldname:"pkg_line10_spares",
										in_list_view: 1,
										label: __('Pkg/Line 10 Spares'),
										columns : 2,
									},
									{fieldtype:"Section Break"},
									{
										fieldtype:'Currency',
										fieldname:"unit_price",
										in_list_view: 1,
										label: __('Unit Price'),
										columns : 2,
										"reqd": 1,
									},
									{fieldtype:"Column Break"},
									{
										fieldtype:'Float',
										fieldname:"unit",
										in_list_view: 1,
										label: __('Unit'),
										columns : 1,
										"reqd": 1,
									},
								],
							},
						]
		            });
		            /*var data = inner_dialog.get_values();*/
					frappe.call({
						method: "frappe.client.get",
						args:{
							doctype: "Product Bundle",
							filters: {'name': data.select_item}
						},
						callback: function(r) {
							if (r.message){ 
								var product_bundle_data = r.message
								product_bundle_data.items.forEach(d => {
				        			inner_dialog.fields_dict.price_schedule_items.df.data.push({
										"item_code": d.item_code,
										"description": d.description,
										"selected_item": product_bundle_data.new_item_code,
									});
								})
								this.data = inner_dialog.fields_dict.price_schedule_items.df.data;
								inner_dialog.fields_dict.price_schedule_items.grid.refresh();
			        		}
						}
					});
					inner_dialog.set_primary_action(__('Get Items'), function() {
						var dialog_data = inner_dialog.get_values()
							dialog_data.price_schedule_items.forEach(d => {
								cur_frm.refresh_fields("items");
								var childTable = cur_frm.add_child("items");
								childTable.item_code = d.item_code
								frappe.call({
									"method": "frappe.client.get",
									"args": {
										"doctype": "Item",
										"name": d.item_code
									},
									"callback": function(response) {
										var item_doc = response.message;

										if (item_doc) {
											childTable.item_name = item_doc.item_name
											childTable.uom = item_doc.stock_uom
										}
									}
								});
								childTable.description = d.description
								childTable.product_bundle_item = d.selected_item
								frappe.call({
									"method": "frappe.client.get",
									"args": {
										"doctype": "Item",
										"name": d.selected_item
									},
									"callback": function(response) {
										var item_doc = response.message;

										if (item_doc) {
											childTable.product_bundle_item_name = item_doc.item_name
										}
									}
								});
								/*childTable.drawaing_no = d.drawaing_no*/
								/*frappe.meta.get_docfield('Price Schedule Items', 'freight_type', cur_frm.doc.name).options = ["Ex-Works","FORD"];
								cur_frm.refresh_field('freight_type');*/
								/*if(frm.doc.sale_type == 'Domestic Tender' || frm.doc.sale_type == 'Domestic Purchase'){
									frappe.meta.get_docfield('Price Schedule Items', 'freight_type', cur_frm.doc.name).options = ["Ex-Works","FORD"];
									frm.refresh_field('freight_type');
									frappe.meta.get_docfield('Price Schedule Items', 'freight_type_2', cur_frm.doc.name).options = ["Ex-Works","FORD"];
									frm.refresh_field('freight_type_2');
								}else if(frm.doc.sale_type == 'Export Tender' || frm.doc.sale_type == 'Export Purchase'){
									frappe.meta.get_docfield('Price Schedule Items', 'freight_type', cur_frm.doc.name).options = ["Ex-Works","FOB","CIF","CFR","CIP","DDP","DDU"];
									frm.refresh_field('freight_type');
									frappe.meta.get_docfield('Price Schedule Items', 'freight_type_2', cur_frm.doc.name).options = ["Ex-Works","FOB","CIF","CFR","CIP","DDP","DDU"];
									frm.refresh_field('freight_type_2');
								}else{
									frappe.meta.get_docfield('Price Schedule Items', 'freight_type', cur_frm.doc.name).options = [];
									frm.refresh_field('freight_type');
									frappe.meta.get_docfield('Price Schedule Items', 'freight_type_2', cur_frm.doc.name).options = [];
									frm.refresh_field('freight_type_2');
								}*/

								childTable.pkg_line1_main = d.pkg_line1_main
								childTable.pkg_line2_main = d.pkg_line2_main
								childTable.pkg_line3_main = d.pkg_line3_main
								childTable.pkg_line4_main = d.pkg_line4_main
								childTable.pkg_line5_main = d.pkg_line5_main
								childTable.pkg_line1_spares = d.pkg_line1_spares
								childTable.pkg_line2_spares = d.pkg_line2_spares
								childTable.pkg_line3_spares = d.pkg_line3_spares
								childTable.pkg_line4_spares = d.pkg_line4_spares
								childTable.pkg_line5_spares = d.pkg_line5_spares
								childTable.pkg_line6_main = d.pkg_line6_main
								childTable.pkg_line7_main = d.pkg_line7_main
								childTable.pkg_line8_main = d.pkg_line8_main
								childTable.pkg_line9_main = d.pkg_line9_main
								childTable.pkg_line10_main = d.pkg_line10_main
								childTable.pkg_line6_spares = d.pkg_line6_spares
								childTable.pkg_line7_spares = d.pkg_line7_spares
								childTable.pkg_line8_spares = d.pkg_line8_spares
								childTable.pkg_line9_spares = d.pkg_line9_spares
								childTable.pkg_line10_spares = d.pkg_line10_spares
								var add_pac_tot = get_add_pac_cal_value(d.pkg_line1_main,d.pkg_line2_main,d.pkg_line3_main,d.pkg_line4_main,d.pkg_line5_main,d.pkg_line1_spares,d.pkg_line2_spares,d.pkg_line3_spares,d.pkg_line4_spares,d.pkg_line5_spares)
								var add_adtinl_pac_tot = get_add_adtinl_pac_cal_value(d.pkg_line6_main,d.pkg_line7_main,d.pkg_line8_main,d.pkg_line9_main,d.pkg_line10_main,d.pkg_line6_spares,d.pkg_line7_spares,d.pkg_line8_spares,d.pkg_line9_spares,d.pkg_line10_spares)
								var final_qty = add_pac_tot + add_adtinl_pac_tot
								
								if (final_qty != 0){
									childTable.total_quantity = final_qty
								}
								
								/*d.total_quantity =total_packages */
								childTable.unit_price = d.unit_price
								childTable.unit = d.unit
								if(final_qty && d.unit){
									var total_qty = final_qty * d.unit
								}else{
									var total_qty = 0
								}

								if(final_qty && d.unit_price){
									var total_qty_ = final_qty * d.unit_price
								}else{
									var total_qty_ = 0
								}
								childTable.total_value = total_qty_
								childTable.total = total_qty
								cur_frm.refresh_fields("items");
							})	
						
						inner_dialog.hide();
		                d.hide();

					});
					inner_dialog.show();
					d.hide();	
		            inner_dialog.$wrapper.find('.modal-dialog').css("margin-left", "165px");
		            inner_dialog.$wrapper.find('.modal-content').css("width", "1000px");
		        });
				d.show()
				d.refresh();	
			});
		}
	   
	},
	setup: function(frm) {
		frm.set_query("quotation_to", function() {
			return{
				"filters": {
					"name": ["in", ["Customer", "Lead"]],
				}
			}
		});

		frm.set_query("selling_price_list", function() {
			return{
				"filters": {
					"selling": 1,
				}
			}
		});

	},
	customer:function(frm){
		if(frm.doc.customer != null){
			frappe.call({
				method:"iac_electricals.iac_electricals.doctype.price_schedule.price_schedule.fetch_address_contact_name",
				args: {
					"name":frm.doc.customer,	
				},
				async: false,
				callback:function(r){
					if(r.message){						
						frm.set_value("customer_address",r.message.address_name)
						frm.set_value("contact_person",r.message.contact_name)
					}
				}
			});
		}
	},
	customer_address:function(frm){
		if(frm.doc.customer_address != null){
			frappe.call({
				method:"iac_electricals.iac_electricals.doctype.price_schedule.price_schedule.address_query",
				args: {
					"name":frm.doc.customer_address,	
				},
				async: false,
				callback:function(r){
					if(r.message){
						var address_details = '';
						if(r.message[0].address_line1 != null){
							address_details += `<span class="text-muted small">${r.message[0].address_line1}</span><br>`;
						}
						if(r.message[0].address_line2 != null){
							address_details += `<span class="text-muted small">${r.message[0].address_line2}</span><br>`;
						}
						if(r.message[0].city != null){
							address_details += `<span class="text-muted small">${r.message[0].city}</span>,`;
						}
						if(r.message[0].state != null){
							address_details += `<span class="text-muted small">${r.message[0].state}</span><br>`;
						}
						if(r.message[0].pincode != null){
							address_details += `<span class="text-muted small">Postal Code: ${r.message[0].pincode}</span><br>`;
						}
						if(r.message[0].country != null){
							address_details += `<span class="text-muted small">${r.message[0].country}</span>.`;
						}
						
						frm.set_value("address_display",address_details)
					}
				}
			});
		}
	},
	shipping_address_name:function(frm){
		if(frm.doc.shipping_address_name != null){
			frappe.call({
				method:"iac_electricals.iac_electricals.doctype.price_schedule.price_schedule.address_query",
				args: {
					"name":frm.doc.shipping_address_name,	
				},
				async: false,
				callback:function(r){
					if(r.message){
						var address_details = '';
						if(r.message[0].address_line1 != null){
							address_details += `<span class="text-muted small">${r.message[0].address_line1}</span><br>`;
						}
						if(r.message[0].address_line2 != null){
							address_details += `<span class="text-muted small">${r.message[0].address_line2}</span><br>`;
						}
						if(r.message[0].city != null){
							address_details += `<span class="text-muted small">${r.message[0].city}</span>,`;
						}
						if(r.message[0].state != null){
							address_details += `<span class="text-muted small">${r.message[0].state}</span><br>`;
						}
						if(r.message[0].pincode != null){
							address_details += `<span class="text-muted small">Postal Code: ${r.message[0].pincode}</span><br>`;
						}
						if(r.message[0].country != null){
							address_details += `<span class="text-muted small">${r.message[0].country}</span>.`;
						}
						
						frm.set_value("shipping_address",address_details)
					}
				}
			});
		}
	},
	contact_person:function(frm){
		if(frm.doc.contact_person != null){
			frappe.call({
				method:"iac_electricals.iac_electricals.doctype.price_schedule.price_schedule.contact_query",
				args: {
					"name":frm.doc.contact_person,	
				},
				async: false,
				callback:function(r){
					if(r.message){
						var contact_details = '';
						if(r.message.first_name != null){
							contact_details += `<span class="text-muted small"> ${r.message.first_name}</span>`;
						}
						if(r.message.middle_name != null){
							contact_details += `<span class="text-muted small"> ${r.message.middle_name}</span>`;
						}
						if(r.message.last_name != null){
							contact_details += `<span class="text-muted small"> ${r.message.last_name}</span><br>`;
						}
						/*if(r.message.email != null){
							contact_details += `<span class="text-muted small">Email: ${r.message.email}</span>`;
						}*/
						
						frm.set_value("contact_person_mobile_no",r.message.mobile_no)
						frm.set_value("contact_display",contact_details)
					}
				}
			});
		}
	},
	sales_taxes_and_charges_template:function(frm){
		if(frm.doc.sales_taxes_and_charges_template == null){
			frm.clear_table("sales_taxes_and_charges");
			frm.refresh_fields("sales_taxes_and_charges");
			frm.set_value("grand_total", "");
			frm.set_value("rounded_total", "");
			frm.set_value("in_words","")
			frm.set_value("total_taxes_and_charges","")

		}
	},
	terms:function(frm){
		if(frm.doc.terms != null){
			frappe.call({
				method: "frappe.client.get",
				args:{
					doctype: "Terms and Conditions",
					filters: {'name': frm.doc.terms}
				},
				callback: function(r) {
					if (r.message){ 
						frm.set_value("term_details",r.message.terms)
	        		}
				}
			});
		}else{
			frm.set_value("term_details","")
		}
	},
	sale_type:function(frm){
		if(frm.doc.sale_type == 'Domestic Tender'){
			frm.set_value("naming_series","SAL-DT-.YYYY.-")
		}else if(frm.doc.sale_type == 'Domestic Purchase'){
			frm.set_value("naming_series","SAL-DP-.YYYY.-")
		}else if(frm.doc.sale_type == 'Export Tender'){
			frm.set_value("naming_series","SAL-ET-.YYYY.-")
		}else if(frm.doc.sale_type == 'Export Purchase'){
			frm.set_value("naming_series","SAL-EP-.YYYY.-")
		}else{
			frm.set_value("naming_series","")
		}
	},
	total:function(frm){
		
		/*frm.set_value("grand_total", "");
		frm.set_value("rounded_total", "");
		frm.set_value("in_words","")
		if(frm.doc.sales_taxes_and_charges_template != null){
			frappe.call({
				method:"iac_electricals.iac_electricals.doctype.price_schedule.price_schedule.calculate_taxes",
				args: {
					"tax_temlet_name":frm.doc.sales_taxes_and_charges_template,
					"total_amount": frm.doc.total	
				},
				async: false,
				callback:function(r){
					if(r.message){
						frm.clear_table("sales_taxes_and_charges");
						frm.refresh_fields("sales_taxes_and_charges");
						r.message.forEach(d => {
							var childTable = cur_frm.add_child("sales_taxes_and_charges");
							childTable.charge_type = d.charge_type
							childTable.account_head = d.account_head
							childTable.description = d.description
							childTable.rate = d.rate
							childTable.tax_amount = d.tax_amount
							childTable.total = d.total
							frm.refresh_fields("sales_taxes_and_charges");
						})
					}
				}
			});
		}else{
			frm.clear_table("sales_taxes_and_charges");
			frm.refresh_fields("sales_taxes_and_charges");
			frm.set_value("grand_total", "");
			frm.set_value("rounded_total", "");
			frm.set_value("in_words","")
			frm.set_value("grand_total", frm.doc.total);
			var rount_ttl = Math.round(frm.doc.total)
			frm.set_value("rounded_total", rount_ttl);
			if(frm.doc.rounded_total != null){
				frappe.call({
					method:"iac_electricals.iac_electricals.doctype.price_schedule.price_schedule.number_to_word",
					args: {
						"amount":frm.doc.rounded_total,	
					},
					async: false,
					callback:function(r){
						if(r.message){
							frm.set_value("in_words",r.message)
						}
					}
				});
			}
		}*/
	}
});


cur_frm.fields_dict['items'].grid.get_field("item_code").get_query = function(doc, cdt, cdn) {
	return{
		filters:{
			'item_group': 'FG',
			'is_stock_item': 1,
			'is_sales_item':1
		}
	};
};

cur_frm.fields_dict["customer_address"].get_query = function(doc) {
	return {
		filters: {
			"link_doctype": "Customer",
			"link_name": doc.customer
		}
	};
};

cur_frm.fields_dict["contact_person"].get_query = function(doc) {
	return {
		filters: {
			"link_doctype": "Customer",
			"link_name": doc.customer
		}
	};
};





frappe.ui.form.on('Price Schedule Items',{
	total_quantity :function(frm,cdt,cdn){
		var d  = locals[cdt][cdn];
		calculate_total(d);
	},
	item_code:function(frm,cdt,cdn){
		var d  = locals[cdt][cdn];
		if(cur_frm.doc.sale_type == ""){
			frappe.throw(__("Please add Sale Type"));
		}
		/*console.log("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@",frm.doc.sale_type)
		if(frm.doc.sale_type == 'Domestic Tender' || frm.doc.sale_type == 'Domestic Purchase'){
			console.log("!!!!11111111",frm.doc.sale_type)
			frappe.meta.get_docfield('Price Schedule Items', 'freight_type', cur_frm.doc.name).options = ["Ex-Works","FORD"];
			console.log("222")
			frm.refresh_field('freight_type');
			console.log("333333")
			frappe.meta.get_docfield('Price Schedule Items', 'freight_type_2', cur_frm.doc.name).options = ["Ex-Works","FORD"];
			console.log("4444444")
			frm.refresh_field('freight_type_2');
			console.log("55555")
		}else if(frm.doc.sale_type == 'Export Tender' || frm.doc.sale_type == 'Export Purchase'){
			console.log("666",frm.doc.sale_type)
			frappe.meta.get_docfield('Price Schedule Items', 'freight_type', cur_frm.doc.name).options = ["Ex-Works","FOB","CIF","CFR","CIP","DDP","DDU"];
			console.log("7777")
			frm.refresh_field('freight_type');
			console.log("8888")
			frappe.meta.get_docfield('Price Schedule Items', 'freight_type_2', cur_frm.doc.name).options = ["Ex-Works","FOB","CIF","CFR","CIP","DDP","DDU"];
			console.log("9999")
			frm.refresh_field('freight_type_2');
			console.log("1010101")
		}else{
			console.log("11111",frm.doc.sale_type)
			frappe.meta.get_docfield('Price Schedule Items', 'freight_type', cur_frm.doc.name).options = [];
			console.log("12121212")
			frm.refresh_field('freight_type');
			console.log("131313")
			frappe.meta.get_docfield('Price Schedule Items', 'freight_type_2', cur_frm.doc.name).options = [];
			console.log("1414141")
			frm.refresh_field('freight_type_2');
			console.log("1515151")
		}*/


	},
	product_bundle_item:function(frm,cdt,cdn){
		var d  = locals[cdt][cdn];
		if(d.product_bundle_item != null){
			frappe.call({
				"method": "frappe.client.get",
				"args": {
					"doctype": "Item",
					"name": d.product_bundle_item
				},
				"callback": function(response) {
					var item_doc = response.message;

					if (item_doc) {
						frappe.model.set_value(d.doctype, d.name, "product_bundle_item_name", item_doc.item_name)
					}
				}
			});
		}else{
			frappe.model.set_value(d.doctype, d.name, "product_bundle_item_name", "")
		}
		
	},
	unit: function(frm,cdt,cdn){
		var d  = locals[cdt][cdn];
		calculate_total(d);
	},
	unit_price: function(frm,cdt,cdn){
		var d  = locals[cdt][cdn];
		calculate_total(d);
	},
	pkg_line1_main: function(frm,cdt,cdn){
		var d  = locals[cdt][cdn];
		total_qty(d)
	},
	pkg_line2_main: function(frm,cdt,cdn){
		var d  = locals[cdt][cdn];
		total_qty(d)
	},
	pkg_line3_main: function(frm,cdt,cdn){
		var d  = locals[cdt][cdn];
		total_qty(d)
	},
	pkg_line4_main: function(frm,cdt,cdn){
		var d  = locals[cdt][cdn];
		total_qty(d)
	},
	pkg_line5_main: function(frm,cdt,cdn){
		var d  = locals[cdt][cdn];
		total_qty(d)
	},
	pkg_line6_main: function(frm,cdt,cdn){
		var d  = locals[cdt][cdn];
		total_qty(d)
	},
	pkg_line7_main: function(frm,cdt,cdn){
		var d  = locals[cdt][cdn];
		total_qty(d)
	},
	pkg_line8_main: function(frm,cdt,cdn){
		var d  = locals[cdt][cdn];
		total_qty(d)
	},
	pkg_line9_main: function(frm,cdt,cdn){
		var d  = locals[cdt][cdn];
		total_qty(d)
	},
	pkg_line10_main: function(frm,cdt,cdn){
		var d  = locals[cdt][cdn];
		total_qty(d)
	},
	pkg_line1_spares: function(frm,cdt,cdn){
		var d  = locals[cdt][cdn];
		total_qty(d)
	},
	pkg_line2_spares: function(frm,cdt,cdn){
		var d  = locals[cdt][cdn];
		total_qty(d)
	},
	pkg_line3_spares: function(frm,cdt,cdn){
		var d  = locals[cdt][cdn];
		total_qty(d)
	},
	pkg_line4_spares: function(frm,cdt,cdn){
		var d  = locals[cdt][cdn];
		total_qty(d)
	},
	pkg_line5_spares: function(frm,cdt,cdn){
		var d  = locals[cdt][cdn];
		total_qty(d)
	},
	pkg_line6_spares: function(frm,cdt,cdn){
		var d  = locals[cdt][cdn];
		total_qty(d)
	},
	pkg_line7_spares: function(frm,cdt,cdn){
		var d  = locals[cdt][cdn];
		total_qty(d)
	},
	pkg_line8_spares: function(frm,cdt,cdn){
		var d  = locals[cdt][cdn];
		total_qty(d)
	},
	pkg_line9_spares: function(frm,cdt,cdn){
		var d  = locals[cdt][cdn];
		total_qty(d)
	},
	pkg_line10_spares: function(frm,cdt,cdn){
		var d  = locals[cdt][cdn];
		total_qty(d)
	},


});

var calculate_total = function(d) {
	if(d.total_quantity){
		var totl_qty = d.total_quantity
	}else{
		var totl_qty = 0
	}

	if(d.unit){
		var unt = d.unit
	}else{
		var unt = 0
	}

	if(d.unit_price){
		var unt_ = d.unit_price
	}else{
		var unt_ = 0
	}

	var total_qty = totl_qty * unt
	var total_qty_ = totl_qty * unt_
	frappe.model.set_value(d.doctype, d.name, "total", total_qty)
	frappe.model.set_value(d.doctype, d.name, "total_value", total_qty_)
}






var get_child_table_data = function(frm) {
	var list = [];
	var itm_data = frm.doc.items
	itm_data.forEach(d => {
		list.push(d)
		/*if(d.__checked){
			list.push(d) 
		}*//*else{
			frappe.throw(__("Please select item for add Packages"));
		}*/
	})
	return list
}

var total_qty = function(d){
	console.log("@@@@@@@@@!!!!!!!!!!!!!!!!!!!!!@@@@@@@@@@@@@@@%%%%%%%%%%%%%")
	var qty_totl = 0;
	/*var pkg_line1_main = 0;
	var pkg_line2_main = 0;
	var pkg_line3_main = 0;
	var pkg_line4_main = 0;
	var pkg_line5_main = 0;
	var pkg_line1_spares = 0;
	var pkg_line2_spares = 0;
	var pkg_line3_spares = 0;
	var pkg_line4_spares = 0;
	var pkg_line5_spares = 0;
	var pkg_line6_main = 0;
	var pkg_line7_main = 0;
	var pkg_line8_main = 0;
	var pkg_line9_main = 0;
	var pkg_line10_main = 0;
	var pkg_line6_spares = 0;
	var pkg_line7_spares = 0;
	var pkg_line8_spares = 0;
	var pkg_line9_spares = 0;
	var pkg_line10_spares = 0;*/

	var pkg_line1_main = (d.pkg_line1_main === undefined) ? 0 : d.pkg_line1_main;
	var pkg_line2_main = (d.pkg_line2_main === undefined) ? 0 : d.pkg_line2_main;
	var pkg_line3_main = (d.pkg_line3_main === undefined) ? 0 : d.pkg_line3_main;
	var pkg_line4_main = (d.pkg_line4_main === undefined) ? 0 : d.pkg_line4_main;
	var pkg_line5_main = (d.pkg_line5_main === undefined) ? 0 : d.pkg_line5_main;

	var pkg_line1_spares = (d.pkg_line1_spares === undefined) ? 0 : d.pkg_line1_spares;
	var pkg_line2_spares = (d.pkg_line2_spares === undefined) ? 0 : d.pkg_line2_spares;
	var pkg_line3_spares = (d.pkg_line3_spares === undefined) ? 0 : d.pkg_line3_spares;
	var pkg_line4_spares = (d.pkg_line4_spares === undefined) ? 0 : d.pkg_line4_spares;
	var pkg_line5_spares = (d.pkg_line5_spares === undefined) ? 0 : d.pkg_line5_spares;

	var pkg_line6_main = (d.pkg_line6_main === undefined) ? 0 : d.pkg_line6_main;
	var pkg_line7_main = (d.pkg_line7_main === undefined) ? 0 : d.pkg_line7_main;
	var pkg_line8_main = (d.pkg_line8_main === undefined) ? 0 : d.pkg_line8_main;
	var pkg_line9_main = (d.pkg_line9_main === undefined) ? 0 : d.pkg_line9_main;
	var pkg_line10_main = (d.pkg_line10_main === undefined) ? 0 : d.pkg_line10_main;

	var pkg_line6_spares = (d.pkg_line6_spares === undefined) ? 0 : d.pkg_line6_spares;
	var pkg_line7_spares = (d.pkg_line7_spares === undefined) ? 0 : d.pkg_line7_spares;
	var pkg_line8_spares = (d.pkg_line8_spares === undefined) ? 0 : d.pkg_line8_spares;
	var pkg_line9_spares = (d.pkg_line9_spares === undefined) ? 0 : d.pkg_line9_spares;
	var pkg_line10_spares = (d.pkg_line10_spares === undefined) ? 0 : d.pkg_line10_spares;
	/*console.log("!!!!!!!!!!!!!!!!!!",typeof(pkg_line1_main),pkg_line1_main)
	console.log("!!!!!!!!!!!!!!!!!!",typeof(pkg_line2_main),pkg_line2_main)
	console.log("!!!!!!!!!!!!!!!!!!",typeof(pkg_line3_main),pkg_line3_main)
	console.log("!!!!!!!!!!!!!!!!!!",typeof(pkg_line4_main),pkg_line4_main)
	console.log("!!!!!!!!!!!!!!!!!!",typeof(pkg_line5_main),pkg_line5_main)
	console.log("!!!!!!!!!!!!!!!!!!",typeof(pkg_line1_spares),pkg_line1_spares)
	console.log("!!!!!!!!!!!!!!!!!!",typeof(pkg_line2_spares),pkg_line2_spares)
	console.log("!!!!!!!!!!!!!!!!!!",typeof(pkg_line3_spares),pkg_line3_spares)
	console.log("!!!!!!!!!!!!!!!!!!",typeof(pkg_line4_spares),pkg_line4_spares)
	console.log("!!!!!!!!!!!!!!!!!!",typeof(pkg_line5_spares),pkg_line5_spares)
	console.log("!!!!!!!!!!!!!!!!!!",typeof(pkg_line6_main),pkg_line6_main)
	console.log("!!!!!!!!!!!!!!!!!!",typeof(pkg_line7_main),pkg_line7_main)
	console.log("!!!!!!!!!!!!!!!!!!",typeof(pkg_line8_main),pkg_line8_main)
	console.log("!!!!!!!!!!!!!!!!!!",typeof(pkg_line9_main),pkg_line9_main)
	console.log("!!!!!!!!!!!!!!!!!!",typeof(pkg_line10_main),pkg_line10_main)
	console.log("!!!!!!!!!!!!!!!!!!",typeof(pkg_line6_spares),pkg_line6_spares)
	console.log("!!!!!!!!!!!!!!!!!!",typeof(pkg_line7_spares),pkg_line7_spares)
	console.log("!!!!!!!!!!!!!!!!!!",typeof(pkg_line8_spares),pkg_line8_spares)
	console.log("!!!!!!!!!!!!!!!!!!",typeof(pkg_line9_spares),pkg_line9_spares)
	console.log("!!!!!!!!!!!!!!!!!!",typeof(pkg_line10_spares),pkg_line10_spares)*/

	var qty_totl = pkg_line1_main+pkg_line2_main+pkg_line3_main+pkg_line4_main+pkg_line5_main+pkg_line1_spares+pkg_line2_spares+pkg_line3_spares+pkg_line4_spares+pkg_line5_spares+pkg_line6_main+pkg_line7_main+pkg_line8_main+pkg_line9_main+pkg_line10_main+pkg_line6_spares+pkg_line7_spares+pkg_line8_spares+pkg_line9_spares+pkg_line10_spares
	frappe.model.set_value(d.doctype, d.name, "total_quantity", qty_totl)
}


var get_add_pac_cal_value = function(pkg_line1_main=0,pkg_line2_main=0,pkg_line3_main=0,pkg_line4_main=0,pkg_line5_main=0,pkg_line1_spares=0,pkg_line2_spares=0,pkg_line3_spares=0,pkg_line4_spares=0,pkg_line5_spares=0){
	var add_pac_totals = pkg_line1_main+pkg_line2_main+pkg_line3_main+pkg_line4_main+pkg_line5_main+pkg_line1_spares+pkg_line2_spares+pkg_line3_spares+pkg_line4_spares+pkg_line5_spares
	return add_pac_totals
}


var get_add_adtinl_pac_cal_value = function(pkg_line6_main=0,pkg_line7_main=0,pkg_line8_main=0,pkg_line9_main=0,pkg_line10_main=0,pkg_line6_spares=0,pkg_line7_spares=0,pkg_line8_spares=0,pkg_line9_spares=0,pkg_line10_spares=0){
	var add_adnl_pac_totals = pkg_line6_main+pkg_line7_main+pkg_line8_main+pkg_line9_main+pkg_line10_main+pkg_line6_spares+pkg_line7_spares+pkg_line8_spares+pkg_line9_spares+pkg_line10_spares
	return add_adnl_pac_totals
}