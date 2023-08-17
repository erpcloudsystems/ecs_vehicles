// Copyright (c) 2023, erpcloud.systems and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Total Count Of Reviewed Vouchers"] = {
	"filters": [
		{
			fieldname: "fiscal_year",
			label: __("السنة المالية"),
			fieldtype: "Link",
			options: "Fiscal Year",
			reqd: 1,
			default: frappe.defaults.get_user_default("fiscal_year"),
		},
		{
			fieldname: "batch_no",
			label: __("رقم الدفعة"),
			fieldtype: "Int",
			reqd: 1,
		}
	]
};
