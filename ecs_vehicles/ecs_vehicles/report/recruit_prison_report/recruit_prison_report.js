

frappe.query_reports["Recruit Prison Report"] = {
	"filters": [
	    {
			fieldname: "start_date",
			label: __("من تاريخ"),
			fieldtype: "Date",
		},
		{
			fieldname: "end_date",
			label: __("إلى تاريخ"),
			fieldtype: "Date",
		},
        {
			fieldname: "recruit",
			label: __("اسم المجند"),
			fieldtype: "Link",
			options: "Employee",
		},
        // {
		// 	fieldname: "overnight",
		// 	label: __("نوع الاجازة"),
		// 	fieldtype: "Select",
		// 	options: ["","مبيت","أجازة دورية"],
		// },


	]
};