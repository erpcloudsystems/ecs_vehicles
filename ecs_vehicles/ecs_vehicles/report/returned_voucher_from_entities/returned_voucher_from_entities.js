// Copyright (c) 2023, erpcloud.systems and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Returned Voucher From Entities"] = {
	"filters": [
		{
			"fieldname": "entity",
			"label": __("الجهة"),
			"fieldtype": "Link",
			"options":"Entity",
		},
		{
			"fieldname": "release_date",
			"label": __("تاريخ الإصدار"),
			"fieldtype": "Link",
			"options": "Release Date",
		},
		{
			"fieldname": "from_date",
			"label": __("من تاريخ"),
			"fieldtype": "Date",
		},
		{
			"fieldname": "to_date",
			"label": __("إلى تاريخ"),
			"fieldtype": "Date",
		},
	]
}
