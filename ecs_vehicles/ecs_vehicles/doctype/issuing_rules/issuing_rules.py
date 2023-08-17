# Copyright (c) 2022, ERP CLOUD SYSTEMS and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class IssuingRules(Document):
    def get_vehicle_type(self, words):
        for item in words:
            if "vehicle_type" in item:
                frappe.msgprint(str(item.split("=")[1]))
                vehicle_type = frappe.db.get_value(
                    "Vehicle Type", {"code": item.split("=")[1]}, "name"
                )
                return " and vehicle_type='{0}'".format(vehicle_type)
        return " "

    def get_vehicle_shape(self, words):
        for item in words:
            if "vehicle_shape" in item:
                vehicle_shape = frappe.db.get_value(
                    "Vehicle Shape", {"code": item.split("=")[1]}, "name"
                )
                return " and vehicle_shape='{0}'".format(vehicle_shape)
        return " "

    def get_vehicle_brand(self, words):
        for item in words:
            if "vehicle_brand" in item:
                vehicle_brand = frappe.db.get_value(
                    "Vehicle Brand", {"brand_code": item.split("=")[1]}, "name"
                )
                return " and vehicle_brand='{0}'".format(vehicle_brand)
        return " "

    def get_vehicle_style(self, words):
        for item in words:
            if "vehicle_style" in item:
                vehicle_style = frappe.db.get_value(
                    "Vehicle Style", {"code": item.split("=")[1]}, "name"
                )
                return " and vehicle_style='{0}'".format(vehicle_style)
        return " "

    def get_vehicle_model(self, words):
        for item in words:
            if "vehicle_model" in item:
                vehicle_model = frappe.db.get_value(
                    "Vehicle Model", {"code": item.split("=")[1]}, "name"
                )
                return " and vehicle_model='{0}'".format(vehicle_model)
        return " "

    def get_processing_type(self, words):
        for item in words:
            if "processing_type" in item:
                processing_type = frappe.db.get_value(
                    "Vehicle Processing Type", {"code": item.split("=")[1]}, "name"
                )
                return " and processing_type='{0}'".format(processing_type)
        return " "

    def get_cylinder_count(self, words):
        for item in words:
            if "cylinder_count" in item:
                return " and cylinder_count='{0}'".format(item.split("=")[1])
        return " "

    def get_fuel_type(self, words):
        for item in words:
            if "fuel_type" in item:
                fuel_types = []
                if "in" in item:
                    text = item.split("in")[1]
                    replaced_txt = text.replace("(", "").replace(")", "")
                    frappe.msgprint(str(replaced_txt))
                    if "," in replaced_txt:
                        for char in replaced_txt.split(","):
                            fuel_type = frappe.db.get_value(
                                "Fuel Type", {"code": char}, "name"
                            )
                            fuel_types.append(fuel_type)
                    else:
                        fuel_type = frappe.db.get_value(
                            "Fuel Type", {"code": replaced_txt}, "name"
                        )
                        fuel_types.append(fuel_type)
                else:
                    fuel_type = frappe.db.get_value(
                        "Fuel Type", {"code": item.split("=")[1]}, "name"
                    )
                    fuel_types.append(fuel_type)
                if len(fuel_types) == 1:
                    fuel_types.append("Nonessss")
                return " and fuel_type in {0}".format(tuple(fuel_types))
        return " "

    def get_litre_capacity(self, words):
        conditions = " "
        for item in words:
            if "litre_capacity " in item:
                conditions += " and {0}".format(item)
        return conditions

    def get_engine_strokes_count(self, words):
        for item in words:
            if "engine_strokes_count" in item:
                return " and engine_strokes_count={0}".format(item.split("=")[1])
        return " "

    def validate(self):
        if not self.old_flag:
            rule_text = ""
            vehicle_type = ""
            if self.all_types == 0:
                vehicle_type = self.vehicle_type
            if self.all_types == 1:
                vehicle_type = "كل الأنواع"
            vehicle_shape = ""
            if self.all_shapes == 0:
                vehicle_shape = self.vehicle_shape
            if self.all_shapes == 1:
                vehicle_shape = "كل الأشكال"
            vehicle_brand = ""
            if self.all_brands == 0:
                vehicle_brand = self.vehicle_brand
            if self.all_brands == 1:
                vehicle_brand = "كل الماركات"
            vehicle_style = ""
            if self.all_styles == 0:
                vehicle_style = self.vehicle_style
            if self.all_styles == 1:
                vehicle_style = "كل الطرازات"
            vehicle_model = ""
            if self.all_models == 0:
                vehicle_model = self.vehicle_model
            if self.all_models == 1:
                vehicle_model = "كل الموديلات"
            processing_type = ""
            if self.all_processing == 0:
                processing_type = self.processing_type
            if self.all_processing == 1:
                processing_type = "كل التجهيزات"

            if self.issue_type == "وقود":
                rule_text = (
                    "<b>"
                    + " نوع المركبة: "
                    + "</b>"
                    + str(
                        str(vehicle_type)
                        + "<br>"
                        + "<b>"
                        + " شكل: "
                        + "</b>"
                        + str(vehicle_shape)
                        + "<br>"
                        + "<b>"
                        + " ماركة: "
                        + "</b>"
                        + str(vehicle_brand)
                        + "<br>"
                        + "<b>"
                        + " طراز: "
                        + "</b>"
                        + str(vehicle_style)
                        + "<br>"
                        + "<b>"
                        + " موديل: "
                        + "</b>"
                        + str(vehicle_model)
                        + "<br>"
                        + "<b>"
                        + " نوع التجهيز: "
                        + "</b>"
                        + str(processing_type)
                        + "<br>"
                        + "<b>"
                        + " عدد السلندرات: "
                        + "</b>"
                        + str(self.cylinder_count)
                        + "<br>"
                        + "<b>"
                        + " نوع الوقود: "
                        + "</b>"
                        + str(self.fuel_type)
                        + "<br>"
                        + "<b>"
                        + " السعة اللترية: "
                        + "</b>"
                        + " من "
                        + str(self.from_litre_capacity)
                        + " إلى "
                        + str(self.to_litre_capacity)
                        + "<br>"
                        + "<b>"
                        + " (يصرف لها "
                        + str(self.litre_count)
                        + " لتر "
                        + str(self.fuel_type)
                        + ")"
                        + "</b>"
                    )
                )

            if self.issue_type == "زيت":
                rule_text = (
                    "<b>"
                    + " نوع المركبة: "
                    + "</b>"
                    + str(
                        str(vehicle_type)
                        + "<br>"
                        + "<b>"
                        + " شكل: "
                        + "</b>"
                        + str(vehicle_shape)
                        + "<br>"
                        + "<b>"
                        + " ماركة: "
                        + "</b>"
                        + str(vehicle_brand)
                        + "<br>"
                        + "<b>"
                        + " طراز: "
                        + "</b>"
                        + str(vehicle_style)
                        + "<br>"
                        + "<b>"
                        + " موديل: "
                        + "</b>"
                        + str(vehicle_model)
                        + "<br>"
                        + "<b>"
                        + " نوع التجهيز: "
                        + "</b>"
                        + str(processing_type)
                        + "<br>"
                        + "<b>"
                        + " عدد السلندرات: "
                        + "</b>"
                        + str(self.cylinder_count)
                        + "<br>"
                        + "<b>"
                        + " نوع الوقود: "
                        + "</b>"
                        + str(self.fuel_type)
                        + "<br>"
                        + "<b>"
                        + " السعة اللترية: "
                        + "</b>"
                        + " من "
                        + str(self.from_litre_capacity)
                        + " إلى "
                        + str(self.to_litre_capacity)
                        + "<br>"
                        + "<b>"
                        + " (يصرف لها "
                        + str(self.oil_count)
                        + " لتر "
                        + str(self.oil_type)
                        + ")"
                        + "</b>"
                    )
                )

            if self.issue_type == "غاز":
                rule_text = (
                    "<b>"
                    + " نوع المركبة: "
                    + "</b>"
                    + str(
                        str(vehicle_type)
                        + "<br>"
                        + "<b>"
                        + " شكل: "
                        + "</b>"
                        + str(vehicle_shape)
                        + "<br>"
                        + "<b>"
                        + " ماركة: "
                        + "</b>"
                        + str(vehicle_brand)
                        + "<br>"
                        + "<b>"
                        + " طراز: "
                        + "</b>"
                        + str(vehicle_style)
                        + "<br>"
                        + "<b>"
                        + " موديل: "
                        + "</b>"
                        + str(vehicle_model)
                        + "<br>"
                        + "<b>"
                        + " نوع التجهيز: "
                        + "</b>"
                        + str(processing_type)
                        + "<br>"
                        + "<b>"
                        + " عدد السلندرات: "
                        + "</b>"
                        + str(self.cylinder_count)
                        + "<br>"
                        + "<b>"
                        + " نوع الوقود: "
                        + "</b>"
                        + str(self.fuel_type)
                        + "<br>"
                        + "<b>"
                        + " السعة اللترية: "
                        + "</b>"
                        + " من "
                        + str(self.from_litre_capacity)
                        + " إلى "
                        + str(self.to_litre_capacity)
                        + "<br>"
                        + "<b>"
                        + " (يصرف لها "
                        + str(self.gas_count)
                        + " متر مكعب "
                        + str("غاز طبيعي")
                        + ")"
                        + "</b>"
                    )
                )

            if self.issue_type == "غسيل":
                rule_text = (
                    "<b>"
                    + " نوع المركبة: "
                    + "</b>"
                    + str(
                        str(vehicle_type)
                        + "<br>"
                        + "<b>"
                        + " الشكل: "
                        + "</b>"
                        + str(vehicle_shape)
                        + "<br>"
                        + "<b>"
                        + " الماركة: "
                        + "</b>"
                        + str(vehicle_brand)
                        + "<br>"
                        + "<b>"
                        + " الطراز: "
                        + "</b>"
                        + str(vehicle_style)
                        + "<br>"
                        + "<b>"
                        + " الموديل: "
                        + "</b>"
                        + str(vehicle_model)
                        + "<br>"
                        + "<b>"
                        + " نوع التجهيز: "
                        + "</b>"
                        + str(processing_type)
                        + "<br>"
                        + "<b>"
                        + " عدد السلندرات: "
                        + "</b>"
                        + str(self.cylinder_count)
                        + "<br>"
                        + "<b>"
                        + " نوع الوقود: "
                        + "</b>"
                        + str(self.fuel_type)
                        + "<br>"
                        + "<b>"
                        + " السعة اللترية: "
                        + "</b>"
                        + " من "
                        + str(self.from_litre_capacity)
                        + " إلى "
                        + str(self.to_litre_capacity)
                        + "<br>"
                        + "<b>"
                        + " (يصرف لها بون "
                        + str(self.washing_voucher)
                        + ")"
                        + "</b>"
                    )
                )

            self.rule_text = str(rule_text)
        else:
            conditions = ""
            words = self.rule_sql.split(
                " and "
            )  # split the sentence into individual words
            frappe.msgprint(str(words))
            conditions += self.get_vehicle_type(words)
            conditions += self.get_vehicle_shape(words)
            conditions += self.get_vehicle_brand(words)
            conditions += self.get_vehicle_style(words)
            conditions += self.get_vehicle_model(words)
            conditions += self.get_processing_type(words)
            conditions += self.get_cylinder_count(words)
            conditions += self.get_fuel_type(words)
            conditions += self.get_litre_capacity(words)
            conditions += self.get_engine_strokes_count(words)
            frappe.msgprint(str(self.name))
            frappe.msgprint(str(conditions))

            vehicles = frappe.db.sql(
                """
            SELECT name FROM `tabVehicles` WHERE 1=1 
            {0}            
            order by name
            """.format(
                    conditions
                ),
                as_dict=1,
            )
            frappe.msgprint(str(vehicles))
            for name in vehicles:
                if self.lqd_type == "1":
                    frappe.db.sql(
                        """
                        UPDATE `tabVehicles`
                        SET oil_type = '{1}',
                         oil_count={2} 
                        WHERE name = '{0}'
                        """.format(
                            name.name,
                            frappe.db.get_value(
                                "Oil Type", {"code": self.bon_code}, "name"
                            ),
                            int(self.tot_volume),
                        )
                    )
                else:
                    frappe.db.sql(
                        """
                        UPDATE `tabVehicles` 
                        SET fuel_voucher = '{1}',
                         litre_count={2} 
                        WHERE name = '{0}'
                        """.format(
                            name.name,
                            frappe.db.get_value(
                                "Fuel Voucher", {"code": self.bon_code}, "name"
                            ),
                            int(self.tot_volume),
                        )
                    )

    def on_submit(self):
        if not self.old_flag:
            if self.issue_type == "وقود":
                conditions = {}
                if self.all_types == 0:
                    conditions["vehicle_type"] = self.vehicle_type
                if self.all_shapes == 0:
                    conditions["vehicle_shape"] = self.vehicle_shape
                if self.all_brands == 0:
                    conditions["vehicle_brand"] = self.vehicle_brand
                if self.all_styles == 0:
                    conditions["vehicle_style"] = self.vehicle_style
                if self.all_models == 0:
                    conditions["vehicle_model"] = self.vehicle_model
                if self.all_processing == 0:
                    conditions["processing_type"] = self.processing_type
                conditions["cylinder_count"] = self.cylinder_count
                conditions["fuel_type"] = self.fuel_type
                # conditions["issuing_rule"] = ""
                conditions["litre_capacity"] = [">=", self.from_litre_capacity]
                conditions["litre_capacity"] = ["<=", self.to_litre_capacity]

                vehicles = frappe.db.get_all("Vehicles", filters=conditions)

                for v in vehicles:
                    vec = frappe.get_doc("Vehicles", v.name)

                    frappe.db.sql(
                        """ UPDATE `tabVehicles` set issuing_rule = '{issuing_rule}' where name = '{name}'
                                """.format(
                            issuing_rule=self.name, name=vec.name
                        )
                    )
                    frappe.db.sql(
                        """ UPDATE `tabVehicles` set litre_count = '{litre_count}' where name = '{name}'
                                """.format(
                            litre_count=self.litre_count, name=vec.name
                        )
                    )

                    # vec.issuing_rule = self.name
                    # vec.litre_count = self.litre_count
                    # vec.save()

            if self.issue_type == "زيت":
                conditions = {}
                if self.all_types == 0:
                    conditions["vehicle_type"] = self.vehicle_type
                if self.all_shapes == 0:
                    conditions["vehicle_shape"] = self.vehicle_shape
                if self.all_brands == 0:
                    conditions["vehicle_brand"] = self.vehicle_brand
                if self.all_styles == 0:
                    conditions["vehicle_style"] = self.vehicle_style
                if self.all_models == 0:
                    conditions["vehicle_model"] = self.vehicle_model
                if self.all_processing == 0:
                    conditions["processing_type"] = self.processing_type
                conditions["cylinder_count"] = self.cylinder_count
                conditions["fuel_type"] = self.fuel_type
                # conditions["oil_issuing_rule"] = ""
                conditions["litre_capacity"] = [">=", self.from_litre_capacity]
                conditions["litre_capacity"] = ["<=", self.to_litre_capacity]

                vehicles = frappe.db.get_all("Vehicles", filters=conditions)

                for v in vehicles:
                    vec = frappe.get_doc("Vehicles", v.name)

                    frappe.db.sql(
                        """ UPDATE `tabVehicles` set oil_issuing_rule = '{oil_issuing_rule}' where name = '{name}'
                                """.format(
                            oil_issuing_rule=self.name, name=vec.name
                        )
                    )
                    frappe.db.sql(
                        """ UPDATE `tabVehicles` set oil_type = '{oil_type}' where name = '{name}'
                                """.format(
                            oil_type=self.oil_type, name=vec.name
                        )
                    )
                    frappe.db.sql(
                        """ UPDATE `tabVehicles` set oil_count = '{oil_count}' where name = '{name}'
                                """.format(
                            oil_count=self.oil_count, name=vec.name
                        )
                    )

                    # vec.oil_issuing_rule = self.name
                    # vec.oil_type = self.oil_type
                    # vec.oil_count = self.oil_count
                    # vec.save()

            if self.issue_type == "غاز":
                conditions = {}
                if self.all_types == 0:
                    conditions["vehicle_type"] = self.vehicle_type
                if self.all_shapes == 0:
                    conditions["vehicle_shape"] = self.vehicle_shape
                if self.all_brands == 0:
                    conditions["vehicle_brand"] = self.vehicle_brand
                if self.all_styles == 0:
                    conditions["vehicle_style"] = self.vehicle_style
                if self.all_models == 0:
                    conditions["vehicle_model"] = self.vehicle_model
                if self.all_processing == 0:
                    conditions["processing_type"] = self.processing_type
                conditions["cylinder_count"] = self.cylinder_count
                conditions["fuel_type"] = self.fuel_type
                # conditions["gas_issuing_rule"] = ""
                conditions["litre_capacity"] = [">=", self.from_litre_capacity]
                conditions["litre_capacity"] = ["<=", self.to_litre_capacity]

                vehicles = frappe.db.get_all("Vehicles", filters=conditions)

                for v in vehicles:
                    vec = frappe.get_doc("Vehicles", v.name)

                    frappe.db.sql(
                        """ UPDATE `tabVehicles` set gas_issuing_rule = '{gas_issuing_rule}' where name = '{name}'
                                """.format(
                            gas_issuing_rule=self.name, name=vec.name
                        )
                    )
                    frappe.db.sql(
                        """ UPDATE `tabVehicles` set gas_count = '{gas_count}' where name = '{name}'
                                """.format(
                            gas_count=self.gas_count, name=vec.name
                        )
                    )

                    # vec.gas_issuing_rule = self.name
                    # vec.gas_count = self.gas_count
                    # vec.save()

            if self.issue_type == "غسيل":
                conditions = {}
                if self.all_types == 0:
                    conditions["vehicle_type"] = self.vehicle_type
                if self.all_shapes == 0:
                    conditions["vehicle_shape"] = self.vehicle_shape
                if self.all_brands == 0:
                    conditions["vehicle_brand"] = self.vehicle_brand
                if self.all_styles == 0:
                    conditions["vehicle_style"] = self.vehicle_style
                if self.all_models == 0:
                    conditions["vehicle_model"] = self.vehicle_model
                if self.all_processing == 0:
                    conditions["processing_type"] = self.processing_type
                conditions["cylinder_count"] = self.cylinder_count
                conditions["fuel_type"] = self.fuel_type
                # conditions["washing_voucher"] = ""
                conditions["litre_capacity"] = [">=", self.from_litre_capacity]
                conditions["litre_capacity"] = ["<=", self.to_litre_capacity]

                vehicles = frappe.db.get_all("Vehicles", filters=conditions)

                for v in vehicles:
                    vec = frappe.get_doc("Vehicles", v.name)

                    frappe.db.sql(
                        """ UPDATE `tabVehicles` set washing_issuing_rule = '{washing_issuing_rule}' where name = '{name}'
                                """.format(
                            washing_issuing_rule=self.name, name=vec.name
                        )
                    )
                    frappe.db.sql(
                        """ UPDATE `tabVehicles` set washing_voucher = '{washing_voucher}' where name = '{name}'
                                """.format(
                            washing_voucher=self.washing_voucher, name=vec.name
                        )
                    )
                    frappe.db.sql(
                        """ UPDATE `tabVehicles` set washing_count = 1 where name = '{name}'
                                """.format(
                            name=vec.name
                        )
                    )

                    # vec.washing_issuing_rule = self.name
                    # vec.washing_voucher = self.washing_voucher
                    # vec.washing_count = 1
                    # vec.save()

    def on_cancel(self):
        if not self.old_flag:
            if self.issue_type == "وقود":
                conditions = {}
                if self.all_types == 0:
                    conditions["vehicle_type"] = self.vehicle_type
                if self.all_shapes == 0:
                    conditions["vehicle_shape"] = self.vehicle_shape
                if self.all_brands == 0:
                    conditions["vehicle_brand"] = self.vehicle_brand
                if self.all_styles == 0:
                    conditions["vehicle_style"] = self.vehicle_style
                if self.all_models == 0:
                    conditions["vehicle_model"] = self.vehicle_model
                if self.all_processing == 0:
                    conditions["processing_type"] = self.processing_type
                conditions["fuel_type"] = self.fuel_type
                conditions["issuing_rule"] = self.name
                conditions["litre_capacity"] = [">=", self.from_litre_capacity]
                conditions["litre_capacity"] = ["<=", self.to_litre_capacity]

                vehicles = frappe.db.get_all("Vehicles", filters=conditions)

                for v in vehicles:
                    vec = frappe.get_doc("Vehicles", v.name)
                    frappe.db.sql(
                        """ UPDATE `tabVehicles` set issuing_rule = "" where name = '{name}'
                                                """.format(
                            name=vec.name
                        )
                    )
                    frappe.db.sql(
                        """ UPDATE `tabVehicles` set litre_count = 0 where name = '{name}'
                                                """.format(
                            name=vec.name
                        )
                    )

                    # vec.issuing_rule = ""
                    # vec.litre_count = 0
                    # vec.save()

            if self.issue_type == "زيت":
                conditions = {}
                if self.all_types == 0:
                    conditions["vehicle_type"] = self.vehicle_type
                if self.all_shapes == 0:
                    conditions["vehicle_shape"] = self.vehicle_shape
                if self.all_brands == 0:
                    conditions["vehicle_brand"] = self.vehicle_brand
                if self.all_styles == 0:
                    conditions["vehicle_style"] = self.vehicle_style
                if self.all_models == 0:
                    conditions["vehicle_model"] = self.vehicle_model
                if self.all_processing == 0:
                    conditions["processing_type"] = self.processing_type
                conditions["fuel_type"] = self.fuel_type
                conditions["oil_issuing_rule"] = self.name
                conditions["litre_capacity"] = [">=", self.from_litre_capacity]
                conditions["litre_capacity"] = ["<=", self.to_litre_capacity]

                vehicles = frappe.db.get_all("Vehicles", filters=conditions)

                for v in vehicles:
                    vec = frappe.get_doc("Vehicles", v.name)

                    frappe.db.sql(
                        """ UPDATE `tabVehicles` set oil_issuing_rule = "" where name = '{name}'
                                """.format(
                            name=vec.name
                        )
                    )
                    frappe.db.sql(
                        """ UPDATE `tabVehicles` set oil_type = "" where name = '{name}'
                                """.format(
                            name=vec.name
                        )
                    )
                    frappe.db.sql(
                        """ UPDATE `tabVehicles` set oil_count = 0 where name = '{name}'
                                """.format(
                            name=vec.name
                        )
                    )

                    # vec.oil_issuing_rule = ""
                    # vec.oil_type = ""
                    # vec.oil_count = 0
                    # vec.save()

            if self.issue_type == "غاز":
                conditions = {}
                if self.all_types == 0:
                    conditions["vehicle_type"] = self.vehicle_type
                if self.all_shapes == 0:
                    conditions["vehicle_shape"] = self.vehicle_shape
                if self.all_brands == 0:
                    conditions["vehicle_brand"] = self.vehicle_brand
                if self.all_styles == 0:
                    conditions["vehicle_style"] = self.vehicle_style
                if self.all_models == 0:
                    conditions["vehicle_model"] = self.vehicle_model
                if self.all_processing == 0:
                    conditions["processing_type"] = self.processing_type
                conditions["fuel_type"] = self.fuel_type
                conditions["gas_issuing_rule"] = self.name
                conditions["litre_capacity"] = [">=", self.from_litre_capacity]
                conditions["litre_capacity"] = ["<=", self.to_litre_capacity]

                vehicles = frappe.db.get_all("Vehicles", filters=conditions)

                for v in vehicles:
                    vec = frappe.get_doc("Vehicles", v.name)

                    frappe.db.sql(
                        """ UPDATE `tabVehicles` set gas_issuing_rule = "" where name = '{name}'
                                                """.format(
                            name=vec.name
                        )
                    )
                    frappe.db.sql(
                        """ UPDATE `tabVehicles` set gas_count = 0 where name = '{name}'
                                                """.format(
                            name=vec.name
                        )
                    )

                    # vec.gas_issuing_rule = ""
                    # vec.gas_count = 0
                    # vec.save()

            if self.issue_type == "غسيل":
                conditions = {}
                if self.all_types == 0:
                    conditions["vehicle_type"] = self.vehicle_type
                if self.all_shapes == 0:
                    conditions["vehicle_shape"] = self.vehicle_shape
                if self.all_brands == 0:
                    conditions["vehicle_brand"] = self.vehicle_brand
                if self.all_styles == 0:
                    conditions["vehicle_style"] = self.vehicle_style
                if self.all_models == 0:
                    conditions["vehicle_model"] = self.vehicle_model
                if self.all_processing == 0:
                    conditions["processing_type"] = self.processing_type
                conditions["fuel_type"] = self.fuel_type
                conditions["washing_issuing_rule"] = self.name
                conditions["litre_capacity"] = [">=", self.from_litre_capacity]
                conditions["litre_capacity"] = ["<=", self.to_litre_capacity]

                vehicles = frappe.db.get_all("Vehicles", filters=conditions)

                for v in vehicles:
                    vec = frappe.get_doc("Vehicles", v.name)

                    frappe.db.sql(
                        """ UPDATE `tabVehicles` set washing_issuing_rule = "" where name = '{name}'
                                """.format(
                            name=vec.name
                        )
                    )
                    frappe.db.sql(
                        """ UPDATE `tabVehicles` set washing_voucher = "" where name = '{name}'
                                """.format(
                            name=vec.name
                        )
                    )
                    frappe.db.sql(
                        """ UPDATE `tabVehicles` set washing_count = 0 where name = '{name}'
                                """.format(
                            name=vec.name
                        )
                    )

                    # vec.washing_issuing_rule = ""
                    # vec.washing_voucher = ""
                    # vec.washing_count = 0
                    # vec.save()
