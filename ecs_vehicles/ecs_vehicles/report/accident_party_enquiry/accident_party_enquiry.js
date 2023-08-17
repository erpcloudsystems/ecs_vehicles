// Copyright (c) 2022, erpcloud.systems and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Accident Party Enquiry"] = {
	"filters": [
	    {
			fieldname: "party_name",
			label: __("اسم الشخص"),
			fieldtype: "Link",
			options: "Accident Party"
		},
		{
			fieldname: "entity",
			label: __("الجهة"),
			fieldtype: "Link",
			options: "Entity",
		},
        {
			fieldname: "party_id",
			label: __("رقم البطاقة"),
			fieldtype: "Data",
		},
		{
			fieldname: "party_id_type",
			label: __("نوع البطاقة"),
			fieldtype: "Link",
			options: "ID Type",
		},
        {
			fieldname: "police_no",
			label: __("رقم الشرطة"),
			fieldtype: "Data",
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