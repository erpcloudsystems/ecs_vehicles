// Copyright (c) 2023, erpcloud.systems and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Police Plates Report"] = {
	"filters": [
        {
			fieldname: "plate_no",
			label: __("رقم الشرطة"),
			fieldtype: "Data",
			reqd: 1,
		},
	]
};