# Copyright (c) 2022, erpcloud.systems and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import nowdate
from frappe.model.document import Document

@frappe.whitelist()
def pass_order_function(vehicles, fis_year, pass_order):
    job_order_list = frappe.db.get_list("Job Order", filters={"vehicles": vehicles, "fiscal_year": fis_year}, fields={"name", "jop_number", "date", "fiscal_year"})
    if job_order_list:
        for y in job_order_list:
            purchase_invoices_list = frappe.db.get_list("Purchase Invoices", filters={"vehicles": vehicles, "jop_order": y.name}, fields={"name"})
            if not purchase_invoices_list and  pass_order == "0" :
                frappe.msgprint(" لا يجوز إضافة إجراء إصلاح خارجي للمركبة وذلك لوجود أمر شغل ساري رقم " + str(y.jop_number) + " بتاريخ " + str(y.date or y.fiscal_year))



class MaintenanceOrder(Document):
    @frappe.whitelist()
    def set_today_date(doc, method=None):
        if not doc.date:
            doc.date = nowdate()


    def after_insert(self):
        if self.custody_report:
            for x in self.maintenance_order_item:
                frappe.db.sql(
                    """ update `tabCustody Report Item` set maintenance_order = '{maintenance_order}'
                        where parent='{parent}' and name='{name}'
                    """.format(maintenance_order=self.name, parent=x.custody_report, name=x.custody_report_item)
                )

        if self.amended_from and self.maintenance_order_item:
            for x in self.maintenance_order_item:
                x.kle = None

    
    def validate(self):		
        for x in self.maintenance_order_item:
            if x.maintenance_method == "إصلاح خارجي":
                job_order_list = frappe.db.get_list("Job Order", filters={"vehicles": self.vehicles, "fiscal_year": self.fis_year}, fields={"name", "jop_number", "date", "fiscal_year"})
                if job_order_list:
                    for y in job_order_list:
                        purchase_invoices_list = frappe.db.get_list("Purchase Invoices", filters={"vehicles": self.vehicles, "jop_order": y.name}, fields={"name"})
                        if not purchase_invoices_list and not self.pass_order:
                            frappe.msgprint(" لا يجوز إضافة إجراء إصلاح خارجي للمركبة وذلك لوجود أمر شغل ساري رقم " + str(y.jop_number) + " بتاريخ " + str(y.date or y.fiscal_year))


            if self.select_all_maintenance_type and x.maintenance_method == "إصلاح خارجي":
                x.maintenance_type = self.select_all_maintenance_type
                self.select_all_maintenance_type = ""
    
    
    def on_submit(self):
        for x in self.maintenance_order_item:
            if x.maintenance_method == "إصلاح خارجي":
                job_order_list = frappe.db.get_list("Job Order", filters={"vehicles": self.vehicles, "fiscal_year": self.fis_year}, fields={"name", "jop_number", "date", "fiscal_year"})
                if job_order_list:
                    for y in job_order_list:
                        purchase_invoices_list = frappe.db.get_list("Purchase Invoices", filters={"vehicles": self.vehicles, "jop_order": y.name}, fields={"name"})
                        if not purchase_invoices_list and not self.pass_order:
                            frappe.throw(" لا يجوز إضافة إجراء إصلاح خارجي للمركبة وذلك لوجود أمر شغل ساري رقم " + str(y.jop_number) + " بتاريخ " + str(y.date or y.fiscal_year))

            if x.maintenance_method == "إصلاح خارجي" and not x.maintenance_type:
                frappe.throw(" برجاء تحديد طبيعة الإصلاح للإصلاح الخارجي ")
            
            if x.maintenance_method == "إذن صرف وإرتجاع" and not x.kle:
                new_doc = frappe.get_doc({
                    "doctype": "Karta Ledger Entry",
                    "ord_serial" : x.parent,
                    "detail_serial" : x.name,
                    "vic_serial" : self.vehicles,
                    "part_universal_code" : x.item_code,
                    "action_date" : nowdate(),
                    "part_unit" : x.default_unit_of_measure,
                    "part_status_ratio" : x.quality,
                    "part_country" : x.brand,
                    "workshop_type" : "ورش داخلية",
                    "workshop_name" : frappe.db.get_value("Item", x.item_code, "warehouse"),
                    "ezn_no" : self.ezn_no,
                    "ezn_date" : self.date,
                    "doc_type" : "Maintenance Order",
                    "geha_code" : self.entity_name,
                    "year" : self.fis_year,
                    "trans_type" : "كارتة عهد",
                    "part_qty" : x.qty,
                    "del_flag": 0
                })
                new_doc.insert(ignore_permissions=True)

        self.reload()

        # trans_type = {
        # 	1:"رصيد إفتتاحي",
        # 	2:"إضافة توريدات",
        # 	3:"إضافة مشتريات ظ إصلاح",
        # 	4:"صرف لمركبة",
        # 	5:"صرف لجهة",
        # 	6:"إرتجاع لمخزن",
        # 	7:"كارتة عهد",
        # 	8:"إصلاح داخلي",
        # 	9:"إصلاح خارجي"
        # }
        
        # maintenance_data = {
        # 	"إذن صرف وإرتجاع":[],
        # 	"حافظة مشتريات":[],
        # 	"إصلاح خارجي":[],
        # 	"إصلاح خارجي على الجهة":[],
        # 	"شهادة إستبدال":[],
        # 	"شهادة إرتجاع":[],
        # 	"إذن صرف":[],
        # 	"إصلاح داخلي":[]
        # 			      }
        # for row in self.maintenance_order_item:
        # 	if row.maintenance_method == "إذن صرف وإرتجاع":
        # 		maintenance_data["إذن صرف وإرتجاع"].append(row)


        # 	if row.maintenance_method == "حافظة مشتريات":
        # 		maintenance_data["حافظة مشتريات"].append(row)


        # 	if row.maintenance_method == "إصلاح خارجي":
        # 		maintenance_data["إصلاح خارجي"].append(row)


        # 	if row.maintenance_method == "إصلاح خارجي على الجهة":
        # 		maintenance_data["إصلاح خارجي على الجهة"].append(row)


        # 	if row.maintenance_method == "شهادة إرتجاع":
        # 		maintenance_data["شهادة إرتجاع"].append(row)

        # 	if row.maintenance_method == "إذن صرف":
        # 		maintenance_data["إذن صرف"].append(row)	

        # 	if row.maintenance_method == "إصلاح داخلي":
        # 		maintenance_data["إصلاح داخلي"].append(row)	


        # if maintenance_data.get("إذن صرف وإرتجاع"):
        # 	items = []
        # 	for row in maintenance_data.get("إذن صرف وإرتجاع"):
        # 		items.append(
        # 			{
        # 						"item_code": row.item_code,
        # 						"item_name":row.item_name,
        # 						"item_group":row.item_group,
        # 						"qty":row.qty,
        # 						"uom": row.default_unit_of_measure,
        # 						"description":row.description,
        # 					}
        # 		)
        # 	doc_receipt = frappe.get_doc({
        # 				'doctype': 'Stock Entry',
        # 				'stock_entry_type': 'Material Receipt',
        # 				"fiscal_year":self.fiscal_year,
        # 				'posting_date': self.date,
        # 				'maintenance_order': self.name,
        # 				'vehicles': self.vehicles,
        # 				'to_warehouse': "المرتجعات والخردة" ,
        # 				"items":items
        # 			})
        # 	doc_receipt.insert(ignore_permissions=True)

        # 	doc_issue = frappe.get_doc({
        # 				'doctype': 'Stock Entry',
        # 				'stock_entry_type': 'Material Issue',
        # 				"fiscal_year":self.fiscal_year,
        # 				'posting_date': self.date,
        # 				'maintenance_order': self.name,
        # 				'vehicles': self.vehicles,
        # 				'from_warehouse': row.store_code if row.store_code else "مخازن - V" ,
        # 				"items":items
        # 			})
        # 	doc_issue.insert(ignore_permissions=True)

    def on_update_after_submit(self):
        for x in self.maintenance_order_item:
            if x.maintenance_method == "إصلاح خارجي" and not x.maintenance_type:
                frappe.throw(" برجاء تحديد طبيعة الإصلاح للإصلاح الخارجي ")

            if x.maintenance_method == "إذن صرف وإرتجاع" and not x.kle:
                new_doc = frappe.get_doc({
                    "doctype": "Karta Ledger Entry",
                    "ord_serial" : x.parent,
                    "detail_serial" : x.name,
                    "vic_serial" : self.vehicles,
                    "part_universal_code" : x.item_code,
                    "action_date" : nowdate(),
                    "part_unit" : x.default_unit_of_measure,
                    "part_status_ratio" : x.quality,
                    "part_country" : x.brand,
                    "workshop_type" : "ورش داخلية",
                    "workshop_name" : frappe.db.get_value("Item", x.item_code, "warehouse"),
                    "ezn_no" : self.ezn_no,
                    "ezn_date" : self.date,
                    "doc_type" : "Maintenance Order",
                    "geha_code" : self.entity_name,
                    "year" : self.fis_year,
                    "trans_type" : "كارتة عهد",
                    "part_qty" : x.qty,
                    "del_flag": "0"
                })
                new_doc.insert(ignore_permissions=True)

        self.reload()


    def on_cancel(self):
        for x in self.maintenance_order_item:
            if x.kle:
                frappe.db.sql(
                        """ update `tabKarta Ledger Entry` set del_flag = 1
                            where name ='{name}'
                        """.format(name=x.kle)
                    )
                frappe.db.sql(
                        """ update `tabMaintenance Order Item` set kle = NULL
                            where name ='{row_name}'
                        """.format(row_name=x.name)
                    )
            if x.custody_report:
                frappe.db.sql(
                    """ update `tabCustody Report Item` set maintenance_order = NULL, include_in_maintenance_order = 0
                        where parent ='{parent}' and name ='{name}'
                    """.format(maintenance_order=self.name, parent=x.custody_report, name=x.custody_report_item)
                )

        

    def on_trash(self):
        for x in self.maintenance_order_item:
            if self.custody_report:
                frappe.db.sql(
                    """ update `tabCustody Report Item` set maintenance_order = NULL, include_in_maintenance_order = 0
                        where parent ='{parent}' and name ='{name}'
                    """.format(maintenance_order=self.name, parent=x.custody_report, name=x.custody_report_item)
                )