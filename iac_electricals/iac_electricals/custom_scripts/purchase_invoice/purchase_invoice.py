# Copyright (c) 2021, IAC Electricals and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from datetime import datetime
from datetime import timedelta, date
from erpnext.accounts.utils import get_account_currency, get_fiscal_year
from frappe.utils import date_diff, add_months, today, getdate, add_days, flt, get_last_day, get_first_day, cint, get_link_to_form, rounded

def validate_LR_No(self,method=None):
    if self.lr_no:
        fiscal_year = get_fiscal_year(self.posting_date, company=self.company, as_dict=True)
        pi = frappe.db.sql('''select name from `tabPurchase Invoice`
            where
                lr_no = %(lr_no)s
                and name != %(name)s
                and docstatus < 2
                and posting_date between %(year_start_date)s and %(year_end_date)s''', {
                    "lr_no": self.lr_no,
                    "name": self.name,
                    "year_start_date": fiscal_year.year_start_date,
                    "year_end_date": fiscal_year.year_end_date
                })
 
        if pi:
            pi = pi[0][0]
            frappe.throw(_("LR No exists in Purchase Invoice {0}".format(pi)))
