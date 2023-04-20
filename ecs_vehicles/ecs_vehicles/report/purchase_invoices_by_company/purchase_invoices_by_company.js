// Copyright (c) 2023, erpcloud.systems and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Purchase Invoices By Company"] = {
	"filters": [
		{
			fieldname: "supplier",
			label: __("المورد"),
			fieldtype: "Link",
			options: "Supplier",
			reqd:1
		},
		{
			fieldname: "from_date",
			label: __("من تاريخ"),
			fieldtype: "Date",
			
		},
		{
			fieldname:"to_date",
			label: __("إلى تاريخ"),
			fieldtype: "Date",
			
		},
	]
};
