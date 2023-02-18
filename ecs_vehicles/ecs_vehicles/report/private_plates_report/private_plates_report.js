// Copyright (c) 2023, erpcloud.systems and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Private Plates Report"] = {
		"filters": [

        {
			fieldname: "plate_no",
			label: __("رقم الملاكي"),
			fieldtype: "Link",
			options: "Private Plate",
			reqd:1,
		},
	]
};