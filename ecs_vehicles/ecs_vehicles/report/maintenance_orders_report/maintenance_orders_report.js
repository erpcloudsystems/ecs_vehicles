// Copyright (c) 2023, erpcloud.systems and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Maintenance Orders Report"] = {
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
			fieldname: "fiscal_year",
			label: __("السنة المالية"),
			fieldtype: "Link",
			options: "Fiscal Year",
		},
        {
			fieldname: "ezn_no",
			label: __("رقم الإذن"),
			fieldtype: "Data",
		},
		{
			fieldname: "maintenance_method",
			label: __("نوع الإجراء"),
			fieldtype: "Select",
			options: ["", "إذن صرف وإرتجاع", "حافظة مشتريات", "إصلاح خارجي", "إصلاح خارجي على الجهة", "شهادة إستبدال", "شهادة إرتجاع", "إذن صرف", "إصلاح داخلي"],
		},
	]
};