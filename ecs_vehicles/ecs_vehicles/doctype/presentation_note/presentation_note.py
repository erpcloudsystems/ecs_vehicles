# Copyright (c) 2022, erpcloud.systems and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import date
from frappe.utils import in_words
from frappe.utils import nowdate, add_to_date


@frappe.whitelist()
def add_po_f(request_for_quotations, supplier, name, method=None):
    today = date.today()
    new_doc = frappe.get_doc(
        {
            "doctype": "Purchase Order",
            "posting_date": today,
            "schedule_date": today,
            "supplier": supplier,
            "presentation_note": name,
        }
    )
    items = frappe.db.sql(
        """ select a.item_group,
                                        a.maintenance_type,
                                        a.item_code,
                                        b.name,
                                        a.item_name,
                                        a.description,
                                        a.default_unit_of_measure,
                                        a.brand,
                                        a.qty,
                                        a.rate,
                                        a.amount,
                                        a.vehicles,
                                        a.vehicle_no,
                                        a.vehicle_brand,
                                        a.maintenance_order,
                                        a.entity_name,
                                        a.vehicle_model
                                        
                                from `tabPresentation Note Item` a join `tabPresentation Note` b
                                on a.parent = b.name
                                where b.name = '{request_for_quotations}'
                                and a.parenttype = "{presentation_note}"
                                and a.parentfield = "{parentfield}"
                            """.format(
            request_for_quotations=request_for_quotations,
            presentation_note="Presentation Note",
            parentfield="presentation_note_item",
        ),
        as_dict=1,
    )

    for x in items:
        table = new_doc.append("items", {})
        table.item_group = x.item_group
        table.maintenance_type = x.maintenance_type
        table.item_code = x.item_code
        table.item_name = x.item_name
        table.description = x.description
        table.vehicle_origin = x.brand
        table.uom = x.default_unit_of_measure
        table.stock_uom = frappe.db.get_value(
            "Item", x.item_code, "stock_uom"
        )  # x.default_unit_of_measure
        table.conversion_factor = 1
        table.brand = x.brand
        table.qty = x.qty
        table.rate = x.rate
        table.amount = x.amount
        table.vehicles = x.vehicles
        table.vehicle_no = x.vehicle_no
        table.vehicle_brand = x.vehicle_brand
        table.maintenance_order = x.maintenance_order
        table.entity_name = x.entity_name
        table.vehicle_model = x.vehicle_model

    new_doc.insert(ignore_permissions=True)
    frappe.msgprint("  تم إنشاء امر توريد برقم رقم " + new_doc.name)


