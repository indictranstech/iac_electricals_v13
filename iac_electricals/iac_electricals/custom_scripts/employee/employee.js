frappe.ui.form.on('Employee', {
others_amount(frm){
 cur_frm.set_value("base", (cur_frm.doc.basic_amount+cur_frm.doc.hra_amount+cur_frm.doc.ca_amount+cur_frm.doc.others_amount));
    		frm.refresh_field("cur_frm.doc.base");
    },
 hra_amount(frm){
 cur_frm.set_value("base", (cur_frm.doc.basic_amount+cur_frm.doc.hra_amount+cur_frm.doc.ca_amount+cur_frm.doc.others_amount));
    		frm.refresh_field("cur_frm.doc.base");
    },    
   basic_amount(frm){
 cur_frm.set_value("base", (cur_frm.doc.basic_amount+cur_frm.doc.hra_amount+cur_frm.doc.ca_amount+cur_frm.doc.others_amount));
    		frm.refresh_field("cur_frm.doc.base");
    },
    ca_amount(frm){
 cur_frm.set_value("base", (cur_frm.doc.basic_amount+cur_frm.doc.hra_amount+cur_frm.doc.ca_amount+cur_frm.doc.others_amount));
    		frm.refresh_field("cur_frm.doc.base");
    },
	validate(frm)  {
    cur_frm.doc.base=cur_frm.doc.basic_amount+cur_frm.doc.hra_amount+cur_frm.doc.ca_amount+cur_frm.doc.others_amount
    // cur_frm.doc.basic_amount=(cur_frm.doc.base*cur_frm.doc.basic)/100
   // cur_frm.doc.hra_amount=(cur_frm.doc.base*cur_frm.doc.hra)/100
   // cur_frm.doc.ca_amount=cur_frm.doc.ca
   // cur_frm.doc.others=cur_frm.doc.base-cur_frm.doc.basic_amount-cur_frm.doc.hra_amount-cur_frm.doc.ca_amount
    //cur_frm.doc.others_amount=cur_frm.doc.base-cur_frm.doc.basic_amount-cur_frm.doc.hra_amount-cur_frm.doc.ca_amount
    refresh_field("cur_frm.doc.base");
 	},
 	
   });
 