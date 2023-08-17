// Copyright (c) 2023, erpcloud.systems and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["External Assignment Report"] = {
	"filters": [
	    {
			fieldname: "from_date",
			label: __("من تاريخ"),
			fieldtype: "Date",
			default: frappe.datetime.add_months(frappe.datetime.get_today(), -12),
		},
		{
			fieldname:"to_date",
			label: __("إلى تاريخ"),
			fieldtype: "Date",
			default: frappe.datetime.get_today(),
		},
        {
			fieldname: "recruit",
			label: __("رقم المجند"),
			fieldtype: "Link",
			options: "Employee",
		},
        {
			fieldname: "assignment_entities",
			label: __("جهات الانتداب"),
			fieldtype: "Link",
			options: "Assignment Entities",
		},

	]
};