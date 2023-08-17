// Copyright (c) 2023, erpcloud.systems and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Liquid Vouchers Issuing Report"] = {
	"filters": [
		{
			fieldname: "from_date",
			label: __("من تاريخ"),
			fieldtype: "Date",
			default: frappe.datetime.get_today(),
		},
		{
			fieldname:"to_date",
			label: __("إلى تاريخ"),
			fieldtype: "Date",	
			default: frappe.datetime.get_today(),
		},
		{
			fieldname: "issue_type",
			label: __("نوع السائل"),
			fieldtype: "Select",
			default: "وقود",
			options: [" ", "وقود", "زيت", "غسيل"],
			reqd: 1,
		},
		{
			fieldname: "entity",
			label: __("الجهة"),
			fieldtype: "Link",
			options:"Entity",
		},
		// {
		// 	fieldname: "liquids_issuing",
		// 	label: __("الصرفية"),
		// 	fieldtype: "Link",
		// 	options: "Liquids Issuing",
		// 	depends_on: "issue_type",
		// 	get_query: function() {
		// 		var entity = frappe.query_report.get_filter_value('entity');
		// 		var issue_type = frappe.query_report.get_filter_value('issue_type');
		// 		var from_date = frappe.query_report.get_filter_value('from_date');
		// 		var to_date = frappe.query_report.get_filter_value('to_date');
		// 		return {
		// 			"doctype": "Liquids Issuing",
		// 			"fields": ["name"],
		// 			"filters": {
		// 				"entity": ["=", entity],
		// 				"issue_type": ["=", issue_type],
		// 				"issue_date": ["between", from_date, to_date],
		// 				"submitted": ["=", 1],
		// 			},
		// 			"order_by":"name",
		// 		}
		// 	},
		// }
	]
}
