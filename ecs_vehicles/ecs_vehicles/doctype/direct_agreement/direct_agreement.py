# Copyright (c) 2023, erpcloud.systems and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import now

class DirectAgreement(Document):
	def validate(self):
		direct_agreement_list = frappe.db.sql(""" Select direct_agreement_no from `tabDirect Agreement`
		where fiscal_year = '{fiscal_year}' and name != '{name}' """.format(name=self.name, fiscal_year=self.fiscal_year), as_dict=1)

		for x in direct_agreement_list:
			if self.direct_agreement_no == x.direct_agreement_no:
				frappe.throw(
					" لا يمكن إستخدام رقم الاتفاق المباشر " + str(x.direct_agreement_no) + " أكثر من مرة ")

		new_agreement_no = self.direct_agreement_no
		new_fiscal_year = self.fiscal_year
		self.document_name = "اتفاق " + "(" + str(new_agreement_no) + ")" + " لسنة " + str(new_fiscal_year)