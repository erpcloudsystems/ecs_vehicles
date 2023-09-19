// Copyright (c) 2023, erpcloud.systems and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Vehicles Changes"] = {
	"filters": [
		{
			fieldname: "entity",
			label: __("الجهة"),
			fieldtype: "Link",
			options: "Entity",
			reqd:1,

		},
		{
			fieldname: "change_type",
			label: __("المتغيرات"),
			fieldtype: "Select",
			options: [
				"المــــــركبات الملــتحقة بالجــهة",
				"المــــــركبات التي تم نقلها من الجهة",
				"المــــــركبات التي تم إصالحها",
				"المــــــركبات التي تم تعطيلها",
				"المــــــركبات التي تم تخريدها",
			],
			reqd:1,

		},
		{
			fieldname: "from_date",
			label: __("من تاريخ"),
			fieldtype: "Date",
			reqd:1,
		},
		{
			fieldname:"to_date",
			label: __("إلى تاريخ"),
			fieldtype: "Date",
			reqd:1,

		},
	]
};
