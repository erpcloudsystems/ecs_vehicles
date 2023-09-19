// Copyright (c) 2022, ERPCloud.Systems and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Vehicle Doesn't Have License Yet"] = {
	"filters":[
//	        {
//           label: __("من تاريخ"),
//            fieldname: "license_from_date",
//            fieldtype: "Date",
//
//        },
//        {
//            label: __("إلى تاريخ"),
//            fieldname: "license_to_date",
//            fieldtype: "Date",
//
//        },
        {
            label: __("كود المركبة"),
            fieldname: "name",
            options: "Vehicles",
            fieldtype: "Link",
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
            label: __("الشكل"),
            fieldname: "vehicle_shape",
            fieldtype: "Link",
            options:"Vehicle Shape",
        },
        {
            label: __("الماركة"),
            fieldname: "vehicle_brand",
            fieldtype: "Link",
            options:"Vehicle Brand",
        },
        {
            label: __("رقم الشاسيه"),
            fieldname: "chassis_no",
            fieldtype: "Data",
            
        },
        {
            label: __("بلد الصنع"),
            fieldname: "vehicle_country",
            fieldtype: "Link",
            options:"Vehicle Country",        
		},

        {
            label: __("مخصص الصرف"),
            fieldname: "exchange_allowance",
            fieldtype: "Link",
            options:"Exchange Allowance", 
        },
        {
            label: __("الجهة"),
            fieldname: "entity",
            fieldtype: "Link",
            options:"Entity", 
		},
        {
            label: __("حالة المركبة"),
            fieldname: "vehicle_status",
			fieldtype: "Link",
            options:"Vehicle Status", 
        },
        {
            label: __("رقم كارت الرخصة"),
            fieldname: "license_no",
            fieldtype: "Link",
            options:"License Card",
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
