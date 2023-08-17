// Copyright (c) 2023, erpcloud.systems and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Job Orders Report"] = {
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
			fieldname: "vehicle_no",
			label: __("رقم الشرطة"),
			fieldtype: "Data",
		},
		{
			fieldname: "entity_name",
			label: __("الجهة"),
			fieldtype: "Link",
			options: "Entity",
		},
		{
			fieldname: "vehicle_brand",
			label: __("الماركة"),
			fieldtype: "Link",
			options: "Vehicle Brand",
		},
		{
			fieldname: "vehicle_style",
			label: __("الطراز"),
			fieldtype: "Link",
			options: "Vehicle Style",
		},
		{
			fieldname: "vehicle_model",
			label: __("الموديل"),
			fieldtype: "Link",
			options: "Vehicle Model",
		},
		{
			fieldname: "supplier",
			label: __("المتعهد"),
			fieldtype: "Link",
			options: "Supplier",
		},
        {
			fieldname: "job_order_no",
			label: __("رقم أمر الشغل"),
			fieldtype: "Data",
		},
		{
			fieldname: "checkup",
			label: __("الفحص"),
			fieldtype: "Select",
			options: ["", "مسدد", "غير مسدد"]
		},
	]
};