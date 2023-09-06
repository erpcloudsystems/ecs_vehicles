# Copyright (c) 2022, erpcloud.systems and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import nowdate
from frappe.model.document import Document

class PurchaseInvoices(Document):
    @frappe.whitelist()
    def set_inv_no(doc, method=None):
        frappe.db.sql(
            """ UPDATE `tabPurchase Invoices` SET inv_no = {inv_no}
                      WHERE name = '{name}' """.format(
                inv_no=doc.inv_no, name=doc.name
            )
        )

    @frappe.whitelist()
    def get_job_order_stat(doc, method=None):
        purchase_invoices = frappe.db.sql(""" select 
                                    name, inv_no
                                   from `tabPurchase Invoices` purchase_invoices
                                    WHERE order_no = "{job_order_no}"
                                    AND year= "{fiscal_year}"
                                     AND vehicles="{vehicles}"
                                     AND name != "{name}"
                               """.format(job_order_no=doc.order_no, fiscal_year=doc.year,vehicles=doc.vehicles, name=doc.name), as_dict=1)
        if purchase_invoices:
            doc.purchase_invoices_status = "معـــــــــــــــــــــــــاد"
            if purchase_invoices[0]["inv_no"]:
                doc.fatora_no = purchase_invoices[0]["inv_no"]
        
    @frappe.whitelist()
    def validate(doc, method=None):
        pass



    def on_submit(doc):
        for x in doc.purchase_invoices_table:
            if x.maintenance_type != "مصنعيات":
                new_doc = frappe.get_doc({
                    "doctype": "Karta Ledger Entry",
                    "ord_serial" : x.parent,
                    "detail_serial" : x.name,
                    "vic_serial" : doc.vehicles,
                    "part_universal_code" : x.item_code,
                    "action_date" : nowdate(),
                    "part_unit" : x.default_unit_of_measure,
                    "part_country" : x.brand,
                    "workshop_type" : "ورش خارجية",
                    "workshop_name" : doc.supplier,
                    "ezn_no" : doc.ezn_no,
                    "ezn_date" : doc.date,
                    "doc_type" : "Purchase Invoices",
                    "geha_code" : doc.entity_name,
                    "year" : doc.year,
                    "trans_type" : x.maintenance_type,
                    "maintenance_method" : "إصلاح خارجي",
                    "part_qty" : x.part_qty,
                    "del_flag": 0
                })
                new_doc.insert(ignore_permissions=True)

        doc.reload()


    def on_cancel(self):
        for x in self.purchase_invoices_table:
            frappe.db.sql(
                    """ update `tabKarta Ledger Entry` set del_flag = "1"
                        where name ='{name}'
                    """.format(name=x.kle)
                )

