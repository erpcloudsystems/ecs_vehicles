import frappe
from frappe.model.document import Document
from frappe.utils import (
    cstr,
    flt,
    getdate,
    comma_or,
    nowdate,
    nowtime,
    get_datetime,
    get_datetime_str,
    get_link_to_form,
    get_url_to_form,
)
from frappe.utils import getdate
from frappe.utils import in_words, nowdate, now_datetime

import datetime


class LiquidsIssuing(Document):
    @frappe.whitelist()
    def update_gas(doc, method=None):
        if doc.gas_per_vehicle_type_table:
            gas_valid_vehicle_list = frappe.db.sql(
                """ Select count(`tabVehicles`.name) as valid_count,
                                    `tabVehicles`.name as vehicle,
                                    `tabVehicles`.vehicle_no as vehicle_no,
                                    `tabVehicles`.vehicle_type as vehicle_type,
                                    `tabVehicles`.entity_name as entity_name,
                                    `tabVehicles`.gas_count as qty
                                    from `tabVehicles` 
                                    where `tabVehicles`.vehicle_status = "صالحة"
                                    and ((`tabVehicles`.entity_name = '{entity}' and (`tabVehicles`.attached_entity is null or `tabVehicles`.attached_entity = ""))
                                    or (`tabVehicles`.entity_name != '{entity}' and `tabVehicles`.attached_entity = '{entity}'))
                                    and `tabVehicles`.exchange_allowance not in ("لوحة فقط", "لوحة وخدمة كاملة فقط")
                                    and `tabVehicles`.vehicle_type != "لانش"
                                    and `tabVehicles`.gas_count != 0
                                    and `tabVehicles`.name not in (select `tabLiquids Issuing Table`.parent 
                                        from `tabLiquids Issuing Table`
                                        where `tabLiquids Issuing Table`.issue_type = '{issue_type}'
                                        and `tabLiquids Issuing Table`.from_date >= '{from_date}'
                                        and `tabLiquids Issuing Table`.to_date <= '{to_date}')
                                """.format(
                    entity=doc.entity,
                    from_date=doc.from_date,
                    to_date=doc.to_date,
                    issue_type="غاز",
                ),
                as_dict=1,
            )
            current_vehicles = []
            for t in gas_valid_vehicle_list:
                current_vehicles.append(t.vehicle)
                vehicle_status = frappe.db.get_value(
                    "Vehicles", t.vehicle, "vehicle_status"
                )
                voucher = ""
                voucher1 = ""
                record_name = 1
                max_id = frappe.db.sql(
                    """
                    SELECT MAX(name) as max_name
                    FROM `tabLiquids Issuing Table`
                    """,
                    as_dict=1,
                )
                if frappe.db.exists("Liquids Issuing Table", 1):
                    record_name = int(max_id[0]["max_name"]) + 1
                voucher = "غاز طبيعي فئة 15 متر مكعب"
                voucher1 = "لا يوجد"
                frappe.db.sql(
                    """ INSERT INTO `tabLiquids Issuing Table`
                                        (issue_date, issue_type, vehicle_status, voucher, from_date, to_date, entity, qty, created_by, issue_no, parent, parentfield, parenttype, name)
                                VALUES ('{issue_date}', '{issue_type}', '{vehicle_status}', '{voucher}' ,'{from_date}', '{to_date}', '{entity}', '{qty}', '{created_by}', '{issue_no}','{parent}', '{parentfield}', '{parenttype}', '{record_name}')
                                """.format(
                        issue_date=doc.issue_date,
                        issue_type="غاز",
                        vehicle_status=vehicle_status,
                        from_date=doc.from_date,
                        voucher=voucher,
                        to_date=doc.to_date,
                        entity=doc.entity,
                        qty=t.qty,
                        created_by=frappe.session.user,
                        issue_no=doc.name,
                        parenttype="Vehicles",
                        parent=t.vehicle,
                        parentfield="liquid_table",
                        record_name=record_name,
                    )
                )

            if len(current_vehicles) == 1:
                current_vehicles.append("None")
            if not current_vehicles:
                frappe.msgprint(str(current_vehicles))
            gas_total_vehicle_list = frappe.db.sql(
                """ Select `tabVehicles`.name as name,
                                    `tabVehicles`.vehicle_status as vehicle_status
                                    from `tabVehicles` 
                                    where `tabVehicles`.vehicle_type != "لانش"
                                    and `tabVehicles`.gas_count != 0
                                    and ((`tabVehicles`.entity_name = '{entity}' and (`tabVehicles`.attached_entity is null or `tabVehicles`.attached_entity = ""))
                                    or (`tabVehicles`.entity_name != '{entity}' and `tabVehicles`.attached_entity = '{entity}'))
                                    and `tabVehicles`.vehicle_status in ("صالحة", "عاطلة", "تحت التخريد")
                                    and name not in {current_vehicles}
                                """.format(
                    entity=doc.entity,
                    current_vehicles=tuple(current_vehicles),
                ),
                as_dict=1,
            )

            for z in gas_total_vehicle_list:
                record_name = 1
                max_id = frappe.db.sql(
                    """
                    SELECT MAX(name) as max_name
                    FROM `tabLiquids Issuing Table`
                    """,
                    as_dict=1,
                )
                if frappe.db.exists("Liquids Issuing Table", 1):
                    record_name = int(max_id[0]["max_name"]) + 1
                voucher = ""
                if doc.issue_type == "وقود":
                    voucher = (
                        frappe.db.get_value("Vehicles", z.name, "fuel_voucher")
                        if frappe.db.get_value("Vehicles", z.name, "fuel_voucher")
                        else "لا يوجد"
                    )
                if doc.issue_type == "زيت":
                    voucher = (
                        frappe.db.get_value("Vehicles", z.name, "oil_type")
                        if frappe.db.get_value("Vehicles", z.name, "oil_type")
                        else "لا يوجد"
                    )
                if doc.issue_type == "غاز":
                    voucher = "غاز طبيعي فئة 15 متر مكعب"
                if doc.issue_type == "غسيل":
                    voucher = (
                        frappe.db.get_value("Vehicles", z.name, "washing_voucher")
                        if frappe.db.get_value("Vehicles", z.name, "washing_voucher")
                        else "لا يوجد"
                    )
                voucher = "غاز طبيعي فئة 15 متر مكعب"
                frappe.db.sql(
                    """ INSERT INTO `tabLiquids Issuing Table`
                                                        (issue_date, issue_type, vehicle_status, voucher, from_date, to_date, entity, qty, created_by, issue_no, parent, parentfield, parenttype, name)
                                                VALUES ('{issue_date}', '{issue_type}', '{vehicle_status}', '{voucher}' ,'{from_date}', '{to_date}', '{entity}', '{qty}', '{created_by}', '{issue_no}','{parent}', '{parentfield}', '{parenttype}', '{record_name}')
                                            """.format(
                        issue_date=doc.issue_date,
                        issue_type="غاز",
                        vehicle_status="عاطلة",
                        from_date=doc.from_date,
                        voucher=voucher,
                        to_date=doc.to_date,
                        entity=doc.entity,
                        qty=0,
                        created_by=frappe.session.user,
                        issue_no=doc.name,
                        parenttype="Vehicles",
                        parent=z.name,
                        parentfield="liquid_table",
                        record_name=record_name,
                    )
                )

        if doc.issue_to == "مركبة أو مجموعة مركبات":
            for t in doc.specified_vehicles_issuing_table:
                if t.last_issue_from_date or t.last_issue_to_date:
                    if (
                        float(t.last_issue_qty) > 0
                        and getdate(t.last_issue_from_date) >= getdate(doc.from_date)
                        and getdate(t.last_issue_from_date) <= getdate(doc.to_date)
                    ):
                        frappe.throw(
                            " الصف # "
                            + str(t.idx)
                            + " : لا يمكن صرف "
                            + doc.issue_type
                            + " إلى المركبة "
                            + str(t.vehicle_no)
                            + " حيث أنه تم الصرف لها من قبل خلال الفترة المحددة إلى جهة "
                            + str(t.entity_name)
                        )

                    if (
                        float(t.last_issue_qty) > 0
                        and getdate(t.last_issue_to_date) >= getdate(doc.from_date)
                        and getdate(t.last_issue_to_date) <= getdate(doc.to_date)
                    ):
                        frappe.throw(
                            " الصف # "
                            + str(t.idx)
                            + " : لا يمكن صرف "
                            + doc.issue_type
                            + " إلى المركبة "
                            + str(t.vehicle_no)
                            + " حيث أنه تم الصرف لها من قبل خلال الفترة المحددة إلى جهة "
                            + str(t.entity_name)
                        )

                vehicle_status = frappe.db.get_value(
                    "Vehicles", t.vehicle, "vehicle_status"
                )
                voucher = ""

                if doc.issue_type == "وقود":
                    voucher = (
                        frappe.db.get_value("Vehicles", t.vehicle, "fuel_voucher")
                        if frappe.db.get_value("Vehicles", t.vehicle, "fuel_voucher")
                        else "لا يوجد"
                    )
                if doc.issue_type == "زيت":
                    voucher = frappe.db.get_value("Vehicles", t.vehicle, "oil_type")
                if doc.issue_type == "غاز":
                    voucher = "غاز طبيعي فئة 15 متر مكعب"
                if doc.issue_type == "غسيل":
                    voucher = frappe.db.get_value(
                        "Vehicles", t.vehicle, "washing_voucher"
                    )

                record_name = 1
                max_id = frappe.db.sql(
                    """
                    SELECT MAX(name) as max_name
                    FROM `tabLiquids Issuing Table`
                    """,
                    as_dict=1,
                )
                if frappe.db.exists("Liquids Issuing Table", 1):
                    record_name = int(max_id[0]["max_name"]) + 1
                frappe.db.sql(
                    """ INSERT INTO `tabLiquids Issuing Table`
                                                        (issue_date, issue_type, vehicle_status, voucher, from_date, to_date, entity, qty, created_by, issue_no, parent, parentfield, parenttype, name)
                                                VALUES ('{issue_date}', '{issue_type}', '{vehicle_status}', '{voucher}', '{from_date}', '{to_date}', '{entity}', '{qty}', '{created_by}', '{issue_no}','{parent}', '{parentfield}', '{parenttype}', '{record_name}')
                                              """.format(
                        issue_date=doc.issue_date,
                        issue_type=doc.issue_type,
                        from_date=doc.from_date,
                        vehicle_status=vehicle_status,
                        voucher=voucher,
                        qty=t.qty,
                        to_date=doc.to_date,
                        entity=doc.entity,
                        created_by=frappe.session.user,
                        issue_no=doc.name,
                        parenttype="Vehicles",
                        parent=t.vehicle,
                        parentfield="liquid_table",
                        record_name=record_name,
                    )
                )

                gas_valid_vehicle_list = frappe.db.sql(
                    """ Select
                        `tabVehicles`.name as vehicle,
                        `tabVehicles`.gas_count as gas_count
                        from `tabVehicles` 
                        where `tabVehicles`.name = '{vehicle}'
                        and `tabVehicles`.gas_count > 0
                        and `tabVehicles`.name not in (select `tabLiquids Issuing Table`.parent 
                            from `tabLiquids Issuing Table`
                            where `tabLiquids Issuing Table`.issue_type = '{issue_type}'
                            and `tabLiquids Issuing Table`.from_date >= '{from_date}'
                            and `tabLiquids Issuing Table`.to_date <= '{to_date}')
                    """.format(
                        entity=doc.entity,
                        from_date=doc.from_date,
                        to_date=doc.to_date,
                        issue_type="غاز",
                        vehicle=t.vehicle,
                    ),
                    as_dict=1,
                )
                current_vehicles = []
                if gas_valid_vehicle_list:
                    current_vehicles.append(t.vehicle)
                    vehicle_status = frappe.db.get_value(
                        "Vehicles", t.vehicle, "vehicle_status"
                    )
                    voucher = ""
                    voucher1 = ""
                    record_name = 1
                    max_id = frappe.db.sql(
                        """
                        SELECT MAX(name) as max_name
                        FROM `tabLiquids Issuing Table`
                        """,
                        as_dict=1,
                    )
                    if frappe.db.exists("Liquids Issuing Table", 1):
                        record_name = int(max_id[0]["max_name"]) + 1
                    voucher = "غاز طبيعي فئة 15 متر مكعب"
                    voucher1 = "لا يوجد"
                    # frappe.throw(str(gas_valid_vehicle_list))
                    frappe.db.sql(
                        """ INSERT INTO `tabLiquids Issuing Table`
                                            (issue_date, issue_type, vehicle_status, voucher, from_date, to_date, entity, qty, created_by, issue_no, parent, parentfield, parenttype, name)
                                    VALUES ('{issue_date}', '{issue_type}', '{vehicle_status}', '{voucher}' ,'{from_date}', '{to_date}', '{entity}', '{qty}', '{created_by}', '{issue_no}','{parent}', '{parentfield}', '{parenttype}', '{record_name}')
                                    """.format(
                            issue_date=doc.issue_date,
                            issue_type="غاز",
                            vehicle_status=vehicle_status,
                            from_date=doc.from_date,
                            voucher=voucher,
                            to_date=doc.to_date,
                            entity=doc.entity,
                            qty=(
                                doc.issue_days
                                * gas_valid_vehicle_list[0].gas_count
                                / 30
                            ),
                            created_by=frappe.session.user,
                            issue_no=doc.name,
                            parenttype="Vehicles",
                            parent=t.vehicle,
                            parentfield="liquid_table",
                            record_name=record_name,
                        )
                    )

                if len(current_vehicles) == 1:
                    current_vehicles.append("None")
                if not current_vehicles:
                    pass
                    # frappe.msgprint("لا يوجد مركبات تستحق الصرف")

    @frappe.whitelist()
    def set_today_date(doc, method=None):
        if not doc.issue_date:
            doc.issue_date = nowdate()
            doc.from_date = (
                datetime.datetime.now().replace(day=1) + datetime.timedelta(days=32)
            ).replace(day=1)

    @frappe.whitelist()
    def get_empty_pages(doc, method=None):
        frappe.db.sql(
            """ UPDATE `tabLiquids Issuing` SET empty_pages = {empty_pages}
                      WHERE name = '{name}' """.format(
                empty_pages=doc.empty_pages, name=doc.name
            )
        )

    @frappe.whitelist()
    def get_fuel_type(doc, method=None):
        frappe.db.sql(
            """ UPDATE `tabLiquids Issuing` SET fuel_type = '{fuel_type}'
                      WHERE name = '{name}' """.format(
                fuel_type=doc.fuel_type, name=doc.name
            )
        )

    @frappe.whitelist()
    def get_cylinder_count(doc, method=None):
        frappe.db.sql(
            """ UPDATE `tabLiquids Issuing` SET cylinder_count = '{cylinder_count}'
                      WHERE name = '{name}' """.format(
                cylinder_count=doc.cylinder_count, name=doc.name
            )
        )

    @frappe.whitelist()
    def get_litre_count(doc, method=None):
        frappe.db.sql(
            """ UPDATE `tabLiquids Issuing` SET litre_count = '{litre_count}'
                      WHERE name = '{name}' """.format(
                litre_count=doc.litre_count, name=doc.name
            )
        )

    @frappe.whitelist()
    def get_compare_with_date(doc, method=None):
        frappe.db.sql(
            """ UPDATE `tabLiquids Issuing` SET compare_with_date = '{compare_with_date}'
                      WHERE name = '{name}' """.format(
                compare_with_date=doc.compare_with_date, name=doc.name
            )
        )

    @frappe.whitelist()
    def get_total_vehicles(self):
        last_doc = frappe.db.sql(
            """
            SELECT `tabLiquids Issuing`.name as name, 
                    `tabLiquids Issuing`.from_date as from_date, 
                    `tabLiquids Issuing`.to_date as to_date
            FROM `tabLiquids Issuing`
            WHERE `tabLiquids Issuing`.submitted = 1 
            AND `tabLiquids Issuing`.issue_to = "{issue_to}"
            AND `tabLiquids Issuing`.entity = "{entity}"
            AND `tabLiquids Issuing`.issue_type = "{issue_type}"
            ORDER BY `tabLiquids Issuing`.from_date DESC LIMIT 1 
        """.format(
                issue_to=self.issue_to,
                entity=self.entity,
                issue_type=self.issue_type,
            ),
            as_dict=1,
        )

        if last_doc:
            last_issue = (
                " من " + str(last_doc[0].from_date) + " إلى " + str(last_doc[0].to_date)
            )
            self.last_issue = last_issue
        if self.issue_type == "وقود":
            total_vehicle_list = frappe.db.sql(
                """ Select count(`tabVehicles`.name) as total_count 
                    from `tabVehicles` 
                    JOIN `tabFuel Voucher` on `tabVehicles`.fuel_voucher = `tabFuel Voucher`.name
                    Where `tabFuel Voucher`.fuel_type in (Select distinct `tabFuel Voucher`.fuel_type as fuel_type 
                            from `tabVehicles`
                            JOIN `tabFuel Voucher` on `tabVehicles`.fuel_voucher = `tabFuel Voucher`.name
                            where `tabVehicles`.vehicle_type != "لانش"
                            and `tabVehicles`.fuel_type != "بدون وقود")
                    and ((`tabVehicles`.entity_name = '{entity}' and (`tabVehicles`.attached_entity is null or `tabVehicles`.attached_entity = ""))
                    or (`tabVehicles`.entity_name != '{entity}' and `tabVehicles`.attached_entity = '{entity}'))
                    and `tabVehicles`.vehicle_status  in ("صالحة", "عاطلة", "تحت التخريد")
                """.format(
                    entity=self.entity
                ),
                as_dict=1,
            )
            valid_vehicle_list = frappe.db.sql(
                """ Select count(`tabVehicles`.name) as total_count 
                    from `tabVehicles` 
                    JOIN `tabFuel Voucher` on `tabVehicles`.fuel_voucher = `tabFuel Voucher`.name

                    Where  `tabFuel Voucher`.fuel_type in (Select distinct `tabFuel Voucher`.fuel_type as fuel_type 
                            from `tabVehicles`
                            JOIN `tabFuel Voucher` on `tabVehicles`.fuel_voucher = `tabFuel Voucher`.name
                            where `tabVehicles`.vehicle_type != "لانش"
                            and `tabVehicles`.fuel_type != "بدون وقود") 
                    and ((`tabVehicles`.entity_name = '{entity}' and (`tabVehicles`.attached_entity is null or `tabVehicles`.attached_entity = ""))
                    or (`tabVehicles`.entity_name != '{entity}' and `tabVehicles`.attached_entity = '{entity}'))
                    and `tabVehicles`.vehicle_status  = "صالحة"
                    and `tabVehicles`.exchange_allowance not in ("لوحة فقط", "لوحة وخدمة كاملة فقط")

                """.format(
                    entity=self.entity,
                    from_date=self.from_date,
                    to_date=self.to_date,
                    issue_type=self.issue_type,
                ),
                as_dict=1,
            )
            invalid_vehicle_list = frappe.db.sql(
                """ Select count(`tabVehicles`.name) as total_count 
                    from `tabVehicles` 
                    JOIN `tabFuel Voucher` on `tabVehicles`.fuel_voucher = `tabFuel Voucher`.name
                    Where  `tabFuel Voucher`.fuel_type in (Select distinct `tabFuel Voucher`.fuel_type as fuel_type 
                            from `tabVehicles`
                            JOIN `tabFuel Voucher` on `tabVehicles`.fuel_voucher = `tabFuel Voucher`.name
                            where `tabVehicles`.vehicle_type != "لانش"
                            and `tabVehicles`.fuel_type != "بدون وقود")
                    and ((`tabVehicles`.entity_name = '{entity}' and (`tabVehicles`.attached_entity is null or `tabVehicles`.attached_entity = ""))
                    or (`tabVehicles`.entity_name != '{entity}' and `tabVehicles`.attached_entity = '{entity}'))
                    and `tabVehicles`.vehicle_status  in ("عاطلة", "تحت التخريد")
                    and `tabVehicles`.exchange_allowance not in ("لوحة فقط", "لوحة وخدمة كاملة فقط")
                """.format(
                    entity=self.entity,
                ),
                as_dict=1,
            )
            plate_only_vehicle_list = frappe.db.sql(
                """ Select count(`tabVehicles`.name) as plate_count
                                        from `tabVehicles` 
                                        JOIN `tabFuel Voucher` on `tabVehicles`.fuel_voucher = `tabFuel Voucher`.name
                                        Where `tabFuel Voucher`.fuel_type in 
                                        (Select distinct `tabFuel Voucher`.fuel_type as fuel_type 
                                        from `tabVehicles`
                                        JOIN `tabFuel Voucher` on `tabVehicles`.fuel_voucher = `tabFuel Voucher`.name
                                        where `tabVehicles`.vehicle_type != "لانش"
                                        and `tabVehicles`.fuel_type != "بدون وقود")
                                        and `tabVehicles`.vehicle_status in ("صالحة","عاطلة","تحت التخريد")
                                        and ((`tabVehicles`.entity_name = '{entity}' and (`tabVehicles`.attached_entity is null or `tabVehicles`.attached_entity = ""))
                                        or (`tabVehicles`.entity_name != '{entity}' and `tabVehicles`.attached_entity = '{entity}'))
                                        and `tabVehicles`.exchange_allowance in ("لوحة فقط", "لوحة وخدمة كاملة فقط")
                                        """.format(
                    entity=self.entity,
                ),
                as_dict=1,
            )
            total_vehicle_list_2 = frappe.db.sql(
                """ Select count(`tabBoats`.name) as total_count 
                                        from `tabBoats`
                                        JOIN `tabFuel Voucher` on `tabBoats`.fuel_voucher = `tabFuel Voucher`.name
                                    Where  `tabFuel Voucher`.fuel_type in (Select distinct `tabFuel Voucher`.fuel_type as fuel_type 
                                            from `tabBoats`
                                            JOIN `tabFuel Voucher` on `tabBoats`.fuel_voucher = `tabFuel Voucher`.name
                                            where `tabBoats`.fuel_type != "بدون وقود")
                                        and `tabBoats`.fuel_type != "بدون وقود"
                                        and `tabBoats`.boat_validity  in ("صالحة", "عاطلة", "تحت التخريد")
                                        and `tabBoats`.entity_name = '{entity}'
                                    """.format(
                    entity=self.entity,
                ),
                as_dict=1,
            )

            valid_vehicle_list_2 = frappe.db.sql(
                """ Select count(`tabBoats`.name) as valid_count,
                                        `tabBoats`.name as vehicle,
                                        `tabBoats`.boat_no as vehicle_no,
                                        `tabBoats`.entity_name as entity_name
                                        from `tabBoats`
                                        JOIN `tabFuel Voucher` on `tabBoats`.fuel_voucher = `tabFuel Voucher`.name
                                        Where  `tabFuel Voucher`.fuel_type in (Select distinct `tabFuel Voucher`.fuel_type as fuel_type 
                                            from `tabBoats`
                                            JOIN `tabFuel Voucher` on `tabBoats`.fuel_voucher = `tabFuel Voucher`.name
                                            where `tabBoats`.fuel_type != "بدون وقود")

                                        and `tabBoats`.entity_name = '{entity}'
                                        and `tabBoats`.boat_validity = "صالحة"
                                        and `tabBoats`.fuel_type != "بدون وقود"

                                    """.format(
                    entity=self.entity,
                    from_date=self.from_date,
                    to_date=self.to_date,
                    issue_type=self.issue_type,
                ),
                as_dict=1,
            )

            totals = []
            for row in total_vehicle_list:
                totals.append(row.total_count + total_vehicle_list_2[0].total_count)
            for row in valid_vehicle_list:
                totals.append(row.total_count + valid_vehicle_list_2[0].valid_count)
            for row in invalid_vehicle_list:
                totals.append(
                    row.total_count
                    + (
                        total_vehicle_list_2[0].total_count
                        - valid_vehicle_list_2[0].valid_count
                    )
                )
            for row in plate_only_vehicle_list:
                totals.append(row.plate_count)

            return totals
        elif self.issue_type == "زيت":
            total_oil_vehicle_list = frappe.db.sql(
                """ Select count(`tabVehicles`.name) as valid_count from `tabVehicles` 
                                        Where `tabVehicles`.oil_type in (
                                        Select distinct `tabVehicles`.oil_type as oil_type 
                                        from `tabVehicles`
                                        JOIN `tabOil Type` ON `tabOil Type`.name = `tabVehicles`.oil_type
                                        where `tabVehicles`.vehicle_type != "لانش"
                                        and `tabVehicles`.oil_count != 0
                                        AND `tabOil Type`.enabled =1
                                        )
                                        and ((`tabVehicles`.entity_name = '{entity}' and (`tabVehicles`.attached_entity is null or `tabVehicles`.attached_entity = ""))
                                        or (`tabVehicles`.entity_name != '{entity}' and `tabVehicles`.attached_entity = '{entity}'))
                                        and `tabVehicles`.vehicle_status in ("صالحة", "عاطلة", "تحت التخريد")

                                    """.format(
                    entity=self.entity,
                ),
                as_dict=1,
            )

            valid_oil_vehicle_list = frappe.db.sql(
                """ Select count(`tabVehicles`.name) as valid_count
                                            from `tabVehicles` 
                                            Where `tabVehicles`.oil_type in (
                                            Select distinct `tabVehicles`.oil_type as oil_type 
                                            from `tabVehicles`
                                            JOIN `tabOil Type` ON `tabOil Type`.name = `tabVehicles`.oil_type
                                            where `tabVehicles`.vehicle_type != "لانش"
                                            and `tabVehicles`.oil_count != 0
                                            AND `tabOil Type`.enabled =1
                                            )
                                            and `tabVehicles`.vehicle_status = "صالحة"
                                            and ((`tabVehicles`.entity_name = '{entity}' and (`tabVehicles`.attached_entity is null or `tabVehicles`.attached_entity = ""))
                                            or (`tabVehicles`.entity_name != '{entity}' and `tabVehicles`.attached_entity = '{entity}'))
                                            and `tabVehicles`.exchange_allowance not in ("لوحة فقط", "لوحة وخدمة كاملة فقط")

                                        """.format(
                    entity=self.entity,
                    from_date=self.from_date,
                    to_date=self.to_date,
                    issue_type=self.issue_type,
                ),
                as_dict=1,
            )
            invalid_oil_vehicle_list = frappe.db.sql(
                """ Select count(`tabVehicles`.name) as valid_count
                                        from `tabVehicles` 
                                        Where `tabVehicles`.oil_type in (
                                            Select 
                                            distinct `tabVehicles`.oil_type as oil_type 
                                            from `tabVehicles`
                                            JOIN `tabOil Type` ON `tabOil Type`.name = `tabVehicles`.oil_type
                                            where `tabVehicles`.vehicle_type != "لانش"
                                            and `tabVehicles`.oil_count != 0
                                            AND `tabOil Type`.enabled =1
                                            )
                                        and ((`tabVehicles`.entity_name = '{entity}' and (`tabVehicles`.attached_entity is null or `tabVehicles`.attached_entity = ""))
                                        or (`tabVehicles`.entity_name != '{entity}' and `tabVehicles`.attached_entity = '{entity}'))

                                        and `tabVehicles`.vehicle_status  in ("عاطلة", "تحت التخريد")
                                        and `tabVehicles`.exchange_allowance not in ("لوحة فقط", "لوحة وخدمة كاملة فقط")
                                    """.format(
                    entity=self.entity,
                    from_date=self.from_date,
                    to_date=self.to_date,
                    issue_type=self.issue_type,
                ),
                as_dict=1,
            )
            plate_only_vehicle_list = frappe.db.sql(
                """ Select count(`tabVehicles`.name) as valid_count
                                        from `tabVehicles` 
                                        Where `tabVehicles`.oil_type in (
                                            Select 
                                            distinct `tabVehicles`.oil_type as oil_type 
                                            from `tabVehicles`
                                            JOIN `tabOil Type` ON `tabOil Type`.name = `tabVehicles`.oil_type
                                            where `tabVehicles`.vehicle_type != "لانش"
                                            and `tabVehicles`.oil_count != 0
                                            AND `tabOil Type`.enabled =1
                                            )
                                        and ((`tabVehicles`.entity_name = '{entity}' and (`tabVehicles`.attached_entity is null or `tabVehicles`.attached_entity = ""))
                                        or (`tabVehicles`.entity_name != '{entity}' and `tabVehicles`.attached_entity = '{entity}'))
                                        and `tabVehicles`.exchange_allowance in ("لوحة فقط", "لوحة وخدمة كاملة فقط")
                                        and `tabVehicles`.vehicle_status in ("صالحة","عاطلة","تحت التخريد")
                                    """.format(
                    entity=self.entity,
                    from_date=self.from_date,
                    to_date=self.to_date,
                ),
                as_dict=1,
            )
            totals = []
            for row in total_oil_vehicle_list:
                totals.append(row.valid_count)
            for row in valid_oil_vehicle_list:
                totals.append(row.valid_count)
            for row in invalid_oil_vehicle_list:
                totals.append(row.valid_count)
            for row in plate_only_vehicle_list:
                totals.append(row.valid_count)

            return totals
        elif self.issue_type == "غسيل":
            total_oil_vehicle_list = frappe.db.sql(
                """ Select count(`tabVehicles`.name) as valid_count from `tabVehicles` 
                                        Where `tabVehicles`.washing_voucher in (
                                        Select distinct `tabVehicles`.washing_voucher as washing_voucher 
                                        from `tabVehicles`
                                        JOIN `tabWashing Vouchers` ON `tabWashing Vouchers`.name = `tabVehicles`.washing_voucher
                                        where `tabVehicles`.vehicle_type != "لانش"
                                        and `tabVehicles`.washing_count > 0
                                        )
                                        
                                        and ((`tabVehicles`.entity_name = '{entity}' and (`tabVehicles`.attached_entity is null or `tabVehicles`.attached_entity = ""))
                                        or (`tabVehicles`.entity_name != '{entity}' and `tabVehicles`.attached_entity = '{entity}'))
                                        and `tabVehicles`.vehicle_status in ("صالحة", "عاطلة", "تحت التخريد")

                                    """.format(
                    entity=self.entity,
                ),
                as_dict=1,
            )

            valid_oil_vehicle_list = frappe.db.sql(
                """ Select count(`tabVehicles`.name) as valid_count
                                            from `tabVehicles` 
                                            Where `tabVehicles`.washing_voucher in (
                                            Select distinct `tabVehicles`.washing_voucher as washing_voucher 
                                            from `tabVehicles`
                                            JOIN `tabWashing Vouchers` ON `tabWashing Vouchers`.name = `tabVehicles`.washing_voucher
                                            where `tabVehicles`.vehicle_type != "لانش"
                                            and `tabVehicles`.washing_count > 0
                                            )
                                            and `tabVehicles`.vehicle_status = "صالحة"
                                            and ((`tabVehicles`.entity_name = '{entity}' and (`tabVehicles`.attached_entity is null or `tabVehicles`.attached_entity = ""))
                                            or (`tabVehicles`.entity_name != '{entity}' and `tabVehicles`.attached_entity = '{entity}'))
                                            and `tabVehicles`.exchange_allowance not in ("لوحة فقط", "لوحة وخدمة كاملة فقط")

                                        """.format(
                    entity=self.entity,
                    from_date=self.from_date,
                    to_date=self.to_date,
                    issue_type=self.issue_type,
                ),
                as_dict=1,
            )
            invalid_oil_vehicle_list = frappe.db.sql(
                """ Select count(`tabVehicles`.name) as valid_count
                                        from `tabVehicles` 
                                        Where `tabVehicles`.washing_voucher in (
                                        Select distinct `tabVehicles`.washing_voucher as washing_voucher 
                                        from `tabVehicles`
                                        JOIN `tabWashing Vouchers` ON `tabWashing Vouchers`.name = `tabVehicles`.washing_voucher
                                        where `tabVehicles`.vehicle_type != "لانش"
                                        and `tabVehicles`.washing_count > 0
                                        )
                                        and ((`tabVehicles`.entity_name = '{entity}' and (`tabVehicles`.attached_entity is null or `tabVehicles`.attached_entity = ""))
                                        or (`tabVehicles`.entity_name != '{entity}' and `tabVehicles`.attached_entity = '{entity}'))

                                        and `tabVehicles`.vehicle_status  in ("عاطلة", "تحت التخريد")
                                        and `tabVehicles`.exchange_allowance not in ("لوحة فقط", "لوحة وخدمة كاملة فقط")
                                    """.format(
                    entity=self.entity,
                    from_date=self.from_date,
                    to_date=self.to_date,
                    issue_type=self.issue_type,
                ),
                as_dict=1,
            )
            plate_only_vehicle_list = frappe.db.sql(
                """ Select count(`tabVehicles`.name) as valid_count
                                        from `tabVehicles` 
                                        Where `tabVehicles`.washing_voucher in (
                                        Select distinct `tabVehicles`.washing_voucher as washing_voucher 
                                        from `tabVehicles`
                                        JOIN `tabWashing Vouchers` ON `tabWashing Vouchers`.name = `tabVehicles`.washing_voucher
                                        where `tabVehicles`.vehicle_type != "لانش"
                                        and `tabVehicles`.washing_count > 0
                                        )
                                        and ((`tabVehicles`.entity_name = '{entity}' and (`tabVehicles`.attached_entity is null or `tabVehicles`.attached_entity = ""))
                                        or (`tabVehicles`.entity_name != '{entity}' and `tabVehicles`.attached_entity = '{entity}'))
                                        and `tabVehicles`.exchange_allowance in ("لوحة فقط", "لوحة وخدمة كاملة فقط")
                                        and `tabVehicles`.vehicle_status in ("صالحة","عاطلة","تحت التخريد")
                                    """.format(
                    entity=self.entity,
                    from_date=self.from_date,
                    to_date=self.to_date,
                ),
                as_dict=1,
            )
            totals = []
            for row in total_oil_vehicle_list:
                totals.append(row.valid_count)
            for row in valid_oil_vehicle_list:
                totals.append(row.valid_count)
            for row in invalid_oil_vehicle_list:
                totals.append(row.valid_count)
            for row in plate_only_vehicle_list:
                totals.append(row.valid_count)

            return totals

    def get_vehicles_count(self, fuel_type):
        summition = 0
        if fuel_type == "غاز طبيعي":
            for row in self.gas_per_vehicle_type_table:
                summition += row.valid_count
            return summition
        if self.issue_to == "جهة":
            for row in self.liquid_per_vehicle_type_table:
                if row.fuel_type == fuel_type:
                    summition += row.valid_count
        else:
            for row in self.specified_vehicles_issuing_table:
                if row.liquid == fuel_type:
                    summition += 1
        return summition

    @frappe.whitelist()
    def get_searched_vehicles(self):
        if frappe.db.exists("Vehicles", {"vehicle_no": self.vehicle_no}):
            if frappe.db.exists(
                "Vehicles",
                {
                    "vehicle_no": self.vehicle_no,
                    "entity_name": self.entity,
                    "vehicle_status": "صالحة",
                },
            ):
                vic = frappe.get_doc(
                    "Vehicles",
                    {
                        "vehicle_no": self.vehicle_no,
                        "entity_name": self.entity,
                        "vehicle_status": "صالحة",
                    },
                )
                vehicle = self.append("specified_vehicles_issuing_table", {})
                vehicle.vehicle_boat = "Vehicles"
                vehicle.vehicle = vic.name
                vehicle.vehicle_no = vic.vehicle_no or vic.police_id
                vehicle.vehicle_type = vic.vehicle_type
                vehicle.entity_name = vic.entity_name
            else:
                vic = frappe.get_doc("Vehicles", {"vehicle_no": self.vehicle_no})
                if vic.entity_name != self.entity:
                    frappe.msgprint(
                        "المركبة رقم {vehicle_no} تابعة لجهة {entity_name}".format(
                            vehicle_no=vic.vehicle_no, entity_name=vic.entity_name
                        )
                    )
                elif vic.vehicle_status != "صالحة":
                    frappe.msgprint(
                        "المركبة رقم {vehicle_no} حالتها {vehicle_status}".format(
                            vehicle_no=vic.vehicle_no, vehicle_status=vic.vehicle_status
                        )
                    )

        elif frappe.db.exists("Boats", {"boat_no": self.vehicle_no}):
            vic = frappe.get_doc("Boats", {"boat_no": self.vehicle_no})
            if vic.entity_name != self.entity:
                frappe.throw(
                    "المركبة رقم {boat_no} تابعة لجهة {entity_name}".format(
                        boat_no=vic.boat_no, entity_name=vic.entity_name
                    )
                )
            elif vic.boat_validity != "صالحة":
                frappe.throw(
                    "المركبة رقم {boat_no} حالتها {boat_validity}".format(
                        boat_no=vic.boat_no, boat_validity=vic.boat_validity
                    )
                )
            vic = frappe.get_doc("Boats", {"boat_no": self.vehicle_no})
            vehicle = self.append("specified_vehicles_issuing_table", {})
            vehicle.vehicle_boat = "Boats"
            vehicle.vehicle = vic.name
            vehicle.vehicle_no = vic.boat_no
            vehicle.vehicle_type = "لانش"
            vehicle.entity_name = vic.entity_name
        else:
            vehicle_no = self.vehicle_no

            frappe.msgprint(
                "لا يوجد مركبة برقم {vehicle_no}".format(vehicle_no=vehicle_no)
            )

    @frappe.whitelist()
    def post_liquid_issuing(self):
        if self.issue_to == "جهة":
            issue_list = frappe.db.get_list(
                "Liquids Issuing",
                filters={
                    "submitted": ["=", 1],
                    "issue_to": ["=", self.issue_to],
                    "entity": ["=", self.entity],
                    "issue_type": ["=", self.issue_type],
                    "name": ["!=", self.name],
                },
                fields=["from_date", "to_date"],
            )

            for m in issue_list:
                if getdate(self.from_date) >= getdate(m.from_date) and getdate(
                    self.from_date
                ) <= getdate(m.to_date):
                    frappe.throw(
                        " لا يمكن صرف "
                        + self.issue_type
                        + " إلى "
                        + self.entity
                        + " حيث أنه تم الصرف من قبل خلال الفترة المحددة "
                    )
                if getdate(self.to_date) >= getdate(m.from_date) and getdate(
                    self.to_date
                ) <= getdate(m.to_date):
                    frappe.throw(
                        " لا يمكن صرف "
                        + self.issue_type
                        + " إلى "
                        + self.entity
                        + " حيث أنه تم الصرف من قبل خلال الفترة المحددة "
                    )

            current_vehicles = []
            valid_vehicle_list = []
            if self.issue_type == "وقود":
                valid_vehicle_list = frappe.db.sql(
                    """ Select `tabBoats`.name as vehicle,
                            "Boats" as vehicle_boat,
                            `tabBoats`.boat_no as boat_no,
                            `tabBoats`.entity_name as entity_name,
                            `tabBoats`.qty as qty
                            from `tabBoats` 
                            Where `tabBoats`.boat_validity = "صالحة"
                            and `tabBoats`.entity_name = '{entity}'
                            and `tabBoats`.fuel_type != "بدون وقود"
                            and `tabBoats`.name not in (select `tabLiquids Issuing Table`.parent 
                            from `tabLiquids Issuing Table`
                            where `tabLiquids Issuing Table`.issue_type = '{issue_type}'
                            and `tabLiquids Issuing Table`.from_date >= '{from_date}'
                            and `tabLiquids Issuing Table`.to_date <= '{to_date}')
                        """.format(
                        entity=self.entity,
                        from_date=self.from_date,
                        to_date=self.to_date,
                        issue_type=self.issue_type,
                    ),
                    as_dict=1,
                )

                valid_vehicle_list_2 = frappe.db.sql(
                    """ Select `tabVehicles`.name as vehicle,
                            "Vehicles" as vehicle_boat,
                            `tabVehicles`.vehicle_no as vehicle_no,
                            `tabVehicles`.vehicle_type as vehicle_type,
                            `tabVehicles`.entity_name as entity_name,
                            `tabVehicles`.fuel_voucher as fuel_voucher,
                            `tabVehicles`.litre_count as qty
                            from `tabVehicles` 
                            Where `tabVehicles`.vehicle_status = "صالحة"
                            and ((`tabVehicles`.entity_name = '{entity}' and (`tabVehicles`.attached_entity is null or `tabVehicles`.attached_entity = ""))
                            or (`tabVehicles`.entity_name != '{entity}' and `tabVehicles`.attached_entity = '{entity}'))
                            and `tabVehicles`.exchange_allowance not in ("لوحة فقط", "لوحة وخدمة كاملة فقط")
                            and `tabVehicles`.litre_count > 0
                            and `tabVehicles`.name not in (select `tabLiquids Issuing Table`.parent 
                                from `tabLiquids Issuing Table`
                                where `tabLiquids Issuing Table`.issue_type = '{issue_type}'
                                and `tabLiquids Issuing Table`.from_date >= '{from_date}' 
                                and `tabLiquids Issuing Table`.to_date <= '{to_date}')
                        """.format(
                        entity=self.entity,
                        from_date=self.from_date,
                        to_date=self.to_date,
                        issue_type=self.issue_type,
                    ),
                    as_dict=1,
                )
                valid_vehicle_list.extend(valid_vehicle_list_2)
            elif self.issue_type == "زيت":
                valid_vehicle_list = frappe.db.sql(
                    """ Select `tabVehicles`.name as vehicle,
                        "Vehicles" as vehicle_boat,
                        `tabVehicles`.vehicle_no as vehicle_no,
                        `tabVehicles`.vehicle_type as vehicle_type,
                        `tabVehicles`.entity_name as entity_name,
                        `tabVehicles`.oil_count as qty
                        from `tabVehicles` 
                        Where `tabVehicles`.vehicle_status = "صالحة"
                        and ((`tabVehicles`.entity_name = '{entity}' and (`tabVehicles`.attached_entity is null or `tabVehicles`.attached_entity = ""))
                        or (`tabVehicles`.entity_name != '{entity}' and `tabVehicles`.attached_entity = '{entity}'))
                        and `tabVehicles`.exchange_allowance not in ("لوحة فقط", "لوحة وخدمة كاملة فقط")
                        and `tabVehicles`.vehicle_type != "لانش"
                        and `tabVehicles`.name not in (select `tabLiquids Issuing Table`.parent 
                            from `tabLiquids Issuing Table`
                            where `tabLiquids Issuing Table`.issue_type = '{issue_type}'
                            and `tabLiquids Issuing Table`.from_date >= '{from_date}' 
                            and `tabLiquids Issuing Table`.to_date <= '{to_date}')
                    """.format(
                        entity=self.entity,
                        from_date=self.from_date,
                        to_date=self.to_date,
                        issue_type=self.issue_type,
                    ),
                    as_dict=1,
                )
            elif self.issue_type == "غسيل":
                valid_vehicle_list = frappe.db.sql(
                    """ Select `tabVehicles`.name as vehicle,
                        "Vehicles" as vehicle_boat,
                        `tabVehicles`.vehicle_no as vehicle_no,
                        `tabVehicles`.vehicle_type as vehicle_type,
                        `tabVehicles`.entity_name as entity_name,
                        `tabVehicles`.washing_voucher as washing_voucher,
                        `tabVehicles`.washing_count as qty
                        from `tabVehicles` 
                        Where `tabVehicles`.vehicle_status = "صالحة"
                        and `tabVehicles`.entity_name = '{entity}'
                        and `tabVehicles`.exchange_allowance not in ("لوحة فقط", "لوحة وخدمة كاملة فقط")
                        and `tabVehicles`.name not in (select `tabLiquids Issuing Table`.parent 
                            from `tabLiquids Issuing Table`
                            where `tabLiquids Issuing Table`.issue_type = '{issue_type}'
                            and `tabLiquids Issuing Table`.from_date >= '{from_date}' 
                            and `tabLiquids Issuing Table`.to_date <= '{to_date}')
                    """.format(
                        entity=self.entity,
                        from_date=self.from_date,
                        to_date=self.to_date,
                        issue_type=self.issue_type,
                    ),
                    as_dict=1,
                )

            for t in valid_vehicle_list:
                current_vehicles.append(t.vehicle)
                vehicle_status = frappe.db.get_value(
                    "Vehicles", t.vehicle, "vehicle_status"
                )
                boat_status = frappe.db.get_value("Boats", t.vehicle, "boat_validity")
                voucher = ""
                voucher1 = ""

                if self.issue_type == "وقود":
                    voucher = (
                        frappe.db.get_value("Vehicles", t.vehicle, "fuel_voucher")
                        if frappe.db.get_value("Vehicles", t.vehicle, "fuel_voucher")
                        else "لا يوجد"
                    )
                    voucher1 = (
                        frappe.db.get_value("Boats", t.vehicle, "fuel_voucher")
                        if frappe.db.get_value("Boats", t.vehicle, "fuel_voucher")
                        else "لا يوجد"
                    )
                if self.issue_type == "زيت":
                    voucher = (
                        frappe.db.get_value("Vehicles", t.vehicle, "oil_type")
                        if frappe.db.get_value("Vehicles", t.vehicle, "oil_type")
                        else "لا يوجد"
                    )
                    voucher1 = "لا يوجد"
                if self.issue_type == "غاز":
                    voucher = "غاز طبيعي فئة 15 متر مكعب"
                    voucher1 = "لا يوجد"
                if self.issue_type == "غسيل":
                    voucher = (
                        frappe.db.get_value("Vehicles", t.vehicle, "washing_voucher")
                        if frappe.db.get_value("Vehicles", t.vehicle, "washing_voucher")
                        else "لا يوجد"
                    )
                    voucher1 = "لا يوجد"

                record_name = 1
                max_id = frappe.db.sql(
                    """
                    SELECT MAX(name) as max_name
                    FROM `tabLiquids Issuing Table`
                    """,
                    as_dict=1,
                )
                if frappe.db.exists("Liquids Issuing Table", 1):
                    record_name = int(max_id[0]["max_name"]) + 1

                if t.vehicle_boat == "Vehicles":
                    frappe.db.sql(
                        """ INSERT INTO `tabLiquids Issuing Table`
                                            (issue_date, issue_type, vehicle_status, voucher, from_date, to_date, entity, qty, created_by, issue_no, parent, parentfield, parenttype, name)
                                    VALUES ('{issue_date}', '{issue_type}', '{vehicle_status}', '{voucher}' ,'{from_date}', '{to_date}', '{entity}', '{qty}', '{created_by}', '{issue_no}','{parent}', '{parentfield}', '{parenttype}', '{record_name}')
                                  """.format(
                            issue_date=self.issue_date,
                            issue_type=self.issue_type,
                            vehicle_status=vehicle_status,
                            from_date=self.from_date,
                            voucher=voucher,
                            to_date=self.to_date,
                            entity=self.entity,
                            qty=t.qty,
                            created_by=frappe.session.user,
                            issue_no=self.name,
                            parenttype=t.vehicle_boat,
                            parent=t.vehicle,
                            parentfield="liquid_table",
                            record_name=record_name,
                        )
                    )

                if t.vehicle_boat == "Boats":
                    frappe.db.sql(
                        """ INSERT INTO `tabLiquids Issuing Table`
                                            (issue_date, issue_type, vehicle_status, voucher, from_date, to_date, entity, qty, created_by, issue_no, parent, parentfield, parenttype, name)
                                    VALUES ('{issue_date}', '{issue_type}', '{vehicle_status}', '{voucher}' ,'{from_date}', '{to_date}', '{entity}', '{qty}', '{created_by}', '{issue_no}','{parent}', '{parentfield}', '{parenttype}', '{record_name}')
                                  """.format(
                            issue_date=self.issue_date,
                            issue_type=self.issue_type,
                            vehicle_status=boat_status,
                            from_date=self.from_date,
                            voucher=voucher1,
                            to_date=self.to_date,
                            entity=frappe.db.get_value(
                                "Boats", t.vehicle, ["entity_name"]
                            ),
                            qty=t.qty,
                            created_by=frappe.session.user,
                            issue_no=self.name,
                            parenttype=t.vehicle_boat,
                            parent=t.vehicle,
                            parentfield="liquid_table",
                            record_name=record_name,
                        )
                    )

            if len(current_vehicles) == 1:
                current_vehicles.append("None")
            if not current_vehicles:
                frappe.msgprint("لا يوجد مركبات تستحق الصرف")
            not_in_vehicle_table = frappe.db.sql(
                """
                select name, vehicle_status
                from `tabVehicles` 
                where  ((`tabVehicles`.entity_name = '{entity}' and (`tabVehicles`.attached_entity is null or `tabVehicles`.attached_entity = ""))
                or (`tabVehicles`.entity_name != '{entity}' and `tabVehicles`.attached_entity = '{entity}'))
                and name not in {current_vehicles}
                and `tabVehicles`.vehicle_status in ("عاطلة","تحت التخريد")
            """.format(
                    entity=self.entity, current_vehicles=tuple(current_vehicles)
                ),
                as_dict=1,
            )
            not_in_boat_table = frappe.db.sql(
                """
                            select name, boat_validity
                            from `tabBoats` 
                            where entity_name = '{cur_entity}'
                            and name not in {current_vehicles}
                            and boat_validity in ("عاطلة","تحت التخريد")

                        """.format(
                    cur_entity=self.entity, current_vehicles=tuple(current_vehicles)
                ),
                as_dict=1,
            )

            for z in not_in_vehicle_table:
                record_name = 1
                max_id = frappe.db.sql(
                    """
                    SELECT MAX(name) as max_name
                    FROM `tabLiquids Issuing Table`
                    """,
                    as_dict=1,
                )
                if frappe.db.exists("Liquids Issuing Table", 1):
                    record_name = int(max_id[0]["max_name"]) + 1
                voucher = ""
                if self.issue_type == "وقود":
                    voucher = (
                        frappe.db.get_value("Vehicles", z.name, "fuel_voucher")
                        if frappe.db.get_value("Vehicles", z.name, "fuel_voucher")
                        else "لا يوجد"
                    )
                if self.issue_type == "زيت":
                    voucher = (
                        frappe.db.get_value("Vehicles", z.name, "oil_type")
                        if frappe.db.get_value("Vehicles", z.name, "oil_type")
                        else "لا يوجد"
                    )
                if self.issue_type == "غاز":
                    voucher = "غاز طبيعي فئة 15 متر مكعب"
                if self.issue_type == "غسيل":
                    voucher = (
                        frappe.db.get_value("Vehicles", z.name, "washing_voucher")
                        if frappe.db.get_value("Vehicles", z.name, "washing_voucher")
                        else "لا يوجد"
                    )

                frappe.db.sql(
                    """ INSERT INTO `tabLiquids Issuing Table`
                                                        (issue_date, issue_type, vehicle_status, voucher, from_date, to_date, entity, qty, created_by, issue_no, parent, parentfield, parenttype, name)
                                                VALUES ('{issue_date}', '{issue_type}', '{vehicle_status}', '{voucher}' ,'{from_date}', '{to_date}', '{entity}', '{qty}', '{created_by}', '{issue_no}','{parent}', '{parentfield}', '{parenttype}', '{record_name}')
                                              """.format(
                        issue_date=self.issue_date,
                        issue_type=self.issue_type,
                        vehicle_status="عاطلة",
                        from_date=self.from_date,
                        voucher=voucher,
                        to_date=self.to_date,
                        entity=self.entity,
                        qty=0,
                        created_by=frappe.session.user,
                        issue_no=self.name,
                        parenttype="Vehicles",
                        parent=z.name,
                        parentfield="liquid_table",
                        record_name=record_name,
                    )
                )

            for w in not_in_boat_table:
                record_name = 1
                max_id = frappe.db.sql(
                    """
                    SELECT MAX(name) as max_name
                    FROM `tabLiquids Issuing Table`
                    """,
                    as_dict=1,
                )
                if frappe.db.exists("Liquids Issuing Table", 1):
                    record_name = int(max_id[0]["max_name"]) + 1
                voucher = ""
                if self.issue_type == "وقود":
                    voucher = (
                        frappe.db.get_value("Boats", w.name, "fuel_voucher")
                        if frappe.db.get_value("Boats", w.name, "fuel_voucher")
                        else "لا يوجد"
                    )
                if self.issue_type == "زيت":
                    voucher = "لا يوجد"
                if self.issue_type == "غاز":
                    voucher = "لا يوجد"
                if self.issue_type == "غسيل":
                    voucher = "لا يوجد"

                frappe.db.sql(
                    """ INSERT INTO `tabLiquids Issuing Table`
                                                        (issue_date, issue_type, vehicle_status, voucher, from_date, to_date, entity, qty, created_by, issue_no, parent, parentfield, parenttype, name)
                                                VALUES ('{issue_date}', '{issue_type}', '{vehicle_status}', '{voucher}' ,'{from_date}', '{to_date}', '{entity}', '{qty}', '{created_by}', '{issue_no}','{parent}', '{parentfield}', '{parenttype}', '{record_name}')
                                              """.format(
                        issue_date=self.issue_date,
                        issue_type=self.issue_type,
                        vehicle_status="عاطلة",
                        from_date=self.from_date,
                        voucher=voucher,
                        to_date=self.to_date,
                        entity=self.entity,
                        qty=0,
                        created_by=frappe.session.user,
                        issue_no=self.name,
                        parenttype="Boats",
                        parent=w.name,
                        parentfield="liquid_table",
                        record_name=record_name,
                    )
                )

            if self.gas_per_vehicle_type_table:
                gas_valid_vehicle_list = frappe.db.sql(
                    """ Select count(`tabVehicles`.name) as valid_count,
                                        `tabVehicles`.name as vehicle,
                                        `tabVehicles`.vehicle_no as vehicle_no,
                                        `tabVehicles`.vehicle_type as vehicle_type,
                                        `tabVehicles`.entity_name as entity_name,
                                        `tabVehicles`.gas_count as qty
                                        from `tabVehicles` 
                                        where `tabVehicles`.vehicle_status = "صالحة"
                                        and ((`tabVehicles`.entity_name = '{entity}' and (`tabVehicles`.attached_entity is null or `tabVehicles`.attached_entity = ""))
                                        or (`tabVehicles`.entity_name != '{entity}' and `tabVehicles`.attached_entity = '{entity}'))
                                        and `tabVehicles`.exchange_allowance not in ("لوحة فقط", "لوحة وخدمة كاملة فقط")
                                        and `tabVehicles`.vehicle_type != "لانش"
                                        and `tabVehicles`.gas_count != 0
                                        and `tabVehicles`.name not in (select `tabLiquids Issuing Table`.parent 
                                            from `tabLiquids Issuing Table`
                                            where `tabLiquids Issuing Table`.issue_type = '{issue_type}'
                                            and `tabLiquids Issuing Table`.from_date >= '{from_date}'
                                            and `tabLiquids Issuing Table`.to_date <= '{to_date}')
                                    """.format(
                        entity=self.entity,
                        from_date=self.from_date,
                        to_date=self.to_date,
                        issue_type="غاز",
                    ),
                    as_dict=1,
                )
                current_vehicles = []
                for t in gas_valid_vehicle_list:
                    current_vehicles.append(str(t.vehicle))
                    vehicle_status = frappe.db.get_value(
                        "Vehicles", t.vehicle, "vehicle_status"
                    )
                    voucher = ""
                    voucher1 = ""
                    record_name = 1
                    max_id = frappe.db.sql(
                        """
                        SELECT MAX(name) as max_name
                        FROM `tabLiquids Issuing Table`
                        """,
                        as_dict=1,
                    )
                    if frappe.db.exists("Liquids Issuing Table", 1):
                        record_name = int(max_id[0]["max_name"]) + 1
                    voucher = "غاز طبيعي فئة 15 متر مكعب"
                    voucher1 = "لا يوجد"
                    frappe.db.sql(
                        """ INSERT INTO `tabLiquids Issuing Table`
                                            (issue_date, issue_type, vehicle_status, voucher, from_date, to_date, entity, qty, created_by, issue_no, parent, parentfield, parenttype, name)
                                    VALUES ('{issue_date}', '{issue_type}', '{vehicle_status}', '{voucher}' ,'{from_date}', '{to_date}', '{entity}', '{qty}', '{created_by}', '{issue_no}','{parent}', '{parentfield}', '{parenttype}', '{record_name}')
                                    """.format(
                            issue_date=self.issue_date,
                            issue_type="غاز",
                            vehicle_status=vehicle_status,
                            from_date=self.from_date,
                            voucher=voucher,
                            to_date=self.to_date,
                            entity=self.entity,
                            qty=t.qty,
                            created_by=frappe.session.user,
                            issue_no=self.name,
                            parenttype="Vehicles",
                            parent=t.vehicle,
                            parentfield="liquid_table",
                            record_name=record_name,
                        )
                    )

                if len(current_vehicles) == 1:
                    current_vehicles.append("None")
                if not current_vehicles:
                    frappe.msgprint(str(current_vehicles))
                gas_total_vehicle_list = frappe.db.sql(
                    """ Select `tabVehicles`.name as name,
                                        `tabVehicles`.vehicle_status as vehicle_status
                                        from `tabVehicles` 
                                        where `tabVehicles`.vehicle_type != "لانش"
                                        and `tabVehicles`.gas_count != 0
                                        and ((`tabVehicles`.entity_name = '{entity}' and (`tabVehicles`.attached_entity is null or `tabVehicles`.attached_entity = ""))
                                        or (`tabVehicles`.entity_name != '{entity}' and `tabVehicles`.attached_entity = '{entity}'))
                                        and `tabVehicles`.vehicle_status in ("صالحة", "عاطلة", "تحت التخريد")
                                        and name not in {current_vehicles}
                                    """.format(
                        entity=self.entity,
                        current_vehicles=tuple(current_vehicles),
                    ),
                    as_dict=1,
                )

                for z in gas_total_vehicle_list:
                    record_name = 1
                    max_id = frappe.db.sql(
                        """
                        SELECT MAX(name) as max_name
                        FROM `tabLiquids Issuing Table`
                        """,
                        as_dict=1,
                    )
                    if frappe.db.exists("Liquids Issuing Table", 1):
                        record_name = int(max_id[0]["max_name"]) + 1
                    voucher = ""
                    if self.issue_type == "وقود":
                        voucher = (
                            frappe.db.get_value("Vehicles", z.name, "fuel_voucher")
                            if frappe.db.get_value("Vehicles", z.name, "fuel_voucher")
                            else "لا يوجد"
                        )
                    if self.issue_type == "زيت":
                        voucher = (
                            frappe.db.get_value("Vehicles", z.name, "oil_type")
                            if frappe.db.get_value("Vehicles", z.name, "oil_type")
                            else "لا يوجد"
                        )
                    if self.issue_type == "غاز":
                        voucher = "غاز طبيعي فئة 15 متر مكعب"
                    if self.issue_type == "غسيل":
                        voucher = (
                            frappe.db.get_value("Vehicles", z.name, "washing_voucher")
                            if frappe.db.get_value(
                                "Vehicles", z.name, "washing_voucher"
                            )
                            else "لا يوجد"
                        )
                    voucher = "غاز طبيعي فئة 15 متر مكعب"
                    frappe.db.sql(
                        """ INSERT INTO `tabLiquids Issuing Table`
                                                            (issue_date, issue_type, vehicle_status, voucher, from_date, to_date, entity, qty, created_by, issue_no, parent, parentfield, parenttype, name)
                                                    VALUES ('{issue_date}', '{issue_type}', '{vehicle_status}', '{voucher}' ,'{from_date}', '{to_date}', '{entity}', '{qty}', '{created_by}', '{issue_no}','{parent}', '{parentfield}', '{parenttype}', '{record_name}')
                                                """.format(
                            issue_date=self.issue_date,
                            issue_type="غاز",
                            vehicle_status="عاطلة",
                            from_date=self.from_date,
                            voucher=voucher,
                            to_date=self.to_date,
                            entity=self.entity,
                            qty=0,
                            created_by=frappe.session.user,
                            issue_no=self.name,
                            parenttype="Vehicles",
                            parent=z.name,
                            parentfield="liquid_table",
                            record_name=record_name,
                        )
                    )

        if self.issue_to == "مركبة أو مجموعة مركبات":
            for t in self.specified_vehicles_issuing_table:
                if t.vehicle_boat != "Boats":
                    if t.last_issue_from_date or t.last_issue_to_date:
                        if (
                            float(t.last_issue_qty) > 0
                            and getdate(t.last_issue_from_date)
                            >= getdate(self.from_date)
                            and getdate(t.last_issue_from_date) <= getdate(self.to_date)
                        ):
                            frappe.throw(
                                " الصف # "
                                + str(t.idx)
                                + " : لا يمكن صرف "
                                + self.issue_type
                                + " إلى المركبة "
                                + str(t.vehicle_no)
                                + " حيث أنه تم الصرف لها من قبل خلال الفترة المحددة إلى جهة "
                                + str(t.entity_name)
                            )

                        if (
                            float(t.last_issue_qty) > 0
                            and getdate(t.last_issue_to_date) >= getdate(self.from_date)
                            and getdate(t.last_issue_to_date) <= getdate(self.to_date)
                        ):
                            frappe.throw(
                                " الصف # "
                                + str(t.idx)
                                + " : لا يمكن صرف "
                                + self.issue_type
                                + " إلى المركبة "
                                + str(t.vehicle_no)
                                + " حيث أنه تم الصرف لها من قبل خلال الفترة المحددة إلى جهة "
                                + str(t.entity_name)
                            )

                    vehicle_status = frappe.db.get_value(
                        "Vehicles", t.vehicle, "vehicle_status"
                    )
                    voucher = ""

                    if self.issue_type == "وقود":
                        voucher = (
                            frappe.db.get_value("Vehicles", t.vehicle, "fuel_voucher")
                            if frappe.db.get_value(
                                "Vehicles", t.vehicle, "fuel_voucher"
                            )
                            else "لا يوجد"
                        )
                    if self.issue_type == "زيت":
                        voucher = frappe.db.get_value("Vehicles", t.vehicle, "oil_type")
                    if self.issue_type == "غاز":
                        voucher = "غاز طبيعي فئة 15 متر مكعب"
                    if self.issue_type == "غسيل":
                        voucher = frappe.db.get_value(
                            "Vehicles", t.vehicle, "washing_voucher"
                        )

                    record_name = 1
                    max_id = frappe.db.sql(
                        """
                        SELECT MAX(name) as max_name
                        FROM `tabLiquids Issuing Table`
                        """,
                        as_dict=1,
                    )
                    if frappe.db.exists("Liquids Issuing Table", 1):
                        record_name = int(max_id[0]["max_name"]) + 1
                    frappe.db.sql(
                        """ INSERT INTO `tabLiquids Issuing Table`
                                                            (issue_date, issue_type, vehicle_status, voucher, from_date, to_date, entity, qty, created_by, issue_no, parent, parentfield, parenttype, name)
                                                    VALUES ('{issue_date}', '{issue_type}', '{vehicle_status}', '{voucher}', '{from_date}', '{to_date}', '{entity}', '{qty}', '{created_by}', '{issue_no}','{parent}', '{parentfield}', '{parenttype}', '{record_name}')
                                                """.format(
                            issue_date=self.issue_date,
                            issue_type=self.issue_type,
                            from_date=self.from_date,
                            vehicle_status=vehicle_status,
                            voucher=voucher,
                            qty=t.qty,
                            to_date=self.to_date,
                            entity=self.entity,
                            created_by=frappe.session.user,
                            issue_no=self.name,
                            parenttype="Vehicles",
                            parent=t.vehicle,
                            parentfield="liquid_table",
                            record_name=record_name,
                        )
                    )

                    gas_valid_vehicle_list = frappe.db.sql(
                        """ Select
                            `tabVehicles`.name as vehicle,
                            `tabVehicles`.gas_count as gas_count
                            from `tabVehicles` 
                            where `tabVehicles`.name = '{vehicle}'
                            and `tabVehicles`.gas_count > 0
                            and `tabVehicles`.name not in (select `tabLiquids Issuing Table`.parent 
                                from `tabLiquids Issuing Table`
                                where `tabLiquids Issuing Table`.issue_type = '{issue_type}'
                                and `tabLiquids Issuing Table`.from_date >= '{from_date}'
                                and `tabLiquids Issuing Table`.to_date <= '{to_date}')
                        """.format(
                            entity=self.entity,
                            from_date=self.from_date,
                            to_date=self.to_date,
                            issue_type="غاز",
                            vehicle=t.vehicle,
                        ),
                        as_dict=1,
                    )
                    current_vehicles = []
                    if gas_valid_vehicle_list:
                        current_vehicles.append(t.vehicle)
                        vehicle_status = frappe.db.get_value(
                            "Vehicles", t.vehicle, "vehicle_status"
                        )
                        voucher = ""
                        voucher1 = ""
                        record_name = 1
                        max_id = frappe.db.sql(
                            """
                            SELECT MAX(name) as max_name
                            FROM `tabLiquids Issuing Table`
                            """,
                            as_dict=1,
                        )
                        if frappe.db.exists("Liquids Issuing Table", 1):
                            record_name = int(max_id[0]["max_name"]) + 1
                        voucher = "غاز طبيعي فئة 15 متر مكعب"
                        voucher1 = "لا يوجد"
                        # frappe.throw(str(gas_valid_vehicle_list))
                        frappe.db.sql(
                            """ INSERT INTO `tabLiquids Issuing Table`
                                                (issue_date, issue_type, vehicle_status, voucher, from_date, to_date, entity, qty, created_by, issue_no, parent, parentfield, parenttype, name)
                                        VALUES ('{issue_date}', '{issue_type}', '{vehicle_status}', '{voucher}' ,'{from_date}', '{to_date}', '{entity}', '{qty}', '{created_by}', '{issue_no}','{parent}', '{parentfield}', '{parenttype}', '{record_name}')
                                        """.format(
                                issue_date=self.issue_date,
                                issue_type="غاز",
                                vehicle_status=vehicle_status,
                                from_date=self.from_date,
                                voucher=voucher,
                                to_date=self.to_date,
                                entity=self.entity,
                                qty=(
                                    self.issue_days
                                    * gas_valid_vehicle_list[0].gas_count
                                    / 30
                                ),
                                created_by=frappe.session.user,
                                issue_no=self.name,
                                parenttype="Vehicles",
                                parent=t.vehicle,
                                parentfield="liquid_table",
                                record_name=record_name,
                            )
                        )

                    if len(current_vehicles) == 1:
                        current_vehicles.append("None")
                    if not current_vehicles:
                        pass
                        # frappe.msgprint("لا يوجد مركبات تستحق الصرف")
                else:
                    if t.last_issue_from_date or t.last_issue_to_date:
                        if (
                            float(t.last_issue_qty) > 0
                            and getdate(t.last_issue_from_date)
                            >= getdate(self.from_date)
                            and getdate(t.last_issue_from_date) <= getdate(self.to_date)
                        ):
                            frappe.throw(
                                " الصف # "
                                + str(t.idx)
                                + " : لا يمكن صرف "
                                + self.issue_type
                                + " إلى المركبة "
                                + str(t.vehicle_no)
                                + " حيث أنه تم الصرف لها من قبل خلال الفترة المحددة إلى جهة "
                                + str(t.entity_name)
                            )

                        if (
                            float(t.last_issue_qty) > 0
                            and getdate(t.last_issue_to_date) >= getdate(self.from_date)
                            and getdate(t.last_issue_to_date) <= getdate(self.to_date)
                        ):
                            frappe.throw(
                                " الصف # "
                                + str(t.idx)
                                + " : لا يمكن صرف "
                                + self.issue_type
                                + " إلى المركبة "
                                + str(t.vehicle_no)
                                + " حيث أنه تم الصرف لها من قبل خلال الفترة المحددة إلى جهة "
                                + str(t.entity_name)
                            )

                    vehicle_status = frappe.db.get_value(
                        "Boats", t.vehicle, "boat_validity"
                    )
                    voucher = ""

                    if self.issue_type == "وقود":
                        voucher = (
                            frappe.db.get_value("Boats", t.vehicle, "fuel_voucher")
                            if frappe.db.get_value("Boats", t.vehicle, "fuel_voucher")
                            else "لا يوجد"
                        )
                    record_name = 1
                    max_id = frappe.db.sql(
                        """
                        SELECT MAX(name) as max_name
                        FROM `tabLiquids Issuing Table`
                        """,
                        as_dict=1,
                    )
                    if frappe.db.exists("Liquids Issuing Table", 1):
                        record_name = int(max_id[0]["max_name"]) + 1
                    frappe.db.sql(
                        """ INSERT INTO `tabLiquids Issuing Table`
                                                            (issue_date, issue_type, vehicle_status, voucher, from_date, to_date, entity, qty, created_by, issue_no, parent, parentfield, parenttype, name)
                                                    VALUES ('{issue_date}', '{issue_type}', '{vehicle_status}', '{voucher}', '{from_date}', '{to_date}', '{entity}', '{qty}', '{created_by}', '{issue_no}','{parent}', '{parentfield}', '{parenttype}', '{record_name}')
                                                """.format(
                            issue_date=self.issue_date,
                            issue_type=self.issue_type,
                            from_date=self.from_date,
                            vehicle_status=vehicle_status,
                            voucher=voucher,
                            qty=t.qty,
                            to_date=self.to_date,
                            entity=self.entity,
                            created_by=frappe.session.user,
                            issue_no=self.name,
                            parenttype="Boats",
                            parent=t.vehicle,
                            parentfield="liquid_table",
                            record_name=record_name,
                        )
                    )

        # set submitted = 1
        frappe.db.sql(
            """
            UPDATE `tabLiquids Issuing` SET submitted = 1, issue_state = 'جاري تحضير الصرفية ومراجعتها'  WHERE name = '{name}'
                    """.format(
                name=self.name
            )
        )
        frappe.db.commit()
        self.reload()

    def get_sum_qty(self, fuel_type):
        sum_qty = 0
        if self.issue_to == "جهة":
            for t in self.liquid_per_vehicle_type_table:
                if fuel_type == t.fuel_type:
                    sum_qty += int(t.total_qty)
            return sum_qty
        else:
            for t in self.specified_vehicles_issuing_table:
                if fuel_type == t.liquid:
                    sum_qty += int(t.qty)
            return sum_qty

    def get_gas_sum_qty(self, fuel_type):
        sum_qty = 0
        if self.issue_to == "جهة":
            for t in self.gas_per_vehicle_type_table:
                sum_qty += int(t.total_qty)
            return sum_qty
        else:
            for t in self.specified_vehicles_issuing_table:
                if fuel_type == t.fuel_type:
                    sum_qty += int(t.total_qty)
            return sum_qty

    def get_liquids(self):
        fuel_types = []
        if self.issue_to == "جهة":
            for row in self.liquid_per_vehicle_type_table:
                if row.fuel_type not in fuel_types:
                    fuel_types.append(row.fuel_type)
        else:
            for row in self.specified_vehicles_issuing_table:
                if row.liquid not in fuel_types:
                    fuel_types.append(row.liquid)
        return fuel_types

    def get_gas_liquids(self):
        gas_types = []
        for row in self.gas_per_vehicle_type_table:
            if row.fuel_type not in gas_types:
                gas_types.append(row.fuel_type)
        return gas_types

    def validate(self):
        current_issue = " من " + str(self.from_date) + " إلى " + str(self.to_date)
        self.current_issue = current_issue

        if getdate(self.from_date) > getdate(self.to_date):
            frappe.throw(
                " تاريخ نهاية الصرفية لا يمكن أن يكون قبل تاريخ بداية الصرفية "
            )

        if self.issue_to == "جهة":
            self.set("specified_vehicles_issuing_table", [])
            self.set("qty_per_liquid", [])
            self.set("previous_vehicles_issuing_table", [])
            self.set("gas_per_vehicle_type_table", [])

            last_doc = frappe.db.sql(
                """
                SELECT `tabLiquids Issuing`.name as name, 
                        `tabLiquids Issuing`.from_date as from_date, 
                        `tabLiquids Issuing`.to_date as to_date
                FROM `tabLiquids Issuing`
                WHERE `tabLiquids Issuing`.submitted = 1 
                AND `tabLiquids Issuing`.issue_to = "{issue_to}"
                AND `tabLiquids Issuing`.entity = "{entity}"
                AND `tabLiquids Issuing`.issue_type = "{issue_type}"
                ORDER BY `tabLiquids Issuing`.from_date DESC LIMIT 1 
            """.format(
                    issue_to=self.issue_to,
                    entity=self.entity,
                    issue_type=self.issue_type,
                ),
                as_dict=1,
            )

            issue_list = frappe.db.get_list(
                "Liquids Issuing",
                filters={
                    "submitted": ["=", 1],
                    "issue_to": ["=", self.issue_to],
                    "entity": ["=", self.entity],
                    "issue_type": ["=", self.issue_type],
                    "name": ["!=", self.name],
                },
                fields=["from_date", "to_date"],
            )

            for m in issue_list:
                if getdate(self.from_date) >= getdate(m.from_date) and getdate(
                    self.from_date
                ) <= getdate(m.to_date):
                    frappe.throw(
                        " لا يمكن صرف "
                        + self.issue_type
                        + " إلى "
                        + self.entity
                        + " حيث أنه تم الصرف من قبل خلال الفترة المحددة "
                    )
                if getdate(self.to_date) >= getdate(m.from_date) and getdate(
                    self.to_date
                ) <= getdate(m.to_date):
                    frappe.throw(
                        " لا يمكن صرف "
                        + self.issue_type
                        + " إلى "
                        + self.entity
                        + " حيث أنه تم الصرف من قبل خلال الفترة المحددة "
                    )

            if last_doc:
                last_issue = (
                    " من "
                    + str(last_doc[0].from_date)
                    + " إلى "
                    + str(last_doc[0].to_date)
                )
                self.last_issue = last_issue

                #     start_date = getdate(last_doc[0].issue_date)
                #     end_date = getdate(self.issue_date)

                previous_vehicles = frappe.db.sql(
                    """
                        Select `tabVehicles`.name as vehicle,
                        `tabVehicles`.vehicle_no as vehicle_no,
                        `tabVehicles`.vehicle_type as vehicle_type,
                        `tabVehicles`.entity_name as entity_name,
                        `tabLiquids Issuing Table`.from_date, 
                        `tabLiquids Issuing Table`.to_date, 
                        `tabLiquids Issuing Table`.entity, 
                        `tabLiquids Issuing Table`.qty
                        from `tabVehicles`
                        JOIN `tabLiquids Issuing Table` ON `tabLiquids Issuing Table`.parent = `tabVehicles`.name
                        Where `tabVehicles`.vehicle_status = 'صالحة'
                        and `tabVehicles`.entity_name = '{entity}'
                        and `tabVehicles`.exchange_allowance not in ('لوحة فقط', 'لوحة وخدمة كاملة فقط')
                        and `tabVehicles`.vehicle_type != 'لانش'
                        and `tabVehicles`.fuel_type != 'بدون وقود'
                        and `tabVehicles`.litre_count != 0
                        and `tabLiquids Issuing Table`.issue_type = '{issue_type}'
                        and `tabLiquids Issuing Table`.from_date >= '{from_date}'
                        and `tabLiquids Issuing Table`.to_date <= '{to_date}'
                        and `tabLiquids Issuing Table`.parenttype = 'Vehicles'
                        and `tabLiquids Issuing Table`.parentfield = 'liquid_table'

                    """.format(
                        entity=self.entity,
                        from_date=self.from_date,
                        to_date=self.to_date,
                        issue_type=self.issue_type,
                    ),
                    as_dict=1,
                )

                #     for q in previous_vehicles:
                #         vehicle_issue_list_ = frappe.db.sql(
                #             """ Select from_date, to_date, entity, qty
                #                 from `tabLiquids Issuing Table`
                #                 where parent = '{parent}' and issue_type = '{issue_type}'
                #                 order by to_date desc limit 1
                #             """.format(

                #                 parent=q.vehicle, issue_type=self.issue_type
                #             ),
                #             as_dict=1,
                #         )

                #         if q.vehicle:
                #             vehicle_row = self.append("previous_vehicles_issuing_table", {})
                #             vehicle_row.vehicle_boat = "Vehicles"
                #             vehicle_row.vehicle = q.vehicle
                #             vehicle_row.vehicle_no = q.vehicle_no
                #             vehicle_row.vehicle_type = q.vehicle_type
                #             vehicle_row.qty = q.qty
                #             for t in vehicle_issue_list_:
                #                 vehicle_row.last_issue_from_date = t.from_date
                #                 vehicle_row.last_issue_to_date = t.to_date
                #                 vehicle_row.entity_name = t.entity
                #     previous_boats = frappe.db.sql(
                #         """ Select
                #             `tabBoats`.name as vehicle,
                #             `tabBoats`.boat_no as vehicle_no,
                #             `tabBoats`.entity_name as entity_name
                #             from `tabBoats`
                #             Where `tabBoats`.boat_validity = "صالحة"
                #             and `tabBoats`.entity_name = '{entity}'
                #             and `tabBoats`.fuel_type != "بدون وقود"
                #             and `tabBoats`.qty != 0
                #             and `tabBoats`.name in (select `tabLiquids Issuing Table`.parent
                #                 from `tabLiquids Issuing Table`
                #                 where `tabLiquids Issuing Table`.issue_type = '{issue_type}'
                #                 and `tabLiquids Issuing Table`.from_date >= '{from_date}'
                #                 and `tabLiquids Issuing Table`.to_date <= '{to_date}')
                #         """.format(
                #             entity=self.entity,
                #             from_date=self.from_date,
                #             to_date=self.to_date,
                #             issue_type=self.issue_type,
                #         ),
                #         as_dict=1,
                #     )

                #     for r in previous_boats:
                #         boat_issue_list_ = frappe.db.sql(
                #             """ Select from_date, to_date, entity, qty
                #                 from `tabLiquids Issuing Table`
                #                 where parent = '{parent}' and issue_type = '{issue_type}'
                #                 order by to_date desc limit 1
                #             """.format(
                #                 parent=r.vehicle, issue_type=self.issue_type
                #             ),
                #             as_dict=1,
                #         )

                #         if r.vehicle:
                #             vehicle_row = self.append("previous_vehicles_issuing_table", {})
                #             vehicle_row.vehicle_boat = "Boats"
                #             vehicle_row.vehicle = r.vehicle
                #             vehicle_row.vehicle_no = r.vehicle_no
                #             vehicle_row.vehicle_type = "لانش"
                #             vehicle_row.qty = r.qty
                #             for t in boat_issue_list_:
                #                 vehicle_row.last_issue_from_date = t.from_date
                #                 vehicle_row.last_issue_to_date = t.to_date
                #                 vehicle_row.entity_name = t.entity

                #     fixed_vehicles = frappe.db.sql(
                #         """ Select DISTINCT
                #             `tabVehicles`.name as name,
                #             `tabVehicles`.vehicle_no as vehicle_no,
                #             `tabVehicles`.vehicle_type as vehicle_type,
                #             `tabVehicles`.vehicle_shape as vehicle_shape,
                #             `tabVehicles`.vehicle_brand as vehicle_brand,
                #             `tabVehicles`.vehicle_style as vehicle_style,
                #             `tabVehicles`.motor_no as motor_no,
                #             `tabVehicles`.chassis_no as chassis_no,
                #             `tabVehicle Status Logs`.date as date
                #             from `tabVehicles` join `tabVehicle Status Logs`
                #             on `tabVehicles`.name = `tabVehicle Status Logs`.parent
                #             where `tabVehicle Status Logs`.value = "صالحة"
                #             and `tabVehicles`.vehicle_status = "صالحة"
                #             and `tabVehicle Status Logs`.idx != 1
                #             and `tabVehicle Status Logs`.date between '{start_date}' and '{end_date}'
                #             and `tabVehicles`.entity_name = '{entity}'
                #             order by `tabVehicle Status Logs`.date
                #         """.format(
                #             start_date=start_date, end_date=end_date, entity=self.entity
                #         ),
                #         as_dict=1,
                #     )

                #     for fixed_vec in fixed_vehicles:
                #         fix = self.append("fixed_vehicles", {})
                #         fix.vehicle = fixed_vec.name
                #         fix.vehicle_no = fixed_vec.vehicle_no
                #         fix.vehicle_type = fixed_vec.vehicle_type
                #         fix.vehicle_shape = fixed_vec.vehicle_shape
                #         fix.vehicle_brand = fixed_vec.vehicle_brand
                #         fix.vehicle_style = fixed_vec.vehicle_style
                #         fix.motor_no = fixed_vec.motor_no
                #         fix.chassis_no = fixed_vec.chassis_no
                #         fix.date = fixed_vec.date

                #     broken_vehicles = frappe.db.sql(
                #         """ Select DISTINCT
                #             `tabVehicles`.name as name,
                #             `tabVehicles`.vehicle_no as vehicle_no,
                #             `tabVehicles`.vehicle_type as vehicle_type,
                #             `tabVehicles`.vehicle_shape as vehicle_shape,
                #             `tabVehicles`.vehicle_brand as vehicle_brand,
                #             `tabVehicles`.vehicle_style as vehicle_style,
                #             `tabVehicles`.motor_no as motor_no,
                #             `tabVehicles`.chassis_no as chassis_no,
                #             `tabVehicle Status Logs`.date as date
                #             from `tabVehicles` join `tabVehicle Status Logs`
                #             on `tabVehicles`.name = `tabVehicle Status Logs`.parent
                #             where `tabVehicle Status Logs`.value = "عاطلة"
                #             and `tabVehicles`.vehicle_status in ("عاطلة", "تحت التخريد")
                #             and `tabVehicle Status Logs`.date between '{start_date}' and '{end_date}'
                #             and `tabVehicles`.entity_name = '{entity}'
                #             order by `tabVehicle Status Logs`.date
                #         """.format(
                #             start_date=start_date, end_date=end_date, entity=self.entity
                #         ),
                #         as_dict=1,
                #     )

                #     for broken_vec in broken_vehicles:
                #         broken = self.append("broken_vehicles", {})
                #         broken.vehicle = broken_vec.name
                #         broken.vehicle_no = broken_vec.vehicle_no
                #         broken.vehicle_type = broken_vec.vehicle_type
                #         broken.vehicle_shape = broken_vec.vehicle_shape
                #         broken.vehicle_brand = broken_vec.vehicle_brand
                #         broken.vehicle_style = broken_vec.vehicle_style
                #         broken.motor_no = broken_vec.motor_no
                #         broken.chassis_no = broken_vec.chassis_no
                #         broken.date = broken_vec.date

                #     scraped_vehicles = frappe.db.sql(
                #         """ Select DISTINCT
                #             `tabVehicles`.name as name,
                #             `tabVehicles`.police_id as vehicle_no,
                #             `tabVehicles`.vehicle_type as vehicle_type,
                #             `tabVehicles`.vehicle_shape as vehicle_shape,
                #             `tabVehicles`.vehicle_brand as vehicle_brand,
                #             `tabVehicles`.vehicle_style as vehicle_style,
                #             `tabVehicles`.motor_no as motor_no,
                #             `tabVehicles`.chassis_no as chassis_no,
                #             `tabVehicle Status Logs`.date as date
                #             from `tabVehicles` join `tabVehicle Status Logs`
                #             on `tabVehicles`.name = `tabVehicle Status Logs`.parent
                #             where `tabVehicle Status Logs`.value = "مخردة"
                #             and `tabVehicles`.vehicle_status = "مخردة"
                #             and `tabVehicle Status Logs`.date between '{start_date}' and '{end_date}'
                #             and `tabVehicles`.entity_name = '{entity}'
                #             order by `tabVehicle Status Logs`.date
                #         """.format(
                #             start_date=start_date, end_date=end_date, entity=self.entity
                #         ),
                #         as_dict=1,
                #     )

                #     for scraped_vec in scraped_vehicles:
                #         scraped = self.append("scraped_vehicles", {})
                #         scraped.vehicle = scraped_vec.name
                #         scraped.vehicle_no = scraped_vec.vehicle_no
                #         scraped.vehicle_type = scraped_vec.vehicle_type
                #         scraped.vehicle_shape = scraped_vec.vehicle_shape
                #         scraped.vehicle_brand = scraped_vec.vehicle_brand
                #         scraped.vehicle_style = scraped_vec.vehicle_style
                #         scraped.motor_no = scraped_vec.motor_no
                #         scraped.chassis_no = scraped_vec.chassis_no
                #         scraped.date = scraped_vec.date

                # transferred_to_vehicles = frappe.db.sql(
                #     """ Select DISTINCT
                #         `tabVehicles`.name as name,
                #         `tabVehicles`.vehicle_no as vehicle_no,
                #         `tabVehicles`.vehicle_type as vehicle_type,
                #         `tabVehicles`.vehicle_shape as vehicle_shape,
                #         `tabVehicles`.vehicle_brand as vehicle_brand,
                #         `tabVehicles`.vehicle_style as vehicle_style,
                #         `tabVehicles`.motor_no as motor_no,
                #         `tabVehicles`.chassis_no as chassis_no,
                #         `tabEntity Logs`.date as date
                #         from `tabVehicles` join `tabEntity Logs`
                #         on `tabVehicles`.name = `tabEntity Logs`.parent
                #         where `tabEntity Logs`.value = '{entity}'
                #         and `tabVehicles`.entity_name = '{entity}'
                #         and `tabEntity Logs`.date between '{start_date}' and '{end_date}'
                #         order by `tabEntity Logs`.date
                #     """.format(
                #         start_date=start_date, end_date=end_date, entity=self.entity
                #     ),
                #     as_dict=1,
                # )

            #     for transferred_to_vec in transferred_to_vehicles:
            #         to_vec = self.append("transferred_to_vehicles", {})
            #         to_vec.vehicle = transferred_to_vec.name
            #         to_vec.vehicle_no = transferred_to_vec.vehicle_no
            #         to_vec.vehicle_type = transferred_to_vec.vehicle_type
            #         to_vec.vehicle_shape = transferred_to_vec.vehicle_shape
            #         to_vec.vehicle_brand = transferred_to_vec.vehicle_brand
            #         to_vec.vehicle_style = transferred_to_vec.vehicle_style
            #         to_vec.motor_no = transferred_to_vec.motor_no
            #         to_vec.chassis_no = transferred_to_vec.chassis_no
            #         to_vec.date = transferred_to_vec.date

            #     query = frappe.db.sql(
            #         """ Select DISTINCT
            #             `tabEntity Logs`.parent as parent
            #             from `tabEntity Logs`
            #             where `tabEntity Logs`.value = '{entity}'
            #             order by `tabEntity Logs`.date
            #         """.format(
            #             entity=self.entity
            #         ),
            #         as_dict=1,
            #     )

            #     for row in query:
            #         idx = frappe.db.sql(
            #             """ Select
            #                 `tabEntity Logs`.date as date,
            #                 `tabEntity Logs`.idx as idx
            #                 from `tabVehicles` join `tabEntity Logs`
            #                 on `tabVehicles`.name = `tabEntity Logs`.parent
            #                 where `tabEntity Logs`.value = '{entity}'
            #                 and `tabEntity Logs`.parent = '{parent}'
            #                 order by `tabEntity Logs`.date desc
            #                 limit 1
            #             """.format(
            #                 parent=row.parent,
            #                 start_date=start_date,
            #                 end_date=end_date,
            #                 entity=self.entity,
            #             ),
            #             as_dict=1,
            #         )

            #         if idx:
            #             to_entity = frappe.db.sql(
            #                 """ Select
            #                     `tabVehicles`.name as name,
            #                     `tabVehicles`.vehicle_no as vehicle_no,
            #                     `tabVehicles`.vehicle_type as vehicle_type,
            #                     `tabVehicles`.vehicle_shape as vehicle_shape,
            #                     `tabVehicles`.vehicle_brand as vehicle_brand,
            #                     `tabVehicles`.vehicle_style as vehicle_style,
            #                     `tabVehicles`.motor_no as motor_no,
            #                     `tabVehicles`.chassis_no as chassis_no,
            #                     `tabEntity Logs`.date as date,
            #                     `tabEntity Logs`.value as value,
            #                     `tabEntity Logs`.idx as idx
            #                     from `tabVehicles` join `tabEntity Logs`
            #                     on `tabVehicles`.name = `tabEntity Logs`.parent
            #                     where `tabEntity Logs`.parent = '{parent}'
            #                     and `tabVehicles`.entity_name != '{entity}'
            #                     and `tabEntity Logs`.idx = '{idx}'
            #                     and `tabEntity Logs`.date between '{start_date}' and '{end_date}'
            #                     order by `tabEntity Logs`.date desc
            #                 """.format(
            #                     idx=idx[0].idx + 1,
            #                     parent=row.parent,
            #                     start_date=start_date,
            #                     end_date=end_date,
            #                     entity=self.entity,
            #                 ),
            #                 as_dict=1,
            #             )

            #             if to_entity:
            #                 from_vec = self.append("transferred_from_vehicles", {})
            #                 from_vec.vehicle = to_entity[0].name
            #                 from_vec.vehicle_no = to_entity[0].vehicle_no
            #                 from_vec.vehicle_type = to_entity[0].vehicle_type
            #                 from_vec.vehicle_shape = to_entity[0].vehicle_shape
            #                 from_vec.vehicle_brand = to_entity[0].vehicle_brand
            #                 from_vec.vehicle_style = to_entity[0].vehicle_style
            #                 from_vec.motor_no = to_entity[0].motor_no
            #                 from_vec.chassis_no = to_entity[0].chassis_no
            #                 from_vec.date = to_entity[0].date
            #                 from_vec.entity = to_entity[0].value

            if not last_doc:
                self.last_issue = ""

            if self.issue_type == "وقود":
                self.set("liquid_per_vehicle_type_table", [])
                self.set("vehicles_issuing_table", [])
                # self.set("gas_per_vehicle_type_table", [])
                fuel_type_list = frappe.db.sql(
                    """ Select distinct `tabFuel Voucher`.fuel_type as fuel_type 
                        from `tabVehicles`
                        JOIN `tabFuel Voucher` on `tabVehicles`.fuel_voucher = `tabFuel Voucher`.name
                        where `tabVehicles`.vehicle_type != "لانش"
                        and `tabVehicles`.fuel_type != "بدون وقود"
                        order by `tabFuel Voucher`.fuel_type
                    """.format(
                        entity=self.entity
                    ),
                    as_dict=1,
                )

                for x in fuel_type_list:
                    vehicle_type_list = frappe.db.sql(
                        """ Select distinct `tabVehicles`.vehicle_type as vehicle_type 
                            from `tabVehicles`
                            JOIN `tabFuel Voucher` on `tabVehicles`.fuel_voucher = `tabFuel Voucher`.name
                            Where `tabFuel Voucher`.fuel_type = '{fuel_type}'
                        """.format(
                            fuel_type=x.fuel_type, entity=self.entity
                        ),
                        as_dict=1,
                    )

                    for y in vehicle_type_list:
                        cylinder_list = frappe.db.sql(
                            """ Select distinct `tabVehicles`.cylinder_count as cylinder_count 
                                from `tabVehicles`
                                JOIN `tabFuel Voucher` on `tabVehicles`.fuel_voucher = `tabFuel Voucher`.name
                                Where `tabFuel Voucher`.fuel_type = '{fuel_type}'
                                and `tabVehicles`.vehicle_type = '{vehicle_type}'
                                order by `tabVehicles`.cylinder_count
                            """.format(
                                fuel_type=x.fuel_type,
                                vehicle_type=y.vehicle_type,
                                entity=self.entity,
                            ),
                            as_dict=1,
                        )

                        for z in cylinder_list:
                            litre_count_list = frappe.db.sql(
                                """ Select distinct `tabVehicles`.litre_count as litre_count 
                                    from `tabVehicles`
                                    JOIN `tabFuel Voucher` on `tabVehicles`.fuel_voucher = `tabFuel Voucher`.name
                                    Where `tabFuel Voucher`.fuel_type = '{fuel_type}'
                                    and `tabVehicles`.vehicle_type = '{vehicle_type}'
                                    and `tabVehicles`.cylinder_count = '{cylinder_count}'
                                    order by `tabVehicles`.litre_count
                                """.format(
                                    fuel_type=x.fuel_type,
                                    vehicle_type=y.vehicle_type,
                                    cylinder_count=z.cylinder_count,
                                    entity=self.entity,
                                ),
                                as_dict=1,
                            )

                            valid_count = 0
                            previous_count = 0
                            previous_vehicles = []
                            plate_count = 0

                            for v in litre_count_list:
                                total_vehicle_list = frappe.db.sql(
                                    """ Select count(`tabVehicles`.name) as total_count 
                                        from `tabVehicles`
                                        JOIN `tabFuel Voucher` on `tabVehicles`.fuel_voucher = `tabFuel Voucher`.name
                                        Where `tabFuel Voucher`.fuel_type = '{fuel_type}'
                                        and `tabVehicles`.vehicle_type = '{vehicle_type}'
                                        and `tabVehicles`.cylinder_count = '{cylinder_count}'
                                        and `tabVehicles`.litre_count = '{litre_count}'
                                        and ((`tabVehicles`.entity_name = '{entity}' and (`tabVehicles`.attached_entity is null or `tabVehicles`.attached_entity = ""))
                                        or (`tabVehicles`.entity_name != '{entity}' and `tabVehicles`.attached_entity = '{entity}'))
                                        and `tabVehicles`.vehicle_status  in ("صالحة", "عاطلة", "تحت التخريد")
                                    """.format(
                                        litre_count=v.litre_count,
                                        fuel_type=x.fuel_type,
                                        vehicle_type=y.vehicle_type,
                                        cylinder_count=z.cylinder_count,
                                        entity=self.entity,
                                    ),
                                    as_dict=1,
                                )

                                valid_vehicle_list = frappe.db.sql(
                                    """ Select count(`tabVehicles`.name) as valid_count,
                                        `tabVehicles`.name as vehicle,
                                        `tabVehicles`.vehicle_no as vehicle_no,
                                        `tabVehicles`.vehicle_type as vehicle_type,
                                        `tabVehicles`.entity_name as entity_name
                                        from `tabVehicles` 
                                        JOIN `tabFuel Voucher` on `tabVehicles`.fuel_voucher = `tabFuel Voucher`.name
                                        Where `tabFuel Voucher`.fuel_type = '{fuel_type}'
                                        and `tabVehicles`.vehicle_type = '{vehicle_type}'
                                        and `tabVehicles`.cylinder_count = '{cylinder_count}'
                                        and `tabVehicles`.litre_count = '{litre_count}'
                                        and `tabVehicles`.vehicle_status = "صالحة"
                                        and ((`tabVehicles`.entity_name = '{entity}' and (`tabVehicles`.attached_entity is null or `tabVehicles`.attached_entity = ""))
                                        or (`tabVehicles`.entity_name != '{entity}' and `tabVehicles`.attached_entity = '{entity}'))
                                        and `tabVehicles`.exchange_allowance not in ("لوحة فقط", "لوحة وخدمة كاملة فقط")
                                        and `tabVehicles`.name not in (select `tabLiquids Issuing Table`.parent 
                                            from `tabLiquids Issuing Table`
                                            where `tabLiquids Issuing Table`.issue_type = '{issue_type}'
                                            and `tabLiquids Issuing Table`.from_date >= '{from_date}'
                                            and `tabLiquids Issuing Table`.to_date <= '{to_date}')
                                    """.format(
                                        litre_count=v.litre_count,
                                        fuel_type=x.fuel_type,
                                        vehicle_type=y.vehicle_type,
                                        cylinder_count=z.cylinder_count,
                                        entity=self.entity,
                                        from_date=self.from_date,
                                        to_date=self.to_date,
                                        issue_type=self.issue_type,
                                    ),
                                    as_dict=1,
                                )

                                previous_vehicle_list = frappe.db.sql(
                                    """ Select count(`tabVehicles`.name) as valid_count,
                                        `tabVehicles`.name as vehicle,
                                        `tabVehicles`.vehicle_no as vehicle_no,
                                        `tabVehicles`.vehicle_type as vehicle_type,
                                        (select `tabLiquids Issuing Table`.entity 
                                            from `tabLiquids Issuing Table`
                                            where `tabLiquids Issuing Table`.issue_type = '{issue_type}'
                                            and `tabLiquids Issuing Table`.from_date >= '{from_date}'
                                            and `tabLiquids Issuing Table`.to_date <= '{to_date}'
                                            and `tabLiquids Issuing Table`.parent = vehicle) as previous_entity,
                                        (select `tabLiquids Issuing Table`.issue_date 
                                        from `tabLiquids Issuing Table`
                                            where `tabLiquids Issuing Table`.issue_type = '{issue_type}'
                                            and `tabLiquids Issuing Table`.from_date >= '{from_date}'
                                            and `tabLiquids Issuing Table`.to_date <= '{to_date}'
                                            and `tabLiquids Issuing Table`.parent = vehicle) as previous_date,
                                        (select `tabLiquids Issuing Table`.qty 
                                        from `tabLiquids Issuing Table`
                                            where `tabLiquids Issuing Table`.issue_type = '{issue_type}'
                                            and `tabLiquids Issuing Table`.from_date >= '{from_date}'
                                            and `tabLiquids Issuing Table`.to_date <= '{to_date}'
                                            and `tabLiquids Issuing Table`.parent = vehicle) as qty,
                                        `tabVehicles`.entity_name as entity_name
                                        from `tabVehicles` 
                                        JOIN `tabFuel Voucher` on `tabVehicles`.fuel_voucher = `tabFuel Voucher`.name
                                        Where `tabFuel Voucher`.fuel_type = '{fuel_type}'
                                        and `tabVehicles`.vehicle_type = '{vehicle_type}'
                                        and `tabVehicles`.cylinder_count = '{cylinder_count}'
                                        and `tabVehicles`.litre_count = '{litre_count}'
                                        and `tabVehicles`.vehicle_status = "صالحة"
                                        and ((`tabVehicles`.entity_name = '{entity}' and (`tabVehicles`.attached_entity is null or `tabVehicles`.attached_entity = ""))
                                        or (`tabVehicles`.entity_name != '{entity}' and `tabVehicles`.attached_entity = '{entity}'))
                                        and `tabVehicles`.exchange_allowance not in ("لوحة فقط", "لوحة وخدمة كاملة فقط")
                                        and `tabVehicles`.name in (select `tabLiquids Issuing Table`.parent 
                                            from `tabLiquids Issuing Table`
                                            where `tabLiquids Issuing Table`.issue_type = '{issue_type}'
                                            and `tabLiquids Issuing Table`.from_date >= '{from_date}'
                                            and `tabLiquids Issuing Table`.to_date <= '{to_date}')
                                    """.format(
                                        litre_count=v.litre_count,
                                        fuel_type=x.fuel_type,
                                        vehicle_type=y.vehicle_type,
                                        cylinder_count=z.cylinder_count,
                                        entity=self.entity,
                                        from_date=self.from_date,
                                        to_date=self.to_date,
                                        issue_type=self.issue_type,
                                    ),
                                    as_dict=1,
                                )
                                plate_only_vehicle_list = frappe.db.sql(
                                    """ Select count(`tabVehicles`.name) as valid_count,
                                        `tabVehicles`.name as vehicle,
                                        `tabVehicles`.vehicle_no as vehicle_no,
                                        `tabVehicles`.vehicle_type as vehicle_type,
                                        `tabVehicles`.entity_name as entity_name
                                        from `tabVehicles` 
                                        JOIN `tabFuel Voucher` on `tabVehicles`.fuel_voucher = `tabFuel Voucher`.name
                                        Where `tabFuel Voucher`.fuel_type = '{fuel_type}'
                                        and `tabVehicles`.vehicle_type = '{vehicle_type}'
                                        and `tabVehicles`.cylinder_count = '{cylinder_count}'
                                        and `tabVehicles`.litre_count = '{litre_count}'
                                        and `tabVehicles`.vehicle_status in ("صالحة","عاطلة","تحت التخريد")
                                        and ((`tabVehicles`.entity_name = '{entity}' and (`tabVehicles`.attached_entity is null or `tabVehicles`.attached_entity = ""))
                                        or (`tabVehicles`.entity_name != '{entity}' and `tabVehicles`.attached_entity = '{entity}'))
                                        and `tabVehicles`.exchange_allowance in ("لوحة فقط", "لوحة وخدمة كاملة فقط")
                                    """.format(
                                        litre_count=v.litre_count,
                                        fuel_type=x.fuel_type,
                                        vehicle_type=y.vehicle_type,
                                        cylinder_count=z.cylinder_count,
                                        entity=self.entity,
                                        from_date=self.from_date,
                                        to_date=self.to_date,
                                    ),
                                    as_dict=1,
                                )

                                for d in valid_vehicle_list:
                                    valid_count = d.valid_count

                                for p in previous_vehicle_list:
                                    previous_count = p.valid_count
                                    if p.valid_count and float(p.qty) > 0:
                                        frappe.msgprint(
                                            " المركبة رقم "
                                            + str(p.vehicle_no)
                                            + " صرفت "
                                            + str(self.issue_type)
                                            + " من قبل في جهة "
                                            + str(p.previous_entity)
                                            + " بتاريخ "
                                            + str(p.previous_date)
                                        )
                                for u in plate_only_vehicle_list:
                                    plate_count = u.valid_count

                                for w in total_vehicle_list:
                                    if w.total_count > 0:
                                        row = self.append(
                                            "liquid_per_vehicle_type_table", {}
                                        )
                                        row.fuel_type = x.fuel_type
                                        row.vehicle_type = y.vehicle_type
                                        row.cylinder_count = z.cylinder_count
                                        row.liquid_qty = v.litre_count
                                        row.total_count = w.total_count
                                        row.valid_count = valid_count
                                        row.previously_issued = previous_count
                                        row.plate_count = plate_count
                                        row.invalid_count = (
                                            w.total_count
                                            - valid_count
                                            - previous_count
                                            - plate_count
                                        )
                                        row.total_qty = (
                                            self.month_count
                                            * v.litre_count
                                            * valid_count
                                        )

                check_coupon_field = frappe.db.sql(
                    """ Select `tabVehicles`.name as vehicle,
                        `tabVehicles`.vehicle_no as vehicle_no,
                        `tabVehicles`.vehicle_type as vehicle_type,
                        `tabVehicles`.entity_name as entity_name,
                        `tabVehicles`.fuel_voucher as fuel_voucher,
                        `tabVehicles`.litre_count as litre_count
                        from `tabVehicles` 
                        Where `tabVehicles`.vehicle_status = "صالحة"
                        and ((`tabVehicles`.entity_name = '{entity}' and (`tabVehicles`.attached_entity is null or `tabVehicles`.attached_entity = ""))
                        or (`tabVehicles`.entity_name != '{entity}' and `tabVehicles`.attached_entity = '{entity}'))
                        and `tabVehicles`.exchange_allowance not in ("لوحة فقط", "لوحة وخدمة كاملة فقط")
                        
                        and `tabVehicles`.name not in (select `tabLiquids Issuing Table`.parent 
                            from `tabLiquids Issuing Table`
                            where `tabLiquids Issuing Table`.issue_type = '{issue_type}'
                            and `tabLiquids Issuing Table`.from_date >= '{from_date}' 
                            and `tabLiquids Issuing Table`.to_date <= '{to_date}')
                        and `tabVehicles`.vehicle_type != "مقطورة"
                    """.format(
                        entity=self.entity,
                        from_date=self.from_date,
                        to_date=self.to_date,
                        issue_type=self.issue_type,
                    ),
                    as_dict=1,
                )

                for row in check_coupon_field:
                    if not row.fuel_voucher or not row.litre_count:
                        if self.seen_vehicles == 0:
                            frappe.msgprint(
                                "المركبة رقم "
                                + str(row.vehicle_no)
                                + "  ليس لها قاعدة صرف للوقود"
                            )
                self.seen_vehicles = 1

                #####################################################################
                fuel_type_list_2 = frappe.db.sql(
                    """ Select  distinct `tabFuel Voucher`.fuel_type as fuel_type 
                   
                        from `tabBoats`
                        JOIN `tabFuel Voucher` on `tabBoats`.fuel_voucher = `tabFuel Voucher`.name
                        Where  `tabFuel Voucher`.fuel_type in (Select distinct `tabFuel Voucher`.fuel_type as fuel_type 
                        from `tabBoats`
                        JOIN `tabFuel Voucher` on `tabBoats`.fuel_voucher = `tabFuel Voucher`.name
                        where `tabBoats`.fuel_type != "بدون وقود")
                        and `tabBoats`.entity_name = '{entity}' 
                        and `tabBoats`.qty != 0
                    """.format(
                        entity=self.entity
                    ),
                    as_dict=1,
                )

                for x in fuel_type_list_2:
                    cylinder_list_2 = frappe.db.sql(
                        """ Select distinct `tabBoats`.cylinder_count as cylinder_count 
                            from `tabBoats`
                            JOIN `tabFuel Voucher` on `tabBoats`.fuel_voucher = `tabFuel Voucher`.name
                            Where `tabFuel Voucher`.fuel_type = '{fuel_type}'
                            and `tabBoats`.entity_name = '{entity}'
                            and `tabBoats`.fuel_type != "بدون وقود"
                        """.format(
                            fuel_type=x.fuel_type, entity=self.entity
                        ),
                        as_dict=1,
                    )

                    for z in cylinder_list_2:
                        litre_count_list_2 = frappe.db.sql(
                            """ Select distinct `tabBoats`.qty as litre_count 
                                from `tabBoats`
                                JOIN `tabFuel Voucher` on `tabBoats`.fuel_voucher = `tabFuel Voucher`.name
                                Where `tabFuel Voucher`.fuel_type = '{fuel_type}'
                                and `tabBoats`.cylinder_count = '{cylinder_count}'
                                and `tabBoats`.entity_name = '{entity}'
                                and `tabBoats`.fuel_type != "بدون وقود"
                            """.format(
                                fuel_type=x.fuel_type,
                                cylinder_count=z.cylinder_count,
                                entity=self.entity,
                            ),
                            as_dict=1,
                        )

                        valid_count = 0
                        previous_count = 0
                        plate_count = 0

                        for v in litre_count_list_2:
                            total_vehicle_list_2 = frappe.db.sql(
                                """ Select count(`tabBoats`.name) as total_count 
                                    from `tabBoats`
                                    JOIN `tabFuel Voucher` on `tabBoats`.fuel_voucher = `tabFuel Voucher`.name
                                    Where `tabFuel Voucher`.fuel_type = '{fuel_type}'
                                    and `tabBoats`.cylinder_count = '{cylinder_count}'
                                    and `tabBoats`.entity_name = '{entity}'
                                    and `tabBoats`.qty = '{litre_count}'
                                    and `tabBoats`.fuel_type != "بدون وقود"
                                    and `tabBoats`.boat_validity  in ("صالحة", "عاطلة", "تحت التخريد")

                                """.format(
                                    litre_count=v.litre_count,
                                    fuel_type=x.fuel_type,
                                    cylinder_count=z.cylinder_count,
                                    entity=self.entity,
                                ),
                                as_dict=1,
                            )

                            valid_vehicle_list_2 = frappe.db.sql(
                                """ Select count(`tabBoats`.name) as valid_count,
                                    `tabBoats`.name as vehicle,
                                    `tabBoats`.boat_no as vehicle_no,
                                    `tabBoats`.entity_name as entity_name
                                    from `tabBoats`
                                    JOIN `tabFuel Voucher` on `tabBoats`.fuel_voucher = `tabFuel Voucher`.name
                                    Where `tabFuel Voucher`.fuel_type = '{fuel_type}'
                                    and `tabBoats`.cylinder_count = '{cylinder_count}'
                                    and `tabBoats`.entity_name = '{entity}'
                                    and `tabBoats`.qty = '{litre_count}'
                                    and `tabBoats`.boat_validity = "صالحة"
                                    and `tabBoats`.fuel_type != "بدون وقود"
                                    and `tabBoats`.name not in (select `tabLiquids Issuing Table`.parent 
                                            from `tabLiquids Issuing Table`
                                            where `tabLiquids Issuing Table`.issue_type = '{issue_type}'
                                            and `tabLiquids Issuing Table`.from_date >= '{from_date}'
                                            and `tabLiquids Issuing Table`.to_date <= '{to_date}')
                                """.format(
                                    litre_count=v.litre_count,
                                    fuel_type=x.fuel_type,
                                    cylinder_count=z.cylinder_count,
                                    entity=self.entity,
                                    from_date=self.from_date,
                                    to_date=self.to_date,
                                    issue_type=self.issue_type,
                                ),
                                as_dict=1,
                            )

                            previous_vehicle_list_2 = frappe.db.sql(
                                """ Select count(`tabBoats`.name) as valid_count,
                                    `tabBoats`.name as vehicle,
                                    `tabBoats`.boat_no as vehicle_no,
                                    `tabBoats`.entity_name as entity_name
                                    from `tabBoats`
                                    JOIN `tabFuel Voucher` on `tabBoats`.fuel_voucher = `tabFuel Voucher`.name
                                    Where `tabFuel Voucher`.fuel_type = '{fuel_type}'
                                    and `tabBoats`.cylinder_count = '{cylinder_count}'
                                    and `tabBoats`.qty = '{litre_count}'
                                    and `tabBoats`.boat_validity = "صالحة"
                                    and `tabBoats`.entity_name = '{entity}'
                                    and `tabBoats`.fuel_type != "بدون وقود"
                                    and `tabBoats`.name in (select `tabLiquids Issuing Table`.parent 
                                        from `tabLiquids Issuing Table`
                                        where `tabLiquids Issuing Table`.issue_type = '{issue_type}'
                                        and `tabLiquids Issuing Table`.from_date >= '{from_date}'
                                        and `tabLiquids Issuing Table`.to_date <= '{to_date}')
                                """.format(
                                    litre_count=v.litre_count,
                                    fuel_type=x.fuel_type,
                                    cylinder_count=z.cylinder_count,
                                    entity=self.entity,
                                    from_date=self.from_date,
                                    to_date=self.to_date,
                                    issue_type=self.issue_type,
                                ),
                                as_dict=1,
                            )

                            for d in valid_vehicle_list_2:
                                valid_count = d.valid_count

                            for p in previous_vehicle_list_2:
                                previous_count = p.valid_count

                            for w in total_vehicle_list_2:
                                if w.total_count > 0:
                                    row = self.append(
                                        "liquid_per_vehicle_type_table", {}
                                    )
                                    row.fuel_type = x.fuel_type
                                    row.vehicle_type = "لانش"
                                    row.cylinder_count = z.cylinder_count
                                    row.liquid_qty = v.litre_count
                                    row.total_count = w.total_count
                                    row.valid_count = valid_count
                                    row.previously_issued = previous_count
                                    row.plate_count = 0
                                    row.invalid_count = w.total_count - valid_count
                                    row.total_qty = (
                                        self.month_count * v.litre_count * valid_count
                                    )

                gas_vehicle_type_list = frappe.db.sql(
                    """ Select distinct `tabVehicles`.vehicle_type as vehicle_type 
                        from `tabVehicles`
                        Where `tabVehicles`.entity_name = '{entity}'
                        and `tabVehicles`.vehicle_type != "لانش"
                        and `tabVehicles`.gas_count != 0
                    """.format(
                        entity=self.entity
                    ),
                    as_dict=1,
                )

                for y in gas_vehicle_type_list:
                    gas_cylinder_list = frappe.db.sql(
                        """ Select distinct `tabVehicles`.cylinder_count as cylinder_count from `tabVehicles`
                            Where `tabVehicles`.vehicle_type = '{vehicle_type}'
                            and `tabVehicles`.entity_name = '{entity}'
                            and `tabVehicles`.vehicle_type != "لانش"
                            and `tabVehicles`.gas_count != 0
                        """.format(
                            vehicle_type=y.vehicle_type, entity=self.entity
                        ),
                        as_dict=1,
                    )

                    for z in gas_cylinder_list:
                        gas_count_list = frappe.db.sql(
                            """ Select distinct `tabVehicles`.gas_count as gas_count from `tabVehicles`
                                Where `tabVehicles`.vehicle_type = '{vehicle_type}'
                                and `tabVehicles`.cylinder_count = '{cylinder_count}'
                                and `tabVehicles`.entity_name = '{entity}'
                                and `tabVehicles`.vehicle_type != "لانش"
                                and `tabVehicles`.gas_count != 0
                            """.format(
                                vehicle_type=y.vehicle_type,
                                cylinder_count=z.cylinder_count,
                                entity=self.entity,
                            ),
                            as_dict=1,
                        )

                        valid_count = 0
                        previous_count = 0
                        plate_count = 0

                        for v in gas_count_list:
                            gas_total_vehicle_list = frappe.db.sql(
                                """ Select count(`tabVehicles`.name) as total_count from `tabVehicles` 
                                    Where `tabVehicles`.vehicle_type = '{vehicle_type}'
                                    and `tabVehicles`.cylinder_count = '{cylinder_count}'
                                    and `tabVehicles`.gas_count = '{gas_count}'
                                    and `tabVehicles`.vehicle_type != "لانش"
                                    and `tabVehicles`.gas_count != 0
                                    and ((`tabVehicles`.entity_name = '{entity}' and (`tabVehicles`.attached_entity is null or `tabVehicles`.attached_entity = ""))
                                    or (`tabVehicles`.entity_name != '{entity}' and `tabVehicles`.attached_entity = '{entity}'))
                                    and `tabVehicles`.vehicle_status in ("صالحة", "عاطلة", "تحت التخريد")
                                """.format(
                                    gas_count=v.gas_count,
                                    vehicle_type=y.vehicle_type,
                                    cylinder_count=z.cylinder_count,
                                    entity=self.entity,
                                ),
                                as_dict=1,
                            )

                            gas_valid_vehicle_list = frappe.db.sql(
                                """ Select count(`tabVehicles`.name) as valid_count,
                                    `tabVehicles`.name as vehicle,
                                    `tabVehicles`.vehicle_no as vehicle_no,
                                    `tabVehicles`.vehicle_type as vehicle_type,
                                    `tabVehicles`.entity_name as entity_name
                                    from `tabVehicles` 
                                    Where `tabVehicles`.vehicle_type = '{vehicle_type}'
                                    and `tabVehicles`.cylinder_count = '{cylinder_count}'
                                    and `tabVehicles`.gas_count = '{gas_count}'
                                    and `tabVehicles`.vehicle_status = "صالحة"
                                    and ((`tabVehicles`.entity_name = '{entity}' and (`tabVehicles`.attached_entity is null or `tabVehicles`.attached_entity = ""))
                                    or (`tabVehicles`.entity_name != '{entity}' and `tabVehicles`.attached_entity = '{entity}'))
                                    
                                    and `tabVehicles`.exchange_allowance not in ("لوحة فقط", "لوحة وخدمة كاملة فقط")
                                    and `tabVehicles`.vehicle_type != "لانش"
                                    and `tabVehicles`.gas_count != 0
                                    and `tabVehicles`.name not in (select `tabLiquids Issuing Table`.parent 
                                        from `tabLiquids Issuing Table`
                                        where `tabLiquids Issuing Table`.issue_type = '{issue_type}'
                                        and `tabLiquids Issuing Table`.from_date >= '{from_date}'
                                        and `tabLiquids Issuing Table`.to_date <= '{to_date}')
                                """.format(
                                    gas_count=v.gas_count,
                                    vehicle_type=y.vehicle_type,
                                    cylinder_count=z.cylinder_count,
                                    entity=self.entity,
                                    from_date=self.from_date,
                                    to_date=self.to_date,
                                    issue_type=self.issue_type,
                                ),
                                as_dict=1,
                            )

                            gas_previous_vehicle_list = frappe.db.sql(
                                """ Select count(`tabVehicles`.name) as valid_count,
                                    `tabVehicles`.name as vehicle,
                                    `tabVehicles`.vehicle_no as vehicle_no,
                                    `tabVehicles`.vehicle_type as vehicle_type,
                                    `tabVehicles`.entity_name as entity_name
                                    from `tabVehicles` 
                                    Where `tabVehicles`.vehicle_type = '{vehicle_type}'
                                    and `tabVehicles`.cylinder_count = '{cylinder_count}'
                                    and `tabVehicles`.gas_count = '{gas_count}'
                                    and `tabVehicles`.vehicle_status = "صالحة"
                                    and ((`tabVehicles`.entity_name = '{entity}' and (`tabVehicles`.attached_entity is null or `tabVehicles`.attached_entity = ""))
                                    or (`tabVehicles`.entity_name != '{entity}' and `tabVehicles`.attached_entity = '{entity}'))
                                    
                                    and `tabVehicles`.exchange_allowance not in ("لوحة فقط", "لوحة وخدمة كاملة فقط")
                                    and `tabVehicles`.vehicle_type != "لانش"
                                    and `tabVehicles`.gas_count != 0
                                    and `tabVehicles`.name in (select `tabLiquids Issuing Table`.parent 
                                        from `tabLiquids Issuing Table`
                                        where `tabLiquids Issuing Table`.issue_type = '{issue_type}'
                                        and `tabLiquids Issuing Table`.from_date >= '{from_date}'
                                        and `tabLiquids Issuing Table`.to_date <= '{to_date}')
                                """.format(
                                    gas_count=v.gas_count,
                                    vehicle_type=y.vehicle_type,
                                    cylinder_count=z.cylinder_count,
                                    entity=self.entity,
                                    from_date=self.from_date,
                                    to_date=self.to_date,
                                    issue_type=self.issue_type,
                                ),
                                as_dict=1,
                            )

                            gas_plate_only_vehicle_list = frappe.db.sql(
                                """ Select count(`tabVehicles`.name) as valid_count,
                                    `tabVehicles`.name as vehicle,
                                    `tabVehicles`.vehicle_no as vehicle_no,
                                    `tabVehicles`.vehicle_type as vehicle_type,
                                    `tabVehicles`.entity_name as entity_name
                                    from `tabVehicles` 
                                    Where `tabVehicles`.vehicle_type = '{vehicle_type}'
                                    and `tabVehicles`.cylinder_count = '{cylinder_count}'
                                    and `tabVehicles`.gas_count = '{gas_count}'
                                    and ((`tabVehicles`.entity_name = '{entity}' and (`tabVehicles`.attached_entity is null or `tabVehicles`.attached_entity = ""))
                                    or (`tabVehicles`.entity_name != '{entity}' and `tabVehicles`.attached_entity = '{entity}'))
                                    and `tabVehicles`.vehicle_status in ("صالحة","عاطلة","تحت التخريد")
                                    and `tabVehicles`.exchange_allowance in ("لوحة فقط", "لوحة وخدمة كاملة فقط")
                                    and `tabVehicles`.vehicle_type != "لانش"
                                    and `tabVehicles`.gas_count != 0
                                """.format(
                                    gas_count=v.gas_count,
                                    vehicle_type=y.vehicle_type,
                                    cylinder_count=z.cylinder_count,
                                    entity=self.entity,
                                    from_date=self.from_date,
                                    to_date=self.to_date,
                                ),
                                as_dict=1,
                            )

                            for d in gas_valid_vehicle_list:
                                valid_count = d.valid_count

                            for p in gas_previous_vehicle_list:
                                previous_count = p.valid_count

                            for u in gas_plate_only_vehicle_list:
                                plate_count = u.valid_count

                            for w in gas_total_vehicle_list:
                                if w.total_count > 0:
                                    row = self.append("gas_per_vehicle_type_table", {})
                                    row.fuel_type = "غاز طبيعي"
                                    row.vehicle_type = y.vehicle_type
                                    row.cylinder_count = z.cylinder_count
                                    row.liquid_qty = v.gas_count
                                    row.total_count = w.total_count
                                    row.valid_count = valid_count
                                    row.previously_issued = previous_count
                                    row.plate_count = plate_count
                                    row.invalid_count = (
                                        w.total_count
                                        - valid_count
                                        - previous_count
                                        - plate_count
                                    )
                                    row.total_qty = (
                                        self.month_count * v.gas_count * valid_count
                                    )

            #####################################################################

            if self.issue_type == "زيت":
                self.set("liquid_per_vehicle_type_table", [])
                self.set("vehicles_issuing_table", [])
                oil_type_list = frappe.db.sql(
                    """ Select distinct `tabVehicles`.oil_type as oil_type from `tabVehicles`
                        JOIN `tabOil Type` ON `tabOil Type`.name = `tabVehicles`.oil_type
                        where `tabVehicles`.vehicle_type != "لانش"
                        and `tabVehicles`.oil_count != 0
                        AND `tabOil Type`.enabled =1
                        order by `tabOil Type`.litre_count, `tabVehicles`.oil_type desc
                    """.format(
                        entity=self.entity
                    ),
                    as_dict=1,
                )

                for x in oil_type_list:
                    vehicle_type_list = frappe.db.sql(
                        """ Select distinct `tabVehicles`.vehicle_type as vehicle_type from `tabVehicles`
                            Where `tabVehicles`.oil_type = '{oil_type}'
                        """.format(
                            oil_type=x.oil_type, entity=self.entity
                        ),
                        as_dict=1,
                    )

                    for y in vehicle_type_list:
                        cylinder_list = frappe.db.sql(
                            """ Select distinct `tabVehicles`.cylinder_count as cylinder_count from `tabVehicles`
                                Where `tabVehicles`.oil_type = '{oil_type}'
                                and `tabVehicles`.vehicle_type = '{vehicle_type}'
                            """.format(
                                oil_type=x.oil_type,
                                vehicle_type=y.vehicle_type,
                                entity=self.entity,
                            ),
                            as_dict=1,
                        )

                        for z in cylinder_list:
                            oil_count_list = frappe.db.sql(
                                """ Select distinct `tabVehicles`.oil_count as oil_count from `tabVehicles`
                                    Where `tabVehicles`.oil_type = '{oil_type}'
                                    and `tabVehicles`.vehicle_type = '{vehicle_type}'
                                    and `tabVehicles`.cylinder_count = '{cylinder_count}'
                                """.format(
                                    oil_type=x.oil_type,
                                    vehicle_type=y.vehicle_type,
                                    cylinder_count=z.cylinder_count,
                                    entity=self.entity,
                                ),
                                as_dict=1,
                            )

                            valid_count = 0
                            previous_count = 0
                            plate_count = 0

                            for v in oil_count_list:
                                total_vehicle_list = frappe.db.sql(
                                    """ Select count(`tabVehicles`.name) as total_count from `tabVehicles` 
                                        Where `tabVehicles`.oil_type = '{oil_type}'
                                        and `tabVehicles`.vehicle_type = '{vehicle_type}'
                                        and `tabVehicles`.cylinder_count = '{cylinder_count}'
                                        and `tabVehicles`.oil_count = '{oil_count}'
                                        and ((`tabVehicles`.entity_name = '{entity}' and (`tabVehicles`.attached_entity is null or `tabVehicles`.attached_entity = ""))
                                        or (`tabVehicles`.entity_name != '{entity}' and `tabVehicles`.attached_entity = '{entity}'))
                                        and `tabVehicles`.vehicle_status in ("صالحة", "عاطلة", "تحت التخريد")

                                    """.format(
                                        oil_count=v.oil_count,
                                        oil_type=x.oil_type,
                                        vehicle_type=y.vehicle_type,
                                        cylinder_count=z.cylinder_count,
                                        entity=self.entity,
                                    ),
                                    as_dict=1,
                                )

                                valid_vehicle_list = frappe.db.sql(
                                    """ Select count(`tabVehicles`.name) as valid_count,
                                        `tabVehicles`.name as vehicle,
                                        `tabVehicles`.vehicle_no as vehicle_no,
                                        `tabVehicles`.vehicle_type as vehicle_type,
                                        `tabVehicles`.entity_name as entity_name
                                        from `tabVehicles` 
                                        Where `tabVehicles`.oil_type = '{oil_type}'
                                        and `tabVehicles`.vehicle_type = '{vehicle_type}'
                                        and `tabVehicles`.cylinder_count = '{cylinder_count}'
                                        and `tabVehicles`.oil_count = '{oil_count}'
                                        and `tabVehicles`.vehicle_status = "صالحة"
                                        and ((`tabVehicles`.entity_name = '{entity}' and (`tabVehicles`.attached_entity is null or `tabVehicles`.attached_entity = ""))
                                        or (`tabVehicles`.entity_name != '{entity}' and `tabVehicles`.attached_entity = '{entity}'))
                                        and `tabVehicles`.exchange_allowance not in ("لوحة فقط", "لوحة وخدمة كاملة فقط")
                                        and `tabVehicles`.name not in (select `tabLiquids Issuing Table`.parent 
                                            from `tabLiquids Issuing Table`
                                            where `tabLiquids Issuing Table`.issue_type = '{issue_type}'
                                            and `tabLiquids Issuing Table`.from_date >= '{from_date}'
                                            and `tabLiquids Issuing Table`.to_date <= '{to_date}')
                                    """.format(
                                        oil_count=v.oil_count,
                                        oil_type=x.oil_type,
                                        vehicle_type=y.vehicle_type,
                                        cylinder_count=z.cylinder_count,
                                        entity=self.entity,
                                        from_date=self.from_date,
                                        to_date=self.to_date,
                                        issue_type=self.issue_type,
                                    ),
                                    as_dict=1,
                                )

                                previous_vehicle_list = frappe.db.sql(
                                    """ Select count(`tabVehicles`.name) as valid_count,
                                        `tabVehicles`.name as vehicle,
                                        `tabVehicles`.vehicle_no as vehicle_no,
                                        `tabVehicles`.vehicle_type as vehicle_type,
                                        `tabVehicles`.entity_name as entity_name
                                        from `tabVehicles` 
                                        Where `tabVehicles`.oil_type = '{oil_type}'
                                        and `tabVehicles`.vehicle_type = '{vehicle_type}'
                                        and `tabVehicles`.cylinder_count = '{cylinder_count}'
                                        and `tabVehicles`.oil_count = '{oil_count}'
                                        and `tabVehicles`.vehicle_status = "صالحة"
                                        and ((`tabVehicles`.entity_name = '{entity}' and (`tabVehicles`.attached_entity is null or `tabVehicles`.attached_entity = ""))
                                        or (`tabVehicles`.entity_name != '{entity}' and `tabVehicles`.attached_entity = '{entity}'))
                                        and `tabVehicles`.exchange_allowance not in ("لوحة فقط", "لوحة وخدمة كاملة فقط")
                                        and `tabVehicles`.name in (select `tabLiquids Issuing Table`.parent 
                                            from `tabLiquids Issuing Table`
                                            where `tabLiquids Issuing Table`.issue_type = '{issue_type}'
                                            and `tabLiquids Issuing Table`.from_date >= '{from_date}'
                                            and `tabLiquids Issuing Table`.to_date <= '{to_date}')
                                    """.format(
                                        oil_count=v.oil_count,
                                        oil_type=x.oil_type,
                                        vehicle_type=y.vehicle_type,
                                        cylinder_count=z.cylinder_count,
                                        entity=self.entity,
                                        from_date=self.from_date,
                                        to_date=self.to_date,
                                        issue_type=self.issue_type,
                                    ),
                                    as_dict=1,
                                )

                                plate_only_vehicle_list = frappe.db.sql(
                                    """ Select count(`tabVehicles`.name) as valid_count,
                                        `tabVehicles`.name as vehicle,
                                        `tabVehicles`.vehicle_no as vehicle_no,
                                        `tabVehicles`.vehicle_type as vehicle_type,
                                        `tabVehicles`.entity_name as entity_name
                                        from `tabVehicles` 
                                        Where `tabVehicles`.oil_type = '{oil_type}'
                                        and `tabVehicles`.vehicle_type = '{vehicle_type}'
                                        and `tabVehicles`.cylinder_count = '{cylinder_count}'
                                        and `tabVehicles`.oil_count = '{oil_count}'
                                        and ((`tabVehicles`.entity_name = '{entity}' and (`tabVehicles`.attached_entity is null or `tabVehicles`.attached_entity = ""))
                                        or (`tabVehicles`.entity_name != '{entity}' and `tabVehicles`.attached_entity = '{entity}'))
                                        and `tabVehicles`.exchange_allowance in ("لوحة فقط", "لوحة وخدمة كاملة فقط")
                                        and `tabVehicles`.vehicle_status in ("صالحة","عاطلة","تحت التخريد")
                                    """.format(
                                        oil_count=v.oil_count,
                                        oil_type=x.oil_type,
                                        vehicle_type=y.vehicle_type,
                                        cylinder_count=z.cylinder_count,
                                        entity=self.entity,
                                        from_date=self.from_date,
                                        to_date=self.to_date,
                                    ),
                                    as_dict=1,
                                )

                                for d in valid_vehicle_list:
                                    valid_count = d.valid_count

                                for p in previous_vehicle_list:
                                    previous_count = p.valid_count

                                for u in plate_only_vehicle_list:
                                    plate_count = u.valid_count

                                for w in total_vehicle_list:
                                    if w.total_count > 0:
                                        row = self.append(
                                            "liquid_per_vehicle_type_table", {}
                                        )
                                        row.fuel_type = x.oil_type
                                        row.vehicle_type = y.vehicle_type
                                        row.cylinder_count = z.cylinder_count
                                        # row.liquid_qty = v.oil_count
                                        row.liquid_qty = 1
                                        row.total_count = w.total_count
                                        row.valid_count = valid_count
                                        row.previously_issued = previous_count
                                        row.plate_count = plate_count
                                        row.invalid_count = (
                                            w.total_count
                                            - valid_count
                                            - previous_count
                                            - plate_count
                                        )
                                        # row.total_qty = v.oil_count * valid_count
                                        row.total_qty = valid_count

                check_coupon_field = frappe.db.sql(
                    """ Select `tabVehicles`.name as vehicle,
                        `tabVehicles`.vehicle_no as vehicle_no,
                        `tabVehicles`.vehicle_type as vehicle_type,
                        `tabVehicles`.entity_name as entity_name,
                        `tabVehicles`.oil_type as oil_type,
                        `tabVehicles`.oil_count as oil_count
                        from `tabVehicles` 
                        Where `tabVehicles`.vehicle_status = "صالحة"
                        and ((`tabVehicles`.entity_name = '{entity}' and (`tabVehicles`.attached_entity is null or `tabVehicles`.attached_entity = ""))
                        or (`tabVehicles`.entity_name != '{entity}' and `tabVehicles`.attached_entity = '{entity}'))
                        and `tabVehicles`.exchange_allowance not in ("لوحة فقط", "لوحة وخدمة كاملة فقط")
                        and `tabVehicles`.vehicle_type != "لانش"
                        and `tabVehicles`.name not in (select `tabLiquids Issuing Table`.parent 
                            from `tabLiquids Issuing Table`
                            where `tabLiquids Issuing Table`.issue_type = '{issue_type}'
                            and `tabLiquids Issuing Table`.from_date >= '{from_date}' 
                            and `tabLiquids Issuing Table`.to_date <= '{to_date}')
                    """.format(
                        entity=self.entity,
                        from_date=self.from_date,
                        to_date=self.to_date,
                        issue_type=self.issue_type,
                    ),
                    as_dict=1,
                )

                for row in check_coupon_field:
                    if not row.oil_type or not row.oil_count:
                        if self.seen_vehicles == 0:
                            frappe.msgprint(
                                "المركبة رقم "
                                + str(row.vehicle_no)
                                + "  ليس لها قاعدة صرف الزيت"
                            )
                self.seen_vehicles = 1

            ############################################

            if self.issue_type == "غسيل":
                self.set("liquid_per_vehicle_type_table", [])
                self.set("vehicles_issuing_table", [])

                washing_type_list = frappe.db.sql(
                    """ Select distinct `tabVehicles`.washing_voucher as washing_voucher from `tabVehicles`
                        where `tabVehicles`.entity_name = '{entity}'
                        and `tabVehicles`.vehicle_type != "لانش"
                        and `tabVehicles`.washing_count != 0
                        order by `tabVehicles`.washing_voucher
                    """.format(
                        entity=self.entity
                    ),
                    as_dict=1,
                )

                for x in washing_type_list:
                    vehicle_type_list = frappe.db.sql(
                        """ Select distinct `tabVehicles`.vehicle_type as vehicle_type from `tabVehicles`
                            Where `tabVehicles`.washing_voucher = '{washing_voucher}'
                            and `tabVehicles`.entity_name = '{entity}'
                        """.format(
                            washing_voucher=x.washing_voucher, entity=self.entity
                        ),
                        as_dict=1,
                    )

                    for y in vehicle_type_list:
                        cylinder_list = frappe.db.sql(
                            """ Select distinct `tabVehicles`.cylinder_count as cylinder_count from `tabVehicles`
                                Where `tabVehicles`.washing_voucher = '{washing_voucher}'
                                and `tabVehicles`.vehicle_type = '{vehicle_type}'
                                and `tabVehicles`.entity_name = '{entity}'
                            """.format(
                                washing_voucher=x.washing_voucher,
                                vehicle_type=y.vehicle_type,
                                entity=self.entity,
                            ),
                            as_dict=1,
                        )

                        for z in cylinder_list:
                            washing_count_list = frappe.db.sql(
                                """ Select distinct `tabVehicles`.washing_count as washing_count from `tabVehicles`
                                    Where `tabVehicles`.washing_voucher = '{washing_voucher}'
                                    and `tabVehicles`.vehicle_type = '{vehicle_type}'
                                    and `tabVehicles`.cylinder_count = '{cylinder_count}'
                                    and `tabVehicles`.entity_name = '{entity}'
                                """.format(
                                    washing_voucher=x.washing_voucher,
                                    vehicle_type=y.vehicle_type,
                                    cylinder_count=z.cylinder_count,
                                    entity=self.entity,
                                ),
                                as_dict=1,
                            )

                            valid_count = 0
                            previous_count = 0
                            plate_count = 0

                            for v in washing_count_list:
                                total_vehicle_list = frappe.db.sql(
                                    """ Select count(`tabVehicles`.name) as total_count from `tabVehicles` 
                                        Where `tabVehicles`.washing_voucher = '{washing_voucher}'
                                        and `tabVehicles`.vehicle_type = '{vehicle_type}'
                                        and `tabVehicles`.cylinder_count = '{cylinder_count}'
                                        and `tabVehicles`.washing_count = '{washing_count}'
                                        and `tabVehicles`.entity_name = '{entity}'
                                    """.format(
                                        washing_count=v.washing_count,
                                        washing_voucher=x.washing_voucher,
                                        vehicle_type=y.vehicle_type,
                                        cylinder_count=z.cylinder_count,
                                        entity=self.entity,
                                    ),
                                    as_dict=1,
                                )

                                valid_vehicle_list = frappe.db.sql(
                                    """ Select count(`tabVehicles`.name) as valid_count,
                                        `tabVehicles`.name as vehicle,
                                        `tabVehicles`.vehicle_no as vehicle_no,
                                        `tabVehicles`.vehicle_type as vehicle_type,
                                        `tabVehicles`.entity_name as entity_name
                                        from `tabVehicles` 
                                        Where `tabVehicles`.washing_voucher = '{washing_voucher}'
                                        and `tabVehicles`.vehicle_type = '{vehicle_type}'
                                        and `tabVehicles`.cylinder_count = '{cylinder_count}'
                                        and `tabVehicles`.washing_count = '{washing_count}'
                                        and `tabVehicles`.vehicle_status = "صالحة"
                                        and `tabVehicles`.entity_name = '{entity}'
                                        and `tabVehicles`.exchange_allowance not in ("لوحة فقط", "لوحة وخدمة كاملة فقط")
                                        and `tabVehicles`.name not in (select `tabLiquids Issuing Table`.parent 
                                            from `tabLiquids Issuing Table`
                                            where `tabLiquids Issuing Table`.issue_type = '{issue_type}'
                                            and `tabLiquids Issuing Table`.from_date >= '{from_date}'
                                            and `tabLiquids Issuing Table`.to_date <= '{to_date}')
                                    """.format(
                                        washing_count=v.washing_count,
                                        washing_voucher=x.washing_voucher,
                                        vehicle_type=y.vehicle_type,
                                        cylinder_count=z.cylinder_count,
                                        entity=self.entity,
                                        from_date=self.from_date,
                                        to_date=self.to_date,
                                        issue_type=self.issue_type,
                                    ),
                                    as_dict=1,
                                )

                                previous_vehicle_list = frappe.db.sql(
                                    """ Select count(`tabVehicles`.name) as valid_count,
                                        `tabVehicles`.name as vehicle,
                                        `tabVehicles`.vehicle_no as vehicle_no,
                                        `tabVehicles`.vehicle_type as vehicle_type,
                                        `tabVehicles`.entity_name as entity_name
                                        from `tabVehicles` 
                                        Where `tabVehicles`.washing_voucher = '{washing_voucher}'
                                        and `tabVehicles`.vehicle_type = '{vehicle_type}'
                                        and `tabVehicles`.cylinder_count = '{cylinder_count}'
                                        and `tabVehicles`.washing_count = '{washing_count}'
                                        and `tabVehicles`.vehicle_status = "صالحة"
                                        and `tabVehicles`.entity_name = '{entity}'
                                        and `tabVehicles`.exchange_allowance not in ("لوحة فقط", "لوحة وخدمة كاملة فقط")
                                        and `tabVehicles`.name in (select `tabLiquids Issuing Table`.parent 
                                            from `tabLiquids Issuing Table`
                                            where `tabLiquids Issuing Table`.issue_type = '{issue_type}'
                                            and `tabLiquids Issuing Table`.from_date >= '{from_date}'
                                            and `tabLiquids Issuing Table`.to_date <= '{to_date}')
                                    """.format(
                                        washing_count=v.washing_count,
                                        washing_voucher=x.washing_voucher,
                                        vehicle_type=y.vehicle_type,
                                        cylinder_count=z.cylinder_count,
                                        entity=self.entity,
                                        from_date=self.from_date,
                                        to_date=self.to_date,
                                        issue_type=self.issue_type,
                                    ),
                                    as_dict=1,
                                )

                                plate_only_vehicle_list = frappe.db.sql(
                                    """ Select count(`tabVehicles`.name) as valid_count,
                                        `tabVehicles`.name as vehicle,
                                        `tabVehicles`.vehicle_no as vehicle_no,
                                        `tabVehicles`.vehicle_type as vehicle_type,
                                        `tabVehicles`.entity_name as entity_name
                                        from `tabVehicles` 
                                        Where `tabVehicles`.washing_voucher = '{washing_voucher}'
                                        and `tabVehicles`.vehicle_type = '{vehicle_type}'
                                        and `tabVehicles`.cylinder_count = '{cylinder_count}'
                                        and `tabVehicles`.washing_count = '{washing_count}'
                                        and `tabVehicles`.vehicle_status in ("صالحة","عاطلة","تحت التخريد")
                                        and `tabVehicles`.entity_name = '{entity}'
                                        and `tabVehicles`.exchange_allowance in ("لوحة فقط", "لوحة وخدمة كاملة فقط")
                                    """.format(
                                        washing_count=v.washing_count,
                                        washing_voucher=x.washing_voucher,
                                        vehicle_type=y.vehicle_type,
                                        cylinder_count=z.cylinder_count,
                                        entity=self.entity,
                                        from_date=self.from_date,
                                        to_date=self.to_date,
                                    ),
                                    as_dict=1,
                                )

                                for d in valid_vehicle_list:
                                    valid_count = d.valid_count

                                for p in previous_vehicle_list:
                                    previous_count = p.valid_count

                                for u in plate_only_vehicle_list:
                                    plate_count = u.valid_count

                                for w in total_vehicle_list:
                                    row = self.append(
                                        "liquid_per_vehicle_type_table", {}
                                    )
                                    row.fuel_type = x.washing_voucher
                                    row.vehicle_type = y.vehicle_type
                                    row.cylinder_count = z.cylinder_count
                                    row.liquid_qty = v.washing_count
                                    row.total_count = w.total_count
                                    row.valid_count = valid_count
                                    row.previously_issued = previous_count
                                    row.plate_count = plate_count
                                    row.invalid_count = (
                                        w.total_count
                                        - valid_count
                                        - previous_count
                                        - plate_count
                                    )
                                    row.total_qty = v.washing_count * valid_count

                check_coupon_field = frappe.db.sql(
                    """ Select `tabVehicles`.name as vehicle,
                        `tabVehicles`.vehicle_no as vehicle_no,
                        `tabVehicles`.vehicle_type as vehicle_type,
                        `tabVehicles`.entity_name as entity_name,
                        `tabVehicles`.washing_count as washing_count
                        from `tabVehicles` 
                        Where `tabVehicles`.vehicle_status = "صالحة"
                        and `tabVehicles`.entity_name = '{entity}'
                        and `tabVehicles`.exchange_allowance not in ("لوحة فقط", "لوحة وخدمة كاملة فقط")
                        and `tabVehicles`.name not in (select `tabLiquids Issuing Table`.parent 
                            from `tabLiquids Issuing Table`
                            where `tabLiquids Issuing Table`.issue_type = '{issue_type}'
                            and `tabLiquids Issuing Table`.from_date >= '{from_date}' 
                            and `tabLiquids Issuing Table`.to_date <= '{to_date}')
                        and `tabVehicles`.vehicle_type != "مقطورة"
                    """.format(
                        entity=self.entity,
                        from_date=self.from_date,
                        to_date=self.to_date,
                        issue_type=self.issue_type,
                    ),
                    as_dict=1,
                )

                for row in check_coupon_field:
                    if not row.washing_voucher or not row.washing_count:
                        if not self.seen_vehicles:
                            frappe.msgprint(
                                "المركبة رقم "
                                + str(row.vehicle_no)
                                + "  ليس لها قاعدة صرف الغسيل"
                            )
                self.seen_vehicles = 1

            ############################################

            ### Calculate Total Section
            total_vehicles_count = 0
            invalid_vehicles_count = 0
            valid_vehicles_count = 0
            total_liquid_count = 0
            previously_issued_count = 0
            plates_only_count = 0

            for t in self.liquid_per_vehicle_type_table:
                total_vehicles_count += t.total_count
                invalid_vehicles_count += t.invalid_count
                valid_vehicles_count += t.valid_count
                previously_issued_count += t.previously_issued
                plates_only_count += t.plate_count
                total_liquid_count += t.total_qty

            self.total_vehicles_count = total_vehicles_count
            self.invalid_vehicles_count = (
                invalid_vehicles_count + previously_issued_count
            )
            self.valid_vehicles_count = valid_vehicles_count
            self.total_liquid_count = total_liquid_count
            self.previously_issued_count = previously_issued_count
            self.plates_only_count = plates_only_count

            liquid = self.get_liquids()
            for h in liquid:
                sum_qty = self.get_sum_qty(h)
                rows = self.append("qty_per_liquid", {})
                rows.liquid = h
                rows.vehicles_count = self.get_vehicles_count(h)
                rows.qty = sum_qty
                rows.in_words = in_words(sum_qty)
            if self.issue_type == "وقود":
                gas = ["غاز طبيعي"]
                for u in gas:
                    sum_qty1 = self.get_gas_sum_qty(h)
                    rowss = self.append("qty_per_liquid", {})
                    rowss.liquid = u
                    rowss.vehicles_count = self.get_vehicles_count(u)
                    rowss.qty = sum_qty1
                    rowss.in_words = in_words(sum_qty1)

        if self.issue_to == "مركبة أو مجموعة مركبات":
            self.set("vehicles_issuing_table", [])
            self.set("liquid_per_vehicle_type_table", [])
            self.set("qty_per_liquid", [])
            self.set("gas_per_vehicle_type_table", [])

            self.total_vehicles_count = 0
            self.invalid_vehicles_count = 0
            self.valid_vehicles_count = 0
            self.total_liquid_count = 0
            self.previously_issued_count = 0
            self.plates_only_count = 0

            if not self.specified_vehicles_issuing_table:
                frappe.throw(" برجاء تحديد المركبات التي سيتم الصرف لها ")
            sum_gas_qty = 0
            vehicle_count = 0
            for t in self.specified_vehicles_issuing_table:
                if t.vehicle_boat != "Boats":
                    t.vehicle_no = frappe.db.get_value(
                        "Vehicles", t.vehicle, "vehicle_no"
                    )
                    t.vehicle_type = frappe.db.get_value(
                        "Vehicles", t.vehicle, "vehicle_type"
                    )
                    vehicle_issue_list = frappe.db.sql(
                        """ Select idx, issue_type, from_date, to_date, entity, qty , issue_no
                            from `tabLiquids Issuing Table` 
                            where parent = '{parent}' and issue_type = '{issue_type}'
                            order by to_date  desc, from_date desc limit 1
                        """.format(
                            parent=t.vehicle, issue_type=self.issue_type
                        ),
                        as_dict=1,
                    )
                    frappe.msgprint(str(vehicle_issue_list))
                    for q in vehicle_issue_list:
                        t.last_issue_from_date = q.from_date
                        t.last_issue_to_date = q.to_date
                        t.entity_name = q.entity
                        t.last_issue_qty = q.qty
                        if (
                            float(q.qty) > 0
                            and getdate(q.from_date) >= getdate(self.from_date)
                            and getdate(q.from_date) <= getdate(self.to_date)
                        ):
                            frappe.throw(
                                " الصف # "
                                + str(q.idx)
                                + " : لا يمكن صرف "
                                + self.issue_type
                                + " إلى المركبة "
                                + str(t.vehicle_no)
                                + " حيث أنه تم الصرف لها من قبل خلال الفترة المحددة إلى جهة "
                                + str(q.entity)
                                + "\n \t \t \t \t \t \t \t \t \t "
                                + "صرفية رقم "
                                + str(q.issue_no)
                            )

                        if (
                            float(q.qty) > 0
                            and getdate(q.to_date) >= getdate(self.from_date)
                            and getdate(q.to_date) <= getdate(self.to_date)
                        ):
                            frappe.throw(
                                " الصف # "
                                + str(q.idx)
                                + " : لا يمكن صرف "
                                + self.issue_type
                                + " إلى المركبة "
                                + str(t.vehicle_no)
                                + " حيث أنه تم الصرف لها من قبل خلال الفترة المحددة إلى جهة "
                                + str(q.entity)
                                + "\n \t \t \t \t \t \t \t \t \t "
                                + "صرفية رقم "
                                + str(q.issue_no)
                            )
                    if self.issue_type == "وقود":
                        t.qty = (
                            self.issue_days
                            * frappe.db.get_value("Vehicles", t.vehicle, "litre_count")
                            / 30
                        )
                        t.liquid = frappe.db.get_value(
                            "Vehicles", t.vehicle, "fuel_type"
                        )
                    if self.issue_type == "زيت":
                        t.qty = 1
                        t.liquid = frappe.db.get_value(
                            "Vehicles", t.vehicle, "oil_type"
                        )

                    if self.issue_type == "غسيل":
                        t.qty = 1
                        t.liquid = frappe.db.get_value(
                            "Vehicles", t.vehicle, "washing_voucher"
                        )
                    liquid = "غاز طبيعي"
                    gas_valid_vehicle_list = frappe.db.sql(
                        """ Select
                            `tabVehicles`.name as vehicle,
                            `tabVehicles`.gas_count as gas_count
                            from `tabVehicles` 
                            where `tabVehicles`.name = '{vehicle}'
                            and `tabVehicles`.gas_count > 0
                            and `tabVehicles`.name not in (select `tabLiquids Issuing Table`.parent 
                                from `tabLiquids Issuing Table`
                                where `tabLiquids Issuing Table`.issue_type = '{issue_type}'
                                and `tabLiquids Issuing Table`.from_date >= '{from_date}'
                                and `tabLiquids Issuing Table`.to_date <= '{to_date}')
                        """.format(
                            from_date=self.from_date,
                            to_date=self.to_date,
                            issue_type="غاز",
                            vehicle=t.vehicle,
                        ),
                        as_dict=1,
                    )
                    current_vehicles = []
                    if gas_valid_vehicle_list:
                        current_vehicles.append(t.vehicle)
                        vehicle_status = frappe.db.get_value(
                            "Vehicles", t.vehicle, "vehicle_status"
                        )
                        voucher = ""
                        voucher1 = ""
                        record_name = 1
                        max_id = frappe.db.sql(
                            """
                            SELECT MAX(name) as max_name
                            FROM `tabLiquids Issuing Table`
                            """,
                            as_dict=1,
                        )
                        if frappe.db.exists("Liquids Issuing Table", 1):
                            record_name = int(max_id[0]["max_name"]) + 1
                        voucher = "غاز طبيعي فئة 15 متر مكعب"
                        voucher1 = "لا يوجد"
                        # frappe.throw(str(gas_valid_vehicle_list))
                        sum_gas_qty += (
                            self.issue_days * gas_valid_vehicle_list[0].gas_count / 30
                        )
                        vehicle_count += 1
                else:
                    t.vehicle_no = frappe.db.get_value("Boats", t.vehicle, "boat_no")
                    t.vehicle_type = "لانش"

                    vehicle_issue_list = frappe.db.sql(
                        """ Select idx, issue_type, from_date, to_date, entity, qty , issue_no
                            from `tabLiquids Issuing Table` 
                            where parent = '{parent}' and issue_type = '{issue_type}'
                            order by to_date  desc, from_date desc limit 1
                        """.format(
                            parent=t.vehicle, issue_type=self.issue_type
                        ),
                        as_dict=1,
                    )
                    # frappe.msgprint(str(vehicle_issue_list))
                    for q in vehicle_issue_list:
                        t.last_issue_from_date = q.from_date
                        t.last_issue_to_date = q.to_date
                        t.entity_name = q.entity
                        t.last_issue_qty = q.qty
                        if (
                            float(q.qty) > 0
                            and getdate(q.from_date) >= getdate(self.from_date)
                            and getdate(q.from_date) <= getdate(self.to_date)
                        ):
                            frappe.throw(
                                " الصف # "
                                + str(q.idx)
                                + " : لا يمكن صرف "
                                + self.issue_type
                                + " إلى المركبة "
                                + str(t.vehicle_no)
                                + " حيث أنه تم الصرف لها من قبل خلال الفترة المحددة إلى جهة "
                                + str(q.entity)
                                + "\n \t \t \t \t \t \t \t \t \t "
                                + "صرفية رقم "
                                + str(q.issue_no)
                            )

                        if (
                            float(q.qty) > 0
                            and getdate(q.to_date) >= getdate(self.from_date)
                            and getdate(q.to_date) <= getdate(self.to_date)
                        ):
                            frappe.throw(
                                " الصف # "
                                + str(q.idx)
                                + " : لا يمكن صرف "
                                + self.issue_type
                                + " إلى المركبة "
                                + str(t.vehicle_no)
                                + " حيث أنه تم الصرف لها من قبل خلال الفترة المحددة إلى جهة "
                                + str(q.entity)
                                + "\n \t \t \t \t \t \t \t \t \t "
                                + "صرفية رقم "
                                + str(q.issue_no)
                            )
                    if self.issue_type == "وقود":
                        t.qty = (
                            self.issue_days
                            * frappe.db.get_value("Boats", t.vehicle, "qty")
                            / 30
                        )
                        t.liquid = frappe.db.get_value("Boats", t.vehicle, "fuel_type")
            liquid = self.get_liquids()
            for h in liquid:
                sum_qty = self.get_sum_qty(h)
                rows = self.append("qty_per_liquid", {})
                rows.liquid = h
                rows.vehicles_count = self.get_vehicles_count(h)
                rows.qty = sum_qty
                rows.in_words = in_words(sum_qty)
            if self.issue_type == "وقود":
                rows = self.append("qty_per_liquid", {})
                rows.liquid = "غاز طبيعي"
                rows.vehicles_count = vehicle_count
                rows.qty = sum_gas_qty
                rows.in_words = in_words(sum_gas_qty)

    def on_submit(self):
        pass

    def on_trash(self):
        self.issue_state = "تم إلغاء تحضير الصرفية"
        if self.issue_to == "جهة":
            current_vehicles = []
            vehicles = frappe.db.sql(
                """
                    SELECT `tabVehicles`.name as vehicle
                    FROM `tabVehicles`
                    JOIN `tabLiquids Issuing Table` ON `tabLiquids Issuing Table`.parent = `tabVehicles`.name
                    WHERE `tabLiquids Issuing Table`.issue_no = '{issue_no}'
                    """.format(
                    issue_no=self.name
                ),
                as_dict=1,
            )

            for row in vehicles:
                current_vehicles.append(row.vehicle)
            frappe.db.sql(
                """ DELETE FROM `tabLiquids Issuing Table` where issue_no = '{issue_no}' 
                """.format(
                    issue_no=self.name
                )
            )

            if len(current_vehicles) == 1:
                current_vehicles.append("None")
            if self.submitted:
                not_in_vehicle_table = frappe.db.sql(
                    """
                                select name
                                from `tabVehicles` 
                                where entity_name = '{cur_entity}'
                                and name not in {current_vehicles}
                            """.format(
                        cur_entity=self.entity, current_vehicles=tuple(current_vehicles)
                    ),
                    as_dict=1,
                )

                for z in not_in_vehicle_table:
                    frappe.db.sql(
                        """ DELETE FROM `tabLiquids Issuing Table` where issue_no = '{issue_no}' and parent = '{parent}'
                                    """.format(
                            issue_no=self.name, parent=z.name
                        )
                    )

                not_in_boat_table = frappe.db.sql(
                    """
                            select name
                            from `tabBoats` 
                            where entity_name = '{cur_entity}'
                            and name not in {current_vehicles}
                        """.format(
                        cur_entity=self.entity, current_vehicles=tuple(current_vehicles)
                    ),
                    as_dict=1,
                )

                for w in not_in_boat_table:
                    frappe.db.sql(
                        """ DELETE FROM `tabLiquids Issuing Table` where issue_no = '{issue_no}' and parent = '{parent}'
                                    """.format(
                            issue_no=self.name, parent=w.name
                        )
                    )

        if self.issue_to == "مركبة أو مجموعة مركبات":
            frappe.db.sql(
                """ DELETE FROM `tabLiquids Issuing Table` where issue_no = '{issue_no}' 
                            """.format(
                    issue_no=self.name
                )
            )


