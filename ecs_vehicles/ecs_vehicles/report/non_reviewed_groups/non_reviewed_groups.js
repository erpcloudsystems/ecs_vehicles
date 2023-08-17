frappe.query_reports["Non Reviewed Groups"] = {
	"filters": [
		{
			"fieldname": "fiscal_year",
			"label": __("السنة"),
			"fieldtype": "Link",
			"options": "Fiscal Year",
			"default": frappe.defaults.get_user_default("fiscal_year"),
			"reqd": 1,
		},
		{
			"fieldname": "batch_no",
			"label": __("رقم الدفعة"),
			"fieldtype": "Data",
			"reqd": 1,
		},
		{
			"fieldname": "from_group",
			"label": __("من مجموعة"),
			"fieldtype": "Int",
			"reqd": 1,
		},
		{
			"fieldname": "to_group",
			"label": __("إلى مجموعة"),
			"fieldtype": "Int",
			"reqd": 1,
		},
	]
}