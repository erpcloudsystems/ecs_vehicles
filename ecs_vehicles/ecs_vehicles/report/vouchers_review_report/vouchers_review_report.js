// Copyright (c) 2023, erpcloud.systems and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Vouchers Review Report"] = {
	"filters": [
		{
			"fieldname": "company_name",
			"label": __("اسم الشركة"),
			"fieldtype": "Link",
			"options": "Gas Station"
		},
		{
			"fieldname": "fiscal_year",
			"label": __("السنة"),
			"fieldtype": "Link",
			"options": "Fiscal Year",
			"default": frappe.defaults.get_user_default("fiscal_year"),
		},
		{
			"fieldname": "batch_no",
			"label": __("رقم الدفعة"),
			"fieldtype": "Data",
		},
		{
			"fieldname": "group_no",
			"label": __("رقم المجموعة"),
			"fieldtype": "Data",
		},
		{
			"fieldname": "user",
			"label": __("اسم المستخدم"),
			"fieldtype": "Link",
			"options": "User",

		},

		
		{
			"fieldname": "batch_from_date",
			"label": __("تاريخ الدفعة من"),
			"fieldtype": "Date",
		},
		{
			"fieldname": "batch_to_date",
			"label": __("تاريخ الدفعة إلى"),
			"fieldtype": "Date",
		},
		{
			"fieldname": "revision_from_date",
			"label": __("تاريخ المراجعة من"),
			"fieldtype": "Date",
		},
		{
			"fieldname": "revision_to_date",
			"label": __("تاريخ المراجعة إلى"),
			"fieldtype": "Date",
		},
	
	]
}
