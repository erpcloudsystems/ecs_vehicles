# Copyright (c) 2023, erpcloud.systems and contributors
# For license information, please see license.txt
import frappe

def execute(filters=None):
    columns, data = [], []
    columns = get_columns()
    data = get_data(filters, columns)
    return columns, data, 


def get_columns():
    return [
        {
            "label": ("الكود"),
            "fieldname": "item_code",
            "fieldtype": "Link",
            "options": "Item",
            "width": 110
        },
        {
            "label": ("اسم الصنف"),
            "fieldname": "item_name",
            "fieldtype": "Data",
            "width": 320,
        },
        {
            "label": ("الماركة"),
            "fieldname": "vehicle_brand",
            "fieldtype": "Link",
            "options": "Stock Brand",
            "width": 220

        },
        {
            "label": ("الموديل"),
            "fieldname": "vehicle_model",
            "fieldtype": "Data",
            "width": 200

        },
        {
            "label": ("المخزن"),
            "fieldname": "warehouse",
            "fieldtype": "Link",
            "options": "Warehouse",
            "width": 180

        },
        {
            "label": ("الرصيد"),
            "fieldname": "stock_balance",
            "fieldtype": "Int",
            "width": 110

        },
        {
            "label": ("القيمة"),
            "fieldname": "stock_rate",
            "fieldtype": "Float",
            "width": 120

        },
    ]


def get_data(filters, columns):
    stock_data = get_stock_data(filters)
    return stock_data
def get_stock_valueandrate_from_bin(warehouse=None, item_code=None):
	values = {}
	conditions = ""
	if warehouse:
		conditions += """ and warehouse in (
						select w2.name from `tabWarehouse` w1
						join `tabWarehouse` w2 on
						w1.name = %(warehouse)s
						and w2.lft between w1.lft and w1.rgt
						) """

		values['warehouse'] = warehouse

	if item_code:
		conditions += " and item_code = %(item_code)s"

		values['item_code'] = item_code

	query = "select sum(stock_value), sum(actual_qty), sum(valuation_rate) from `tabBin` where 1 = 1 %s" % conditions

	stock_value = frappe.db.sql(query, values)

	return stock_value

def get_stock_data(filters):
    conditions = ""
    if filters.get("warehouse"):
        conditions += "and item.warehouse = '{warehouse}' ".format(warehouse=filters.get("warehouse"))
    if filters.get("vehicle_brand"):
        conditions += "and item.custom_brand = '{brand}' ".format(brand=filters.get("vehicle_brand"))
    if filters.get("vehicle_model"):
        conditions += "and item.custom_model like '%{0}%' ".format(filters.get("vehicle_model"))
    if filters.get("item_name"):
        conditions += "and item.item_name like '%{0}%' ".format(filters.get("item_name"))

    result = []

    item_results = frappe.db.sql("""
            select 
                item.name,
                item.item_code,
                item.item_name,
                item.custom_brand as vehicle_brand,
                item.custom_model as vehicle_model,
                item.warehouse as warehouse,
                item.stock_uom as stock_uom
                from `tabItem` item 
                JOIN `tabWarehouse` warehouse ON warehouse.name = item.warehouse
                where item.item_category = "مخازن"
                and item.disabled = 0
                and item.warehouse is not null
                and item.is_stock_item = 1
                and warehouse.warehouse_type = "Spare Parts"
                {conditions}
                order by item.item_code asc, item.warehouse desc
        """.format(conditions=conditions), as_dict=1)

    for item_dict in item_results:
        stock_value = get_stock_valueandrate_from_bin(item_dict.warehouse, item_dict.name)[0]
        data = {
            'item_code': item_dict.item_code or "--",
            'item_name': item_dict.item_name or "--",
            'vehicle_brand': item_dict.vehicle_brand or "--",
            'vehicle_model': item_dict.vehicle_model or "--",
            'warehouse': item_dict.warehouse or "--",
            'stock_uom': item_dict.stock_uom or "--",
            'stock_balance':stock_value[1] if  isinstance(stock_value[1], float)  else 0 ,
            'stock_rate': stock_value[0] if  isinstance(stock_value[0], float) else 0,
            'valuation_rate': stock_value[2] if  isinstance(stock_value[2], float) else 0,
            
        }
        result.append(data)
    
    
    try:
         result[0]["cur_user"] = frappe.db.get_value("User", frappe.session.user, ["full_name"])
    except:
         pass
    return result