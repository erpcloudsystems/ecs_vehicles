# Copyright (c) 2022, erpcloud.systems and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class LiquidVouchersIssuing(Document):
	def after_insert(self):
		pass
		'''
		if self.type == "صرفية شهرية":
			self.qty_per_liquid = []
			liquid_issuing = frappe.get_doc("Liquids Issuing", self.liquids_issuing)
			for x in liquid_issuing.qty_per_liquid:
				if x.qty > 0:
					row = self.append("qty_per_liquid", {})
					row.liquid = x.liquid
					row.qty = x.qty
					row.in_words = x.in_words
		'''

	def validate(self):
		for y in self.qty_per_liquid:
			min_code_list = frappe.db.sql(
				""" 
					select min(serial_no) as min, max(serial_no) as max from `tabVoucher`
					where issue_no is null and disabled = 0 
					and serial_no > 0
					and fuel_type = '{liquid}'
				""".format(liquid=y.liquid), as_dict=1)

			if not min_code_list[0]["min"]:
				frappe.throw(" البونات الموجودة لا تكفي ... برجاء إضافة بونات جديدة من " + y.liquid)

			serial = int(min_code_list[0]["min"])
			y.from_serial = serial
			if not int(y.notebook_count):
				frappe.throw(" برجاء إدخال عدد الدفاتر المصروفة من {0} في الصف رقم ".format(y.liquid) + str(y.idx))
			if (serial + (y.notebook_count * 25) - 1) > int(min_code_list[0]["max"]):
				frappe.throw(" البونات الموجودة لا تكفي ... برجاء إضافة بونات جديدة من " + y.liquid)
			to_serial = frappe.db.sql("""
						SELECT serial_no
						FROM `tabVoucher`
						WHERE issue_no is null 
						AND serial_no >= "{serial}"
						AND disabled = 0 
						AND fuel_type = '{liquid}'
						ORDER BY serial_no  
						LIMIT {notebook_count}
					""".format(liquid=y.liquid,serial=serial, notebook_count=int(y.notebook_count) * 25),as_dict=1)
			y.to_serial = to_serial[-1].serial_no

	def on_submit(self):
		for x in self.qty_per_liquid:
			serial_count = x.to_serial - x.from_serial + 1
			voucher = x.from_serial
			while serial_count > 0:
				frappe.db.sql(""" UPDATE `tabVoucher` set issue_no = '{issue_no}', issue_date='{issue_date}', entity='{entity}'
								  WHERE serial_no='{serial_no}' and fuel_type='{fuel_type}' 
							  """.format(issue_no=self.name, issue_date=self.issue_date,
										 entity=self.entity,
										 serial_no=voucher, fuel_type=x.liquid))
				# voucher_name = frappe.get_doc("Voucher", {"serial_no": voucher, "fuel_type": x.liquid})
				# voucher_name.issue_no = self.name
				# voucher_name.issue_date = self.issue_date
				# voucher_name.entity = self.entity
				# voucher_name.save()
				next_serial = voucher + 1
				voucher = next_serial
				serial_count -= 1





		frappe.db.sql(""" UPDATE `tabLiquids Issuing` set issue_state = "تم صرف البونات من خزينة السوائل"
						  WHERE name='{name}' """.format(name=self.liquids_issuing))

		liquid_issuing = frappe.get_doc("Liquids Issuing", self.liquids_issuing)
		liquid_issuing.reload()

	def on_cancel(self):
		for x in self.qty_per_liquid:
			serial_count = int(x.to_serial) - int(x.from_serial) + 1
			voucher = int(x.from_serial)
			while serial_count > 0:
				frappe.db.sql(""" UPDATE `tabVoucher` set issue_no=null, issue_date=null, entity=null
								  WHERE serial_no='{serial_no}' and fuel_type='{fuel_type}' 
							  """.format(serial_no=voucher, fuel_type=x.liquid))

				next_serial = voucher + 1
				voucher = next_serial
				serial_count -= 1

		frappe.db.sql(""" UPDATE `tabLiquids Issuing` set issue_state = "جاري تحضير الصرفية ومراجعتها"
								  WHERE name='{name}' """.format(name=self.liquids_issuing))

		liquid_issuing = frappe.get_doc("Liquids Issuing", self.liquids_issuing)
		liquid_issuing.reload()