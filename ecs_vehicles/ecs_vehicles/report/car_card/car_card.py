# Copyright (c) 2023, erpcloud.systems and contributors
# For license information, please see license.txt
import frappe


def execute(filters=None):
    columns, data = [], []
    columns = get_columns()
    data = get_data(filters, columns)
    return columns, data


def get_columns():
    return [
               {
            "label": ("كود القطعة"),
            "fieldname": "item_code",
            "fieldtype": "Link",
            "options": "Item",
            "width": 100
        },
         {
            "label": ("قطعة الغيار"),
            "fieldname": "item_name",
            "fieldtype": "Data",

            "width": 100
        },
         {
            "label": ("تاريخ الإجراء"),
            "fieldname": "date",
            "fieldtype": "data",
            "width": 120
        },
        {
            "label": ("الكمية"),
            "fieldname": "qty",
            "fieldtype": "Data",
            "width": 90
        },
        {
            "label": ("الوحدة"),
            "fieldname": "default_unit_of_measure",
            "fieldtype": "Data",
            "width": 150
        },
        {
            "label": ("المنشأ"),
            "fieldname": "brand",
            "fieldtype": "Data",
            "width": 80
        },
        {
            "label": ("الصلاحية"),
            "fieldname": "validity",
            "fieldtype": "Data",
            "width": 220
        },
        {
            "label": ("نوع النموذج"),
            "fieldname": "namozg",
            "fieldtype": "Data",
            "width": 150
        },
        {
            "label": ("رقم النموذج"),
            "fieldname": "ezn_no",
            "fieldtype": "Data",
            "width": 150
        },
        {
            "label": ("تاريخ النموذج"),
            "fieldname": "date2",
            "fieldtype": "Data",
            "width": 70
        },
        {
            "label": ("جهة الصيانة"),
            "fieldname": "maintenance_entity",
            "fieldtype": "Data",
            "width": 120
        },
        {
            "label": ("نوع الورش"),
            "fieldname": "werash",
            "fieldtype": "Data",
            "width": 120
        },
        {
            "label": ("إسم الورشة"),
            "fieldname": "werash_name",
            "fieldtype": "Data",
            "width": 120
        },

    ]

def get_data(filters, columns):
    item_price_qty_data = []
    item_price_qty_data = get_item_price_qty_data(filters)
    return item_price_qty_data


