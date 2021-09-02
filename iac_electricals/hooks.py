from . import __version__ as app_version

app_name = "iac_electricals"
app_title = "IAC Electricals"
app_publisher = "IAC Electricals"
app_description = "IAC Electricals"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "anil.p@indictrans.in"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/iac_electricals/css/iac_electricals.css"
# app_include_js = "/assets/iac_electricals/js/iac_electricals.js"

# include js, css files in header of web template
# web_include_css = "/assets/iac_electricals/css/iac_electricals.css"
# web_include_js = "/assets/iac_electricals/js/iac_electricals.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "iac_electricals/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}
doctype_js = {
	"Quotation": "iac_electricals/custom_scripts/quotation/quotation.js",
	"Product Bundle": "iac_electricals/custom_scripts/product_bundle/product_bundle.js",
	"Opportunity": "iac_electricals/custom_scripts/opportunity/opportunity.js",
	"Lead": "iac_electricals/custom_scripts/lead/lead.js",
	"Customer": "iac_electricals/custom_scripts/customer/customer.js",
	"Blanket Order": "iac_electricals/custom_scripts/blanket_order/blanket_order.js",
	"Sales Order": "iac_electricals/custom_scripts/sales_order/sales_order.js",
	"Sales Invoice": "iac_electricals/custom_scripts/sales_invoice/sales_invoice.js"
}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

fixtures = ['Custom Field', 'Property Setter', 'Print Format', 'Letter Head'
 ]

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "iac_electricals.install.before_install"
# after_install = "iac_electricals.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "iac_electricals.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

doc_events = {
	"Opportunity" : {
		"validate": "iac_electricals.iac_electricals.custom_scripts.opportunity.opportunity.validate"
	},
	"Employee" : {
   		"autoname" : "iac_electricals.iac_electricals.custom_scripts.employee.employee.autoname"
   },
   "Sales Order" : {
		"validate": "iac_electricals.iac_electricals.custom_scripts.sales_order.sales_order.validate"
	},
	"Sales Invoice" : {
		"validate": "iac_electricals.iac_electricals.custom_scripts.sales_invoice.sales_invoice.validate"
	}
}

# Scheduled Tasks
# ---------------

scheduler_events = {
# 	"all": [
# 		"iac_electricals.tasks.all"
# 	],
	"daily": [
		"iac_electricals.iac_electricals.custom_scripts.attendance.attendance.generate_leave_without_approval_reminder",
		"iac_electricals.iac_electricals.custom_scripts.attendance.attendance.birthday_reminder"
	],
# 	"hourly": [
# 		"iac_electricals.tasks.hourly"
# 	],
# 	"weekly": [
# 		"iac_electricals.tasks.weekly"
# 	]
# 	"monthly": [
# 		"iac_electricals.tasks.monthly"
# 	]
}

# Testing
# -------

# before_tests = "iac_electricals.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "iac_electricals.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "iac_electricals.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


# User Data Protection
# --------------------

user_data_fields = [
	{
		"doctype": "{doctype_1}",
		"filter_by": "{filter_by}",
		"redact_fields": ["{field_1}", "{field_2}"],
		"partial": 1,
	},
	{
		"doctype": "{doctype_2}",
		"filter_by": "{filter_by}",
		"partial": 1,
	},
	{
		"doctype": "{doctype_3}",
		"strict": False,
	},
	{
		"doctype": "{doctype_4}"
	}
]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"iac_electricals.auth.validate"
# ]

