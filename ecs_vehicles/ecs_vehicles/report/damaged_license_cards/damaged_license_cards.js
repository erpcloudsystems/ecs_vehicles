// Copyright (c) 2022, ERPCloud.Systems and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Damaged License Cards"] = {

	"filters": [
		{
            fieldname: "name",
            label: __("الرخصة"),
            fieldtype: "Link",
            options: "License Card",
        },

        {
            label: __("نوع المركبة"),
            fieldname: "vehicle_type",
            fieldtype: "Link",
            options:"Vehicle Type",

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
        {
            label: __("رقم الرخصة"),
            fieldname: "vehicle_license",
            fieldtype: "Link",
            options: "Vehicle License",
            
        },
        {
            label: __("المركبة"),
            fieldname: "vehicle",
            fieldtype: "Link",
            options: "Vehicles",
        },
        {
            label: __("حالة الإصدار"),
            fieldname: "issue_status",
            fieldtype: "Select",
			options: [
				"",
				{ "value": "ترخيص أول مرة", "label": __("ترخيص أول مرة") },
				{ "value": "تجديد", "label": __("تجديد") },

			],

        },
        {
            label: __("نوع التجديد"),
            fieldname: "renewal_type",
            fieldtype: "Select",
			options: [
				"",
				{ "value": "ترخيص أول مرة", "label": __("ترخيص أول مرة") },
				{ "value": "إنتهاء مدة", "label": __("إنتهاء مدة") },
				{ "value": "بدل فاقد", "label": __("بدل فاقد") },
				{ "value": "بدل تالف", "label": __("بدل تالف") },
				{ "value": "نقل إلى جهة", "label": __("نقل إلى جهة") },
				{ "value": "تعديل لون", "label": __("تعديل لون") },
				{ "value": "تعديل رقم الشاسيه", "label": __("تعديل رقم الشاسيه") },
				{ "value": "تعديل رقم المحرك", "label": __("تعديل رقم المحرك") },
				{ "value": "تعديل رقم الملاكي", "label": __("تعديل رقم الملاكي") },
				{ "value": "إضافة رقم ملاكي", "label": __("إضافة رقم ملاكي") },
				{ "value": "تعديل بيانات", "label": __("تعديل بيانات") },
			],

        },
        {
            label: __("بواسطة"),
            fieldname: "owner",
            fieldtype: "Link",
			options:"User"
        },

	]
};	
