# Copyright (c) 2022, ERP CLOUD SYSTEMS and contributors
# For license information, please see license.txt

import frappe
from datetime import datetime
from frappe.model.document import Document


class Boats(Document):
    def before_insert(self):
        if len(self.engine_table) > 2:
            frappe.throw(" لا يمكن إضافة أكثر من محركين للانش " + self.boat_no)

    def after_insert(self):
        self.engine_count = len(self.engine_table)

        entity = self.append("entity_table", {})
        entity.date = datetime.now()
        entity.value = self.entity_name
        entity.remarks = "الجهة الأساسية للبدن التي تم إدخالها مع إنشاء اللنش"
        entity.edited_by = frappe.db.get_value("User", self.owner, "full_name")
        self.save()

        validity = self.append("validity_table", {})
        validity.date = datetime.now()
        validity.value = self.boat_validity
        validity.remarks = "الصلاحية الأساسية للبدن التي تم إدخالها مع إنشاء اللنش"
        validity.edited_by = frappe.db.get_value("User", self.owner, "full_name")
        self.save()
        """
        for x in self.engine_table:
            engine = self.append("engines_table", {})
            engine.date = datetime.now()
            engine.value = x.engine_no
            engine.remarks = "رقم المحرك الأساسي الذي تم إدخاله مع إنشاء اللنش"
            engine.edited_by = frappe.db.get_value("User", self.owner, "full_name")
            engine.doctype_name = "Boats"
            engine.edit_vehicle = self.name
            engine.save()

            history = [
                {
                    "doctype": "Editing Table",
                    "date": datetime.now(),
                    "value": self.name,
                    "edited_by": frappe.db.get_value("User", self.owner, "full_name"),
                    "doctype_name": "Boats",
                    "edit_vehicle": self.name,
                    "remarks": "رقم اللانش الأساسي الذي تم إضافته مع إنشاء المحرك"
                }
            ]

            new_doc = frappe.get_doc({
                "doctype": "Boat Motor",
                "engine_no": x.engine_no,
                "engine_brand": x.engine_brand,
                "engine_style": x.engine_style,
                "engine_power": x.engine_power,
                "cylinder_count": x.cylinder_count,
                "feeding_type": x.feeding_type,
                "fuel_type": x.fuel_type,
                "entity": x.entity,
                "transfer_history": history,
                "boat_no": self.name
            })
            new_doc.insert(ignore_permissions=True)
        """
    def validate(self):
        if len(self.engine_table) > 2:
            frappe.throw(" لا يمكن إضافة أكثر من محركين للانش " + self.boat_no)

        self.engine_count = len(self.engine_table)

        if self.is_new():
            pass

        else:
            for y in self.engine_table:
                #if frappe.db.exists("Boat Motor", {"name": y.engine_no, "boat_no": self.name}):
                #    pass

                if frappe.db.exists("Boat Motor", {"name": y.engine_no, "boat_no": self.name}):
                    pass
                elif frappe.db.exists("Boat Motor", {"name": y.engine_no}):
                    pass

                else:
                    engine = self.append("engines_table", {})
                    engine.date = datetime.now()
                    engine.value = y.engine_no
                    engine.remarks = "رقم المحرك الأساسي الذي تم إدخاله مع إنشاء اللنش"
                    engine.edited_by = frappe.db.get_value("User", self.owner, "full_name")
                    engine.save()

                    history = [
                        {
                            "doctype": "Editing Table",
                            "date": datetime.now(),
                            "value": self.name,
                            "edited_by": frappe.db.get_value("User", self.owner, "full_name"),
                            "remarks": "رقم اللانش الأساسي الذي تم إضافته مع إنشاء المحرك"
                        }
                    ]

                    new_doc = frappe.get_doc({
                        "doctype": "Boat Motor",
                        "engine_no": y.engine_no,
                        "engine_brand": y.engine_brand,
                        "engine_style": y.engine_style,
                        "engine_power": y.engine_power,
                        "cylinder_count": y.cylinder_count,
                        "feeding_type": y.feeding_type,
                        "fuel_type": y.fuel_type,
                        "entity": y.entity,
                        "transfer_history": history,
                        "boat_no": self.name
                    })
                    new_doc.insert(ignore_permissions=True)

        '''
        boat_engines = frappe.db.get_list('Boat Motor', fields='name')
        for y in self.engine_table:
            for x in boat_engines:
                if x.name == y.engine_no:
                    frappe.msgprint("EXISTS")
                else:
                    engine = self.append("engines_table", {})
                    engine.date = datetime.now()
                    engine.value = y.engine_no
                    engine.remarks = "رقم المحرك الأساسي الذي تم إدخاله مع إنشاء اللنش"
                    engine.edited_by = frappe.db.get_value("User", self.owner, "full_name")
                    engine.doctype_name = "Boats"
                    engine.edit_vehicle = self.name
                    engine.save()

                    history = [
                        {
                            "doctype": "Editing Table",
                            "date": datetime.now(),
                            "value": self.name,
                            "edited_by": frappe.db.get_value("User", self.owner, "full_name"),
                            "doctype_name": "Boats",
                            "edit_vehicle": self.name,
                            "remarks": "رقم اللانش الأساسي الذي تم إضافته مع إنشاء المحرك"
                        }
                    ]

                    new_doc = frappe.get_doc({
                        "doctype": "Boat Motor",
                        "engine_no": y.engine_no,
                        "engine_brand": y.engine_brand,
                        "engine_style": y.engine_style,
                        "engine_power": y.engine_power,
                        "cylinder_count": y.cylinder_count,
                        "feeding_type": y.feeding_type,
                        "fuel_type": y.fuel_type,
                        "entity": y.entity,
                        "transfer_history": history,
                        "boat_no": self.name
                    })
                    new_doc.insert(ignore_permissions=True)
        '''
