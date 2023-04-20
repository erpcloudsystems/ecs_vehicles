# Copyright (c) 2022, ERP CLOUD SYSTEMS and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import getdate
from frappe.utils import in_words


class LiquidsIssuing(Document):
    def validate(self):
        current_issue = " من " + str(self.from_date) + " إلى " + str(self.to_date)
        self.current_issue = current_issue

        if getdate(self.from_date) > getdate(self.to_date):
            frappe.throw(" تاريخ نهاية الصرفية لا يمكن أن يكون قبل تاريخ بداية الصرفية ")

        if self.issue_to == "جهة":
            self.set("specified_vehicles_issuing_table", [])
            self.set("qty_per_liquid", [])
            self.set("fixed_vehicles", [])
            self.set("broken_vehicles", [])
            self.set("scraped_vehicles", [])
            self.set("transferred_to_vehicles", [])
            self.set("transferred_from_vehicles", [])
            self.set("previous_vehicles_issuing_table", [])
            self.set("gas_per_vehicle_type_table", [])

            # if frappe.db.exists('Liquids Issuing', {"docstatus": 1, "issue_to": self.issue_to, "entity": self.entity,
            #                                         "issue_type": self.issue_type}):
                # last_doc = frappe.get_last_doc('Liquids Issuing',
                #                                {"docstatus": 1, "issue_to": self.issue_to, "entity": self.entity,
                #                                 "issue_type": self.issue_type})

            last_doc = frappe.db.sql("""
                SELECT `tabLiquids Issuing`.name as name, `tabLiquids Issuing`.from_date as from_date, `tabLiquids Issuing`.to_date as to_date
                FROM `tabLiquids Issuing`
                WHERE `tabLiquids Issuing`.docstatus = 1 
                AND `tabLiquids Issuing`.issue_to = "{issue_to}"
                AND `tabLiquids Issuing`.entity = "{entity}"
                AND `tabLiquids Issuing`.issue_type = "{issue_type}"
                ORDER BY `tabLiquids Issuing`.from_date DESC
                LIMIT 1 
            """.format(issue_to=self.issue_to, entity=self.entity, issue_type=self.issue_type), as_dict=1)

            issue_list = frappe.db.get_list('Liquids Issuing',
                                           {"docstatus": 1, "issue_to": self.issue_to, "entity": self.entity,
                                            "issue_type": self.issue_type}, ["from_date", "to_date"])

            for m in issue_list:
                if getdate(self.from_date) >= getdate(m.from_date) and getdate(self.from_date) <= getdate(m.to_date):
                    frappe.throw(
                        " لا يمكن صرف " + self.issue_type + " إلى " + self.entity + " حيث أنه تم الصرف من قبل خلال الفترة المحددة ")

                if getdate(self.to_date) >= getdate(m.from_date) and getdate(self.to_date) <= getdate(
                        m.to_date):
                    frappe.throw(
                        " لا يمكن صرف " + self.issue_type + " إلى " + self.entity + " حيث أنه تم الصرف من قبل خلال الفترة المحددة ")

            if last_doc:
                last_issue = " من " + str(last_doc[0].from_date) + " إلى " + str(last_doc[0].to_date)
                self.last_issue = last_issue

                start_date = getdate(last_doc[0].issue_date)
                end_date = getdate(self.issue_date)


                previous_vehicles = frappe.db.sql(
                    """ Select 
                        `tabVehicles`.name as vehicle,
                        `tabVehicles`.vehicle_no as vehicle_no,
                        `tabVehicles`.vehicle_type as vehicle_type,
                        `tabVehicles`.entity_name as entity_name
                         from `tabVehicles` 
                         Where `tabVehicles`.vehicle_status = "صالحة"
                         and `tabVehicles`.entity_name = '{entity}'
                         and `tabVehicles`.exchange_allowance not in ("لوحة فقط", "لوحة وخدمة كاملة فقط")
                         and `tabVehicles`.vehicle_type != "لانش"
                         and `tabVehicles`.fuel_type != "بدون وقود"
                         and `tabVehicles`.litre_count != 0
                         and `tabVehicles`.name in (select `tabLiquids Issuing Table`.parent 
                              from `tabLiquids Issuing Table`
                              where `tabLiquids Issuing Table`.issue_type = '{issue_type}'
                              and `tabLiquids Issuing Table`.from_date >= '{from_date}'
                              and `tabLiquids Issuing Table`.to_date <= '{to_date}')
                    """.format(entity=self.entity, from_date=self.from_date,
                               to_date=self.to_date, issue_type=self.issue_type), as_dict=1)

                for q in previous_vehicles:
                    vehicle_issue_list_ = frappe.db.sql(
                        """ Select from_date, to_date, entity, qty
                            from `tabLiquids Issuing Table` 
                            where parent = '{parent}' and issue_type = '{issue_type}'
                            order by to_date desc limit 1
                        """.format(parent=q.vehicle, issue_type=self.issue_type), as_dict=1)

                    if q.vehicle:
                        vehicle_row = self.append("previous_vehicles_issuing_table", {})
                        vehicle_row.vehicle_boat = "Vehicles"
                        vehicle_row.vehicle = q.vehicle
                        vehicle_row.vehicle_no = q.vehicle_no
                        vehicle_row.vehicle_type = q.vehicle_type
                        vehicle_row.qty = q.qty
                        for t in vehicle_issue_list_:
                            vehicle_row.last_issue_from_date = t.from_date
                            vehicle_row.last_issue_to_date = t.to_date
                            vehicle_row.entity_name = t.entity

                previous_boats = frappe.db.sql(
                    """ Select
                        `tabBoats`.name as vehicle,
                        `tabBoats`.boat_no as vehicle_no,
                        `tabBoats`.entity_name as entity_name
                         from `tabBoats`
                         Where `tabBoats`.boat_validity = "صالحة"
                         and `tabBoats`.entity_name = '{entity}'
                         and `tabBoats`.fuel_type != "بدون وقود"
                         and `tabBoats`.qty != 0
                         and `tabBoats`.name in (select `tabLiquids Issuing Table`.parent 
                               from `tabLiquids Issuing Table`
                               where `tabLiquids Issuing Table`.issue_type = '{issue_type}'
                               and `tabLiquids Issuing Table`.from_date >= '{from_date}'
                               and `tabLiquids Issuing Table`.to_date <= '{to_date}')
                    """.format(entity=self.entity, from_date=self.from_date,
                               to_date=self.to_date, issue_type=self.issue_type), as_dict=1)

                for r in previous_boats:
                    boat_issue_list_ = frappe.db.sql(
                        """ Select from_date, to_date, entity, qty
                            from `tabLiquids Issuing Table` 
                            where parent = '{parent}' and issue_type = '{issue_type}'
                            order by to_date desc limit 1
                        """.format(parent=r.vehicle, issue_type=self.issue_type), as_dict=1)

                    if r.vehicle:
                        vehicle_row = self.append("previous_vehicles_issuing_table", {})
                        vehicle_row.vehicle_boat = "Boats"
                        vehicle_row.vehicle = r.vehicle
                        vehicle_row.vehicle_no = r.vehicle_no
                        vehicle_row.vehicle_type = "لانش"
                        vehicle_row.qty = r.qty
                        for t in boat_issue_list_:
                            vehicle_row.last_issue_from_date = t.from_date
                            vehicle_row.last_issue_to_date = t.to_date
                            vehicle_row.entity_name = t.entity

                fixed_vehicles = frappe.db.sql(
                    """ Select DISTINCT
                        `tabVehicles`.name as name,
                        `tabVehicles`.vehicle_no as vehicle_no,
                        `tabVehicles`.vehicle_type as vehicle_type,
                        `tabVehicles`.vehicle_shape as vehicle_shape,
                        `tabVehicles`.vehicle_brand as vehicle_brand,
                        `tabVehicles`.vehicle_style as vehicle_style,
                        `tabVehicles`.motor_no as motor_no,
                        `tabVehicles`.chassis_no as chassis_no,
                        `tabVehicle Status Logs`.date as date
                        from `tabVehicles` join `tabVehicle Status Logs`
                        on `tabVehicles`.name = `tabVehicle Status Logs`.parent
                        where `tabVehicle Status Logs`.value = "صالحة"
                        and `tabVehicles`.vehicle_status = "صالحة"
                        and `tabVehicle Status Logs`.idx != 1
                        and `tabVehicle Status Logs`.date between '{start_date}' and '{end_date}'
                        and `tabVehicles`.entity_name = '{entity}'
                        order by `tabVehicle Status Logs`.date
                    """.format(start_date=start_date, end_date=end_date, entity=self.entity), as_dict=1)

                for fixed_vec in fixed_vehicles:
                    fix = self.append("fixed_vehicles", {})
                    fix.vehicle = fixed_vec.name
                    fix.vehicle_no = fixed_vec.vehicle_no
                    fix.vehicle_type = fixed_vec.vehicle_type
                    fix.vehicle_shape = fixed_vec.vehicle_shape
                    fix.vehicle_brand = fixed_vec.vehicle_brand
                    fix.vehicle_style = fixed_vec.vehicle_style
                    fix.motor_no = fixed_vec.motor_no
                    fix.chassis_no = fixed_vec.chassis_no
                    fix.date = fixed_vec.date

                broken_vehicles = frappe.db.sql(
                    """ Select DISTINCT
                        `tabVehicles`.name as name,
                        `tabVehicles`.vehicle_no as vehicle_no,
                        `tabVehicles`.vehicle_type as vehicle_type,
                        `tabVehicles`.vehicle_shape as vehicle_shape,
                        `tabVehicles`.vehicle_brand as vehicle_brand,
                        `tabVehicles`.vehicle_style as vehicle_style,
                        `tabVehicles`.motor_no as motor_no,
                        `tabVehicles`.chassis_no as chassis_no,
                        `tabVehicle Status Logs`.date as date
                        from `tabVehicles` join `tabVehicle Status Logs`
                        on `tabVehicles`.name = `tabVehicle Status Logs`.parent
                        where `tabVehicle Status Logs`.value = "عاطلة"
                        and `tabVehicles`.vehicle_status in ("عاطلة", "تحت التخريد")
                        and `tabVehicle Status Logs`.date between '{start_date}' and '{end_date}'
                        and `tabVehicles`.entity_name = '{entity}'
                        order by `tabVehicle Status Logs`.date
                    """.format(start_date=start_date, end_date=end_date, entity=self.entity), as_dict=1)

                for broken_vec in broken_vehicles:
                    broken = self.append("broken_vehicles", {})
                    broken.vehicle = broken_vec.name
                    broken.vehicle_no = broken_vec.vehicle_no
                    broken.vehicle_type = broken_vec.vehicle_type
                    broken.vehicle_shape = broken_vec.vehicle_shape
                    broken.vehicle_brand = broken_vec.vehicle_brand
                    broken.vehicle_style = broken_vec.vehicle_style
                    broken.motor_no = broken_vec.motor_no
                    broken.chassis_no = broken_vec.chassis_no
                    broken.date = broken_vec.date

                scraped_vehicles = frappe.db.sql(
                    """ Select DISTINCT
                        `tabVehicles`.name as name,
                        `tabVehicles`.police_id as vehicle_no,
                        `tabVehicles`.vehicle_type as vehicle_type,
                        `tabVehicles`.vehicle_shape as vehicle_shape,
                        `tabVehicles`.vehicle_brand as vehicle_brand,
                        `tabVehicles`.vehicle_style as vehicle_style,
                        `tabVehicles`.motor_no as motor_no,
                        `tabVehicles`.chassis_no as chassis_no,
                        `tabVehicle Status Logs`.date as date
                        from `tabVehicles` join `tabVehicle Status Logs`
                        on `tabVehicles`.name = `tabVehicle Status Logs`.parent
                        where `tabVehicle Status Logs`.value = "مخردة"
                        and `tabVehicles`.vehicle_status = "مخردة"
                        and `tabVehicle Status Logs`.date between '{start_date}' and '{end_date}'
                        and `tabVehicles`.entity_name = '{entity}'
                        order by `tabVehicle Status Logs`.date
                    """.format(start_date=start_date, end_date=end_date, entity=self.entity), as_dict=1)

                for scraped_vec in scraped_vehicles:
                    scraped = self.append("scraped_vehicles", {})
                    scraped.vehicle = scraped_vec.name
                    scraped.vehicle_no = scraped_vec.vehicle_no
                    scraped.vehicle_type = scraped_vec.vehicle_type
                    scraped.vehicle_shape = scraped_vec.vehicle_shape
                    scraped.vehicle_brand = scraped_vec.vehicle_brand
                    scraped.vehicle_style = scraped_vec.vehicle_style
                    scraped.motor_no = scraped_vec.motor_no
                    scraped.chassis_no = scraped_vec.chassis_no
                    scraped.date = scraped_vec.date

                transferred_to_vehicles = frappe.db.sql(
                    """ Select DISTINCT
                        `tabVehicles`.name as name,
                        `tabVehicles`.vehicle_no as vehicle_no,
                        `tabVehicles`.vehicle_type as vehicle_type,
                        `tabVehicles`.vehicle_shape as vehicle_shape,
                        `tabVehicles`.vehicle_brand as vehicle_brand,
                        `tabVehicles`.vehicle_style as vehicle_style,
                        `tabVehicles`.motor_no as motor_no,
                        `tabVehicles`.chassis_no as chassis_no,
                        `tabEntity Logs`.date as date
                        from `tabVehicles` join `tabEntity Logs`
                        on `tabVehicles`.name = `tabEntity Logs`.parent
                        where `tabEntity Logs`.value = '{entity}'
                        and `tabVehicles`.entity_name = '{entity}'
                        and `tabEntity Logs`.date between '{start_date}' and '{end_date}'
                        order by `tabEntity Logs`.date
                    """.format(start_date=start_date, end_date=end_date, entity=self.entity), as_dict=1)

                for transferred_to_vec in transferred_to_vehicles:
                    to_vec = self.append("transferred_to_vehicles", {})
                    to_vec.vehicle = transferred_to_vec.name
                    to_vec.vehicle_no = transferred_to_vec.vehicle_no
                    to_vec.vehicle_type = transferred_to_vec.vehicle_type
                    to_vec.vehicle_shape = transferred_to_vec.vehicle_shape
                    to_vec.vehicle_brand = transferred_to_vec.vehicle_brand
                    to_vec.vehicle_style = transferred_to_vec.vehicle_style
                    to_vec.motor_no = transferred_to_vec.motor_no
                    to_vec.chassis_no = transferred_to_vec.chassis_no
                    to_vec.date = transferred_to_vec.date

                query = frappe.db.sql(
                    """ Select DISTINCT
                        `tabEntity Logs`.parent as parent
                        from `tabEntity Logs`
                        where `tabEntity Logs`.value = '{entity}'
                        order by `tabEntity Logs`.date
                    """.format(entity=self.entity), as_dict=1)

                for row in query:
                    idx = frappe.db.sql(
                        """ Select 
                            `tabEntity Logs`.date as date,
                            `tabEntity Logs`.idx as idx
                            from `tabVehicles` join `tabEntity Logs`
                            on `tabVehicles`.name = `tabEntity Logs`.parent
                            where `tabEntity Logs`.value = '{entity}'
                            and `tabEntity Logs`.parent = '{parent}'
                            order by `tabEntity Logs`.date desc
                            limit 1
                        """.format(parent=row.parent, start_date=start_date, end_date=end_date,
                                   entity=self.entity), as_dict=1)

                    if idx:
                        to_entity = frappe.db.sql(
                            """ Select 
                                `tabVehicles`.name as name,
                                `tabVehicles`.vehicle_no as vehicle_no,
                                `tabVehicles`.vehicle_type as vehicle_type,
                                `tabVehicles`.vehicle_shape as vehicle_shape,
                                `tabVehicles`.vehicle_brand as vehicle_brand,
                                `tabVehicles`.vehicle_style as vehicle_style,
                                `tabVehicles`.motor_no as motor_no,
                                `tabVehicles`.chassis_no as chassis_no,
                                `tabEntity Logs`.date as date,
                                `tabEntity Logs`.value as value,
                                `tabEntity Logs`.idx as idx
                                from `tabVehicles` join `tabEntity Logs`
                                on `tabVehicles`.name = `tabEntity Logs`.parent
                                where `tabEntity Logs`.parent = '{parent}'
                                and `tabVehicles`.entity_name != '{entity}'
                                and `tabEntity Logs`.idx = '{idx}'
                                and `tabEntity Logs`.date between '{start_date}' and '{end_date}'
                                order by `tabEntity Logs`.date desc
                            """.format(idx=idx[0].idx + 1, parent=row.parent, start_date=start_date, end_date=end_date,
                                       entity=self.entity), as_dict=1)

                        if to_entity:
                            from_vec = self.append("transferred_from_vehicles", {})
                            from_vec.vehicle = to_entity[0].name
                            from_vec.vehicle_no = to_entity[0].vehicle_no
                            from_vec.vehicle_type = to_entity[0].vehicle_type
                            from_vec.vehicle_shape = to_entity[0].vehicle_shape
                            from_vec.vehicle_brand = to_entity[0].vehicle_brand
                            from_vec.vehicle_style = to_entity[0].vehicle_style
                            from_vec.motor_no = to_entity[0].motor_no
                            from_vec.chassis_no = to_entity[0].chassis_no
                            from_vec.date = to_entity[0].date
                            from_vec.entity = to_entity[0].value

            # if not frappe.db.exists('Liquids Issuing',
            #                         {"docstatus": 1, "issue_to": self.issue_to, "entity": self.entity,
            #                          "issue_type": self.issue_type}):
            if not last_doc:
                self.last_issue = ""

            if self.issue_type == "وقود":
                self.set("liquid_per_vehicle_type_table", [])
                self.set("vehicles_issuing_table", [])
                # self.set("gas_per_vehicle_type_table", [])

                fuel_type_list = frappe.db.sql(
                    """ Select distinct `tabVehicles`.fuel_type as fuel_type 
                        from `tabVehicles`
                        where `tabVehicles`.entity_name = '{entity}'
                        and `tabVehicles`.vehicle_type != "لانش"
                        and `tabVehicles`.fuel_type != "بدون وقود"
                        and `tabVehicles`.litre_count != 0
                        order by `tabVehicles`.fuel_type
                    """.format(entity=self.entity), as_dict=1)

                # golf_fuel_type_list = frappe.db.sql(
                #     """ Select distinct `tabVehicles`.fuel_type as fuel_type 
                #         from `tabVehicles`
                #         where `tabVehicles`.entity_name = 'ا.ع لمكافحه المخدرات'
                #         and `tabVehicles`.vehicle_type = "جولف"
                #     """, as_dict=1)
                # fuel_type_list.extend(golf_fuel_type_list)

                for x in fuel_type_list:
                    vehicle_type_list = frappe.db.sql(
                        """ Select distinct `tabVehicles`.vehicle_type as vehicle_type 
                            from `tabVehicles`
                            Where `tabVehicles`.fuel_type = '{fuel_type}'
                            and `tabVehicles`.entity_name = '{entity}'
                        """.format(fuel_type=x.fuel_type, entity=self.entity), as_dict=1)

                    for y in vehicle_type_list:
                        cylinder_list = frappe.db.sql(
                            """ Select distinct `tabVehicles`.cylinder_count as cylinder_count 
                                from `tabVehicles`
                                Where `tabVehicles`.fuel_type = '{fuel_type}'
                                and `tabVehicles`.vehicle_type = '{vehicle_type}'
                                and `tabVehicles`.entity_name = '{entity}'
                            """.format(fuel_type=x.fuel_type, vehicle_type=y.vehicle_type,
                                       entity=self.entity), as_dict=1)

                        for z in cylinder_list:
                            litre_count_list = frappe.db.sql(
                                """ Select distinct `tabVehicles`.litre_count as litre_count 
                                    from `tabVehicles`
                                    Where `tabVehicles`.fuel_type = '{fuel_type}'
                                    and `tabVehicles`.vehicle_type = '{vehicle_type}'
                                    and `tabVehicles`.cylinder_count = '{cylinder_count}'
                                    and `tabVehicles`.entity_name = '{entity}'
                                """.format(fuel_type=x.fuel_type, vehicle_type=y.vehicle_type,
                                           cylinder_count=z.cylinder_count, entity=self.entity), as_dict=1)

                            valid_count = 0
                            previous_count = 0
                            plate_count = 0

                            for v in litre_count_list:
                                total_vehicle_list = frappe.db.sql(
                                    """ Select count(`tabVehicles`.name) as total_count from `tabVehicles` 
                                        Where `tabVehicles`.fuel_type = '{fuel_type}'
                                        and `tabVehicles`.vehicle_type = '{vehicle_type}'
                                        and `tabVehicles`.cylinder_count = '{cylinder_count}'
                                        and `tabVehicles`.litre_count = '{litre_count}'
                                        and `tabVehicles`.entity_name = '{entity}'
                                    """.format(litre_count=v.litre_count, fuel_type=x.fuel_type,
                                               vehicle_type=y.vehicle_type, cylinder_count=z.cylinder_count,
                                               entity=self.entity), as_dict=1)

                                valid_vehicle_list = frappe.db.sql(
                                    """ Select count(`tabVehicles`.name) as valid_count,
                                        `tabVehicles`.name as vehicle,
                                        `tabVehicles`.vehicle_no as vehicle_no,
                                        `tabVehicles`.vehicle_type as vehicle_type,
                                        `tabVehicles`.entity_name as entity_name
                                         from `tabVehicles` 
                                         Where `tabVehicles`.fuel_type = '{fuel_type}'
                                         and `tabVehicles`.vehicle_type = '{vehicle_type}'
                                         and `tabVehicles`.cylinder_count = '{cylinder_count}'
                                         and `tabVehicles`.litre_count = '{litre_count}'
                                         and `tabVehicles`.vehicle_status = "صالحة"
                                         and `tabVehicles`.entity_name = '{entity}'
                                         and `tabVehicles`.exchange_allowance not in ("لوحة فقط", "لوحة وخدمة كاملة فقط")
                                         and `tabVehicles`.name not in (select `tabLiquids Issuing Table`.parent 
                                              from `tabLiquids Issuing Table`
                                              where `tabLiquids Issuing Table`.issue_type = '{issue_type}'
                                              and `tabLiquids Issuing Table`.from_date >= '{from_date}'
                                              and `tabLiquids Issuing Table`.to_date <= '{to_date}')
                                    """.format(litre_count=v.litre_count, fuel_type=x.fuel_type,
                                               vehicle_type=y.vehicle_type, cylinder_count=z.cylinder_count,
                                               entity=self.entity, from_date=self.from_date,
                                               to_date=self.to_date, issue_type=self.issue_type), as_dict=1)

                                previous_vehicle_list = frappe.db.sql(
                                    """ Select count(`tabVehicles`.name) as valid_count,
                                        `tabVehicles`.name as vehicle,
                                        `tabVehicles`.vehicle_no as vehicle_no,
                                        `tabVehicles`.vehicle_type as vehicle_type,
                                        `tabVehicles`.entity_name as entity_name
                                         from `tabVehicles` 
                                         Where `tabVehicles`.fuel_type = '{fuel_type}'
                                         and `tabVehicles`.vehicle_type = '{vehicle_type}'
                                         and `tabVehicles`.cylinder_count = '{cylinder_count}'
                                         and `tabVehicles`.litre_count = '{litre_count}'
                                         and `tabVehicles`.vehicle_status = "صالحة"
                                         and `tabVehicles`.entity_name = '{entity}'
                                         and `tabVehicles`.exchange_allowance not in ("لوحة فقط", "لوحة وخدمة كاملة فقط")
                                         and `tabVehicles`.name in (select `tabLiquids Issuing Table`.parent 
                                              from `tabLiquids Issuing Table`
                                              where `tabLiquids Issuing Table`.issue_type = '{issue_type}'
                                              and `tabLiquids Issuing Table`.from_date >= '{from_date}'
                                              and `tabLiquids Issuing Table`.to_date <= '{to_date}')
                                    """.format(litre_count=v.litre_count, fuel_type=x.fuel_type,
                                               vehicle_type=y.vehicle_type, cylinder_count=z.cylinder_count,
                                               entity=self.entity, from_date=self.from_date,
                                               to_date=self.to_date, issue_type=self.issue_type), as_dict=1)

                                plate_only_vehicle_list = frappe.db.sql(
                                    """ Select count(`tabVehicles`.name) as valid_count,
                                        `tabVehicles`.name as vehicle,
                                        `tabVehicles`.vehicle_no as vehicle_no,
                                        `tabVehicles`.vehicle_type as vehicle_type,
                                        `tabVehicles`.entity_name as entity_name
                                         from `tabVehicles` 
                                         Where `tabVehicles`.fuel_type = '{fuel_type}'
                                         and `tabVehicles`.vehicle_type = '{vehicle_type}'
                                         and `tabVehicles`.cylinder_count = '{cylinder_count}'
                                         and `tabVehicles`.litre_count = '{litre_count}'
                                         and `tabVehicles`.vehicle_status = "صالحة"
                                         and `tabVehicles`.entity_name = '{entity}'
                                         and `tabVehicles`.exchange_allowance in ("لوحة فقط", "لوحة وخدمة كاملة فقط")                                         
                                    """.format(litre_count=v.litre_count, fuel_type=x.fuel_type,
                                               vehicle_type=y.vehicle_type, cylinder_count=z.cylinder_count,
                                               entity=self.entity, from_date=self.from_date,
                                               to_date=self.to_date), as_dict=1)

                                for d in valid_vehicle_list:
                                    valid_count = d.valid_count

                                for p in previous_vehicle_list:
                                    previous_count = p.valid_count

                                for u in plate_only_vehicle_list:
                                    plate_count = u.valid_count

                                for w in total_vehicle_list:
                                    row = self.append("liquid_per_vehicle_type_table", {})
                                    row.fuel_type = x.fuel_type
                                    row.vehicle_type = y.vehicle_type
                                    row.cylinder_count = z.cylinder_count
                                    row.liquid_qty = v.litre_count
                                    row.total_count = w.total_count
                                    row.valid_count = valid_count
                                    row.previously_issued = previous_count
                                    row.plate_count = plate_count
                                    row.invalid_count = w.total_count - valid_count - previous_count - plate_count
                                    row.total_qty = self.month_count * v.litre_count * valid_count

                valid_vehicle_list_2 = frappe.db.sql(
                    """ Select `tabVehicles`.name as vehicle,
                        `tabVehicles`.vehicle_no as vehicle_no,
                        `tabVehicles`.vehicle_type as vehicle_type,
                        `tabVehicles`.entity_name as entity_name,
                        `tabVehicles`.litre_count as litre_count
                        from `tabVehicles` 
                        Where `tabVehicles`.vehicle_status = "صالحة"
                        and `tabVehicles`.entity_name = '{entity}'
                        and `tabVehicles`.exchange_allowance not in ("لوحة فقط", "لوحة وخدمة كاملة فقط")
                        and `tabVehicles`.name not in (select `tabLiquids Issuing Table`.parent 
                            from `tabLiquids Issuing Table`
                            where `tabLiquids Issuing Table`.issue_type = '{issue_type}'
                            and `tabLiquids Issuing Table`.from_date >= '{from_date}' 
                            and `tabLiquids Issuing Table`.to_date <= '{to_date}')
                    """.format(entity=self.entity, from_date=self.from_date,
                               to_date=self.to_date, issue_type=self.issue_type), as_dict=1)

                for b in valid_vehicle_list_2:
                    vehicle_issue_list = frappe.db.sql(
                        """ Select from_date, to_date, entity
                            from `tabLiquids Issuing Table` 
                            where parent = '{parent}' and issue_type = '{issue_type}'
                            order by to_date desc limit 1
                        """.format(parent=b.vehicle, issue_type=self.issue_type), as_dict=1)

                    if b.vehicle:
                        vehicle_row = self.append("vehicles_issuing_table", {})
                        vehicle_row.vehicle_boat = "Vehicles"
                        vehicle_row.vehicle = b.vehicle
                        vehicle_row.vehicle_no = b.vehicle_no
                        vehicle_row.vehicle_type = b.vehicle_type
                        vehicle_row.qty = self.month_count * b.litre_count
                        for q in vehicle_issue_list:
                            vehicle_row.last_issue_from_date = q.from_date
                            vehicle_row.last_issue_to_date = q.to_date
                            vehicle_row.entity_name = q.entity

                #####################################################################
                fuel_type_list_2 = frappe.db.sql(
                    """ Select distinct `tabBoats`.fuel_type as fuel_type 
                        from `tabBoats`
                        where `tabBoats`.entity_name = '{entity}' 
                        and `tabBoats`.fuel_type != "بدون وقود"
                        and `tabBoats`.qty != 0
                    """.format(entity=self.entity), as_dict=1)

                for x in fuel_type_list_2:
                    cylinder_list_2 = frappe.db.sql(
                        """ Select distinct `tabBoats`.cylinder_count as cylinder_count 
                            from `tabBoats`
                            Where `tabBoats`.fuel_type = '{fuel_type}'
                            and `tabBoats`.entity_name = '{entity}'
                            and `tabBoats`.fuel_type != "بدون وقود"
                            and `tabBoats`.qty != 0
                        """.format(fuel_type=x.fuel_type, entity=self.entity), as_dict=1)

                    for z in cylinder_list_2:
                        litre_count_list_2 = frappe.db.sql(
                            """ Select distinct `tabBoats`.qty as litre_count 
                                from `tabBoats`
                                Where `tabBoats`.fuel_type = '{fuel_type}'
                                and `tabBoats`.cylinder_count = '{cylinder_count}'
                                and `tabBoats`.entity_name = '{entity}'
                                and `tabBoats`.fuel_type != "بدون وقود"
                                and `tabBoats`.qty != 0
                            """.format(fuel_type=x.fuel_type, cylinder_count=z.cylinder_count,
                                       entity=self.entity), as_dict=1)

                        valid_count = 0
                        previous_count = 0
                        plate_count = 0

                        for v in litre_count_list_2:
                            total_vehicle_list_2 = frappe.db.sql(
                                """ Select count(`tabBoats`.name) as total_count 
                                    from `tabBoats`
                                    Where `tabBoats`.fuel_type = '{fuel_type}'
                                    and `tabBoats`.cylinder_count = '{cylinder_count}'
                                    and `tabBoats`.entity_name = '{entity}'
                                    and `tabBoats`.qty = '{litre_count}'
                                    and `tabBoats`.fuel_type != "بدون وقود"
                                    and `tabBoats`.qty != 0
                                """.format(litre_count=v.litre_count, fuel_type=x.fuel_type,
                                           cylinder_count=z.cylinder_count, entity=self.entity), as_dict=1)

                            valid_vehicle_list_2 = frappe.db.sql(
                                """ Select count(`tabBoats`.name) as valid_count,
                                    `tabBoats`.name as vehicle,
                                    `tabBoats`.boat_no as vehicle_no,
                                    `tabBoats`.entity_name as entity_name
                                     from `tabBoats`
                                    Where `tabBoats`.fuel_type = '{fuel_type}'
                                    and `tabBoats`.cylinder_count = '{cylinder_count}'
                                    and `tabBoats`.entity_name = '{entity}'
                                    and `tabBoats`.qty = '{litre_count}'
                                    and `tabBoats`.boat_validity = "صالحة"
                                    and `tabBoats`.fuel_type != "بدون وقود"
                                    and `tabBoats`.qty != 0
                                    and `tabBoats`.name not in (select `tabLiquids Issuing Table`.parent 
                                              from `tabLiquids Issuing Table`
                                              where `tabLiquids Issuing Table`.issue_type = '{issue_type}'
                                              and `tabLiquids Issuing Table`.from_date >= '{from_date}'
                                              and `tabLiquids Issuing Table`.to_date <= '{to_date}')
                                """.format(litre_count=v.litre_count, fuel_type=x.fuel_type,
                                           cylinder_count=z.cylinder_count, entity=self.entity,
                                           from_date=self.from_date, to_date=self.to_date,
                                           issue_type=self.issue_type), as_dict=1)

                            previous_vehicle_list_2 = frappe.db.sql(
                                """ Select count(`tabBoats`.name) as valid_count,
                                    `tabBoats`.name as vehicle,
                                    `tabBoats`.boat_no as vehicle_no,
                                    `tabBoats`.entity_name as entity_name
                                     from `tabBoats`
                                     Where `tabBoats`.fuel_type = '{fuel_type}'
                                     and `tabBoats`.cylinder_count = '{cylinder_count}'
                                     and `tabBoats`.qty = '{litre_count}'
                                     and `tabBoats`.boat_validity = "صالحة"
                                     and `tabBoats`.entity_name = '{entity}'
                                     and `tabBoats`.fuel_type != "بدون وقود"
                                     and `tabBoats`.qty != 0
                                     and `tabBoats`.name in (select `tabLiquids Issuing Table`.parent 
                                           from `tabLiquids Issuing Table`
                                           where `tabLiquids Issuing Table`.issue_type = '{issue_type}'
                                           and `tabLiquids Issuing Table`.from_date >= '{from_date}'
                                           and `tabLiquids Issuing Table`.to_date <= '{to_date}')
                                """.format(litre_count=v.litre_count, fuel_type=x.fuel_type,
                                           cylinder_count=z.cylinder_count, entity=self.entity,
                                           from_date=self.from_date, to_date=self.to_date,
                                           issue_type=self.issue_type), as_dict=1)

                            for d in valid_vehicle_list_2:
                                valid_count = d.valid_count

                            for p in previous_vehicle_list_2:
                                previous_count = p.valid_count

                            for w in total_vehicle_list_2:
                                row = self.append("liquid_per_vehicle_type_table", {})
                                row.fuel_type = x.fuel_type
                                row.vehicle_type = "لانش"
                                row.cylinder_count = z.cylinder_count
                                row.liquid_qty = v.litre_count
                                row.total_count = w.total_count
                                row.valid_count = valid_count
                                row.previously_issued = previous_count
                                row.plate_count = 0
                                row.invalid_count = w.total_count - valid_count
                                row.total_qty = self.month_count * v.litre_count * valid_count

                valid_vehicle_list_3 = frappe.db.sql(
                    """ Select `tabBoats`.name as vehicle,
                        `tabBoats`.boat_no as boat_no,
                        `tabBoats`.entity_name as entity_name,
                        `tabBoats`.qty as qty
                        from `tabBoats` 
                        Where `tabBoats`.boat_validity = "صالحة"
                        and `tabBoats`.entity_name = '{entity}'
                        and `tabBoats`.qty != 0
                        and `tabBoats`.fuel_type != "بدون وقود"
                        and `tabBoats`.name not in (select `tabLiquids Issuing Table`.parent 
                          from `tabLiquids Issuing Table`
                          where `tabLiquids Issuing Table`.issue_type = '{issue_type}'
                          and `tabLiquids Issuing Table`.from_date >= '{from_date}'
                          and `tabLiquids Issuing Table`.to_date <= '{to_date}')
                    """.format(entity=self.entity, from_date=self.from_date,
                               to_date=self.to_date, issue_type=self.issue_type), as_dict=1)

                for b in valid_vehicle_list_3:
                    vehicle_issue_list_ = frappe.db.sql(
                        """ Select from_date, to_date, entity
                            from `tabLiquids Issuing Table` 
                            where parent = '{parent}' and issue_type = '{issue_type}'
                            order by to_date desc limit 1
                        """.format(parent=b.vehicle, issue_type=self.issue_type), as_dict=1)

                    if b.vehicle:
                        vehicle_row = self.append("vehicles_issuing_table", {})
                        vehicle_row.vehicle_boat = "Boats"
                        vehicle_row.vehicle = b.vehicle
                        vehicle_row.vehicle_no = b.boat_no
                        vehicle_row.qty = b.boat_no
                        vehicle_row.vehicle_type = "لانش"
                        vehicle_row.qty = self.month_count * b.qty
                        for q in vehicle_issue_list_:
                            vehicle_row.last_issue_from_date = q.from_date
                            vehicle_row.last_issue_to_date = q.to_date
                            vehicle_row.entity_name = q.entity

                gas_vehicle_type_list = frappe.db.sql(
                    """ Select distinct `tabVehicles`.vehicle_type as vehicle_type 
                        from `tabVehicles`
                        Where `tabVehicles`.entity_name = '{entity}'
                        and `tabVehicles`.vehicle_type != "لانش"
                        and `tabVehicles`.gas_count != 0
                    """.format(entity=self.entity), as_dict=1)

                for y in gas_vehicle_type_list:
                    gas_cylinder_list = frappe.db.sql(
                        """ Select distinct `tabVehicles`.cylinder_count as cylinder_count from `tabVehicles`
                            Where `tabVehicles`.vehicle_type = '{vehicle_type}'
                            and `tabVehicles`.entity_name = '{entity}'
                            and `tabVehicles`.vehicle_type != "لانش"
                            and `tabVehicles`.gas_count != 0
                        """.format(vehicle_type=y.vehicle_type, entity=self.entity), as_dict=1)

                    for z in gas_cylinder_list:
                        gas_count_list = frappe.db.sql(
                            """ Select distinct `tabVehicles`.gas_count as gas_count from `tabVehicles`
                                Where `tabVehicles`.vehicle_type = '{vehicle_type}'
                                and `tabVehicles`.cylinder_count = '{cylinder_count}'
                                and `tabVehicles`.entity_name = '{entity}'
                                and `tabVehicles`.vehicle_type != "لانش"
                                and `tabVehicles`.gas_count != 0
                            """.format(vehicle_type=y.vehicle_type, cylinder_count=z.cylinder_count,
                                       entity=self.entity), as_dict=1)

                        valid_count = 0
                        previous_count = 0
                        plate_count = 0

                        for v in gas_count_list:
                            gas_total_vehicle_list = frappe.db.sql(
                                """ Select count(`tabVehicles`.name) as total_count from `tabVehicles` 
                                    Where `tabVehicles`.vehicle_type = '{vehicle_type}'
                                    and `tabVehicles`.cylinder_count = '{cylinder_count}'
                                    and `tabVehicles`.gas_count = '{gas_count}'
                                    and `tabVehicles`.entity_name = '{entity}'
                                    and `tabVehicles`.vehicle_type != "لانش"
                                    and `tabVehicles`.gas_count != 0
                                """.format(gas_count=v.gas_count, vehicle_type=y.vehicle_type,
                                           cylinder_count=z.cylinder_count, entity=self.entity), as_dict=1)

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
                                    and `tabVehicles`.entity_name = '{entity}'
                                    and `tabVehicles`.exchange_allowance not in ("لوحة فقط", "لوحة وخدمة كاملة فقط")
                                    and `tabVehicles`.vehicle_type != "لانش"
                                    and `tabVehicles`.gas_count != 0
                                    and `tabVehicles`.name not in (select `tabLiquids Issuing Table`.parent 
                                        from `tabLiquids Issuing Table`
                                        where `tabLiquids Issuing Table`.issue_type = '{issue_type}'
                                        and `tabLiquids Issuing Table`.from_date >= '{from_date}'
                                        and `tabLiquids Issuing Table`.to_date <= '{to_date}')
                                """.format(gas_count=v.gas_count, vehicle_type=y.vehicle_type,
                                           cylinder_count=z.cylinder_count, entity=self.entity,
                                           from_date=self.from_date, to_date=self.to_date,
                                           issue_type=self.issue_type), as_dict=1)

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
                                     and `tabVehicles`.entity_name = '{entity}'
                                     and `tabVehicles`.exchange_allowance not in ("لوحة فقط", "لوحة وخدمة كاملة فقط")
                                     and `tabVehicles`.vehicle_type != "لانش"
                                     and `tabVehicles`.gas_count != 0
                                     and `tabVehicles`.name in (select `tabLiquids Issuing Table`.parent 
                                           from `tabLiquids Issuing Table`
                                           where `tabLiquids Issuing Table`.issue_type = '{issue_type}'
                                           and `tabLiquids Issuing Table`.from_date >= '{from_date}'
                                           and `tabLiquids Issuing Table`.to_date <= '{to_date}')
                                """.format(gas_count=v.gas_count, vehicle_type=y.vehicle_type,
                                           cylinder_count=z.cylinder_count, entity=self.entity,
                                           from_date=self.from_date, to_date=self.to_date,
                                           issue_type=self.issue_type), as_dict=1)

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
                                     and `tabVehicles`.vehicle_status = "صالحة"
                                     and `tabVehicles`.entity_name = '{entity}'
                                     and `tabVehicles`.exchange_allowance in ("لوحة فقط", "لوحة وخدمة كاملة فقط")
                                     and `tabVehicles`.vehicle_type != "لانش"
                                     and `tabVehicles`.gas_count != 0
                                """.format(gas_count=v.gas_count, vehicle_type=y.vehicle_type,
                                           cylinder_count=z.cylinder_count, entity=self.entity,
                                           from_date=self.from_date, to_date=self.to_date), as_dict=1)

                            for d in gas_valid_vehicle_list:
                                valid_count = d.valid_count

                            for p in gas_previous_vehicle_list:
                                previous_count = p.valid_count

                            for u in gas_plate_only_vehicle_list:
                                plate_count = u.valid_count

                            for w in gas_total_vehicle_list:
                                row = self.append("gas_per_vehicle_type_table", {})
                                row.fuel_type = "غاز طبيعي"
                                row.vehicle_type = y.vehicle_type
                                row.cylinder_count = z.cylinder_count
                                row.liquid_qty = v.gas_count
                                row.total_count = w.total_count
                                row.valid_count = valid_count
                                row.previously_issued = previous_count
                                row.plate_count = plate_count
                                row.invalid_count = w.total_count - valid_count - previous_count - plate_count
                                row.total_qty = self.month_count * v.gas_count * valid_count

                # valid_vehicle_list_2 = frappe.db.sql(
                #     """ Select `tabVehicles`.name as vehicle,
                #         `tabVehicles`.vehicle_no as vehicle_no,
                #         `tabVehicles`.vehicle_type as vehicle_type,
                #         `tabVehicles`.entity_name as entity_name,
                #         `tabVehicles`.gas_count as gas_count
                #         from `tabVehicles`
                #         Where `tabVehicles`.vehicle_status = "صالحة"
                #         and `tabVehicles`.entity_name = '{entity}'
                #         and `tabVehicles`.gas_count != 0
                #         and `tabVehicles`.exchange_allowance not in ("لوحة فقط", "لوحة وخدمة كاملة فقط")
                #         and `tabVehicles`.vehicle_type != "لانش"
                #         and `tabVehicles`.gas_count != 0
                #         and `tabVehicles`.name not in (select `tabLiquids Issuing Table`.parent
                #             from `tabLiquids Issuing Table`
                #             where `tabLiquids Issuing Table`.issue_type = '{issue_type}'
                #             and `tabLiquids Issuing Table`.from_date >= '{from_date}'
                #             and `tabLiquids Issuing Table`.to_date <= '{to_date}')
                #     """.format(entity=self.entity, from_date=self.from_date,
                #                to_date=self.to_date, issue_type=self.issue_type), as_dict=1)
                #
                # for b in valid_vehicle_list_2:
                #     vehicle_issue_list = frappe.db.sql(
                #         """ Select from_date, to_date, entity from `tabLiquids Issuing Table`
                #             where parent = '{parent}' and issue_type = '{issue_type}'
                #             order by to_date desc limit 1
                #         """.format(parent=b.vehicle, issue_type=self.issue_type), as_dict=1)
                #
                #     if b.vehicle:
                #         vehicle_row = self.append("vehicles_issuing_table", {})
                #         vehicle_row.vehicle_boat = "Vehicles"
                #         vehicle_row.vehicle = b.vehicle
                #         vehicle_row.vehicle_no = b.vehicle_no
                #         vehicle_row.vehicle_type = b.vehicle_type
                #         vehicle_row.qty = self.month_count * b.gas_count
                #         for q in vehicle_issue_list:
                #             vehicle_row.last_issue_from_date = q.from_date
                #             vehicle_row.last_issue_to_date = q.to_date
                #             vehicle_row.entity_name = q.entity

            #####################################################################
            if self.issue_type == "زيت":
                self.set("liquid_per_vehicle_type_table", [])
                self.set("vehicles_issuing_table", [])

                oil_type_list = frappe.db.sql(
                    """ Select distinct `tabVehicles`.oil_type as oil_type from `tabVehicles`
                        where `tabVehicles`.entity_name = '{entity}'
                        and `tabVehicles`.vehicle_type != "لانش"
                        and `tabVehicles`.oil_count != 0
                        order by `tabVehicles`.oil_type desc
                    """.format(entity=self.entity), as_dict=1)

                for x in oil_type_list:
                    vehicle_type_list = frappe.db.sql(
                        """ Select distinct `tabVehicles`.vehicle_type as vehicle_type from `tabVehicles`
                            Where `tabVehicles`.oil_type = '{oil_type}'
                            and `tabVehicles`.entity_name = '{entity}'
                        """.format(oil_type=x.oil_type, entity=self.entity), as_dict=1)

                    for y in vehicle_type_list:
                        cylinder_list = frappe.db.sql(
                            """ Select distinct `tabVehicles`.cylinder_count as cylinder_count from `tabVehicles`
                                Where `tabVehicles`.oil_type = '{oil_type}'
                                and `tabVehicles`.vehicle_type = '{vehicle_type}'
                                and `tabVehicles`.entity_name = '{entity}'
                            """.format(oil_type=x.oil_type, vehicle_type=y.vehicle_type, entity=self.entity), as_dict=1)

                        for z in cylinder_list:
                            oil_count_list = frappe.db.sql(
                                """ Select distinct `tabVehicles`.oil_count as oil_count from `tabVehicles`
                                    Where `tabVehicles`.oil_type = '{oil_type}'
                                    and `tabVehicles`.vehicle_type = '{vehicle_type}'
                                    and `tabVehicles`.cylinder_count = '{cylinder_count}'
                                    and `tabVehicles`.entity_name = '{entity}'
                                """.format(oil_type=x.oil_type, vehicle_type=y.vehicle_type,
                                           cylinder_count=z.cylinder_count, entity=self.entity), as_dict=1)

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
                                        and `tabVehicles`.entity_name = '{entity}'
                                    """.format(oil_count=v.oil_count, oil_type=x.oil_type, vehicle_type=y.vehicle_type,
                                               cylinder_count=z.cylinder_count, entity=self.entity), as_dict=1)

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
                                        and `tabVehicles`.entity_name = '{entity}'
                                        and `tabVehicles`.exchange_allowance not in ("لوحة فقط", "لوحة وخدمة كاملة فقط")
                                        and `tabVehicles`.name not in (select `tabLiquids Issuing Table`.parent 
                                              from `tabLiquids Issuing Table`
                                              where `tabLiquids Issuing Table`.issue_type = '{issue_type}'
                                              and `tabLiquids Issuing Table`.from_date >= '{from_date}'
                                              and `tabLiquids Issuing Table`.to_date <= '{to_date}')
                                    """.format(oil_count=v.oil_count, oil_type=x.oil_type,
                                               vehicle_type=y.vehicle_type, cylinder_count=z.cylinder_count,
                                               entity=self.entity, from_date=self.from_date,
                                               to_date=self.to_date, issue_type=self.issue_type), as_dict=1)

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
                                         and `tabVehicles`.entity_name = '{entity}'
                                         and `tabVehicles`.exchange_allowance not in ("لوحة فقط", "لوحة وخدمة كاملة فقط")
                                         and `tabVehicles`.name in (select `tabLiquids Issuing Table`.parent 
                                               from `tabLiquids Issuing Table`
                                               where `tabLiquids Issuing Table`.issue_type = '{issue_type}'
                                               and `tabLiquids Issuing Table`.from_date >= '{from_date}'
                                               and `tabLiquids Issuing Table`.to_date <= '{to_date}')
                                    """.format(oil_count=v.oil_count, oil_type=x.oil_type,
                                               vehicle_type=y.vehicle_type, cylinder_count=z.cylinder_count,
                                               entity=self.entity, from_date=self.from_date,
                                               to_date=self.to_date, issue_type=self.issue_type), as_dict=1)

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
                                         and `tabVehicles`.vehicle_status = "صالحة"
                                         and `tabVehicles`.entity_name = '{entity}'
                                         and `tabVehicles`.exchange_allowance in ("لوحة فقط", "لوحة وخدمة كاملة فقط")
                                    """.format(oil_count=v.oil_count, oil_type=x.oil_type,
                                               vehicle_type=y.vehicle_type, cylinder_count=z.cylinder_count,
                                               entity=self.entity, from_date=self.from_date,
                                               to_date=self.to_date), as_dict=1)

                                for d in valid_vehicle_list:
                                    valid_count = d.valid_count

                                for p in previous_vehicle_list:
                                    previous_count = p.valid_count

                                for u in plate_only_vehicle_list:
                                    plate_count = u.valid_count

                                for w in total_vehicle_list:
                                    row = self.append("liquid_per_vehicle_type_table", {})
                                    row.fuel_type = x.oil_type
                                    row.vehicle_type = y.vehicle_type
                                    row.cylinder_count = z.cylinder_count
                                    row.liquid_qty = v.oil_count
                                    row.total_count = w.total_count
                                    row.valid_count = valid_count
                                    row.previously_issued = previous_count
                                    row.plate_count = plate_count
                                    row.invalid_count = w.total_count - valid_count - previous_count - plate_count
                                    row.total_qty = self.month_count * v.oil_count * valid_count

                valid_vehicle_list_2 = frappe.db.sql(
                    """ Select `tabVehicles`.name as vehicle,
                        `tabVehicles`.vehicle_no as vehicle_no,
                        `tabVehicles`.vehicle_type as vehicle_type,
                        `tabVehicles`.entity_name as entity_name,
                        `tabVehicles`.oil_count as oil_count
                        from `tabVehicles` 
                        Where `tabVehicles`.vehicle_status = "صالحة"
                        and `tabVehicles`.entity_name = '{entity}'
                        and `tabVehicles`.oil_count != 0
                        and `tabVehicles`.exchange_allowance not in ("لوحة فقط", "لوحة وخدمة كاملة فقط")
                        and `tabVehicles`.vehicle_type != "لانش"
                        and `tabVehicles`.name not in (select `tabLiquids Issuing Table`.parent 
                            from `tabLiquids Issuing Table`
                            where `tabLiquids Issuing Table`.issue_type = '{issue_type}'
                            and `tabLiquids Issuing Table`.from_date >= '{from_date}' 
                            and `tabLiquids Issuing Table`.to_date <= '{to_date}')
                    """.format(entity=self.entity, from_date=self.from_date,
                               to_date=self.to_date, issue_type=self.issue_type), as_dict=1)

                for b in valid_vehicle_list_2:
                    vehicle_issue_list = frappe.db.sql(
                        """ Select from_date, to_date, entity from `tabLiquids Issuing Table` 
                            where parent = '{parent}' and issue_type = '{issue_type}'
                            order by to_date desc limit 1
                        """.format(parent=b.vehicle, issue_type=self.issue_type), as_dict=1)

                    if b.vehicle:
                        vehicle_row = self.append("vehicles_issuing_table", {})
                        vehicle_row.vehicle_boat = "Vehicles"
                        vehicle_row.vehicle = b.vehicle
                        vehicle_row.vehicle_no = b.vehicle_no
                        vehicle_row.vehicle_type = b.vehicle_type
                        vehicle_row.qty = self.month_count * b.oil_count
                        for q in vehicle_issue_list:
                            vehicle_row.last_issue_from_date = q.from_date
                            vehicle_row.last_issue_to_date = q.to_date
                            vehicle_row.entity_name = q.entity

            if self.issue_type == "غاز":
                self.set("liquid_per_vehicle_type_table", [])
                self.set("vehicles_issuing_table", [])

                vehicle_type_list = frappe.db.sql(
                    """ Select distinct `tabVehicles`.vehicle_type as vehicle_type 
                        from `tabVehicles`
                        Where `tabVehicles`.entity_name = '{entity}'
                        and `tabVehicles`.vehicle_type != "لانش"
                        and `tabVehicles`.gas_count != 0
                    """.format(entity=self.entity), as_dict=1)

                for y in vehicle_type_list:
                    cylinder_list = frappe.db.sql(
                        """ Select distinct `tabVehicles`.cylinder_count as cylinder_count from `tabVehicles`
                            Where `tabVehicles`.vehicle_type = '{vehicle_type}'
                            and `tabVehicles`.entity_name = '{entity}'
                        """.format(vehicle_type=y.vehicle_type, entity=self.entity), as_dict=1)

                    for z in cylinder_list:
                        gas_count_list = frappe.db.sql(
                            """ Select distinct `tabVehicles`.gas_count as gas_count from `tabVehicles`
                                Where `tabVehicles`.vehicle_type = '{vehicle_type}'
                                and `tabVehicles`.cylinder_count = '{cylinder_count}'
                                and `tabVehicles`.entity_name = '{entity}'
                            """.format(vehicle_type=y.vehicle_type, cylinder_count=z.cylinder_count,
                                       entity=self.entity), as_dict=1)

                        valid_count = 0
                        previous_count = 0
                        plate_count = 0

                        for v in gas_count_list:
                            total_vehicle_list = frappe.db.sql(
                                """ Select count(`tabVehicles`.name) as total_count from `tabVehicles` 
                                    Where `tabVehicles`.vehicle_type = '{vehicle_type}'
                                    and `tabVehicles`.cylinder_count = '{cylinder_count}'
                                    and `tabVehicles`.gas_count = '{gas_count}'
                                    and `tabVehicles`.entity_name = '{entity}'
                                """.format(gas_count=v.gas_count, vehicle_type=y.vehicle_type,
                                           cylinder_count=z.cylinder_count, entity=self.entity), as_dict=1)

                            valid_vehicle_list = frappe.db.sql(
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
                                    and `tabVehicles`.entity_name = '{entity}'
                                    and `tabVehicles`.exchange_allowance not in ("لوحة فقط", "لوحة وخدمة كاملة فقط")
                                    and `tabVehicles`.name not in (select `tabLiquids Issuing Table`.parent 
                                        from `tabLiquids Issuing Table`
                                        where `tabLiquids Issuing Table`.issue_type = '{issue_type}'
                                        and `tabLiquids Issuing Table`.from_date >= '{from_date}'
                                        and `tabLiquids Issuing Table`.to_date <= '{to_date}')
                                """.format(gas_count=v.gas_count, vehicle_type=y.vehicle_type,
                                           cylinder_count=z.cylinder_count, entity=self.entity,
                                           from_date=self.from_date, to_date=self.to_date,
                                           issue_type=self.issue_type), as_dict=1)

                            previous_vehicle_list = frappe.db.sql(
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
                                     and `tabVehicles`.entity_name = '{entity}'
                                     and `tabVehicles`.exchange_allowance not in ("لوحة فقط", "لوحة وخدمة كاملة فقط")
                                     and `tabVehicles`.name in (select `tabLiquids Issuing Table`.parent 
                                           from `tabLiquids Issuing Table`
                                           where `tabLiquids Issuing Table`.issue_type = '{issue_type}'
                                           and `tabLiquids Issuing Table`.from_date >= '{from_date}'
                                           and `tabLiquids Issuing Table`.to_date <= '{to_date}')
                                """.format(gas_count=v.gas_count, vehicle_type=y.vehicle_type,
                                           cylinder_count=z.cylinder_count, entity=self.entity,
                                           from_date=self.from_date, to_date=self.to_date,
                                           issue_type=self.issue_type), as_dict=1)

                            plate_only_vehicle_list = frappe.db.sql(
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
                                     and `tabVehicles`.entity_name = '{entity}'
                                     and `tabVehicles`.exchange_allowance in ("لوحة فقط", "لوحة وخدمة كاملة فقط")
                                """.format(gas_count=v.gas_count, vehicle_type=y.vehicle_type,
                                           cylinder_count=z.cylinder_count, entity=self.entity,
                                           from_date=self.from_date, to_date=self.to_date), as_dict=1)

                            for d in valid_vehicle_list:
                                valid_count = d.valid_count

                            for p in previous_vehicle_list:
                                previous_count = p.valid_count

                            for u in plate_only_vehicle_list:
                                plate_count = u.valid_count

                            for w in total_vehicle_list:
                                row = self.append("liquid_per_vehicle_type_table", {})
                                row.fuel_type = "غاز طبيعي"
                                row.vehicle_type = y.vehicle_type
                                row.cylinder_count = z.cylinder_count
                                row.liquid_qty = v.gas_count
                                row.total_count = w.total_count
                                row.valid_count = valid_count
                                row.previously_issued = previous_count
                                row.plate_count = plate_count
                                row.invalid_count = w.total_count - valid_count - previous_count - plate_count
                                row.total_qty = self.month_count * v.gas_count * valid_count

                valid_vehicle_list_2 = frappe.db.sql(
                    """ Select `tabVehicles`.name as vehicle,
                        `tabVehicles`.vehicle_no as vehicle_no,
                        `tabVehicles`.vehicle_type as vehicle_type,
                        `tabVehicles`.entity_name as entity_name,
                        `tabVehicles`.gas_count as gas_count
                        from `tabVehicles` 
                        Where `tabVehicles`.vehicle_status = "صالحة"
                        and `tabVehicles`.entity_name = '{entity}'
                        and `tabVehicles`.gas_count != 0
                        and `tabVehicles`.exchange_allowance not in ("لوحة فقط", "لوحة وخدمة كاملة فقط")
                        and `tabVehicles`.name not in (select `tabLiquids Issuing Table`.parent 
                            from `tabLiquids Issuing Table`
                            where `tabLiquids Issuing Table`.issue_type = '{issue_type}'
                            and `tabLiquids Issuing Table`.from_date >= '{from_date}' 
                            and `tabLiquids Issuing Table`.to_date <= '{to_date}')
                    """.format(entity=self.entity, from_date=self.from_date,
                               to_date=self.to_date, issue_type=self.issue_type), as_dict=1)

                for b in valid_vehicle_list_2:
                    vehicle_issue_list = frappe.db.sql(
                        """ Select from_date, to_date, entity from `tabLiquids Issuing Table` 
                            where parent = '{parent}' and issue_type = '{issue_type}'
                            order by to_date desc limit 1
                        """.format(parent=b.vehicle, issue_type=self.issue_type), as_dict=1)

                    if b.vehicle:
                        vehicle_row = self.append("vehicles_issuing_table", {})
                        vehicle_row.vehicle_boat = "Vehicles"
                        vehicle_row.vehicle = b.vehicle
                        vehicle_row.vehicle_no = b.vehicle_no
                        vehicle_row.vehicle_type = b.vehicle_type
                        vehicle_row.qty = self.month_count * b.gas_count
                        for q in vehicle_issue_list:
                            vehicle_row.last_issue_from_date = q.from_date
                            vehicle_row.last_issue_to_date = q.to_date
                            vehicle_row.entity_name = q.entity

            ############################################
            if self.issue_type == "غسيل":
                self.set("liquid_per_vehicle_type_table", [])
                self.set("vehicles_issuing_table", [])

                washing_type_list = frappe.db.sql(
                    """ Select distinct `tabVehicles`.washing_voucher as washing_voucher from `tabVehicles`
                        where `tabVehicles`.entity_name = '{entity}'
                        and `tabVehicles`.vehicle_type != "لانش"
                        and `tabVehicles`.washing_count != 0
                    """.format(entity=self.entity), as_dict=1)

                for x in washing_type_list:
                    vehicle_type_list = frappe.db.sql(
                        """ Select distinct `tabVehicles`.vehicle_type as vehicle_type from `tabVehicles`
                            Where `tabVehicles`.washing_voucher = '{washing_voucher}'
                            and `tabVehicles`.entity_name = '{entity}'
                        """.format(washing_voucher=x.washing_voucher, entity=self.entity), as_dict=1)

                    for y in vehicle_type_list:
                        cylinder_list = frappe.db.sql(
                            """ Select distinct `tabVehicles`.cylinder_count as cylinder_count from `tabVehicles`
                                Where `tabVehicles`.washing_voucher = '{washing_voucher}'
                                and `tabVehicles`.vehicle_type = '{vehicle_type}'
                                and `tabVehicles`.entity_name = '{entity}'
                            """.format(washing_voucher=x.washing_voucher, vehicle_type=y.vehicle_type,
                                       entity=self.entity), as_dict=1)

                        for z in cylinder_list:
                            washing_count_list = frappe.db.sql(
                                """ Select distinct `tabVehicles`.washing_count as washing_count from `tabVehicles`
                                    Where `tabVehicles`.washing_voucher = '{washing_voucher}'
                                    and `tabVehicles`.vehicle_type = '{vehicle_type}'
                                    and `tabVehicles`.cylinder_count = '{cylinder_count}'
                                    and `tabVehicles`.entity_name = '{entity}'
                                """.format(washing_voucher=x.washing_voucher, vehicle_type=y.vehicle_type,
                                           cylinder_count=z.cylinder_count, entity=self.entity),
                                as_dict=1)

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
                                    """.format(washing_count=v.washing_count, washing_voucher=x.washing_voucher,
                                               vehicle_type=y.vehicle_type,
                                               cylinder_count=z.cylinder_count, entity=self.entity),
                                    as_dict=1)

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
                                    """.format(washing_count=v.washing_count, washing_voucher=x.washing_voucher,
                                               vehicle_type=y.vehicle_type,
                                               cylinder_count=z.cylinder_count,
                                               entity=self.entity, from_date=self.from_date,
                                               to_date=self.to_date, issue_type=self.issue_type),
                                    as_dict=1)

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
                                    """.format(washing_count=v.washing_count, washing_voucher=x.washing_voucher,
                                               vehicle_type=y.vehicle_type,
                                               cylinder_count=z.cylinder_count,
                                               entity=self.entity, from_date=self.from_date,
                                               to_date=self.to_date, issue_type=self.issue_type),
                                    as_dict=1)

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
                                         and `tabVehicles`.vehicle_status = "صالحة"
                                         and `tabVehicles`.entity_name = '{entity}'
                                         and `tabVehicles`.exchange_allowance in ("لوحة فقط", "لوحة وخدمة كاملة فقط")
                                    """.format(washing_count=v.washing_count, washing_voucher=x.washing_voucher,
                                               vehicle_type=y.vehicle_type,
                                               cylinder_count=z.cylinder_count,
                                               entity=self.entity, from_date=self.from_date,
                                               to_date=self.to_date), as_dict=1)

                                for d in valid_vehicle_list:
                                    valid_count = d.valid_count

                                for p in previous_vehicle_list:
                                    previous_count = p.valid_count

                                for u in plate_only_vehicle_list:
                                    plate_count = u.valid_count

                                for w in total_vehicle_list:
                                    row = self.append("liquid_per_vehicle_type_table", {})
                                    row.fuel_type = x.washing_voucher
                                    row.vehicle_type = y.vehicle_type
                                    row.cylinder_count = z.cylinder_count
                                    row.liquid_qty = v.washing_count
                                    row.total_count = w.total_count
                                    row.valid_count = valid_count
                                    row.previously_issued = previous_count
                                    row.plate_count = plate_count
                                    row.invalid_count = w.total_count - valid_count - previous_count - plate_count
                                    row.total_qty = self.month_count * v.washing_count * valid_count

                valid_vehicle_list_2 = frappe.db.sql(
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
                    """.format(entity=self.entity, from_date=self.from_date,
                               to_date=self.to_date, issue_type=self.issue_type), as_dict=1)

                for b in valid_vehicle_list_2:
                    vehicle_issue_list = frappe.db.sql(
                        """ Select from_date, to_date, entity from `tabLiquids Issuing Table` 
                            where parent = '{parent}' and issue_type = '{issue_type}'
                            order by to_date desc limit 1
                        """.format(parent=b.vehicle, issue_type=self.issue_type), as_dict=1)

                    if b.vehicle:
                        vehicle_row = self.append("vehicles_issuing_table", {})
                        vehicle_row.vehicle_boat = "Vehicles"
                        vehicle_row.vehicle = b.vehicle
                        vehicle_row.vehicle_no = b.vehicle_no
                        vehicle_row.vehicle_type = b.vehicle_type
                        vehicle_row.qty = self.month_count * b.washing_count
                        for q in vehicle_issue_list:
                            vehicle_row.last_issue_from_date = q.from_date
                            vehicle_row.last_issue_to_date = q.to_date
                            vehicle_row.entity_name = q.entity

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
            self.invalid_vehicles_count = invalid_vehicles_count
            self.valid_vehicles_count = valid_vehicles_count
            self.total_liquid_count = total_liquid_count
            self.previously_issued_count = previously_issued_count
            self.plates_only_count = plates_only_count

            liquid = frappe.db.sql(
                """ select distinct fuel_type
                    from `tabLiquid Per Vehicle Type Table`
                    where parent = '{parent}'
                    and parentfield = "liquid_per_vehicle_type_table"
                """.format(parent=self.name), as_dict=1)

            for h in liquid:
                sum_qty = frappe.db.sql(
                    """ select sum(total_qty)
                        from `tabLiquid Per Vehicle Type Table`
                        where parent = '{parent}'
                        and fuel_type = '{fuel_type}'
                        and parentfield = "liquid_per_vehicle_type_table"
                    """.format(parent=self.name, fuel_type=h.fuel_type), as_dict=0)

                rows = self.append("qty_per_liquid", {})
                rows.liquid = h.fuel_type
                rows.qty = sum_qty[0][0]
                rows.in_words = in_words(sum_qty[0][0])

            gas = frappe.db.sql(
                """ select distinct fuel_type
                    from `tabLiquid Per Vehicle Type Table`
                    where parent = '{parent}'
                    and parentfield = "gas_per_vehicle_type_table"
                """.format(parent=self.name), as_dict=1)

            for u in gas:
                sum_qty1 = frappe.db.sql(
                    """ select sum(total_qty)
                        from `tabLiquid Per Vehicle Type Table`
                        where parent = '{parent}'
                        and parentfield = "gas_per_vehicle_type_table"
                        and fuel_type = '{fuel_type}'
                    """.format(parent=self.name, fuel_type=u.fuel_type), as_dict=0)

                rowss = self.append("qty_per_liquid", {})
                rowss.liquid = u.fuel_type
                rowss.qty = sum_qty1[0][0]
                rowss.in_words = in_words(sum_qty1[0][0])

        if self.issue_to == "مركبة أو مجموعة مركبات":
            self.set("vehicles_issuing_table", [])
            self.set("liquid_per_vehicle_type_table", [])
            self.set("qty_per_liquid", [])
            self.total_vehicles_count = 0
            self.invalid_vehicles_count = 0
            self.valid_vehicles_count = 0
            self.total_liquid_count = 0
            self.previously_issued_count = 0
            self.plates_only_count = 0

            if not self.specified_vehicles_issuing_table:
                frappe.throw(" برجاء تحديد المركبات التي سيتم الصرف لها ")

            for t in self.specified_vehicles_issuing_table:
                t.vehicle_no = frappe.db.get_value("Vehicles", t.vehicle, "vehicle_no")
                t.vehicle_type = frappe.db.get_value("Vehicles", t.vehicle, "vehicle_type")
                vehicle_issue_list = frappe.db.sql(
                    """ Select from_date, to_date, entity from `tabLiquids Issuing Table` 
                        where parent = '{parent}' and issue_type = '{issue_type}'
                        order by to_date desc limit 1
                    """.format(parent=t.vehicle, issue_type=self.issue_type), as_dict=1)
                for q in vehicle_issue_list:
                    t.last_issue_from_date = q.from_date
                    t.last_issue_to_date = q.to_date
                    t.entity_name = q.entity
                if self.issue_type == "وقود":
                    t.qty = self.issue_days * frappe.db.get_value("Vehicles", t.vehicle, "litre_count") / 30
                    t.liquid = frappe.db.get_value("Vehicles", t.vehicle, "fuel_type")
                if self.issue_type == "زيت":
                    t.qty = self.issue_days * frappe.db.get_value("Vehicles", t.vehicle, "oil_count") / 30
                    t.liquid = frappe.db.get_value("Vehicles", t.vehicle, "oil_type")
                if self.issue_type == "غاز":
                    t.qty = self.issue_days * frappe.db.get_value("Vehicles", t.vehicle, "gas_count") / 30
                    t.liquid = "غاز طبيعي"
                if self.issue_type == "غسيل":
                    t.qty = self.issue_days * frappe.db.get_value("Vehicles", t.vehicle, "washing_count") / 30
                    t.liquid = frappe.db.get_value("Vehicles", t.vehicle, "washing_voucher")

            liquid = frappe.db.sql(
                """ select distinct liquid
                    from `tabSpecified Vehicles Issuing Table`
                    where parent = '{parent}'
                """.format(parent=self.name), as_dict=1)

            for h in liquid:
                sum_qty = frappe.db.sql(
                    """ select sum(qty)
                        from `tabSpecified Vehicles Issuing Table`
                        where parent = '{parent}'
                        and liquid = '{liquid}'
                    """.format(parent=self.name, liquid=h.liquid), as_dict=0)

                rows = self.append("qty_per_liquid", {})
                rows.liquid = h.liquid
                rows.qty = sum_qty[0][0]
                rows.in_words = in_words(sum_qty[0][0])

    def on_submit(self):
        self.issue_state = "جاري تحضير الصرفية ومراجعتها"
        if self.issue_to == "جهة":
            current_vehicles = []
            for t in self.vehicles_issuing_table:
                current_vehicles.append(t.vehicle)

                vehicle_status = frappe.db.get_value("Vehicles", t.vehicle, "vehicle_status")
                boat_status = frappe.db.get_value("Boats", t.vehicle, "boat_validity")
                voucher = ""
                voucher1 = ""

                if self.issue_type == "وقود":
                    voucher = frappe.db.get_value("Vehicles", t.vehicle, "fuel_voucher") if frappe.db.get_value(
                        "Vehicles", t.vehicle, "fuel_voucher") else "لا يوجد"
                    voucher1 = frappe.db.get_value("Boats", t.vehicle, "fuel_voucher") if frappe.db.get_value("Boats",
                                                                                                              t.vehicle,
                                                                                                              "fuel_voucher") else "لا يوجد"
                if self.issue_type == "زيت":
                    voucher = frappe.db.get_value("Vehicles", t.vehicle, "oil_type") if frappe.db.get_value("Vehicles",
                                                                                                            t.vehicle,
                                                                                                            "oil_type") else "لا يوجد"
                    voucher1 = "لا يوجد"
                if self.issue_type == "غاز":
                    voucher = "غاز طبيعي فئة 15 متر مكعب"
                    voucher1 = "لا يوجد"
                if self.issue_type == "غسيل":
                    voucher = frappe.db.get_value("Vehicles", t.vehicle, "washing_voucher") if frappe.db.get_value(
                        "Vehicles", t.vehicle, "washing_voucher") else "لا يوجد"
                    voucher1 = "لا يوجد"

                record_name = self.name + str(t.idx)

                if t.vehicle_boat == "Vehicles":
                    frappe.db.sql(""" INSERT INTO `tabLiquids Issuing Table`
                                            (issue_date, issue_type, vehicle_status, voucher, from_date, to_date, entity, qty, created_by, issue_no, parent, parentfield, parenttype, name)
                                    VALUES ('{issue_date}', '{issue_type}', '{vehicle_status}', '{voucher}' ,'{from_date}', '{to_date}', '{entity}', '{qty}', '{created_by}', '{issue_no}','{parent}', '{parentfield}', '{parenttype}', '{record_name}')
                                  """.format(issue_date=self.issue_date, issue_type=self.issue_type,
                                             vehicle_status=vehicle_status,
                                             from_date=self.from_date, voucher=voucher, to_date=self.to_date,
                                             entity=self.entity,
                                             qty=t.qty, created_by=frappe.session.user, issue_no=self.name,
                                             parenttype=t.vehicle_boat,
                                             parent=t.vehicle, parentfield="liquid_table", record_name=record_name))

                if t.vehicle_boat == "Boats":
                    frappe.db.sql(""" INSERT INTO `tabLiquids Issuing Table`
                                            (issue_date, issue_type, vehicle_status, voucher, from_date, to_date, entity, qty, created_by, issue_no, parent, parentfield, parenttype, name)
                                    VALUES ('{issue_date}', '{issue_type}', '{vehicle_status}', '{voucher}' ,'{from_date}', '{to_date}', '{entity}', '{qty}', '{created_by}', '{issue_no}','{parent}', '{parentfield}', '{parenttype}', '{record_name}')
                                  """.format(issue_date=self.issue_date, issue_type=self.issue_type,
                                             vehicle_status=boat_status,
                                             from_date=self.from_date, voucher=voucher1, to_date=self.to_date,
                                             entity=self.entity,
                                             qty=t.qty, created_by=frappe.session.user, issue_no=self.name,
                                             parenttype=t.vehicle_boat,
                                             parent=t.vehicle, parentfield="liquid_table", record_name=record_name))

            if len(current_vehicles) == 1:
                current_vehicles.append("None")

            not_in_vehicle_table = frappe.db.sql("""
                select name, vehicle_status
                from `tabVehicles` 
                where entity_name = '{cur_entity}'
                and name not in {current_vehicles}
            """.format(cur_entity=self.entity, current_vehicles=tuple(current_vehicles)), as_dict=1)

            not_in_boat_table = frappe.db.sql("""
                            select name, boat_validity
                            from `tabBoats` 
                            where entity_name = '{cur_entity}'
                            and name not in {current_vehicles}
                        """.format(cur_entity=self.entity, current_vehicles=tuple(current_vehicles)), as_dict=1)

            for z in not_in_vehicle_table:
                record_name = self.name + str(z.name)
                voucher = ""
                if self.issue_type == "وقود":
                    voucher = frappe.db.get_value("Vehicles", z.name, "fuel_voucher") if frappe.db.get_value("Vehicles",
                                                                                                             z.name,
                                                                                                             "fuel_voucher") else "لا يوجد"
                if self.issue_type == "زيت":
                    voucher = frappe.db.get_value("Vehicles", z.name, "oil_type") if frappe.db.get_value("Vehicles",
                                                                                                         z.name,
                                                                                                         "oil_type") else "لا يوجد"
                if self.issue_type == "غاز":
                    voucher = "غاز طبيعي فئة 15 متر مكعب"
                if self.issue_type == "غسيل":
                    voucher = frappe.db.get_value("Vehicles", z.name, "washing_voucher") if frappe.db.get_value(
                        "Vehicles", z.name, "washing_voucher") else "لا يوجد"

                frappe.db.sql(""" INSERT INTO `tabLiquids Issuing Table`
                                                        (issue_date, issue_type, vehicle_status, voucher, from_date, to_date, entity, qty, created_by, issue_no, parent, parentfield, parenttype, name)
                                                VALUES ('{issue_date}', '{issue_type}', '{vehicle_status}', '{voucher}' ,'{from_date}', '{to_date}', '{entity}', '{qty}', '{created_by}', '{issue_no}','{parent}', '{parentfield}', '{parenttype}', '{record_name}')
                                              """.format(issue_date=self.issue_date, issue_type=self.issue_type,
                                                         vehicle_status=z.vehicle_status,
                                                         from_date=self.from_date, voucher=voucher,
                                                         to_date=self.to_date,
                                                         entity=self.entity,
                                                         qty=0, created_by=frappe.session.user, issue_no=self.name,
                                                         parenttype="Vehicles",
                                                         parent=z.name, parentfield="liquid_table",
                                                         record_name=record_name))

            for w in not_in_boat_table:
                record_name = self.name + str(w.name)
                voucher = ""
                if self.issue_type == "وقود":
                    voucher = frappe.db.get_value("Boats", w.name, "fuel_voucher") if frappe.db.get_value("Boats",
                                                                                                          w.name,
                                                                                                          "fuel_voucher") else "لا يوجد"
                if self.issue_type == "زيت":
                    voucher = "لا يوجد"
                if self.issue_type == "غاز":
                    voucher = "لا يوجد"
                if self.issue_type == "غسيل":
                    voucher = "لا يوجد"

                frappe.db.sql(""" INSERT INTO `tabLiquids Issuing Table`
                                                        (issue_date, issue_type, vehicle_status, voucher, from_date, to_date, entity, qty, created_by, issue_no, parent, parentfield, parenttype, name)
                                                VALUES ('{issue_date}', '{issue_type}', '{vehicle_status}', '{voucher}' ,'{from_date}', '{to_date}', '{entity}', '{qty}', '{created_by}', '{issue_no}','{parent}', '{parentfield}', '{parenttype}', '{record_name}')
                                              """.format(issue_date=self.issue_date, issue_type=self.issue_type,
                                                         vehicle_status=w.boat_validity,
                                                         from_date=self.from_date, voucher=voucher,
                                                         to_date=self.to_date,
                                                         entity=self.entity,
                                                         qty=0, created_by=frappe.session.user, issue_no=self.name,
                                                         parenttype="Boats",
                                                         parent=w.name, parentfield="liquid_table",
                                                         record_name=record_name))

        if self.issue_to == "مركبة أو مجموعة مركبات":
            for t in self.specified_vehicles_issuing_table:
                if getdate(t.last_issue_from_date) >= getdate(self.from_date) and getdate(
                        t.last_issue_from_date) <= getdate(self.to_date):
                    frappe.throw(" الصف # " + str(t.idx) + " : لا يمكن صرف " + self.issue_type + " إلى المركبة " + str(
                        t.vehicle_no) + " حيث أنه تم الصرف لها من قبل خلال الفترة المحددة إلى جهة " + str(
                        t.entity_name))

                if getdate(t.last_issue_to_date) >= getdate(self.from_date) and getdate(
                        t.last_issue_to_date) <= getdate(self.to_date):
                    frappe.throw(" الصف # " + str(t.idx) + " : لا يمكن صرف " + self.issue_type + " إلى المركبة " + str(
                        t.vehicle_no) + " حيث أنه تم الصرف لها من قبل خلال الفترة المحددة إلى جهة " + str(
                        t.entity_name))

                vehicle_status = frappe.db.get_value("Vehicles", t.vehicle, "vehicle_status")
                voucher = ""

                if self.issue_type == "وقود":
                    voucher = frappe.db.get_value("Vehicles", t.vehicle, "fuel_voucher") if frappe.db.get_value(
                        "Vehicles", t.vehicle, "fuel_voucher") else "لا يوجد"
                if self.issue_type == "زيت":
                    voucher = frappe.db.get_value("Vehicles", t.vehicle, "oil_type")
                if self.issue_type == "غاز":
                    voucher = "غاز طبيعي فئة 15 متر مكعب"
                if self.issue_type == "غسيل":
                    voucher = frappe.db.get_value("Vehicles", t.vehicle, "washing_voucher")

                record_name = self.name + str(t.idx)
                frappe.db.sql(""" INSERT INTO `tabLiquids Issuing Table`
                                                        (issue_date, issue_type, vehicle_status, voucher, from_date, to_date, entity, qty, created_by, issue_no, parent, parentfield, parenttype, name)
                                                VALUES ('{issue_date}', '{issue_type}', '{vehicle_status}', '{voucher}', '{from_date}', '{to_date}', '{entity}', '{qty}', '{created_by}', '{issue_no}','{parent}', '{parentfield}', '{parenttype}', '{record_name}')
                                              """.format(issue_date=self.issue_date, issue_type=self.issue_type,
                                                         from_date=self.from_date, vehicle_status=vehicle_status,
                                                         voucher=voucher, qty=t.qty,
                                                         to_date=self.to_date, entity=self.entity,
                                                         created_by=frappe.session.user, issue_no=self.name,
                                                         parenttype="Vehicles", parent=t.vehicle,
                                                         parentfield="liquid_table", record_name=record_name))

    def on_cancel(self):
        self.issue_state = "تم إلغاء تحضير الصرفية"
        if self.issue_to == "جهة":
            current_vehicles = []
            for t in self.vehicles_issuing_table:
                current_vehicles.append(t.vehicle)

                frappe.db.sql(""" DELETE FROM `tabLiquids Issuing Table` where issue_no = '{issue_no}' and parent = '{parent}'
                 """.format(issue_no=self.name, parent=t.vehicle))

            if len(current_vehicles) == 1:
                current_vehicles.append("None")

            # frappe.throw(str(current_vehicles))

            not_in_vehicle_table = frappe.db.sql("""
                            select name
                            from `tabVehicles` 
                            where entity_name = '{cur_entity}'
                            and name not in {current_vehicles}
                        """.format(cur_entity=self.entity, current_vehicles=tuple(current_vehicles)), as_dict=1)

            for z in not_in_vehicle_table:
                frappe.db.sql(""" DELETE FROM `tabLiquids Issuing Table` where issue_no = '{issue_no}' and parent = '{parent}'
                                 """.format(issue_no=self.name, parent=z.name))

            not_in_boat_table = frappe.db.sql("""
                        select name
                        from `tabBoats` 
                        where entity_name = '{cur_entity}'
                        and name not in {current_vehicles}
                    """.format(cur_entity=self.entity, current_vehicles=tuple(current_vehicles)), as_dict=1)

            for w in not_in_boat_table:
                frappe.db.sql(""" DELETE FROM `tabLiquids Issuing Table` where issue_no = '{issue_no}' and parent = '{parent}'
                                 """.format(issue_no=self.name, parent=w.name))

        if self.issue_to == "مركبة أو مجموعة مركبات":
            for t in self.specified_vehicles_issuing_table:
                frappe.db.sql(""" DELETE FROM `tabLiquids Issuing Table` where issue_no = '{issue_no}' and parent = '{parent}'
                                 """.format(issue_no=self.name, parent=t.vehicle))