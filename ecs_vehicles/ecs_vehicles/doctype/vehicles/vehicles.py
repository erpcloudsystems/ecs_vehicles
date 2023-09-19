import frappe
from datetime import datetime
from frappe.model.document import Document
from frappe.utils import getdate
from time import sleep


class Vehicles(Document):
    @frappe.whitelist()
    def check_police_no(doc, method=None):
        vehicle_list = frappe.db.sql(
            """ Select name, vehicle_no, vehicle_type from `tabVehicles` where docstatus = 0""",
            as_dict=1,
        )

        for x in vehicle_list:
            if doc.vehicle_no == x.vehicle_no and doc.vehicle_no:
                frappe.throw(
                    " لا يمكن إستخدام رقم الشرطة "
                    + x.vehicle_no
                    + " أكثر من مرة حيث أنه مستخدم في المركبة رقم "
                    + x.name
                )

        frappe.throw(" رقم الشرطة " + doc.vehicle_no + " متاح للإستخدام ")

    @frappe.whitelist()
    def check_chassis_no(doc, method=None):
        chassis_list = frappe.db.sql(
            """ Select name, chassis_no from `tabVehicles` where docstatus = 0 and vehicle_status not in ("مخردة", "بيعت بالمزاد") """,
            as_dict=1,
        )

        for x in chassis_list:
            if doc.chassis_no == x.chassis_no and doc.chassis_no:
                frappe.throw(
                    " لا يمكن إستخدام رقم الشاسيه "
                    + x.chassis_no
                    + " أكثر من مرة حيث أنه مستخدم في المركبة رقم "
                    + x.name
                )

        frappe.throw(" رقم الشاسيه " + doc.chassis_no + " متاح للإستخدام ")

    def before_insert(self):
        chassis_list = frappe.db.sql(
            """ Select chassis_no, vehicle_no from `tabVehicles` where docstatus = 0 and vehicle_status not in ("مخردة", "بيعت بالمزاد") """,
            as_dict=1,
        )

        for x in chassis_list:
            if self.chassis_no == x.chassis_no and self.chassis_no:
                frappe.throw(
                    " لا يمكن إستخدام رقم الشاسيه "
                    + x.chassis_no
                    + " أكثر من مرة حيث أنه مستخدم في المركبة رقم "
                    + x.vehicle_no
                )

        vehicle_list = frappe.db.sql(
            """ Select name, vehicle_no, vehicle_type from `tabVehicles` where docstatus = 0""",
            as_dict=1,
        )

        for x in vehicle_list:
            if self.vehicle_no == x.vehicle_no and self.vehicle_type == x.vehicle_type:
                frappe.throw(
                    " لا يمكن إستخدام رقم الشرطة "
                    + x.vehicle_no
                    + " أكثر من مرة حيث أنه مستخدم في المركبة رقم "
                    + x.name
                )

        if frappe.db.exists(
            "Police Plate",
            {
                "plate_no": self.vehicle_no,
                "vehicle_type": self.vehicle_type,
                "status": "معدمة",
            },
        ):
            frappe.throw(
                " لا يمكن إستخدام لوحة الشرطة رقم "
                + self.vehicle_no
                + " حيث أن حالتها معدمة "
            )

    def after_insert(self):
        if self.vehicle_no:
            vehicle = self.append("vehicle_no_table", {})
            vehicle.date = datetime.now()
            vehicle.value = self.vehicle_no
            vehicle.remarks = "رقم الشرطة الأساسي الذي تم إدخاله مع إنشاء المركبة"
            vehicle.edited_by = frappe.db.get_value("User", self.owner, "full_name")
            self.police_id = self.vehicle_no
            self.save()

            if not frappe.db.exists(
                "Police Plate",
                {"plate_no": self.vehicle_no, "vehicle_type": self.vehicle_type},
            ):
                police_plate_no = frappe.get_doc(
                    {
                        "doctype": "Police Plate",
                        "plate_no": self.vehicle_no,
                        "vehicle_type": self.vehicle_type,
                        "current_vehicle": self.name,
                    }
                )
                police_plate_no.insert(ignore_permissions=True)

                plate_no = police_plate_no.append("plate_table", {})
                plate_no.date = datetime.now()
                plate_no.value = self.name
                plate_no.edited_by = frappe.session.user
                plate_no.doctype_name = "Vehicles"
                plate_no.edit_vehicle = self.name
                plate_no.save()
                police_plate_no.save()

            if frappe.db.exists(
                "Police Plate",
                {"plate_no": self.vehicle_no, "vehicle_type": self.vehicle_type},
            ):
                pol_plate = frappe.get_doc(
                    "Police Plate",
                    {"plate_no": self.vehicle_no, "vehicle_type": self.vehicle_type},
                )
                plate_no_ = pol_plate.append("plate_table", {})
                plate_no_.date = datetime.now()
                plate_no_.value = self.name
                plate_no_.edited_by = frappe.session.user
                plate_no_.doctype_name = "Vehicles"
                plate_no_.edit_vehicle = self.name
                plate_no_.save()
                pol_plate.current_vehicle = self.name
                pol_plate.save()

        if self.private_no:
            private = self.append("private_no_table", {})
            private.date = datetime.now()
            private.value = self.private_no
            private.traffic_entity = self.traffic_entity
            private.plate_type = self.plate_type
            private.remarks = "رقم الملاكي الأساسي الذي تم إدخاله مع إنشاء المركبة"
            private.edited_by = frappe.db.get_value("User", self.owner, "full_name")
            self.save()

            private_plate_no = frappe.get_doc("Private Plate", self.private_no)
            private_plate_no.current_vehicle = self.name
            private_plate_no.police_no = self.vehicle_no

            private_no = private_plate_no.append("plate_table", {})
            private_no.date = datetime.now()
            private_no.value = self.name + " - " + self.vehicle_no
            private_no.edited_by = frappe.session.user
            private_no.doctype_name = "Vehicles"
            private_no.edit_vehicle = self.name
            private_no.save()

            private_plate_no.save()

        if self.motor_no:
            motor = self.append("motor_table", {})
            motor.date = datetime.now()
            motor.value = self.motor_no
            motor.remarks = "رقم الموتور الأساسي الذي تم إدخاله مع إنشاء المركبة"
            motor.edited_by = frappe.db.get_value("User", self.owner, "full_name")
            self.save()

            motor_no = frappe.get_doc("Vehicle Motor", self.motor_no)
            motor_no.current_vehicle = self.name

            motor = motor_no.append("motor_table", {})
            motor.date = datetime.now()
            motor.value = self.name
            motor.edited_by = frappe.session.user
            motor.doctype_name = "Vehicles"
            motor.edit_vehicle = self.name
            motor.save()

            motor_no.save()

        if self.entity_name:
            entity = self.append("entity_table", {})
            entity.date = datetime.now()
            entity.value = self.entity_name
            entity.remarks = "الجهة الأساسية التي تم إدخالها مع إنشاء المركبة"
            entity.edited_by = frappe.db.get_value("User", self.owner, "full_name")
            self.save()

        if self.vehicle_color:
            color = self.append("color_table", {})
            color.date = datetime.now()
            color.value = self.vehicle_color
            color.remarks = "اللون الأساسي الذي تم إدخاله مع إنشاء المركبة"
            color.edited_by = frappe.db.get_value("User", self.owner, "full_name")
            self.save()

        if self.processing_type:
            processing_type = self.append("processing_type_table", {})
            processing_type.date = datetime.now()
            processing_type.value = self.processing_type
            processing_type.remarks = (
                "نوع التجهيز الأساسي الذي تم إدخاله مع إنشاء المركبة"
            )
            processing_type.edited_by = frappe.db.get_value(
                "User", self.owner, "full_name"
            )
            self.save()

        if self.chassis_no:
            chassis_no = self.append("chassis_no_table", {})
            chassis_no.date = datetime.now()
            chassis_no.value = self.chassis_no
            chassis_no.remarks = "رقم الشاسيه الأساسي الذي تم إدخاله مع إنشاء المركبة"
            chassis_no.edited_by = frappe.db.get_value("User", self.owner, "full_name")
            self.save()

        if self.group_shape:
            group_shape = self.append("group_shape_table", {})
            group_shape.date = datetime.now()
            group_shape.value = self.group_shape
            group_shape.remarks = (
                "مجموعة الشكل الأساسية التي تم إدخالها مع إنشاء المركبة"
            )
            group_shape.edited_by = frappe.db.get_value("User", self.owner, "full_name")
            self.save()

        if self.vehicle_shape:
            shape = self.append("shape_table", {})
            shape.date = datetime.now()
            shape.value = self.vehicle_shape
            shape.remarks = "الشكل الأساسي الذي تم إدخاله مع إنشاء المركبة"
            shape.edited_by = frappe.db.get_value("User", self.owner, "full_name")
            self.save()

        if self.vehicle_brand:
            brand = self.append("brand_table", {})
            brand.date = datetime.now()
            brand.value = self.vehicle_brand
            brand.remarks = "الماركة الأساسية التي تم إدخالها مع إنشاء المركبة"
            brand.edited_by = frappe.db.get_value("User", self.owner, "full_name")
            self.save()

        if self.vehicle_style:
            style = self.append("style_table", {})
            style.date = datetime.now()
            style.value = self.vehicle_style
            style.remarks = "الطراز الأساسي الذي تم إدخاله مع إنشاء المركبة"
            style.edited_by = frappe.db.get_value("User", self.owner, "full_name")
            self.save()

        if self.vehicle_model:
            model = self.append("model_table", {})
            model.date = datetime.now()
            model.value = self.vehicle_model
            model.remarks = "الموديل الأساسي الذي تم إدخاله مع إنشاء المركبة"
            model.edited_by = frappe.db.get_value("User", self.owner, "full_name")
            self.save()

        if self.vehicle_country:
            country = self.append("country_table", {})
            country.date = datetime.now()
            country.value = self.vehicle_country
            country.remarks = "بلد الصنع الأساسي الذي تم إدخاله مع إنشاء المركبة"
            country.edited_by = frappe.db.get_value("User", self.owner, "full_name")
            self.save()

        if self.exchange_allowance:
            exchange_allowance = self.append("exchange_allowance_table", {})
            exchange_allowance.date = datetime.now()
            exchange_allowance.value = self.exchange_allowance
            exchange_allowance.remarks = (
                "مخصص الصرف الأساسي الذي تم إدخاله مع إنشاء المركبة"
            )
            exchange_allowance.edited_by = frappe.db.get_value(
                "User", self.owner, "full_name"
            )
            self.save()

        if self.maintenance_entity:
            maintenance_entity = self.append("maintenance_entity_table", {})
            maintenance_entity.date = datetime.now()
            maintenance_entity.value = self.maintenance_entity
            maintenance_entity.remarks = (
                "جهة الصيانة الأساسية التي تم إدخالها مع إنشاء المركبة"
            )
            maintenance_entity.edited_by = frappe.db.get_value(
                "User", self.owner, "full_name"
            )
            self.save()

        if self.vehicle_status:
            status = self.append("status_table", {})
            status.date = datetime.now()
            status.value = self.vehicle_status
            status.remarks = "حالة المركبة الأساسية التي تم إدخالها مع إنشاء المركبة"
            status.edited_by = frappe.db.get_value("User", self.owner, "full_name")
            self.save()

    def validate(self):
        if self.oil_type:
            if self.oil_count is None or self.oil_count != 0:
                self.oil_count = frappe.db.get_value(
                    "Oil Type", self.oil_type, ["litre_count"]
                )

        # chassis_list = frappe.db.sql(""" Select chassis_no, vehicle_no from `tabVehicles`
        # where vehicle_status not in ("مخردة", "بيعت بالمزاد") and name != '{name}' """.format(name=self.name), as_dict=1)

        # for x in chassis_list:
        #     if self.chassis_no == x.chassis_no:
        #         frappe.throw(" لا يمكن إستخدام رقم الشاسيه " + x.chassis_no + " أكثر من مرة حيث أنه مستخدم في المركبة رقم " + x.vehicle_no)
        if self.edit_vehicle_no:
            last_vehicle_no_date = frappe.db.sql(
                """ Select date as date from `tabPolice Plate Logs` 
                    where parent = '{parent}'
                    order by date desc limit 1
                """.format(
                    parent=self.name
                ),
                as_dict=1,
            )

            for v in last_vehicle_no_date:
                if getdate(self.edit_vehicle_no_date) < getdate(v.date):
                    frappe.throw(" لا يمكن تخصيص رقم شرطة قبل " + str(v.date))

            if self.vehicle_no == self.new_vehicle_no:
                frappe.throw(" يجب إختيار رقم شرطة جديد للمركبة ")

            vehicle_list = frappe.db.sql(
                """ Select name, vehicle_no, vehicle_type from `tabVehicles` 
                    where docstatus = 0 and name != '{name}' """.format(
                    name=self.name
                ),
                as_dict=1,
            )

            for x in vehicle_list:
                if (
                    self.new_vehicle_no == x.vehicle_no
                    and self.vehicle_type == x.vehicle_type
                ):
                    frappe.throw(
                        " لا يمكن إستخدام رقم الشرطة "
                        + x.vehicle_no
                        + " أكثر من مرة حيث أنه مستخدم في المركبة رقم "
                        + x.name
                    )

            if self.vehicle_no != self.new_vehicle_no:
                if frappe.db.exists(
                    "Police Plate",
                    {
                        "plate_no": self.new_vehicle_no,
                        "vehicle_type": self.vehicle_type,
                    },
                ):
                    existing_police_plate = frappe.get_doc(
                        "Police Plate",
                        {
                            "plate_no": self.new_vehicle_no,
                            "vehicle_type": self.vehicle_type,
                        },
                    )
                    if (
                        existing_police_plate.current_vehicle
                        and existing_police_plate.current_vehicle
                        != "إحتياطي مخزن لوحات"
                    ):
                        frappe.throw(
                            " لا يمكن إستخدام رقم الشرطة "
                            + self.new_vehicle_no
                            + " أكثر من مرة حيث أنه مستخدم في المركبة رقم "
                            + existing_police_plate.current_vehicle
                        )

                    if (
                        existing_police_plate.current_vehicle == "إحتياطي مخزن لوحات"
                        and existing_police_plate.status == "معدمة"
                    ):
                        frappe.throw(
                            " لا يمكن إستخدام لوحة الشرطة رقم "
                            + self.new_vehicle_no
                            + " حيث أن حالتها معدمة "
                        )

                    else:
                        vehicle = self.append("vehicle_no_table", {})
                        vehicle.date = self.edit_vehicle_no_date
                        vehicle.value = self.new_vehicle_no
                        vehicle.remarks = self.vehicle_no_remarks
                        vehicle.edited_by = frappe.session.user

                        existing_police_plate2 = frappe.get_doc(
                            "Police Plate",
                            {
                                "plate_no": self.new_vehicle_no,
                                "vehicle_type": self.vehicle_type,
                            },
                        )
                        existing_police_plate2.current_vehicle = self.name
                        plate = existing_police_plate2.append("plate_table", {})
                        plate.date = self.edit_vehicle_no_date
                        plate.value = self.name
                        plate.remarks = self.vehicle_no_remarks
                        plate.edited_by = frappe.session.user
                        plate.doctype_name = "Vehicles"
                        plate.edit_vehicle = self.name
                        plate.save()
                        existing_police_plate2.save()

                        if self.vehicle_no:
                            old_police_plate = frappe.get_doc(
                                "Police Plate",
                                {
                                    "plate_no": self.vehicle_no,
                                    "vehicle_type": self.vehicle_type,
                                },
                            )
                            old_police_plate.current_vehicle = "إحتياطي مخزن لوحات"
                            old_plate = old_police_plate.append("plate_table", {})
                            old_plate.date = self.edit_vehicle_no_date
                            old_plate.value = "إحتياطي مخزن لوحات"
                            old_plate.remarks = self.vehicle_no_remarks
                            old_plate.edited_by = frappe.session.user
                            old_plate.doctype_name = "Vehicles"
                            old_plate.edit_vehicle = self.name
                            old_plate.save()
                            old_police_plate.save()

                if not frappe.db.exists(
                    "Police Plate",
                    {
                        "plate_no": self.new_vehicle_no,
                        "vehicle_type": self.vehicle_type,
                    },
                ):
                    vehicle = self.append("vehicle_no_table", {})
                    vehicle.date = self.edit_vehicle_no_date
                    vehicle.value = self.new_vehicle_no
                    vehicle.remarks = self.vehicle_no_remarks
                    vehicle.edited_by = frappe.session.user

                    new_police_plate = frappe.get_doc(
                        {
                            "doctype": "Police Plate",
                            "plate_no": self.new_vehicle_no,
                            "status": "صالحة",
                            "vehicle_type": self.vehicle_type,
                            "current_vehicle": self.name,
                        }
                    )
                    new_police_plate.insert(ignore_permissions=True)

                    plate = new_police_plate.append("plate_table", {})
                    plate.date = self.edit_vehicle_no_date
                    plate.value = self.name
                    plate.remarks = self.vehicle_no_remarks
                    plate.edited_by = frappe.session.user
                    plate.doctype_name = "Vehicles"
                    plate.edit_vehicle = self.name
                    plate.save()
                    new_police_plate.save()

                    if self.vehicle_no:
                        old_police_plate2 = frappe.get_doc(
                            "Police Plate",
                            {
                                "plate_no": self.vehicle_no,
                                "vehicle_type": self.vehicle_type,
                            },
                        )
                        old_police_plate2.current_vehicle = "إحتياطي مخزن لوحات"
                        old_plate = old_police_plate2.append("plate_table", {})
                        old_plate.date = self.edit_vehicle_no_date
                        old_plate.value = "إحتياطي مخزن لوحات"
                        old_plate.remarks = self.vehicle_no_remarks
                        old_plate.edited_by = frappe.session.user
                        old_plate.doctype_name = "Vehicles"
                        old_plate.edit_vehicle = self.name
                        old_plate.save()
                        old_police_plate2.save()

            self.vehicle_no = self.new_vehicle_no
            self.edit_vehicle_no = ""
            self.new_vehicle_no = ""
            self.edit_vehicle_no_date = ""
            self.vehicle_no_remarks = ""

        if self.edit_private_no:
            last_private_no_date = frappe.db.sql(
                """ Select date as date from `tabPrivate Plate Logs` 
                    where parent = '{parent}'
                    order by date desc limit 1
                """.format(
                    parent=self.name
                ),
                as_dict=1,
            )

            for v in last_private_no_date:
                if getdate(self.edit_private_no_date) < getdate(v.date):
                    frappe.throw(" لا يمكن تخصيص رقم ملاكي قبل " + str(v.date))

            if self.private_no == self.new_private_no:
                frappe.throw(" يجب إختيار رقم ملاكي جديد للمركبة ")
            if (
                frappe.db.exists(
                    "Vehicles",
                    [
                        ["private_no", "=", self.new_private_no],
                        ["name", "!=", self.name],
                        ["new_private_no", "!=", "0"],
                    ],
                )
                and self.new_private_no != "0"
            ):
                vehicle_no = frappe.db.get_value(
                    "Vehicles",
                    [
                        ["private_no", "=", self.new_private_no],
                        ["name", "!=", self.name],
                        ["new_private_no", "!=", "0"],
                    ],
                    ["vehicle_no"],
                )
                frappe.throw(
                    "لا يمكن تخصيص رقم الملاكي لانه مستخدم في المركبة رقم " + vehicle_no
                )

            else:
                private = self.append("private_no_table", {})
                private.date = self.edit_private_no_date
                private.value = self.new_private_no
                private.remarks = self.private_no_remarks
                private.edited_by = frappe.session.user
                private.traffic_entity = self.new_traffic_entity
                private.plate_type = self.new_plate_type

                new_private_plate = frappe.get_doc("Private Plate", self.new_private_no)
                new_private_plate.current_vehicle = self.name
                new_private_plate.police_no = self.vehicle_no
                new_private_plate.current_entity = self.entity_name
                plate1 = new_private_plate.append("plate_table", {})
                plate1.date = self.edit_private_no_date
                plate1.value = self.name + " - " + self.vehicle_no
                plate1.remarks = self.private_no_remarks
                plate1.edited_by = frappe.session.user
                plate1.doctype_name = "Vehicles"
                plate1.edit_vehicle = self.name
                plate1.save()
                new_private_plate.save()

                if self.private_no:
                    old_private_plate = frappe.get_doc("Private Plate", self.private_no)
                    old_private_plate.current_vehicle = ""
                    old_private_plate.police_no = ""
                    old_private_plate.current_entity = self.entity_name
                    old_private = old_private_plate.append("plate_table", {})
                    old_private.date = self.edit_private_no_date
                    old_private.value = " إحتياطي جهة " + self.entity_name
                    old_private.remarks = self.private_no_remarks
                    old_private.edited_by = frappe.session.user
                    old_private.doctype_name = "Vehicles"
                    old_private.edit_vehicle = self.name
                    old_private.save()
                    old_private_plate.save()

            self.private_no = self.new_private_no
            self.traffic_entity = self.new_traffic_entity
            self.plate_type = self.new_plate_type
            self.edit_private_no = ""
            self.new_private_no = ""
            self.new_traffic_entity = ""
            self.new_plate_type = ""
            self.edit_private_no_date = ""
            self.private_no_remarks = ""

            # plates_list = frappe.db.sql(
            #     """ Select name, private_no from `tabVehicles` where docstatus = 0 and private_no = '{private_no}' and name != '{vehicle}'
            #     """.format(private_no=self.new_private_no, vehicle=self.name), as_dict=1)

            # if plates_list:
            #     for vehicle in plates_list:
            #         if frappe.db.exists("Vehicles", vehicle.name):
            #             vehicle_doc = frappe.get_doc("Vehicles", vehicle.name)
            #             vehicle_doc.private_no = "0"
            #             vehicle_doc.traffic_entity = ""
            #             vehicle_doc.plate_type = ""
            #             private_logs = vehicle_doc.append("private_no_table", {})
            #             private_logs.date = self.edit_private_no_date
            #             private_logs.value = "0"
            #             private_logs.remarks = self.private_no_remarks
            #             private_logs.edited_by = frappe.session.user
            #             private_logs.traffic_entity = "-"
            #             private_logs.plate_type = "-"
            #             vehicle_doc.save()

        if self.edit_motor_no:
            last_motor_date = frappe.db.sql(
                """ Select date as date from `tabMotor Logs` 
                    where parent = '{parent}'
                    order by date desc limit 1
                """.format(
                    parent=self.name
                ),
                as_dict=1,
            )

            for v in last_motor_date:
                if getdate(self.edit_motor_no_date) < getdate(v.date):
                    frappe.throw(" لا يمكن تخصيص موتور قبل " + str(v.date))

            if self.motor_no == self.new_motor_no:
                frappe.throw(" يجب إختيار رقم موتور جديد للمركبة ")
            else:
                motor = self.append("motor_table", {})
                motor.date = self.edit_motor_no_date
                motor.value = self.new_motor_no
                motor.remarks = self.motor_no_remarks
                motor.edited_by = frappe.session.user

                new_motor_no = frappe.get_doc("Vehicle Motor", self.new_motor_no)
                new_motor_no.current_vehicle = self.name
                new_motor = new_motor_no.append("motor_table", {})
                new_motor.date = self.edit_motor_no_date
                new_motor.value = self.name
                new_motor.remarks = self.motor_no_remarks
                new_motor.edited_by = frappe.session.user
                new_motor.doctype_name = "Vehicles"
                new_motor.edit_vehicle = self.name
                new_motor.save()
                new_motor_no.save()

                if self.motor_no:
                    old_motor_no = frappe.get_doc("Vehicle Motor", self.motor_no)
                    old_motor_no.current_vehicle = "إحتياطي مخزن"
                    old_motor = old_motor_no.append("motor_table", {})
                    old_motor.date = self.edit_motor_no_date
                    old_motor.value = "إحتياطي مخزن"
                    old_motor.remarks = self.motor_no_remarks
                    old_motor.edited_by = frappe.session.user
                    old_motor.doctype_name = "Vehicles"
                    old_motor.edit_vehicle = self.name
                    old_motor.save()
                    old_motor_no.save()

            self.motor_no = self.new_motor_no
            self.edit_motor_no = ""
            self.new_motor_no = ""
            self.edit_motor_no_date = ""
            self.motor_no_remarks = ""

        if self.edit_style:
            last_style_date = frappe.db.sql(
                """ Select date as date from `tabStyle No Logs` 
                    where parent = '{parent}'
                    order by date desc limit 1
                """.format(
                    parent=self.name
                ),
                as_dict=1,
            )

            for v in last_style_date:
                if getdate(self.edit_style_date) < getdate(v.date):
                    frappe.throw(" لا يمكن تخصيص طراز قبل " + str(v.date))

            if self.vehicle_style == self.new_style:
                frappe.throw(" يجب إختيار طراز جديد للمركبة ")
            else:
                style = self.append("style_table", {})
                style.date = self.edit_style_date
                style.value = self.new_style
                style.remarks = self.style_remarks
                style.edited_by = frappe.session.user
                self.vehicle_style = self.new_style
                self.edit_style = ""
                self.new_style = ""
                self.edit_style_date = ""
                self.style_remarks = ""

        if self.edit_attached_entity:
            last_attached_entity_date = frappe.db.sql(
                """ Select date as date from `tabAttached Entity Logs` 
                    where parent = '{parent}'
                    order by date desc limit 1
                """.format(
                    parent=self.name
                ),
                as_dict=1,
            )

            for v in last_attached_entity_date:
                if getdate(self.edit_attached_entity_date) < getdate(v.date):
                    frappe.throw(" لا يمكن تخصيص جهة الإلحاق قبل " + str(v.date))

            if self.attached_entity == self.new_attached_entity:
                frappe.throw(" يجب إختيار جهة إلحاق جديدة للمركبة ")

            if self.entity_name == self.new_attached_entity:
                frappe.throw(" يجب إختيار جهة إلحاق مختلفة عن الجهة الأساسية للمركبة ")

            else:
                attached_entity = self.append("attached_entity_logs", {})
                attached_entity.date = self.edit_attached_entity_date
                attached_entity.value = self.new_attached_entity
                attached_entity.remarks = self.attached_entity_remarks
                attached_entity.edited_by = frappe.session.user
                self.attached_entity = self.new_attached_entity
                self.edit_attached_entity = ""
                self.new_attached_entity = ""
                self.edit_attached_entity_date = ""
                self.attached_entity_remarks = ""

        if self.edit_color:
            last_color_date = frappe.db.sql(
                """ Select date as date from `tabColor Logs` 
                    where parent = '{parent}'
                    order by date desc limit 1
                """.format(
                    parent=self.name
                ),
                as_dict=1,
            )

            for v in last_color_date:
                if getdate(self.edit_color_date) < getdate(v.date):
                    frappe.throw(" لا يمكن تخصيص لون قبل " + str(v.date))

            if self.vehicle_color == self.new_color:
                frappe.throw(" يجب إختيار لون جديد للمركبة ")
            else:
                color = self.append("color_table", {})
                color.date = self.edit_color_date
                color.value = self.new_color
                color.remarks = self.color_remarks
                color.edited_by = frappe.session.user
                self.vehicle_color = self.new_color
                self.edit_color = ""
                self.new_color = ""
                self.edit_color_date = ""
                self.color_remarks = ""

        if self.edit_processing_type:
            last_processing_type = frappe.db.sql(
                """ Select date as date from `tabProcessing Type Logs` 
                    where parent = '{parent}'
                    order by date desc limit 1
                """.format(
                    parent=self.name
                ),
                as_dict=1,
            )

            for v in last_processing_type:
                if getdate(self.edit_processing_type_date) < getdate(v.date):
                    frappe.throw(" لا يمكن تخصيص نوع تجهيز قبل " + str(v.date))

            if self.processing_type == self.new_processing_type:
                frappe.throw(" يجب إختيار نوع تجهيز جديد للمركبة ")
            else:
                processing_type = self.append("processing_type_table", {})
                processing_type.date = self.edit_processing_type_date
                processing_type.value = self.new_processing_type
                processing_type.remarks = self.processing_type_remarks
                processing_type.edited_by = frappe.session.user
                self.processing_type = self.new_processing_type
                self.edit_processing_type = ""
                self.new_processing_type = ""
                self.edit_processing_type_date = ""
                self.processing_type_remarks = ""

        if self.edit_entity:
            # check if vehicle has Liquids Issuing Table record in the same month
            # if yes, then msgprint
            vehicle_liquid_table = frappe.db.sql(
                """ Select name , issue_no, issue_date, from_date, to_date, issue_type,
                    entity
                    from `tabLiquids Issuing Table` 
                    where parent = '{parent}' and issue_date between '{first_day}' and '{last_day}'
                """.format(
                    parent=self.name, first_day=frappe.utils.get_first_day(self.edit_entity_date), last_day=self.edit_entity_date
                ),
                as_dict=1,
            )
            if vehicle_liquid_table:
                for row in vehicle_liquid_table:
                    frappe.msgprint("المركبة لها سجل صرف سوائل في نفس الشهر" + "<br>" 
                                    + "رقم الصرفية : {issue_no} ".format(issue_no=row.issue_no)
                                              + "<br>" + 
                                    "تاريخ الصرفية : {issue_date}".format(issue_date=row.issue_date)
                                              + "<br>" +
                                    " من تاريخ : {from_date}".format(from_date=row.from_date)
                                              + "<br>" +
                                    "إلى تاريخ : {to_date}".format(to_date=row.to_date)
                                            + "<br>" +
                                    " نوع الصرفية : {issue_type} ".format(issue_type=row.issue_type)
                                            + "<br>" +
                                    "جهة الصرف : {entity}".format(issue_no=row.issue_no, issue_date=row.issue_date,
                                            from_date=row.from_date, to_date=row.to_date,
                                            issue_type=row.issue_type, entity=row.entity))
            last_entity_date = frappe.db.sql(
                """ Select date as date from `tabEntity Logs` 
                    where parent = '{parent}'
                    order by date desc limit 1
                """.format(
                    parent=self.name
                ),
                as_dict=1,
            )

            for v in last_entity_date:
                if getdate(self.edit_entity_date) < getdate(v.date):
                    frappe.throw(" لا يمكن تخصيص جهة قبل " + str(v.date))

            if self.entity_name == self.new_entity:
                frappe.throw(" يجب إختيار جهة جديدة للمركبة ")

            else:
                entity = self.append("entity_table", {})
                entity.date = self.edit_entity_date
                entity.value = self.new_entity
                entity.remarks = self.entity_remarks
                entity.edited_by = frappe.session.user

                m_entity = frappe.db.get_value(
                    "Entity", self.new_entity, "maintenance_entity"
                )
                if m_entity != self.maintenance_entity and m_entity:
                    maint_entity = self.append("maintenance_entity_table", {})
                    maint_entity.date = self.edit_entity_date
                    maint_entity.value = m_entity
                    maint_entity.remarks = (
                        " تم تعديل جهة الصيانة تلقائيا مع تعديل جهة المركبة "
                    )
                    maint_entity.edited_by = frappe.session.user
                    self.maintenance_entity = m_entity

                if self.private_no and self.new_entity != "احتياطى مخازن المركبات":
                    new_private_plate = frappe.get_doc("Private Plate", self.private_no)
                    new_private_plate.current_entity = self.new_entity
                    new_private_plate.save()

                if self.private_no and self.new_entity == "احتياطى مخازن المركبات":
                    new_private_plate = frappe.get_doc("Private Plate", self.private_no)
                    new_private_plate.current_vehicle = ""
                    new_private_plate.police_no = ""
                    new_private_plate.current_entity = self.entity_name
                    plate1 = new_private_plate.append("plate_table", {})
                    plate1.date = self.edit_entity_date
                    plate1.value = " إحتياطي جهة " + self.entity_name
                    plate1.remarks = " تم تخصيص جهة المركبة إلى إحتياطي مخزن "
                    plate1.edited_by = frappe.session.user
                    plate1.doctype_name = "Vehicles"
                    plate1.edit_vehicle = self.name
                    plate1.save()
                    new_private_plate.save()
                    self.private_no = ""

                self.entity_name = self.new_entity
                self.entity_date = self.edit_entity_date
                self.edit_entity = ""
                self.new_entity = ""
                self.edit_entity_date = ""
                self.entity_remarks = ""

        if self.edit_maintenance_entity:
            last_maintenance_entity_date = frappe.db.sql(
                """ Select date as date from `tabMaintenance Entity Logs` 
                    where parent = '{parent}'
                    order by date desc limit 1
                """.format(
                    parent=self.name
                ),
                as_dict=1,
            )

            for v in last_maintenance_entity_date:
                if getdate(self.edit_maintenance_entity_date) < getdate(v.date):
                    frappe.throw(" لا يمكن تخصيص جهة صيانة قبل " + str(v.date))

            if self.maintenance_entity == self.new_maintenance_entity:
                frappe.throw(" يجب إختيار جهة صيانة جديدة للمركبة ")
            else:
                maintenance_entity = self.append("maintenance_entity_table", {})
                maintenance_entity.date = self.edit_maintenance_entity_date
                maintenance_entity.value = self.new_maintenance_entity
                maintenance_entity.remarks = self.maintenance_entity_remarks
                maintenance_entity.edited_by = frappe.session.user
                self.maintenance_entity = self.new_maintenance_entity
                self.edit_maintenance_entity = ""
                self.new_maintenance_entity = ""
                self.edit_maintenance_entity_date = ""
                self.maintenance_entity_remarks = ""

        if self.edit_status:
            last_status_date = frappe.db.sql(
                """ Select date as date from `tabVehicle Status Logs` 
                    where parent = '{parent}'
                    order by date desc limit 1
                """.format(
                    parent=self.name
                ),
                as_dict=1,
            )

            for v in last_status_date:
                if getdate(self.edit_status_date) < getdate(v.date):
                    frappe.throw(" لا يمكن تخصيص حالة المركبة قبل " + str(v.date))

            if self.vehicle_status == self.new_status:
                frappe.throw(" يجب إختيار حالة جديدة للمركبة ")

            if self.new_status == "صالحة" and self.vehicle_status == "تحت التخريد":
                frappe.throw(
                    " يجب تخصيص حالة المركبة إلى عاطلة أولا حتى تتمكن من تخصيص حالتها إلى صالحة "
                )

            if self.new_status == "تحت التخريد" and self.vehicle_status != "عاطلة":
                frappe.throw(
                    " يجب تخصيص حالة المركبة إلى عاطلة أولا حتى تتمكن من تخصيص حالتها إلى تحت التخريد "
                )

            if self.new_status == "مخردة" and self.vehicle_status != "تحت التخريد":
                frappe.throw(
                    " يجب تخصيص حالة المركبة إلى تحت التخريد أولا حتى تتمكن من تخصيص حالتها إلى مخردة "
                )

            if self.new_status == "مخردة" and self.vehicle_no:
                police_plate_id = self.vehicle_no + " - " + self.vehicle_type
                police_plate = frappe.get_doc("Police Plate", police_plate_id)
                police_plate.current_vehicle = "إحتياطي مخزن لوحات"
                plate = police_plate.append("plate_table", {})
                plate.date = self.edit_status_date
                plate.value = "إحتياطي مخزن لوحات"
                plate.remarks = "تم تخريد المركبة"
                plate.edited_by = frappe.session.user
                plate.doctype_name = "Vehicles"
                plate.edit_vehicle = self.name
                plate.save()
                police_plate.save()

                status = self.append("status_table", {})
                status.date = self.edit_status_date
                status.value = self.new_status
                status.remarks = self.status_remarks
                status.edited_by = frappe.session.user
                self.vehicle_status = self.new_status
                self.edit_status = ""
                self.new_status = ""
                self.edit_status_date = ""
                self.status_remarks = ""
                self.police_id = self.vehicle_no
                self.vehicle_no = ""

            else:
                status = self.append("status_table", {})
                status.date = self.edit_status_date
                status.value = self.new_status
                status.remarks = self.status_remarks
                status.edited_by = frappe.session.user
                self.vehicle_status = self.new_status
                self.edit_status = ""
                self.new_status = ""
                self.edit_status_date = ""
                self.status_remarks = ""

        if self.edit_chassis_no:
            last_chassis_date = frappe.db.sql(
                """ Select date as date from `tabChassis No Logs` 
                    where parent = '{parent}'
                    order by date desc limit 1
                """.format(
                    parent=self.name
                ),
                as_dict=1,
            )

            for v in last_chassis_date:
                if getdate(self.edit_chassis_no_date) < getdate(v.date):
                    frappe.throw(" لا يمكن تخصيص رقم الشاسيه قبل " + str(v.date))

            if self.chassis_no == self.new_chassis_no:
                frappe.throw(" يجب إختيار رقم شاسيه جديد للمركبة ")
            else:
                chassis_no = self.append("chassis_no_table", {})
                chassis_no.date = self.edit_chassis_no_date
                chassis_no.value = self.new_chassis_no
                chassis_no.remarks = self.chassis_no_remarks
                chassis_no.edited_by = frappe.session.user
                self.chassis_no = self.new_chassis_no
                self.edit_chassis_no = ""
                self.new_chassis_no = ""
                self.edit_chassis_no_date = ""
                self.chassis_no_remarks = ""

        if self.edit_group_shape:
            last_group_shape_date = frappe.db.sql(
                """ Select date as date from `tabGroup Shape Logs` 
                    where parent = '{parent}'
                    order by date desc limit 1
                """.format(
                    parent=self.name
                ),
                as_dict=1,
            )

            for v in last_group_shape_date:
                if getdate(self.edit_group_shape_date) < getdate(v.date):
                    frappe.throw(" لا يمكن تخصيص مجموعة الشكل قبل " + str(v.date))

            if self.group_shape == self.new_group_shape:
                frappe.throw(" يجب إختيار مجموعة شكل جديدة للمركبة ")
            else:
                group_shape = self.append("group_shape_table", {})
                group_shape.date = self.edit_group_shape_date
                group_shape.value = self.new_group_shape
                group_shape.remarks = self.group_shape_remarks
                group_shape.edited_by = frappe.session.user
                self.group_shape = self.new_group_shape
                self.edit_group_shape = ""
                self.new_group_shape = ""
                self.edit_group_shape_date = ""
                self.group_shape_remarks = ""

        if self.edit_shape:
            last_shape_date = frappe.db.sql(
                """ Select date as date from `tabShape No Logs` 
                    where parent = '{parent}'
                    order by date desc limit 1
                """.format(
                    parent=self.name
                ),
                as_dict=1,
            )

            for v in last_shape_date:
                if getdate(self.edit_shape_date) < getdate(v.date):
                    frappe.throw(" لا يمكن تخصيص الشكل قبل " + str(v.date))

            if self.vehicle_shape == self.new_shape:
                frappe.throw(" يجب إختيار شكل جديد للمركبة ")
            else:
                shape = self.append("shape_table", {})
                shape.date = self.edit_shape_date
                shape.value = self.new_shape
                shape.remarks = self.shape_remarks
                shape.edited_by = frappe.session.user
                self.vehicle_shape = self.new_shape
                self.edit_shape = ""
                self.new_shape = ""
                self.edit_shape_date = ""
                self.shape_remarks = ""

        if self.edit_brand:
            last_brand_date = frappe.db.sql(
                """ Select date as date from `tabBrand No Logs` 
                    where parent = '{parent}'
                    order by date desc limit 1
                """.format(
                    parent=self.name
                ),
                as_dict=1,
            )

            for v in last_brand_date:
                if getdate(self.edit_brand_date) < getdate(v.date):
                    frappe.throw(" لا يمكن تخصيص الماركة قبل " + str(v.date))

            if self.vehicle_brand == self.new_brand:
                frappe.throw(" يجب إختيار ماركة جديد للمركبة ")
            else:
                brand = self.append("brand_table", {})
                brand.date = self.edit_brand_date
                brand.value = self.new_brand
                brand.remarks = self.brand_remarks
                brand.edited_by = frappe.session.user
                self.vehicle_brand = self.new_brand
                self.edit_brand = ""
                self.new_brand = ""
                self.edit_brand_date = ""
                self.brand_remarks = ""

        if self.edit_model:
            last_model_date = frappe.db.sql(
                """ Select date as date from `tabModel No Loge` 
                    where parent = '{parent}'
                    order by date desc limit 1
                """.format(
                    parent=self.name
                ),
                as_dict=1,
            )

            for v in last_model_date:
                if getdate(self.edit_model_date) < getdate(v.date):
                    frappe.throw(" لا يمكن تخصيص الموديل قبل " + str(v.date))

            if self.vehicle_model == self.new_model:
                frappe.throw(" يجب إختيار موديل جديد للمركبة ")
            else:
                model = self.append("model_table", {})
                model.date = self.edit_model_date
                model.value = self.new_model
                model.remarks = self.model_remarks
                model.edited_by = frappe.session.user
                self.vehicle_model = self.new_model
                self.edit_model = ""
                self.new_model = ""
                self.edit_model_date = ""
                self.model_remarks = ""

        if self.edit_country:
            last_country_date = frappe.db.sql(
                """ Select date as date from `tabCountry No Logs` 
                    where parent = '{parent}'
                    order by date desc limit 1
                """.format(
                    parent=self.name
                ),
                as_dict=1,
            )

            for v in last_country_date:
                if getdate(self.edit_country_date) < getdate(v.date):
                    frappe.throw(" لا يمكن تخصيص بلد الصنع قبل " + str(v.date))

            if self.vehicle_country == self.new_country:
                frappe.throw(" يجب إختيار بلد صنع جديد للمركبة ")
            else:
                country = self.append("country_table", {})
                country.date = self.edit_country_date
                country.value = self.new_country
                country.remarks = self.country_remarks
                country.edited_by = frappe.session.user
                self.vehicle_country = self.new_country
                self.edit_country = ""
                self.new_country = ""
                self.edit_country_date = ""
                self.country_remarks = ""

        if self.edit_exchange_allowance:
            last_exchange_allowance_date = frappe.db.sql(
                """ Select date as date from `tabExchange Allowance Logs` 
                    where parent = '{parent}'
                    order by date desc limit 1
                """.format(
                    parent=self.name
                ),
                as_dict=1,
            )

            for v in last_exchange_allowance_date:
                if getdate(self.edit_exchange_allowance_date) < getdate(v.date):
                    frappe.throw(" لا يمكن تخصيص مخصص الصرف قبل " + str(v.date))

            if self.exchange_allowance == self.new_exchange_allowance:
                frappe.throw(" يجب إختيار مخصص صرف جديد للمركبة ")
            else:
                exchange_allowance = self.append("exchange_allowance_table", {})
                exchange_allowance.date = self.edit_exchange_allowance_date
                exchange_allowance.value = self.new_exchange_allowance
                exchange_allowance.remarks = self.exchange_allowance_remarks
                exchange_allowance.edited_by = frappe.session.user
                self.exchange_allowance = self.new_exchange_allowance
                self.edit_exchange_allowance = ""
                self.new_exchange_allowance = ""
                self.edit_exchange_allowance_date = ""
                self.exchange_allowance_remarks = ""

    @frappe.whitelist()
    def delete_vehicle(doc, method=None):
        if frappe.db.exists("Police Plate", {"current_vehicle": doc.vehicle_no}):
            frappe.db.sql(
                """ UPDATE `tabPolice Plate` SET current_vehicle = "" WHERE current_vehicle = '{vehicle}'
                """.format(
                    vehicle=doc.name
                )
            )

        if frappe.db.exists("Private Plate", {"current_vehicle": doc.vehicle_no}):
            frappe.db.sql(
                """ UPDATE `tabPrivate Plate` SET current_vehicle = "" WHERE current_vehicle = '{vehicle}'
                """.format(
                    vehicle=doc.name
                )
            )

        if frappe.db.exists("Vehicle Motor", {"current_vehicle": doc.name}):
            frappe.db.sql(
                """ UPDATE `tabVehicle Motor` SET current_vehicle = "" WHERE current_vehicle = '{vehicle}'
                """.format(
                    vehicle=doc.name
                )
            )

        if frappe.db.exists("Editing Table", {"edit_vehicle": doc.name}):
            frappe.db.sql(
                """ DELETE FROM `tabEditing Table` WHERE edit_vehicle = '{vehicle}'
                """.format(
                    vehicle=doc.name
                )
            )

        if frappe.db.exists("Edit Vehicle", {"vehicle_no": doc.name}):
            frappe.db.sql(
                """ UPDATE `tabEdit Vehicle` SET vehicle_no = "" WHERE vehicle_no = '{vehicle}'
            """.format(
                    vehicle=doc.name
                )
            )

        if frappe.db.exists("Vehicle Maintenance Process", {"vehicles": doc.name}):
            frappe.db.sql(
                """ UPDATE `tabVehicle Maintenance Process` SET vehicles = "" WHERE vehicles = '{vehicle}'
            """.format(
                    vehicle=doc.name
                )
            )

        if frappe.db.exists("Vehicles Issuing Table", {"vehicle": doc.name}):
            frappe.db.sql(
                """ UPDATE `tabVehicles Issuing Table` SET vehicle = "" WHERE vehicle = '{vehicle}'
            """.format(
                    vehicle=doc.name
                )
            )

        if frappe.db.exists("Specified Vehicles Issuing Table", {"vehicle": doc.name}):
            frappe.db.sql(
                """ UPDATE `tabSpecified Vehicles Issuing Table` SET vehicle = "" WHERE vehicle = '{vehicle}'
            """.format(
                    vehicle=doc.name
                )
            )

        if frappe.db.exists("Vehicles Table", {"vehicle": doc.name}):
            frappe.db.sql(
                """ UPDATE `tabVehicles Table` SET vehicle = "" WHERE vehicle = '{vehicle}'
            """.format(
                    vehicle=doc.name
                )
            )

        if frappe.db.exists("Accident", {"vehicle": doc.name}):
            frappe.db.sql(
                """ UPDATE `tabAccident` SET vehicle = "" WHERE vehicle = '{vehicle}'
                """.format(
                    vehicle=doc.name
                )
            )

        if frappe.db.exists("Vehicle License", {"vehicle": doc.name}):
            frappe.db.sql(
                """ UPDATE `tabVehicle License` SET vehicle = "" WHERE vehicle = '{vehicle}'
            """.format(
                    vehicle=doc.name
                )
            )

        if frappe.db.exists("Vehicle License", {"vehicle2": doc.name}):
            frappe.db.sql(
                """ UPDATE `tabVehicle License` SET vehicle2 = "" WHERE vehicle2 = '{vehicle}'
            """.format(
                    vehicle=doc.name
                )
            )

        if frappe.db.exists("Vehicle License", {"vehicle3": doc.name}):
            frappe.db.sql(
                """ UPDATE `tabVehicle License` SET vehicle3 = "" WHERE vehicle3 = '{vehicle}'
            """.format(
                    vehicle=doc.name
                )
            )

        if frappe.db.exists("Vehicle License", {"vehicle4": doc.name}):
            frappe.db.sql(
                """ UPDATE `tabVehicle License` SET vehicle4 = "" WHERE vehicle4 = '{vehicle}'
            """.format(
                    vehicle=doc.name
                )
            )

        if frappe.db.exists("Vehicle License Entries", {"vehicle": doc.name}):
            frappe.db.sql(
                """ UPDATE `tabVehicle License Entries` SET vehicle = "" WHERE vehicle = '{vehicle}'
            """.format(
                    vehicle=doc.name
                )
            )

        if frappe.db.exists("Custody Report", {"vehicles": doc.name}):
            frappe.db.sql(
                """ UPDATE `tabCustody Report` SET vehicles = "" WHERE vehicles = '{vehicle}'
            """.format(
                    vehicle=doc.name
                )
            )

        if frappe.db.exists("Maintenance Order", {"vehicles": doc.name}):
            frappe.db.sql(
                """ UPDATE `tabMaintenance Order` SET vehicles = "" WHERE vehicles = '{vehicle}'
            """.format(
                    vehicle=doc.name
                )
            )

        if frappe.db.exists(
            "Maintenance Request for Quotations", {"vehicles": doc.name}
        ):
            frappe.db.sql(
                """ UPDATE `tabMaintenance Request for Quotations` SET vehicles = "" WHERE vehicles = '{vehicle}'
            """.format(
                    vehicle=doc.name
                )
            )

        if frappe.db.exists("Presentation Note Out", {"vehicles": doc.name}):
            frappe.db.sql(
                """ UPDATE `tabPresentation Note Out` SET vehicles = "" WHERE vehicles = '{vehicle}'
            """.format(
                    vehicle=doc.name
                )
            )

        if frappe.db.exists("Job Order", {"vehicles": doc.name}):
            frappe.db.sql(
                """ UPDATE `tabJob Order` SET vehicles = "" WHERE vehicles = '{vehicle}'
            """.format(
                    vehicle=doc.name
                )
            )

        if frappe.db.exists("Presentation Note Item", {"vehicles": doc.name}):
            frappe.db.sql(
                """ UPDATE `tabPresentation Note Item` SET vehicles = "" WHERE vehicles = '{vehicle}'
            """.format(
                    vehicle=doc.name
                )
            )

        if frappe.db.exists("Purchase Order Item", {"vehicles": doc.name}):
            frappe.db.sql(
                """ UPDATE `tabPurchase Order Item` SET vehicles = "" WHERE vehicles = '{vehicle}'
            """.format(
                    vehicle=doc.name
                )
            )

        if frappe.db.exists("Purchase Invoices", {"vehicles": doc.name}):
            frappe.db.sql(
                """ UPDATE `tabPurchase Invoices` SET vehicles = "" WHERE vehicles = '{vehicle}'
            """.format(
                    vehicle=doc.name
                )
            )

        if frappe.db.exists("Finance Form Invoices", {"vehicle": doc.name}):
            frappe.db.sql(
                """ UPDATE `tabFinance Form Invoices` SET vehicle = "" WHERE vehicle = '{vehicle}'
            """.format(
                    vehicle=doc.name
                )
            )

        if frappe.db.exists("Stock Entry", {"vehicles": doc.name}):
            frappe.db.sql(
                """ UPDATE `tabStock Entry` SET vehicles = "" WHERE vehicles = '{vehicle}'
            """.format(
                    vehicle=doc.name
                )
            )

        frappe.db.sql(
            """ DELETE FROM `tabVehicles` WHERE name = '{vehicle}'
            """.format(
                vehicle=doc.name
            )
        )
        # doc.delete(ignore_permissions=True)
        frappe.msgprint(" تم حذف المركبة بنجاح ")
