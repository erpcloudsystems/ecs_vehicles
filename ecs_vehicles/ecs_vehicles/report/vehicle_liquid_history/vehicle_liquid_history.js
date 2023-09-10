// Copyright (c) 2023, erpcloud.systems and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Vehicle Liquid History"] = {
	"filters": [
		{
			fieldname: "name",
			label: __("رقم المركبة"),
			fieldtype: "Data",
			reqd: 1
		},
		{
			fieldname: "entity",
			label: __("الجهة"),
			fieldtype: "Link",
			options: "Entity"
		},
		{
			fieldname: "vehicle_type",
			label: __("نوع المركبة"),
			fieldtype: "Link",
			options: "Vehicle Type"
		},
		{
			fieldname: "issue_type",
			label: __("نوع السائل"),
			fieldtype: "Select",
			options: ["وقود", "زيت", "غاز", "غسيل"],
			default: "وقود",
		},
		{
			fieldname: "from_date",
			label: __("من تاريخ"),
			fieldtype: "Date",
			default: frappe.datetime.add_months(frappe.datetime.month_start(), -84),
		},
		{
			fieldname: "to_date",
			label: __("إلى تاريخ"),
			fieldtype: "Date",
			default: frappe.datetime.get_today(),
		},
	]
};

