# Copyright (c) 2023, erpcloud.systems and contributors
# For license information, please see license.txt

# import frappe


# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt
from __future__ import unicode_literals
import frappe
from frappe import msgprint, _
from frappe.utils import flt


def execute(filters=None):
    columns, data = [], []
    columns = get_columns()
    data = get_data(filters, columns)
    return columns, data


def get_columns():
    return [
        {
            "label": _("إسم الجهة التابعة لها"),
            "fieldname": "entity",
            "fieldtype": "Data",
            "width": 220,
        },
        {
            "label": _("حالة المركبة"),
            "fieldname": "vehicle_status",
            "fieldtype": "Data",
            "width": 100,
        },
        {
            "label": _("إسم البون"),
            "fieldname": "voucher",
            "fieldtype": "Data",
            "width": 200,
        },
        {
            "label": _("الكمية باللتر"),
            "fieldname": "qty",
            "fieldtype": "Int",
            "width": 110,
        },
        {
            "label": _("بداية الفترة"),
            "fieldname": "from_date",
            "fieldtype": "Date",
            "width": 100,
        },
        {
            "label": _("نهاية الفترة"),
            "fieldname": "to_date",
            "fieldtype": "Date",
            "width": 100,
        },
    ]


def get_data(filters, columns):
    item_price_qty_data = []
    item_price_qty_data = get_item_price_qty_data(filters)
    return item_price_qty_data


def get_conditions(filters):
    conditions = ""
    if filters.get("from_date"):
        conditions += " AND `tabLiquids Issuing Table`.from_date >= '{0}'".format(
            filters.get("from_date")
        )
    if filters.get("to_date"):
        conditions += " AND `tabLiquids Issuing Table`.from_date <= '{0}'".format(
            filters.get("to_date")
        )
    return conditions


