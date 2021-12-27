frappe.ui.form.on('Salary Slip', {
payment_days(frm){
 cur_frm.set_value("emp_working_days", (cur_frm.doc.payment_days+cur_frm.doc.absent_days+cur_frm.doc.leave_without_pay+cur_frm.doc.unmarked_days));
    		frm.refresh_field("cur_frm.doc.emp_working_days");
    },
	validate(frm)  {
     cur_frm.set_value("emp_working_days", (cur_frm.doc.payment_days+cur_frm.doc.absent_days+cur_frm.doc.leave_without_pay+cur_frm.doc.unmarked_days));
    refresh_field("cur_frm.doc.emp_working_days");
 	},
 	
   });
