// Copyright (c) 2023, erpcloud.systems and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Vehicle Washing History"] = {
	"filters": [
        {
			fieldname: "name",
			label: __("رقم المركبة"),
			fieldtype: "Link",
			options:"Vehicles"
		},
	]
};
