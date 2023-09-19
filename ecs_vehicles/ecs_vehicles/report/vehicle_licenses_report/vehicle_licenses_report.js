// Copyright (c) 2022, erpcloud.systems and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Vehicle Licenses Report"] = {
	"filters": [
		{
            fieldname: "name",
            label: __("كارت الرخصة"),
            fieldtype: "Link",
            options: "Vehicle License",
        },
		{
            label: __("رقم الشرطة"),
            fieldname: "police_no",
            fieldtype: "Data",
        },
        {
            label: __("نوع المركبة"),
            fieldname: "vehicle_type",
            fieldtype: "Link",
            options:"Vehicle Type",

        },
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
            default: frappe.datetime.get_today(),


        },
        {
            fieldname:"to_date",
            label: __("إلى تاريخ"),
            fieldtype: "Date",
            default: frappe.datetime.get_today(),

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
				{ "value": "حذف رقم ملاكي", "label": __("حذف رقم ملاكي") },
				{ "value": "تعديل بيانات", "label": __("تعديل بيانات") },
				{ "value": "تصريح مؤقت", "label": __("تصريح مؤقت") },
			],

        },
        {
            label: __("بواسطة"),
            fieldname: "user",
            fieldtype: "Data",
        },
        {
            label: __("الرخصة على"),
            fieldname: "license_on",
            fieldtype: "Select",
            options: [
				{ "value": "اللوحة", "label": __("لوحة") },
				{ "value": "المركبة", "label": __("مركبة") },
			],
            default: "اللوحة",
        },

	]
};

