// Copyright (c) 2023, erpcloud.systems and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Reviewed Vouchers Count Report"] = {
	"filters": [
		{
			"fieldname": "from_date",
			"label": __("من تاريخ"),
			"fieldtype": "Date",
			"default": frappe.datetime.get_today(),
		},
		{
			"fieldname": "to_date",
			"label": __("إلى تاريخ"),
			"fieldtype": "Date",
			"default": frappe.datetime.get_today(),
		},
		{
			"fieldname": "fuel",
			"label": __("وقود"),
			"fieldtype": "Check",
			"default":1,
		},
		{
			"fieldname": "oil",
			"label": __("زيت"),
			"fieldtype": "Check",
			"default":1,

		},
		{
			"fieldname": "gas",
			"label": __("غاز"),
			"fieldtype": "Check",
			"default":1,

		},
		{
			"fieldname": "washing",
			"label": __("غسيل"),
			"fieldtype": "Check",
			"default":1,

		},
				{
			"fieldname": "release_date",
			"label": __("تاريخ الإصدار"),
			"fieldtype": "Link",
			"options": "Release Date",
		},
	]
}
