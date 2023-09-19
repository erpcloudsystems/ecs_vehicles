// Copyright (c) 2023, erpcloud.systems and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Recruit Vacation Report"] = {
	"filters": [
	    {
			fieldname: "start_date",
			label: __("من تاريخ"),
			fieldtype: "Date",
		},
		{
			fieldname: "end_date",
			label: __("إلى تاريخ"),
			fieldtype: "Date",
		},
        {
			fieldname: "recruit",
			label: __("اسم المجند"),
			fieldtype: "Link",
			options: "Employee",
		},
        {
			fieldname: "overnight",
			label: __("نوع الاجازة"),
			fieldtype: "Select",
			options: ["","مبيت","أجازة دورية"],
		},


	]
};