@frappe.whitelist()
def remove_duplicated_privateno():
    query = frappe.db.sql(
        """
        SELECT `tabVehicles`.name, `tabVehicles`.private_no, `tabPrivate Plate Logs`.date
        From `tabVehicles`
        JOIN `tabPrivate Plate Logs` ON `tabVehicles`.name = `tabPrivate Plate Logs`.parent
        where `tabVehicles`.private_no = `tabPrivate Plate Logs`.value
        and `tabPrivate Plate Logs`.idx = (select max(idx) from `tabPrivate Plate Logs` where `tabPrivate Plate Logs`.parent = `tabVehicles`.name)
        ORDER BY `tabPrivate Plate Logs`.date DESC
        """,
        as_dict=1,
    )
    formatted_dict = {}
    for row in query:
        if row.private_no not in formatted_dict:
            formatted_dict[row.private_no] = [{row.name: row.date}]
        else:
            formatted_dict[row.private_no].append({row.name: row.date})
    filtered_dict = []
    for row in formatted_dict:
        if len(formatted_dict[row]) > 1:
            filtered_dict.append({row: formatted_dict[row]})
    print(filtered_dict)
    for row in filtered_dict:
        for private_no in row:
            for vehicle in row[private_no][1:]:
                for vehicle_name in vehicle:
                    frappe.db.sql(
                        """
                        Update `tabVehicles`
                        set private_no = NULL
                        where name = "{vehicle_name}"
                        """.format(
                            vehicle_name=vehicle_name, private_no=private_no
                        )
                    )
                    frappe.db.commit()
