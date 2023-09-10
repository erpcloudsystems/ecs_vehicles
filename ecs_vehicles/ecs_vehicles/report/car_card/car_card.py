# Copyright (c) 2023, erpcloud.systems and contributors
# For license information, please see license.txt
import frappe


def execute(filters=None):
    columns, data = [], []
    columns = get_columns()
    data = get_data(filters, columns)
    header = ""
    
    entity = "<b> رقم الشرطة  : </b>{0}  <span style='margin-right:50px'></span> <b> الجهة : </b>{1}  <span style='margin-right:50px'></span> <b> نوع التجهيز  : </b>{2} <span style='margin-right:50px'></span> ".format(data[0]["vehicle_no"], data[0]["entity_name"], data[0]["processing_type"])
    vehicle_brand = "<b> نوع المركبة : </b>{0}  <span style='margin-right:50px'></span> <b> مجموعة الشكل  : </b>{1}  <span style='margin-right:50px'></span> <b> الشكل : </b>{2}  <br>".format(data[0]["vehicle_type"], data[0]["group_shape"], data[0]["vehicle_shape"])
    vehicle_style = "<b> الماركة : </b>{0}  <span style='margin-right:50px'></span> <b> الطراز  : </b>{1} <span style='margin-right:50px'></span>  <b> الموديل : </b>{2} <span style='margin-right:50px'></span> ".format(data[0]["vehicle_brand"], data[0]["vehicle_style"], data[0]["vehicle_model"])
    exchange_allowance = "<b> رقم الشاسيه  : </b>{0}  <span style='margin-right:50px'></span> <b> رقم الموتور  : </b>{1}  <span style='margin-right:50px'></span> <b> نوع الوقود  : </b>{2} <span style='margin-right:50px'></span>".format(data[0]["chassis_no"], data[0]["motor_no"], data[0]["fuel_type"])
    private_no = "<b> تاريخ الحيازة : </b>{0}  <br>".format(data[0]["possession_date"] or "0")
    header = " "  + entity + " " + vehicle_brand + " " + vehicle_style + " " + exchange_allowance  + " " + private_no 

    message = [header]
    return columns, data, message


