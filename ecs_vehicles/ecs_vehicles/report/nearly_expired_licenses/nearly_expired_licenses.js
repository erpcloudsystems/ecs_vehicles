
frappe.query_reports["Nearly Expired Licenses"] = {
	"filters":[

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
            label: __("عدد الأشهر قبل إنتهاء مدة الرخصة"),
            fieldname: "months_count",
            fieldtype: "Data",
            default:2,
        },
    ]
};	