class PresentationNote(Document):
    @frappe.whitelist()
    def create_purchase_import_order(doc, method=None):
        items = []
        for row in doc.presentation_note_item:
            items.append(
                {
                    "item_code": row.item_code,
                    "maintenance_method": row.maintenance_method,
                    "description": row.description,
                    "uom": row.default_unit_of_measure,
                    "brand": row.brand,
                    "qty": row.qty,
                    "rate": row.rate,
                    "amount": row.amount,
                    "vehicles": row.vehicles,
                    "vehicle_no": row.vehicle_no,
                    "vehicle_brand": row.vehicle_brand,
                    "entity_name": row.entity_name,
                    "vehicle_model": row.vehicle_model,
                    "disc": row.disc,
                    "vehicle_origin": row.brand,
                    "vehicle_maintenance_process": row.vehicle_maintenance_process,
                    "ezn_no": row.ezn_no,
                }
            )
        purchase_order = frappe.get_doc(
            {
                "doctype": "Purchase Order",
                "presentation_note": doc.name,
                "mozakira_no": doc.mozakira_no,
                "fiscal_year_purchase": doc.fiscal_year,
                "supplier": doc.supplier,
                "schedule_date": nowdate(),
                "in_words2": doc.in_words,
                "items": items,
            }
        )
        purchase_order.insert(ignore_permissions=True)
        # frappe.msgprint(" تم إنشاء إذن إصلاح رقم <a href=/app/maintenance-order/{0}>{1}</a>".format(new_doc.name,new_doc.name))

        frappe.msgprint(
            "تم إنشاء أمر توريد رقم <a href=/app/purchase-order/{0}>{0}</a>".format(
                purchase_order.name
            )
        )

    @frappe.whitelist()
    def get_data(doc, method=None):
        items = frappe.db.sql(
            """ select ezn_egraa_item.item_group,
                                        ezn_egraa_item.maintenance_type,
                                        ezn_egraa_item.maintenance_method,
                                        ezn_egraa_item.item_code,
                                        ezn_egraa_item.item_name,
                                        ezn_egraa_item.description,
                                        ezn_egraa_item.default_unit_of_measure,
                                        ezn_egraa_item.brand,
                                        ezn_egraa_item.qty,
                                        ezn_egraa_item.disc,
                                        vehicle_maintenance_process.name,
                                        vehicle_maintenance_process.vehicles,
                                        vehicle_maintenance_process.vehicle_no,
                                        vehicle_maintenance_process.vehicle_brand,
                                        vehicle_maintenance_process.vehicle_model,
                                        vehicle_maintenance_process.ezn_no,
                                        vehicle_maintenance_process.entity_name,
                                        item.last_purchase_rate
                                        
                                from `tabVehicle Maintenance Process` vehicle_maintenance_process join `tabEzn Egraa Item` ezn_egraa_item
                                on vehicle_maintenance_process.name = ezn_egraa_item.parent
                                JOIN `tabItem` item ON item.name =  ezn_egraa_item.item_code
                                where vehicle_maintenance_process.name = "{name}" 
                                and ezn_egraa_item.maintenance_method = '{maintenance_method}'
                            """.format(
                maintenance_method="حافظة مشتريات", name=doc.request_for_quotations
            ),
            as_dict=1,
        )
        for x in items:
            table = doc.append("presentation_note_item", {})
            table.item_group = x.item_group
            table.maintenance_type = x.maintenance_type
            table.maintenance_method = x.maintenance_method
            table.item_code = x.item_code
            table.item_name = x.item_name
            table.description = x.description
            table.default_unit_of_measure = x.default_unit_of_measure
            table.brand = x.brand
            table.qty = x.qty
            table.disc = x.disc
            table.rate = 0
            table.amount = x.amount
            table.vehicles = x.vehicles
            table.vehicle_no = x.vehicle_no
            table.vehicle_brand = x.vehicle_brand
            table.maintenance_order = x.maintenance_order
            table.entity_name = x.entity_name
            table.vehicle_model = x.vehicle_model
            table.vehicle_maintenance_process = x.name
            table.ezn_no = x.ezn_no
            table.last_purchase_rate = x.last_purchase_rate

    @frappe.whitelist()
    def validate(self):
        mozakira_no_list = frappe.db.sql(
            """ Select mozakira_no, name from `tabPresentation Note`
            where fiscal_year = '{fiscal_year}' and name != '{name}' """.format(
                name=self.name, fiscal_year=self.fiscal_year
            ),
            as_dict=1,
        )

        for x in mozakira_no_list:
            if self.mozakira_no == x.mozakira_no:
                frappe.throw(
                    " لا يمكن تكرار رقم المذكرة "
                    + str(x.mozakira_no)
                    + " أكثر من مرة قي نفس السنة المالية حيث أنه مستخدم في المستند "
                    + x.name
                )

        if self.total:
            if self.edit_in_words == 0:
                self.in_words = in_words(self.total, "جنيها مصريا فقط لا غير")
        # total1 =0
        # total2 =0
        # for row in self.presentation_note_item:
        # 	total = row.rate * row.qty
        # 	row.amount = total
        # 	total2 += row.amount
        # 	self.total = total2

    @frappe.whitelist()
    def on_submit(self):
        if not self.supplier:
            frappe.throw(" برجاء تحديد المورد المقبول ")
        items = []
        for row in self.presentation_note_item:
            items.append(
                {
                    "item_code": row.item_code,
                    "maintenance_method": row.maintenance_method,
                    "description": row.description,
                    "uom": row.default_unit_of_measure,
                    "vehicle_origin": row.brand,
                    "qty": row.qty,
                    "rate": row.rate,
                    "amount": row.amount,
                    "vehicles": row.vehicles,
                    "vehicle_no": row.vehicle_no,
                    "vehicle_brand": row.vehicle_brand,
                    "vehicle_origin": row.brand,
                    "entity_name": row.entity_name,
                    "vehicle_model": row.vehicle_model,
                    "disc": row.disc,
                    "vehicle_maintenance_process": row.vehicle_maintenance_process,
                    "ezn_no": row.ezn_no,
                }
            )
        purchase_order = frappe.get_doc(
            {
                "doctype": "Purchase Order",
                "presentation_note": self.name,
                "mozakira_no": self.mozakira_no,
                "fiscal_year_purchase": self.fiscal_year,
                "supplier": self.supplier,
                "schedule_date": nowdate(),
                "in_words2": self.in_words,
                "items": items,
            }
        )
        purchase_order.insert()
        # frappe.msgprint(" تم إنشاء إذن إصلاح رقم <a href=/app/maintenance-order/{0}>{1}</a>".format(new_doc.name,new_doc.name))

        frappe.msgprint(
            "تم إنشاء أمر توريد رقم <a href=/app/purchase-order/{0}>{0}</a>".format(
                purchase_order.name
            )
        )


@frappe.whitelist()
def add_maintenance_invoice(doc, method=None):
    new_doc = frappe.get_doc(
        {
            "doctype": "Purchase Invoices",
            "year": doc.fiscal_year_purchase,
            "date": nowdate(),
            # "ezn_no": doc.ezn_no,
            # "vehicle_maintenance_process": doc.name,
            # "jop_order" : doc.name,
            # "order_no" : doc.job_order_no,
            "purchase_invoice": doc.name,
            "order_date": doc.transaction_date,
            # "pre_no_type" : doc.fix_type,
            "supplier": doc.supplier,
            # "vehicles" : doc.vehicles,
            "total": doc.grand_total,
            # "vehicle_no" : doc.vehicle_no,
            # "vehicle_brand" : doc.vehicle_brand,
            # "group_shape" : doc.group_shape,
            # "vehicle_model" : doc.vehicle_model,
            # "chassis_no" : doc.chassis_no,
            # "entity_name" : doc.entity_name,
            # "possession_type" : doc.possession_type,
            # "vehicle_shape" : doc.vehicle_shape,
            # "vehicle_style" : doc.vehicle_style,
            # "maintenance_entity" : doc.maintenance_entity,
        }
    )

    for x in doc.items:
        table = new_doc.append("purchase_invoices_table", {})
        table.item_group = x.item_group
        # table.maintenance_type = x.maintenance_type
        # table.dis_cause = x.consumption_type
        table.item_code = x.item_code
        table.item_name = x.item_name
        table.description = x.description
        table.default_unit_of_measure = x.uom
        table.brand = x.brand
        table.part_qty = x.qty
        table.part_price = x.rate
        table.amount = x.amount
        table.dis_rate = x.discount_amount

    new_doc.insert(ignore_permissions=True)
    frappe.msgprint(
        " تم إنشاء فاتورة صيانة <a href=/app/purchase-invoices/{0}>{1}</a>".format(
            new_doc.name, new_doc.name
        )
    )
