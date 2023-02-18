// Copyright (c) 2023, erpcloud.systems and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Vehicle Liquid History"] = {
	"filters": [
        {
			fieldname: "name",
			label: __("رقم المركبة"),
			fieldtype: "Link",
			options: "Vehicles"
		},
		{
			fieldname: "issue_type",
			label: __("نوع السائل"),
			fieldtype: "Select",
			options: ["وقود","زيت","غاز","غسيل"],
			default: "وقود",
		},
		{
			fieldname: "from_date",
			label: __("من تاريخ"),
			fieldtype: "Date",
		},
		{
			fieldname: "to_date",
			label: __("إلى تاريخ"),
			fieldtype: "Date",
		},
	]
};