def get_item_price_qty_data(filters):
    result = []
    conditions = get_conditions(filters)
    if frappe.db.exists("Vehicles", {"vehicle_no": filters.get("name")}):
        if frappe.db.count("Vehicles", {"vehicle_no": filters.get("name")}) > 1 and (
            not filters.get("entity") and not filters.get("vehicle_type")
        ):
            # get vehicles with the filters.get("name")
            vehicles = frappe.get_all(
                "Vehicles",
                filters={"vehicle_no": filters.get("name")},
                fields=["name", "vehicle_type", "entity_name", "vehicle_no"],
            )
            vehicle_types_entity = " <br> "
            for row in vehicles:
                vehicle_types_entity = (
                    vehicle_types_entity
                    + " <br> "
                    + row.vehicle_type
                    + " بجهة "
                    + row.entity_name
                )
            frappe.throw(
                "هناك أكثر من مركبة بنفس رقم الشرطة {vehicle_no}  : <b>{vehicle_types}</b> <br> <br> برجاء تحديد نوع المركبة أو الجهة".format(
                    vehicle_types=vehicle_types_entity, vehicle_no=filters.get("name")
                ),
                title="تحذير",
            )
        vehicle = frappe.get_doc("Vehicles", {"vehicle_no": filters.get("name")})
        if filters.get("entity"):
            conditions += " AND `tabVehicles`.entity_name >= '{0}'".format(
                filters.get("entity")
            )
        if filters.get("vehicle_type"):
            conditions += " AND `tabVehicles`.vehicle_type >= '{0}'".format(
                filters.get("vehicle_type")
            )
        item_results = frappe.db.sql(
            """
            select
                `tabLiquids Issuing Table`.entity,
                `tabLiquids Issuing Table`.vehicle_status,
                `tabLiquids Issuing Table`.voucher,
                `tabLiquids Issuing Table`.qty,
                `tabLiquids Issuing Table`.from_date,
                `tabLiquids Issuing Table`.to_date
            from
                `tabLiquids Issuing Table` 
            join `tabVehicles` on `tabLiquids Issuing Table`.parent = `tabVehicles`.name
            where
                `tabVehicles`.vehicle_no = '{name}'
                and `tabLiquids Issuing Table`.issue_type = '{issue_type}'
                {conditions}
            order by
                `tabLiquids Issuing Table`.from_date
            """.format(
                name=filters.get("name"),
                issue_type=filters.get("issue_type"),
                conditions=conditions,
            ),
            filters,
            as_dict=1,
        )

        total = frappe.db.sql(
            """
            select
                SUM(`tabLiquids Issuing Table`.qty) as sum_qty
            from
                `tabLiquids Issuing Table` join `tabVehicles`
                on `tabLiquids Issuing Table`.parent = `tabVehicles`.name
            where
                `tabVehicles`.vehicle_no = '{name}'
                and `tabLiquids Issuing Table`.issue_type = '{issue_type}'
                {conditions}
            """.format(
                name=filters.get("name"),
                issue_type=filters.get("issue_type"),
                conditions=conditions,
            ),
            filters,
            as_dict=1,
        )

        for item_dict in item_results:
            data = {
                "entity": item_dict.entity,
                "vehicle_status": item_dict.vehicle_status,
                "voucher": item_dict.voucher,
                "qty": item_dict.qty,
                "from_date": item_dict.from_date,
                "to_date": item_dict.to_date,
                "plate_no": filters.get("name"),
                "fuel_type": vehicle.fuel_type,
                "entity_name": vehicle.entity_name,
                "vehicle_type": vehicle.vehicle_type,
                "vehicle_shape": vehicle.vehicle_shape,
                "vehicle_brand": vehicle.vehicle_brand,
                "vehicle_style": vehicle.vehicle_style,
                "vehicle_model": vehicle.vehicle_model,
                "possession_date": vehicle.possession_date,
                "vehicle_code": vehicle.name,
                "total_qty": "",
                "cur_user": frappe.db.get_value(
                    "User", frappe.session.user, "full_name"
                ),
            }
            result.append(data)

    elif frappe.db.exists("Boats", {"boat_no": filters.get("name")}):
        vehicle = frappe.get_doc("Boats", {"boat_no": filters.get("name")})
        if filters.get("entity"):
            conditions += " AND `tabBoats`.entity_name >= '{0}'".format(
                filters.get("entity")
            )
        item_results = frappe.db.sql(
            """
            select
                `tabLiquids Issuing Table`.entity,
                `tabLiquids Issuing Table`.vehicle_status,
                `tabLiquids Issuing Table`.voucher,
                `tabLiquids Issuing Table`.qty,
                `tabLiquids Issuing Table`.from_date,
                `tabLiquids Issuing Table`.to_date
            from
                `tabLiquids Issuing Table` join `tabBoats`
                on `tabLiquids Issuing Table`.parent = `tabBoats`.name
            where
                `tabBoats`.boat_no = '{name}'
                and `tabLiquids Issuing Table`.issue_type = '{issue_type}'
                {conditions}
            order by
                `tabLiquids Issuing Table`.from_date
            """.format(
                name=filters.get("name"),
                issue_type=filters.get("issue_type"),
                conditions=conditions,
            ),
            filters,
            as_dict=1,
        )

        total = frappe.db.sql(
            """
            select
                SUM(`tabLiquids Issuing Table`.qty) as sum_qty
            from
                `tabLiquids Issuing Table` join `tabBoats`
                on `tabLiquids Issuing Table`.parent = `tabBoats`.name
            where
                `tabBoats`.boat_no = '{name}'
                and `tabLiquids Issuing Table`.issue_type = '{issue_type}'
                {conditions}
            """.format(
                name=filters.get("name"),
                issue_type=filters.get("issue_type"),
                conditions=conditions,
            ),
            filters,
            as_dict=1,
        )

        for item_dict in item_results:
            data = {
                "entity": item_dict.entity,
                "vehicle_status": item_dict.vehicle_status,
                "voucher": item_dict.voucher,
                "qty": item_dict.qty,
                "from_date": item_dict.from_date,
                "to_date": item_dict.to_date,
                "plate_no": filters.get("name"),
                "fuel_type": vehicle.fuel_type,
                "entity_name": vehicle.entity_name,
                "vehicle_type": "لانش",
                "vehicle_shape": vehicle.body_type,
                "vehicle_brand": vehicle.boat_brand,
                "vehicle_style": "",
                "vehicle_model": vehicle.boat_model,
                "possession_date": vehicle.issue_date,
                "vehicle_code": vehicle.name,
                "total_qty": "",
                "cur_user": frappe.db.get_value(
                    "User", frappe.session.user, "full_name"
                ),
            }
            result.append(data)

    if result:
        result[0]["total_qty"] = total[0]["sum_qty"]
    return result
