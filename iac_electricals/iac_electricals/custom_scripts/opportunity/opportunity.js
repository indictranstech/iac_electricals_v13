frappe.ui.form.on("Opportunity", {
	refresh: function(frm) {
		$(".inner-group-button").hide();
		/*cur_frm.remove_custom_button("Quotation", 'Create');*/
		/*$('.btn:contains("Create"):visible').hide();*/
		$("[data-doctype='Quotation']").hide();
		if(!frm.doc.__islocal){
			frm.add_custom_button(("Price Schedule"), function() {
				frappe.model.open_mapped_doc({
					method: "iac_electricals.iac_electricals.custom_scripts.opportunity.opportunity.make_price_schedule",
					frm : cur_frm
				})
			}, __("Create New"));
		}
		
	},
	sale_type:function(frm){
		if(frm.doc.sale_type == 'Domestic Tender'){
			frm.set_value("naming_series","IAC-OPP-DT-.YYYY.-")
		}else if(frm.doc.sale_type == 'Domestic Purchase'){
			frm.set_value("naming_series","IAC-OPP-DP-.YYYY.-")
		}else if(frm.doc.sale_type == 'Export Tender'){
			frm.set_value("naming_series","IAC-OPP-ET-.YYYY.-")
		}else if(frm.doc.sale_type == 'Export Purchase'){
			frm.set_value("naming_series","IAC-OPP-EP-.YYYY.-")
		}else{
			frm.set_value("naming_series","")
		}
	},
	currency:function(frm){
		if(frm.doc.currency != null){
			frappe.call({
				method: 'iac_electricals.iac_electricals.custom_scripts.opportunity.opportunity.get_exchange_rate_',
				args: {
					from_currency: frm.doc.currency
				},
				callback: function(r) {
					if (r.message ==0 ) {
						frm.set_value("exchange_rate",0)
					}else{
						var exchange_rate = r.message;
						frm.set_value("exchange_rate",exchange_rate)
					}
				}
			});
		}
		else{
			frm.set_value("exchange_rate","")
		}
		
	},
	onload:function(frm){
		if(frm.doc.currency != null){
			frappe.call({
				method: 'iac_electricals.iac_electricals.custom_scripts.opportunity.opportunity.get_exchange_rate_',
				args: {
					from_currency: frm.doc.currency
				},
				callback: function(r) {
					if (r.message ==0 ) {
						frm.set_value("exchange_rate",0)
					}else{
						var exchange_rate = r.message;
						frm.set_value("exchange_rate",exchange_rate)
					}
				}
			});
		}else{
			frm.set_value("exchange_rate","")
		}
		
	},
	validate:function(frm){
		frm.set_value("currency_in_lakhs","")
		if(frm.doc.exchange_rate != 0){
			var value_in_lakhs = frm.doc.price*frm.doc.exchange_rate / 100000
			if(frm.doc.currency != 'INR'){
				frm.set_value("currency_in_lakhs",value_in_lakhs)
			}else{
				frm.set_value("currency_in_lakhs",frm.doc.price)
			}
		}
	},
	after_save:function(frm){
		/*location.reload();*/
	}
})