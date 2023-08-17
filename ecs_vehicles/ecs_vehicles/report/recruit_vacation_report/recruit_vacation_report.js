// Copyright (c) 2023, erpcloud.systems and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Recruit Vacation Report"] = {
	"filters": [
	    {
			fieldname: "start_date",
			label: __("تاريخ بداية الاجازة"),
			fieldtype: "Date",
		},
		{
			fieldname: "end_date",
			label: __("تاريخ نهاية الاجازة"),
			fieldtype: "Date",
		},
        {
			fieldname: "recruit",
			label: __("رقم المجند"),
			fieldtype: "Link",
			options: "Employee",
		},
        {
			fieldname: "overnight",
			label: __("نوع الاجازة"),
			fieldtype: "Select",
			options: ["","مبيت","اجازة دورية"],
			reqd: 1,
		},


	]
};