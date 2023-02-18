// Copyright (c) 2023, erpcloud.systems and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Vehicles Stock Entry"] = {
	"filters": [
		{
			"fieldname": "vehicle",
			"label": __("كود المركبة"),
			"fieldtype": "Link",
			"options": "Vehicles",
			"reqd":1
		},
		{
			"fieldname": "maintenance",
			"label": __("إذن الصيانة"),
			"fieldtype": "Link",
			"options": "Maintenance Order",
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

		}
	]
}
