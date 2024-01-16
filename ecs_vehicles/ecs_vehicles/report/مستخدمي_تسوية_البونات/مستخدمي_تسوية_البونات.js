// Copyright (c) 2023, erpcloud.systems and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["مستخدمي تسوية البونات"] = {
	"filters": [

	    {
			fieldname: "user",
			label: __("المستخدم"),
			fieldtype: "Link",
			options:"User"
		},
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
			fieldname: "vr_name",
			label: __("رقم التسوية"),
			fieldtype: "Data",
		},
		{
			fieldname:"group_no",
			label: __("رقم المجموعة"),
			fieldtype: "Data",
			
		},
		{
			fieldname: "batch_no",
			label: __("رقم الدفعة"),
			fieldtype: "Data",
		},
		{
			fieldname: "release_date",
			label: __("إصدار"),
			fieldtype: "Link",
			options:"Release Date"
		}
]
}