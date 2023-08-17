// Copyright (c) 2023, erpcloud.systems and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Car Card"] = {
	"filters": [
        {
			fieldname: "vic_serial",
			label: __("رقم المركبة"),
			fieldtype: "Link",
			options: "Vehicles",
			reqd:1,

		},
		{
			fieldname: "part_universal_code",
			label: __("كود القطعة"),
			fieldtype: "Link",
			options:"Item",
			"get_query": function() {
				return {
					"doctype": "Item",
					"fields": ["name"],
					"filters": {
						"is_stock_item":1,
					},
				}
			},
			
		},
		// {
		// 	fieldname: "item_name",
		// 	label: __("اسم القطعة"),
		// 	fieldtype: "Data",
			
		// },
		{
			fieldname: "ezn_no",
			label: __("رقم الإذن"),
			fieldtype: "Data",
			
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
