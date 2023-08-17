// Copyright (c) 2023, erpcloud.systems and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Recruit Trials Report"] = {
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
			fieldname: "trial_type",
			label: __("نوع المحاكمة"),
			fieldtype: "Select",
			options: ["","عسكرية","مدنية"],
        },
	]
};