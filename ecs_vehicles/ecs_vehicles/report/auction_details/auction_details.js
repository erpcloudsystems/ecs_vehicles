// Copyright (c) 2023, erpcloud.systems and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Auction Details"] = {
	"filters": [
		{
            fieldname: "name",
            label: __("كود المزاد"),
            fieldtype: "Link",
            options: "Auction Info",
        },
		{
            label: __("رقم الشرطة "),
            fieldname: "police_no",
            fieldtype: "Data",
        },
		{
            label: __("رقم اللوط"),
            fieldname: "lot_no",
            fieldtype: "Data",
        },
		{
            label: __("رقم اللوط المجمع"),
            fieldname: "grouped_lot_no",
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
