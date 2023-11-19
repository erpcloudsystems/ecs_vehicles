// Copyright (c) 2023, erpcloud.systems and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Item Warehouse Balance"] = {
	"filters": [
        {
			fieldname: "warehouse",
			label: __("المخزن"),
			fieldtype: "Link",
			options: "Warehouse",
		},
		{
			fieldname: "vehicle_brand",
			label: __("الماركة"),
			fieldtype: "Link",
			options: "Stock Brand",
			depends_on: "warehouse",
			"get_query": function () {
				var warehouse = frappe.query_report.get_filter_value('warehouse');
				return {
					"doctype": "Stock Brand",
					"fields": ["name"],
					"filters": {
						"warehouse": warehouse,
					},
				}
			},
		},
		{
			fieldname: "vehicle_model",
			label: __("الموديل"),
			fieldtype: "Data",
			depends_on: "warehouse",
		},
		{
			fieldname: "item_name",
			label: __("اسم الصنف"),
			fieldtype: "Data",
		},
		// {
		// 	fieldname: "item_code",
		// 	label: __("كود القطعة"),
		// 	fieldtype: "Link",
		// 	options:"Item",
		// 	"get_query": function() {
		// 		return {
		// 			"doctype": "Item",
		// 			"fields": ["name"],
		// 			"filters": {
		// 				"is_stock_item":1,
		// 				"item_category":"مخازن",
		// 			},
		// 		}
		// 	},
	]
};
