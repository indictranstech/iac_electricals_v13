import frappe
from frappe import _
from frappe.model.document import Document
from frappe.model.naming import make_autoname

# Autoname the series According To Branch
def autoname(doc, method):
   	if doc.branch:
   		if doc.branch == 'Behala' :
   			doc.name = make_autoname("B"+".####")
   			return doc.name
   		elif doc.branch == 'Dhulagadh' :
   			doc.name = make_autoname("D"+".####")
   			return doc.name
   		elif doc.branch == 'HO' :
   			doc.name = make_autoname("H"+".####")
   			return doc.name
   		else :
   			return doc.name