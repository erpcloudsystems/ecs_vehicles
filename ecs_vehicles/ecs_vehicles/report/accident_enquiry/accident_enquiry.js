// Copyright (c) 2022, erpcloud.systems and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Accident Enquiry"] = {
	"filters": [
	    {
			fieldname: "from_date",
			label: __("من تاريخ"),
			fieldtype: "Date",
			default: frappe.datetime.add_months(frappe.datetime.get_today(), -6),
		},
		{
			fieldname:"to_date",
			label: __("إلى تاريخ"),
			fieldtype: "Date",
			default: frappe.datetime.get_today(),
		},
        {
			fieldname: "police_no",
			label: __("رقم الشرطة"),
			fieldtype: "Data",
		},
		{
			fieldname: "entity",
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
			fieldname: "accident_no",
			label: __("رقم الواقعة"),
			fieldtype: "Data",
		},
		{
			fieldname: "name",
			label: __("كود الواقعة"),
			fieldtype: "Link",
			options: "Accident",
		},
		{
			fieldname: "accident_type",
			label: __("نوع الواقعة"),
			fieldtype: "Link",
			options: "Accident Type",
		},
	]
};