def get_columns():
    return [
                {
            "label": ("نوع النموذج"),
            "fieldname": "namozg",
            "fieldtype": "Data",
            "width": 130
        },
        {
            "label": ("رقم النموذج"),
            "fieldname": "ezn_no",
            "fieldtype": "Data",
            "width": 120
        },
        
        {
            "label": ("قطعة الغيار"),
            "fieldname": "item_name",
            "fieldtype": "Data",

            "width": 200
        },
        {
            "label": ("تاريخ الإجراء"),
            "fieldname": "date",
            "fieldtype": "data",
            "width": 110
        },
        {
            "label": ("الكمية"),
            "fieldname": "qty",
            "fieldtype": "Data",
            "width": 70
        },
        {
            "label": ("الوحدة"),
            "fieldname": "default_unit_of_measure",
            "fieldtype": "Data",
            "width": 90
        },
        {
            "label": ("الصلاحية"),
            "fieldname": "validity",
            "fieldtype": "Data",
            "width": 90
        },

        {
            "label": ("تاريخ النموذج"),
            "fieldname": "date2",
            "fieldtype": "Data",
            "width": 110
        },
        
        {
            "label": ("نوع الورش"),
            "fieldname": "werash",
            "fieldtype": "Data",
            "width": 110
        },
        {
            "label": ("إسم الورشة"),
            "fieldname": "werash_name",
            "fieldtype": "Data",
            "width": 180
        },
        {
            "label": ("الكارتة"),
            "fieldname": "name",
            "fieldtype": "Link",
            "options": "Karta Ledger Entry",
            "width": 100
        },
        {
            "label": ("كود القطعة"),
            "fieldname": "item_code",
            "fieldtype": "Link",
            "options": "Item",
            "width": 90
        },
        {
            "label": ("المنشأ"),
            "fieldname": "brand",
            "fieldtype": "Data",
            "width": 80
        },
        {
            "label": ("جهة الصيانة"),
            "fieldname": "maintenance_entity",
            "fieldtype": "Data",
            "width": 140
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
    if filters.get("part_universal_code"):
        conditions += "and stock_ledger.part_universal_code = %(part_universal_code)s"
    # if filters.get("name"):
    #     conditions1 += "and maintenance_order1.vehicle_no = %(name)s"
    if filters.get("from_date"):
        conditions += " and stock_ledger.action_date >= %(from_date)s"
    if filters.get("to_date"):
        conditions += " and stock_ledger.action_date <= %(to_date)s"
    if filters.get("item_name"):
        conditions += "and item.item_name = %(item_name)s"
    if filters.get("ezn_no"):
        conditions += "and stock_ledger.ezn_no = %(ezn_no)s"
    if filters.get("maintenance_method"):
        conditions += "and stock_ledger.maintenance_method = %(maintenance_method)s"
    # if filters.get("name"):
    #     conditions2 += "and maintenance_order.vehicle_no = %(name)s"
    # if filters.get("from_date"):
    #     conditions += " and maintenance_order.date >= %(from_date)s"
    # if filters.get("to_date"):
    #     conditions += " and maintenance_order.date <= %(to_date)s"
    if filters.get("vic_serial"):
        conditions3 += "and stock_ledger.vic_serial = %(vic_serial)s"
    # if filters.get("name"):
    #     conditions3 += "and purchase_invoice.vehicle_no = %(name)s"
    if filters.get("from_date"):
        conditions3 += " and stock_ledger.action_date >= %(from_date)s"
    if filters.get("to_date"):
        conditions3 += " and stock_ledger.action_date <= %(to_date)s"

    result = []

    item_results = frappe.db.sql("""
            select 
            stock_ledger.name as name,
            stock_ledger.part_universal_code as item_code,
            item.item_name,
            stock_ledger.ord_serial,
            stock_ledger.part_unit,
            stock_ledger.part_status_ratio,
            stock_ledger.trans_type, 
            stock_ledger.action_date,
            stock_ledger.part_qty,
            stock_ledger.ezn_no, 
            stock_ledger.doc_type, 
            stock_ledger.doc_no, 
            stock_ledger.maintenance_method, 
            stock_ledger.workshop_type,
            stock_ledger.workshop_name
            from `tabKarta Ledger Entry` stock_ledger 
            join `tabItem` item on stock_ledger.part_universal_code = item.item_code
            where stock_ledger.del_flag = "0"
            and stock_ledger.vic_serial = "{vehicles}"
            {conditions}
            order by item.item_name, stock_ledger.action_date desc
        """.format(vehicles=filters.get("vic_serial"), conditions=conditions, conditions3=conditions3), filters, as_dict=1)

    for item_dict in item_results:
        namozg_type = ""
        if item_dict.doc_type == "Add To Karta" or item_dict.doc_type == "1":
            namozg_type = "خطاب جهة"
        elif item_dict.doc_type == "2":
            namozg_type = "إستمارة صرف"
        elif item_dict.doc_type == "3":
            namozg_type = "شهادة إستبدال"
        elif item_dict.doc_type == "4":
            namozg_type = "إذن ورشة"
        elif item_dict.doc_type == "Purchase Invoices" or item_dict.doc_type == "5" or (item_dict.doc_type == "Vehicle Maintenance Process" and item_dict.maintenance_method != "إذن صرف وإرتجاع"):
            namozg_type = "أمر شغل مباشر"
        elif item_dict.doc_type == "6":
            namozg_type = "أمر شغل ممارسات"
        elif item_dict.doc_type == "7":
            namozg_type = "شهادة إرتجاع"
        elif (item_dict.doc_type == "Vehicle Maintenance Process" and item_dict.maintenance_method == "إذن صرف وإرتجاع") or item_dict.doc_type == "Maintenance Order" or item_dict.doc_type == "8":
            namozg_type = "تحت القيد"
        else:
            namozg_type = "-"

        if item_dict.maintenance_method == "إصلاح خارجي" and item_dict.ord_serial.startswith("VMP-"):
            pass
        else:
            data = {
                "name":item_dict.name,
                'item_code': item_dict.item_code,
                'item_name': item_dict.item_name,
                'date': item_dict.action_date if  item_dict.action_date else "-",
                'qty': item_dict.part_qty if item_dict.part_qty >= 0 else -1 * item_dict.part_qty,
                'default_unit_of_measure': frappe.db.get_value("Item", item_dict.item_code, "stock_uom"),
                'brand':  item_dict.part_country,
                'validity': item_dict.part_status_ratio if item_dict.part_status_ratio else "-",
                'ezn_no': item_dict.ezn_no if item_dict.ezn_no else item_dict.doc_no if item_dict.doc_no else "-",
                "namozg": namozg_type if namozg_type else "-",
                'date2': frappe.db.get_value("Vehicle Maintenance Process", item_dict.ord_serial, "ezn_date") if frappe.db.get_value("Vehicle Maintenance Process", item_dict.ord_serial, "ezn_date") else item_dict.action_date,
                'maintenance_entity': item_dict.geha_code if item_dict.geha_code else "-",
                'werash': item_dict.workshop_type,
                'werash_name': item_dict.workshop_name,
            }
            result.append(data)
    if not result:
        # frappe.throw("لا يوجد صرفيات سابقة لهذه المركبة")

        result= [{
            "name":"لا يوجد صرفيات سابقة لهذه المركبة",
            'item_code': "لا يوجد صرفيات سابقة لهذه المركبة",
            'item_name': "لا يوجد صرفيات سابقة لهذه المركبة",
            'date': "لا يوجد صرفيات سابقة لهذه المركبة"
        }]
        veh_name = frappe.get_doc("Vehicles", str(filters.get("vic_serial")))
        result[0]["cur_user"] = frappe.db.get_value("User", frappe.session.user, ["full_name"])
        result[0]["vehicle_brand"] = veh_name.vehicle_brand or "-"
        result[0]["vehicle_style"] = veh_name.vehicle_style or "-"
        result[0]["vehicle_shape"] = veh_name.vehicle_shape or "-"
        result[0]["group_shape"] = veh_name.group_shape or "-"
        result[0]["vehicle_model"] = veh_name.vehicle_model or "-"
        result[0]["litre_capacity"] = veh_name.litre_capacity or "-"
        result[0]["possession_type"] = veh_name.possession_type or "-"
        result[0]["exchange_allowance"] = veh_name.exchange_allowance or "-"
        result[0]["fuel_type"] = veh_name.fuel_type or "-"
        result[0]["entity_name"] = veh_name.entity_name or "-"
        result[0]["private_no"] = veh_name.private_no or "-"
        result[0]["vehicle_no"] = veh_name.vehicle_no or "-"
        result[0]["vehicle_model"] = veh_name.vehicle_model or "-"
        result[0]["possession_date"] = veh_name.possession_date or "-"
        result[0]["chassis_no"] = veh_name.chassis_no or "-"
        result[0]["motor_no"] = veh_name.motor_no or "-"
        result[0]["processing_type"] = veh_name.processing_type or "-"
        result[0]["vehicle_type"] = veh_name.vehicle_type or "-"

    else:
        veh_name = frappe.get_doc("Vehicles", str(filters.get("vic_serial")))
        result[0]["cur_user"] = frappe.db.get_value("User", frappe.session.user, ["full_name"])
        result[0]["vehicle_brand"] = veh_name.vehicle_brand or "-"
        result[0]["vehicle_style"] = veh_name.vehicle_style or "-"
        result[0]["vehicle_shape"] = veh_name.vehicle_shape or "-"
        result[0]["group_shape"] = veh_name.group_shape or "-"
        result[0]["vehicle_model"] = veh_name.vehicle_model or "-"
        result[0]["litre_capacity"] = veh_name.litre_capacity or "-"
        result[0]["possession_type"] = veh_name.possession_type or "-"
        result[0]["exchange_allowance"] = veh_name.exchange_allowance or "-"
        result[0]["fuel_type"] = veh_name.fuel_type or "-"
        result[0]["entity_name"] = veh_name.entity_name or "-"
        result[0]["private_no"] = veh_name.private_no or "-"
        result[0]["vehicle_no"] = veh_name.vehicle_no or "-"
        result[0]["vehicle_model"] = veh_name.vehicle_model or "-"
        result[0]["possession_date"] = veh_name.possession_date or "-"
        result[0]["chassis_no"] = veh_name.chassis_no or "-"
        result[0]["motor_no"] = veh_name.motor_no or "-"
        result[0]["processing_type"] = veh_name.processing_type or "-"
        result[0]["vehicle_type"] = veh_name.vehicle_type or "-"
   


    return result