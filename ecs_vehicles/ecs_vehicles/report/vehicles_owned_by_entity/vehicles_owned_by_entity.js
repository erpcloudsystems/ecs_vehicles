// Copyright (c) 2023, erpcloud.systems and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Vehicles Owned by Entity"] = {
	"filters": [
		{
			fieldname: "entity",
			label: __("الجهة"),
			fieldtype: "Link",
			options: "Entity",
			reqd:1
		},
		{
			fieldname: "posting_date",
			label: __("التاريخ"),
			fieldtype: "Date",
			default:frappe.datetime.nowdate(),
			reqd:1,
			hidden:0
			
		},
		{
			fieldname: "page_length",
			label: __("عدد الصفحات الفارغة "),
			fieldtype: "Int",
			default:0,
		},

	]
};
