// Copyright (c) 2023, erpcloud.systems and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Liquids Issuing Report"] = {
	"filters": [
		{
			"fieldname": "entity",
			"label": __("الجهة"),
			"fieldtype": "Link",
			"options": "Entity",
			"reqd": 1,
		},
		{
			"fieldname": "issue_type",
			"label": __("نوع السائل"),
			"fieldtype": "Select",
			"depends_on": "entity",
			"options": [" ", "وقود", "زيت", "غاز", "غسيل"],
			"reqd": 1,

		},
		{
			"fieldname": "liquids_issuing",
			"label": __("الصرفية"),
			"fieldtype": "Link",
			"options": "Liquids Issuing",
			"depends_on": "issue_type",
			"get_query": function () {
				var entity = frappe.query_report.get_filter_value('entity');
				var issue_type = frappe.query_report.get_filter_value('issue_type');
				return {
					"doctype": "Liquids Issuing",
					"fields": ["name"],
					"filters": {
						"entity": entity,
						"issue_type": issue_type,
						"submitted": 1,
					},
					"order_by": ["issue_date asc"],
				}
			},
			"reqd": 1,
		}
	]
}
