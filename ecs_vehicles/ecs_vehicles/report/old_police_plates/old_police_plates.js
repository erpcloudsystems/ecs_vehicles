// Copyright (c) 2023, erpcloud.systems and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Old Police Plates"] = {
	"filters": [
        {
			fieldname: "name",
			label: __("رقم المركبة"),
			fieldtype: "Link",
			options: "Vehicles",
		},
		{
			fieldname: "vehicle_type",
			label: __("النوع"),
			fieldtype: "Link",
			options: "Vehicle Type",
			default:"سيارة"
		},
        {
			fieldname: "vehicle_shape",
			label: __("الشكل"),
			fieldtype: "Link",
			options: "Vehicle Shape",
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
			fieldname: "vehicle_color",
			label: __("اللون"),
			fieldtype: "Link",
			options: "Vehicle Color",
		},
		{
			fieldname: "entity",
			label: __("الجهة"),
			fieldtype: "Link",
			options: "Entity",
		},
		{
			fieldname: "motor_no",
			label: __("رقم الموتور"),
			fieldtype: "Data",
		},
		{
			fieldname: "chassis_no",
			label: __("رقم الشاسيه"),
			fieldtype: "Data",
		},
		{
			fieldname: "private_no",
			label: __("رقم الملاكي"),
			fieldtype: "Link",
			options: "Private Plate",
		},
		{
			fieldname: "vehicle_status",
			label: __("الحالة"),
			fieldtype: "Link",
			options: "Vehicle Status",
		},
		{
			fieldname: "maintenance_entity",
			label: __("جهة الصيانة"),
			fieldtype: "Link",
			options: "Maintenance Entity",
		},
		{
			fieldname: "processing_type",
			label: __("نوع التجهيز"),
			fieldtype: "Link",
			options: "Vehicle Processing Type",
		},
		{
			fieldname: "exchange_allowance",
			label: __("مخصص الصرف"),
			fieldtype: "Link",
			options: "Exchange Allowance",
		},
		{
			fieldname: "fuel_type",
			label: __("نوع الوقود"),
			fieldtype: "Link",
			options: "Fuel Type",
		},
        {
			fieldname: "cylinder_count",
			label: __("عدد السلندرات"),
			fieldtype: "Link",
			options: "Cylinder Count",
		},
//		{
//			fieldname: "from_date",
//			label: __("منشئة من تاريخ"),
//			fieldtype: "Date",
//		},
//		{
//			fieldname: "to_date",
//			label: __("منشئة إلى تاريخ"),
//			fieldtype: "Date",
//		},
	]
};