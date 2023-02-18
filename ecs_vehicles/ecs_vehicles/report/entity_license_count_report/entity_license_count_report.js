// Copyright (c) 2022, ERPCloud.Systems and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Entity License Count Report"] = {
	"filters": [

        {
            label: __("الجهة"),
            fieldname: "entity",
            fieldtype: "Link",
            options:"Entity",

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
