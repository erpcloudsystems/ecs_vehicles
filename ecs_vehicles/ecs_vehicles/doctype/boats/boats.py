# Copyright (c) 2022, ERP CLOUD SYSTEMS and contributors
# For license information, please see license.txt

import frappe
from datetime import datetime
from frappe.model.document import Document


class Boats(Document):
    @frappe.whitelist()
    def get_lanch_entity(self):
        entity = frappe.db.get_value("Boats", {"boat_no": self.lanch_no}, "entity")
        self.entity_lable = entity

    def remove_engine_from_boat(self):
        if self.engin_transaction == self.engine_no:
            self.engine_no = None
            self.engine_brand = None
            self.engine_power = None
            self.motor_cylinder_count = None
            self.feeding_type = None
            self.motor_fuel_type = None
            self.entity = None
            self.motor_capacity = None
            self.current_validity = None

        elif self.engin_transaction == self.engine_no2:
            self.engine_no2 = None
            self.engine_brand2 = None
            self.engine_power2 = None
            self.motor_cylinder_count2 = None
            self.feeding_type2 = None
            self.motor_fuel_type2 = None
            self.entity2 = None
            self.motor_capacity2 = None
            self.current_validity2 = None
        to_remove = []
        for motor in self.engine_table:
            if motor.engine_no == self.engin_transaction:
                to_remove.append(motor)
        [self.remove(d) for d in to_remove]
        self.engin_transaction = None
        self.lanch_no = None
        self.entity_lable = None
        self.spare_warehouse = 0
        self.save(ignore_permissions=True)

    @frappe.whitelist()
    def motor_add(self):
        if not frappe.db.exists("Boat Motor", self.motor_no):
            frappe.throw("المحرك غير موجود")
        if self.motor_no in [self.engine_no, self.engine_no2]:
            frappe.throw("المحرك موجود بالفعل في اللانش")
        if self.engine_no and self.engine_no2:
            frappe.throw("لا يمكن إضافة محرك ثالث")
        boat_motor = frappe.get_doc("Boat Motor", self.motor_no)
        if boat_motor.boat_no:
            frappe.throw("المحرك موجود بالفعل في لنش آخر" + " " + boat_motor.boat_no)
        engine = self.append("engine_table", {})
        engine.engine_no = boat_motor.name
        engine.engine_brand = boat_motor.engine_brand
        engine.engine_power = boat_motor.engine_power
        engine.cylinder_count = boat_motor.cylinder_count
        engine.feeding_type = boat_motor.feeding_type
        engine.fuel_type = boat_motor.fuel_type
        engine.entity = self.entity_name
        engine.motor_capacity = self.motor_capacity
        engine.current_validity = self.current_validity
        if self.engine_no:
            self.engine_no2 = boat_motor.name
            self.engine_brand2 = boat_motor.engine_brand
            self.engine_power2 = boat_motor.engine_power
            self.motor_cylinder_count2 = boat_motor.cylinder_count
            self.feeding_type2 = boat_motor.feeding_type
            self.motor_fuel_type2 = boat_motor.fuel_type
            self.entity2 = self.entity_name
            self.motor_capacity2 = self.motor_capacity
            self.current_validity2 = self.current_validity

        else:
            self.engine_no = boat_motor.name
            self.engine_brand = boat_motor.engine_brand
            self.engine_power = boat_motor.engine_power
            self.motor_cylinder_count = boat_motor.cylinder_count
            self.feeding_type = boat_motor.feeding_type
            self.motor_fuel_type = boat_motor.fuel_type
            self.entity = self.entity_name
            self.motor_capacity = self.motor_capacity
            self.current_validity = self.current_validity
        if boat_motor.motor_validity == "احتياطي مخزن":
            boat_motor.motor_validity = "صالح"
            history = {
                "date": datetime.now(),
                "value": self.name,
                "edited_by": frappe.db.get_value("User", self.owner, "full_name"),
                "remarks": "احتياطي مخزن من جهة"
                + " "
                + boat_motor.entity
                + " "
                + "إلى"
                + " "
                + self.entity_name,
            }
        else:
            history = {
                "date": datetime.now(),
                "value": self.name,
                "edited_by": frappe.db.get_value("User", self.owner, "full_name"),
                "remarks": self.entity_name,
            }

        boat_motor.append("transfer_history", history)
        boat_motor.boat_no = self.name
        boat_motor.entity = self.entity_name
        boat_motor.save(ignore_permissions=True)
        self.motor_no = None
        self.save(ignore_permissions=True)
        frappe.msgprint("تمت الإضافة بنجاح")

    @frappe.whitelist()
    def motor_transport(self):
        if self.engin_transaction not in [self.engine_no, self.engine_no2]:
            frappe.throw("المحرك المدخل غير موجود في اللانش")
        if self.spare_warehouse:
            motor_doc = frappe.get_doc("Boat Motor", self.engin_transaction)
            motor_doc.motor_validity = "احتياطي مخزن"
            motor_doc.boat_no = None
            history = {
                "date": datetime.now(),
                "value": "احتياطي مخزن على جهة" + " " + self.entity,
                "edited_by": frappe.db.get_value("User", self.owner, "full_name"),
                "remarks": "احتياطي مخزن على جهة" + " " + self.entity,
            }

            motor_doc.append("transfer_history", history)
            motor_doc.save(ignore_permissions=True)
            self.remove_engine_from_boat()

            frappe.msgprint("تم نقل المحرك إلى احتياطي مخزن")
        else:
            motor_doc = frappe.get_doc("Boat Motor", self.engin_transaction)
            for row in self.engine_table:
                if row.engine_no == self.engin_transaction:
                    new_boat_name = frappe.get_doc("Boats", {"boat_no": self.lanch_no})
                    if len(new_boat_name.engine_table) > 1:
                        frappe.throw(
                            "لا يمكن إضافة أكثر من محركين للانش "
                            + new_boat_name.boat_no
                        )
                    motor_doc.entity = row.entity
                    motor_doc.boat_no = new_boat_name.name
                    history = {
                        "date": datetime.now(),
                        "value": new_boat_name.name,
                        "edited_by": frappe.db.get_value(
                            "User", self.owner, "full_name"
                        ),
                        "remarks": "رقم اللانش الأساسي الذي تم إضافته مع إنشاء المحرك",
                    }

                    motor_doc.append("transfer_history", history)
                    motor_doc.save(ignore_permissions=True)

                    new_boat = new_boat_name.append("engine_table", {})
                    new_boat.engine_no = row.engine_no
                    new_boat.engine_brand = row.engine_brand
                    new_boat.engine_power = row.engine_power
                    new_boat.cylinder_count = row.cylinder_count
                    new_boat.feeding_type = row.feeding_type
                    new_boat.fuel_type = row.fuel_type
                    new_boat.entity = row.entity
                    new_boat.motor_capacity = row.motor_capacity
                    new_boat.current_validity = row.current_validity
                    if new_boat_name.engine_no:
                        new_boat_name.engine_no2 = row.engine_no
                        new_boat_name.engine_brand2 = row.engine_brand
                        new_boat_name.engine_power2 = row.engine_power
                        new_boat_name.motor_cylinder_count2 = row.cylinder_count
                        new_boat_name.feeding_type2 = row.feeding_type
                        new_boat_name.motor_fuel_type2 = row.fuel_type
                        new_boat_name.entity2 = row.entity
                        new_boat_name.motor_capacity2 = row.motor_capacity
                        new_boat_name.current_validity2 = row.current_validity
                    else:
                        new_boat_name.engine_no = row.engine_no
                        new_boat_name.engine_brand = row.engine_brand
                        new_boat_name.engine_power = row.engine_power
                        new_boat_name.motor_cylinder_count = row.motor_cylinder_count
                        new_boat_name.feeding_type = row.feeding_type
                        new_boat_name.motor_fuel_type = row.motor_fuel_type
                        new_boat_name.entity = row.entity
                        new_boat_name.motor_capacity = row.motor_capacity
                        new_boat_name.current_validity = row.current_validity
                    new_boat_name.save(ignore_permissions=True)
            self.remove_engine_from_boat()
            frappe.msgprint("تم نقل المحرك إلى اللانش الجديد")

    def before_insert(self):
        if len(self.engine_table) > 2:
            frappe.throw(" لا يمكن إضافة أكثر من محركين للانش " + self.boat_no)

    def after_insert(self):
        # self.engine_count = len(self.engine_table)
        if self.engine_no:
            engine = self.append("engine_table", {})
            engine.engine_no = self.engine_no
            engine.engine_brand = self.engine_brand
            engine.engine_power = self.engine_power
            engine.cylinder_count = self.motor_cylinder_count
            engine.feeding_type = self.feeding_type
            engine.fuel_type = self.motor_fuel_type
            engine.entity = self.entity
            engine.motor_capacity = self.motor_capacity
            engine.current_validity = self.current_validity
        if self.engine_no2:
            engine = self.append("engine_table", {})
            engine.engine_no = self.engine_no2
            engine.engine_brand = self.engine_brand2
            engine.engine_power = self.engine_power2
            engine.cylinder_count = self.motor_cylinder_count2
            engine.feeding_type = self.feeding_type2
            engine.fuel_type = self.motor_fuel_type2
            engine.entity = self.entity2
            engine.motor_capacity = self.motor_capacity2
            engine.current_validity = self.current_validity2

        entity = self.append("entity_table", {})
        entity.date = datetime.now()
        entity.value = self.entity_name
        entity.remarks = "الجهة الأساسية للبدن التي تم إدخالها مع إنشاء اللانش"
        entity.edited_by = frappe.db.get_value("User", self.owner, "full_name")
        self.save(ignore_permissions=True)

        validity = self.append("validity_table", {})
        validity.date = datetime.now()
        validity.value = self.boat_validity
        validity.remarks = "الصلاحية الأساسية للبدن التي تم إدخالها مع إنشاء اللانش"
        validity.edited_by = frappe.db.get_value("User", self.owner, "full_name")
        self.save(ignore_permissions=True)
        """
        for x in self.engine_table:
            engine = self.append("engines_table", {})
            engine.date = datetime.now()
            engine.value = x.engine_no
            engine.remarks = "رقم المحرك الأساسي الذي تم إدخاله مع إنشاء اللانش"
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
        elif not self.engine_no and not self.engine_no2:
            self.boat_validity = "عاطلة"
        status = frappe.db.sql("""
                    SELECT current_validity
                    FROM `tabBoats`
                    WHERE name = '{name}'
                """.format(name=self.name), as_dict=1)
        if status:
            if status[0].current_validity != self.current_validity:
                doc = frappe.get_doc("Boat Motor", self.engine_no)
                doc.motor_validity = self.current_validity
                doc.append('status_history', {
                    "value": self.current_validity,
                    "date": datetime.now(),
                    "remarks": "الصلاحية من {0} إلا {1} ".format(status[0].current_validity, self.current_validity),
                })
                doc.save()
        status = frappe.db.sql("""
                    SELECT current_validity2
                    FROM `tabBoats`
                    WHERE name = '{name}'
                """.format(name=self.name), as_dict=1)
        if status:
            if status[0].current_validity2 != self.current_validity:
                doc = frappe.get_doc("Boat Motor", self.engine_no)
                doc.motor_validity = self.current_validity
                doc.append('status_history', {
                    "value": self.current_validity,
                    "date": datetime.now(),
                    "remarks": "الصلاحية من {0} إلا {1} ".format(status[0].current_validity2, self.current_validity),
                })
                doc.save()
        for row in self.engine_table:
            if frappe.db.exists("Boat Motor", row.engine_no):
                boat_motor = frappe.get_doc("Boat Motor", row.engine_no)
                # frappe.msgprint(str(boat_motor.boat_no) + " " + str(self.name))
                if boat_motor.entity or boat_motor.boat_no:
                    if boat_motor.boat_no != self.name:
                        frappe.throw(
                            f"الموتور رقم {boat_motor.name} موجود على لانش رقم {boat_motor.boat_no} على جهة {boat_motor.entity}"
                        )

        for row in self.engine_table:
            self.fuel_type = row.fuel_type
            self.cylinder_count = row.cylinder_count

        if self.is_new():
            pass

        else:
            for y in self.engine_table:
                # if frappe.db.exists("Boat Motor", {"name": y.engine_no, "boat_no": self.name}):
                #    pass

                if frappe.db.exists(
                    "Boat Motor", {"name": y.engine_no, "boat_no": self.name}
                ):
                    pass
                elif frappe.db.exists("Boat Motor", {"name": y.engine_no}):
                    pass

                else:
                    engine = self.append("engines_table", {})
                    engine.date = datetime.now()
                    engine.value = y.engine_no
                    engine.remarks = "رقم المحرك الأساسي الذي تم إدخاله مع إنشاء اللانش"
                    engine.edited_by = frappe.db.get_value(
                        "User", self.owner, "full_name"
                    )
                    engine.save(ignore_permissions=True)

                    history = [
                        {
                            "doctype": "Editing Table",
                            "date": datetime.now(),
                            "value": self.name,
                            "edited_by": frappe.db.get_value(
                                "User", self.owner, "full_name"
                            ),
                            "remarks": "رقم اللانش الأساسي الذي تم إضافته مع إنشاء المحرك",
                        }
                    ]
                    status_history = [
                                {
                                    "value": y.current_validity,
                                    "date": datetime.now(),
                                    "remarks": "الصلاحية الأساسية للمحرك",
                                }
                            ]
                    new_doc = frappe.get_doc(
                        {
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
                            "boat_no": self.name,
                            "motor_validity": y.current_validity,
                            "status_history": status_history,
                        }
                    )
                    new_doc.insert(ignore_permissions=True)
        self.engine_count = len(self.engine_table)

        """
        boat_engines = frappe.db.get_list('Boat Motor', fields='name')
        for y in self.engine_table:
            for x in boat_engines:
                if x.name == y.engine_no:
                    frappe.msgprint("EXISTS")
                else:
                    engine = self.append("engines_table", {})
                    engine.date = datetime.now()
                    engine.value = y.engine_no
                    engine.remarks = "رقم المحرك الأساسي الذي تم إدخاله مع إنشاء اللانش"
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
        """