def get_item_price_qty_data(filters):
    conditions = ""
    conditions1=""
    conditions2 =""
    conditions3=""
    if filters.get("name"):
        conditions1 += "and maintenance_order.vehicle_no = %(name)s"
    if filters.get("from_date"):
        conditions1 += " and maintenance_order.date >= %(from_date)s"
    if filters.get("to_date"):
        conditions1 += " and maintenance_order.date <= %(to_date)s"
    if filters.get("name"):
        conditions2 += "and custody_report.vehicle_no = %(name)s"
    if filters.get("from_date"):
        conditions2 += " and custody_report.date >= %(from_date)s"
    if filters.get("to_date"):
        conditions2 += " and custody_report.date <= %(to_date)s"
    if filters.get("name"):
        conditions3 += "and job_order.vehicle_no = %(name)s"
    if filters.get("from_date"):
        conditions3 += " and job_order.date >= %(from_date)s"
    if filters.get("to_date"):
        conditions3 += " and job_order.date <= %(to_date)s"

    result = []
    item_results = frappe.db.sql("""
        (Select
            maintenance_order.name as name,
			maintenance_order.vehicle_no as vehicle_no,
			maintenance_order.vehicles as vehicles,	
			maintenance_order.date as date,
            maintenance_order.ezn_no as ezn_no,
            maintenance_order.entity_name as maintenance_entity,
			maintenance_order_item.item_code as item_code,
			maintenance_order_item.item_name as item_name,
			maintenance_order_item.qty as qty,
			maintenance_order_item.default_unit_of_measure as default_unit_of_measure,
			maintenance_order_item.brand as brand,

			maintenance_order_item.last_issue_detail as last_issue_detail

        from `tabMaintenance Order` maintenance_order join `tabMaintenance Order Item` maintenance_order_item on maintenance_order.name = maintenance_order_item.parent
        where maintenance_order.docstatus = 1
        {conditions1}
       )
        UNION
        (Select
            custody_report.name as name,
			custody_report.vehicle_no as vehicle_no,
			custody_report.vehicles as vehicles,	
			custody_report.date as date,
            custody_report.ezn_no as ezn_no,
            custody_report.entity_name as maintenance_entity,
			custody_report_item.item_code as item_code,
			custody_report_item.item_name as item_name,
			custody_report_item.qty as qty,
			custody_report_item.default_unit_of_measure as default_unit_of_measure,
			custody_report_item.brand as brand,
			custody_report_item.last_issue_detail as last_issue_detail

        from `tabCustody Report` custody_report join `tabCustody Report Item` custody_report_item on custody_report.name = custody_report_item.parent
        where custody_report.docstatus = 1
        {conditions2}
        )
        UNION
        (Select
            job_order.name as name,
			job_order.vehicle_no as vehicle_no,
			job_order.vehicles as vehicles,	
			job_order.date as date,
            job_order.ezn_no as ezn_no,
            job_order.entity_name as maintenance_entity,
			job_order_item.item_code as item_code,
			job_order_item.item_name as item_name,
			job_order_item.qty as qty,
			job_order_item.default_unit_of_measure as default_unit_of_measure,
			job_order_item.brand as brand,
			job_order.supplier as last_issue_detail

        from `tabJob Order` job_order join `tabJob Order Item` job_order_item on job_order.name = job_order_item.parent
        where job_order.docstatus = 1
        {conditions3}
        )
        """.format(conditions1=conditions1, conditions2=conditions2, conditions3=conditions3), filters, as_dict=1)

    for item_dict in item_results:
        data = {
			'item_code': item_dict.item_code,
			'item_name': item_dict.item_name,
            'date': item_dict.date if  item_dict.date else "-",
			'qty': item_dict.qty.split(".")[0] if  item_dict.qty else "-",
            'default_unit_of_measure': item_dict.default_unit_of_measure if  item_dict.default_unit_of_measure else "-",
            'brand': item_dict.brand if  item_dict.brand else "-",
            'validity': 100,
            'ezn_no': item_dict.ezn_no if  item_dict.ezn_no else "-",
            "namozg": "تحت القيد" if  item_dict.name.startswith("C-R") else "إستمارة صرف" if item_dict.name.startswith("MO") else "أمر شغل مباشر",
            'date2': item_dict.date if  item_dict.date else "-",
            'maintenance_entity': item_dict.maintenance_entity if  item_dict.maintenance_entity else "-",
            'werash': "ورش داخلية" if not item_dict.name.startswith("J-O") else "ورش خارجية",
			'werash_name': item_dict.item_name if not item_dict.name.startswith("J-O") else item_dict.last_issue_detail,
        }

        result.append(data)
    # if filters.get("name") and result:
    name = frappe.db.get_value("Vehicles", {"vehicle_no": filters.get("name")}, ["name"])
    veh_name = frappe.get_doc("Vehicles", str(name))

    # vehicle_brand, vehicle_style,vehicle_shape, entity_name, private_no, vehicle_model,possession_date, motor_no,chassis_no = frappe.db.get_value("Vehicles", {"vehicle_no": filters.get("name")}, ["vehicle_brand", "vehicle_style","vehicle_shape", "entity_name", "private_no", "vehicle_model","possession_date", "motor_no","chassis_no" ])
    result[0]["user"] = frappe.db.get_value("User", frappe.session.user, ["full_name"])
    result[0]["vehicle_brand"] = veh_name.vehicle_brand or "-"
    result[0]["vehicle_style"] = veh_name.vehicle_style or "-"
    result[0]["vehicle_shape"] = veh_name.vehicle_shape or "-"
    result[0]["entity_name"] = veh_name.entity_name or "-"
    result[0]["private_no"] = veh_name.private_no or "-"
    result[0]["vehicle_model"] = veh_name.vehicle_model or "-"
    result[0]["possession_date"] = veh_name.possession_date or "-"
    result[0]["chassis_no"] = veh_name.chassis_no or "-"
    result[0]["motor_no"] = veh_name.motor_no or "-"


    return result