from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from datetime import date, timedelta, datetime
from frappe.utils import getdate, get_datetime, flt, nowdate, cstr, today

# Reminder For Absent Employees Not Present Form Last 3 days
def generate_leave_without_approval_reminder():
    data = {}
    report_data ={}
    emp = frappe.db.sql("select name,employee_name,personal_email,department,reports_to,reports_to_2 from `tabEmployee`")
    for i in emp:
        item_list = []
        report_list = []
        todays_date = date.today()
        if todays_date.weekday()!=5 or todays_date.weekday()!=6:
            if todays_date.weekday() == 1:
                three_days_previous_date = date.today() - timedelta(days=5)
            # elif todays_date.weekday() == 2:
            #     three_days_previous_date = date.today() - timedelta(days=4)
            else:
                three_days_previous_date = date.today() - timedelta(days=3)
            attendance_data = frappe.db.sql(""" SELECT *  FROM `tabAttendance` 
                    WHERE employee = '{0}' and attendance_date between 
                    '{1}' AND '{2}' """.format(i[0],three_days_previous_date ,todays_date),as_dict=1)

            if not attendance_data:
                    # attendance not present 
                    # check for on leave or not     
                    leave_data = frappe.db.sql(""" SELECT *  FROM `tabLeave Application` 
                    WHERE employee = '{0}' and from_date >= '{1}' 
                    and to_date <= '{2}' """.format(i[0],three_days_previous_date ,todays_date),as_dict=1)

                    if not leave_data:
                        report_manager_list = []
                        item_list.append(i[0])
                        item_list.append(i[1])
                        item_list.append(i[2])
                        item_list.append(i[3])
                        data[i[0]]=item_list
                        if i[4]:
                            report_list.append(i[0])
                            report_list.append(i[1])
                            report_list.append(i[2])
                            report_list.append(i[3])
                            report_data[i[0]] = report_list
                            report_manager = frappe.db.sql(""" SELECT personal_email FROM `tabEmployee` 
                                    WHERE name = '{0}' """.format(i[4]),as_dict=1)
                            email_template = frappe.get_doc("Email Template", "Attendance")
                            report_message = frappe.render_template(email_template.response_html,{'data':report_data})
                            if report_manager[0].get("personal_email"):
                                frappe.sendmail(
                                recipients = report_manager[0].get("personal_email"),
                                subject = "Reminder: Absent Employee Without Leave Approval",
                                message = report_message
                            )

                        if i[5]:
                            report_list.append(i[0])
                            report_list.append(i[1])
                            report_list.append(i[2])
                            report_list.append(i[3])
                            report_data[i[0]] = report_list
                            report_manager_second = frappe.db.sql(""" SELECT personal_email FROM `tabEmployee` 
                                    WHERE name = '{0}' """.format(i[5]),as_dict=1)
                            email_template = frappe.get_doc("Email Template", "Attendance")
                            report_message = frappe.render_template(email_template.response_html,{'data':report_data})
                            if report_manager_second[0].get("personal_email"):
                                frappe.sendmail(
                                recipients = report_manager_second[0].get("personal_email"),
                                subject = "Reminder: Absent Employee Without Leave Approval",
                                message = report_message
                            )

    email_template = frappe.get_doc("Email Template", "Attendance")
    message = frappe.render_template(email_template.response_html,{'data':data})
    frappe.sendmail(
        recipients = "hr@iacelectricals.com",
        subject = "Reminder: List Of Employees Leave Without Approval",
        message = message
    )


def birthday_reminder():
    file_att = []
    emp_list = []
    attachments = frappe.db.sql(""" SELECT file_name  FROM tabFile 
                WHERE file_name = '{0}'""".format("Birthday_wish.jpg"),as_dict=1)
    if attachments:
        for row in attachments:
            _file = frappe.get_doc("File", {"file_name": row.file_name})
            content = _file.get_content()
            if not content:
                return
            attachment_list = {'fname':row.file_name,'fcontent':content}
            file_att.append(attachment_list)
    emp = frappe.db.sql("select name,employee_name,personal_email,date_of_birth from `tabEmployee`",as_dict=1)
    # Employee list To Put in BCC
    for e in emp:
        if e.personal_email:
            emp_list.append(e.personal_email)

    for e1 in emp:
        data = {}
        current_month = date.today().month
        current_day = date.today().day
        Birthday_month = e1.date_of_birth.month
        Birthday_day = e1.date_of_birth.day

        if (current_month == Birthday_month and current_day == Birthday_day):
            email_template = frappe.get_doc("Email Template", "Birthday Wish")
            message = frappe.render_template(email_template.response_html,{'data':data})
            Birthday_person_email = e1.personal_email
            if Birthday_person_email:
                frappe.sendmail(
            # sender = sender,
                    recipients = Birthday_person_email,
                    subject = "Happy Birthday " + e1.employee_name,
                    # cc =  "name cc list",
                    bcc = emp_list,
                    message = message,
                    attachments = file_att,
                    )
