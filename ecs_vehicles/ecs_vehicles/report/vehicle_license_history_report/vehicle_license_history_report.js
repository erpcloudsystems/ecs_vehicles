// Copyright (c) 2022, erpcloud.systems and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Vehicle License History Report"] = {
	"filters": [
		{
            fieldname: "name",
            label: __("المركبة"),
            fieldtype: "Data",
        },
        {
            label: __("رقم الرخصة"),
            fieldname: "license_no",
            fieldtype: "Link",
            options:"License Card",

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
            label: __("مدة الترخيص"),
            fieldname: "license_duration",
            fieldtype: "Select",
            options: [
				"",
				{ "value": "1", "label": __("سنة") },
				{ "value": "3", "label": __("3 سنوات") },
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

	]
};

