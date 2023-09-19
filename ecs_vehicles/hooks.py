from . import __version__ as app_version

ecs_vehicles = "ecs_vehicles"
app_title = "ecs_vehicles"
app_publisher = "erpcloud.systems"
app_description = "customizations"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "info@erpcloud.systems"
app_license = "MIT"


doc_events = {
	"Journal Entry": {
		"before_insert": "ecs_vehicles.doctype_triggers.accounting.journal_entry.journal_entry.before_insert",
		"after_insert": "ecs_vehicles.doctype_triggers.accounting.journal_entry.journal_entry.after_insert",
		"onload": "ecs_vehicles.doctype_triggers.accounting.journal_entry.journal_entry.onload",
		"before_validate": "ecs_vehicles.doctype_triggers.accounting.journal_entry.journal_entry.before_validate",
		"validate": "ecs_vehicles.doctype_triggers.accounting.journal_entry.journal_entry.validate",
		"on_submit": "ecs_vehicles.doctype_triggers.accounting.journal_entry.journal_entry.on_submit",
		"on_cancel": "ecs_vehicles.doctype_triggers.accounting.journal_entry.journal_entry.on_cancel",
		"on_update_after_submit": "ecs_vehicles.doctype_triggers.accounting.journal_entry.journal_entry.on_update_after_submit",
		"before_save": "ecs_vehicles.doctype_triggers.accounting.journal_entry.journal_entry.before_save",
		"before_cancel": "ecs_vehicles.doctype_triggers.accounting.journal_entry.journal_entry.before_cancel",
		"on_update": "ecs_vehicles.doctype_triggers.accounting.journal_entry.journal_entry.on_update",
	},
	"Payment Entry": {
		"before_insert": "ecs_vehicles.doctype_triggers.accounting.payment_entry.payment_entry.before_insert",
		"after_insert": "ecs_vehicles.doctype_triggers.accounting.payment_entry.payment_entry.after_insert",
		"onload": "ecs_vehicles.doctype_triggers.accounting.payment_entry.payment_entry.onload",
		"before_validate": "ecs_vehicles.doctype_triggers.accounting.payment_entry.payment_entry.before_validate",
		"validate": "ecs_vehicles.doctype_triggers.accounting.payment_entry.payment_entry.validate",
		"on_submit": "ecs_vehicles.doctype_triggers.accounting.payment_entry.payment_entry.on_submit",
		"on_cancel": "ecs_vehicles.doctype_triggers.accounting.payment_entry.payment_entry.on_cancel",
		"on_update_after_submit": "ecs_vehicles.doctype_triggers.accounting.payment_entry.payment_entry.on_update_after_submit",
		"before_save": "ecs_vehicles.doctype_triggers.accounting.payment_entry.payment_entry.before_save",
		"before_cancel": "ecs_vehicles.doctype_triggers.accounting.payment_entry.payment_entry.before_cancel",
		"on_update": "ecs_vehicles.doctype_triggers.accounting.payment_entry.payment_entry.on_update",
	},
	"Purchase Invoice": {
		"before_insert": "ecs_vehicles.doctype_triggers.accounting.purchase_invoice.purchase_invoice.before_insert",
		"after_insert": "ecs_vehicles.doctype_triggers.accounting.purchase_invoice.purchase_invoice.after_insert",
		"onload": "ecs_vehicles.doctype_triggers.accounting.purchase_invoice.purchase_invoice.onload",
		"before_validate": "ecs_vehicles.doctype_triggers.accounting.purchase_invoice.purchase_invoice.before_validate",
		"validate": "ecs_vehicles.doctype_triggers.accounting.purchase_invoice.purchase_invoice.validate",
		"on_submit": "ecs_vehicles.doctype_triggers.accounting.purchase_invoice.purchase_invoice.on_submit",
		"on_cancel": "ecs_vehicles.doctype_triggers.accounting.purchase_invoice.purchase_invoice.on_cancel",
		"on_update_after_submit": "ecs_vehicles.doctype_triggers.accounting.purchase_invoice.purchase_invoice.on_update_after_submit",
		"before_save": "ecs_vehicles.doctype_triggers.accounting.purchase_invoice.purchase_invoice.before_save",
		"before_cancel": "ecs_vehicles.doctype_triggers.accounting.purchase_invoice.purchase_invoice.before_cancel",
		"on_update": "ecs_vehicles.doctype_triggers.accounting.purchase_invoice.purchase_invoice.on_update",
	},
	"Sales Invoice": {
		"before_insert": "ecs_vehicles.doctype_triggers.accounting.sales_invoice.sales_invoice.before_insert",
		"after_insert": "ecs_vehicles.doctype_triggers.accounting.sales_invoice.sales_invoice.after_insert",
		"onload": "ecs_vehicles.doctype_triggers.accounting.sales_invoice.sales_invoice.onload",
		"before_validate": "ecs_vehicles.doctype_triggers.accounting.sales_invoice.sales_invoice.before_validate",
		"validate": "ecs_vehicles.doctype_triggers.accounting.sales_invoice.sales_invoice.validate",
		"on_submit": "ecs_vehicles.doctype_triggers.accounting.sales_invoice.sales_invoice.on_submit",
		"on_cancel": "ecs_vehicles.doctype_triggers.accounting.sales_invoice.sales_invoice.on_cancel",
		"on_update_after_submit": "ecs_vehicles.doctype_triggers.accounting.sales_invoice.sales_invoice.on_update_after_submit",
		"before_save": "ecs_vehicles.doctype_triggers.accounting.sales_invoice.sales_invoice.before_save",
		"before_cancel": "ecs_vehicles.doctype_triggers.accounting.sales_invoice.sales_invoice.before_cancel",
		"on_update": "ecs_vehicles.doctype_triggers.accounting.sales_invoice.sales_invoice.on_update",
	},
	"Material Request": {
		"before_insert": "ecs_vehicles.doctype_triggers.buying.material_request.material_request.before_insert",
		"after_insert": "ecs_vehicles.doctype_triggers.buying.material_request.material_request.after_insert",
		"onload": "ecs_vehicles.doctype_triggers.buying.material_request.material_request.onload",
		"before_validate": "ecs_vehicles.doctype_triggers.buying.material_request.material_request.before_validate",
		"validate": "ecs_vehicles.doctype_triggers.buying.material_request.material_request.validate",
		"on_submit": "ecs_vehicles.doctype_triggers.buying.material_request.material_request.on_submit",
		"on_cancel": "ecs_vehicles.doctype_triggers.buying.material_request.material_request.on_cancel",
		"on_update_after_submit": "ecs_vehicles.doctype_triggers.buying.material_request.material_request.on_update_after_submit",
		"before_save": "ecs_vehicles.doctype_triggers.buying.material_request.material_request.before_save",
		"before_cancel": "ecs_vehicles.doctype_triggers.buying.material_request.material_request.before_cancel",
		"on_update": "ecs_vehicles.doctype_triggers.buying.material_request.material_request.on_update",
	},
	"Purchase Order": {
		"before_insert": "ecs_vehicles.doctype_triggers.buying.purchase_order.purchase_order.before_insert",
		"after_insert": "ecs_vehicles.doctype_triggers.buying.purchase_order.purchase_order.after_insert",
		"onload": "ecs_vehicles.doctype_triggers.buying.purchase_order.purchase_order.onload",
		"before_validate": "ecs_vehicles.doctype_triggers.buying.purchase_order.purchase_order.before_validate",
		"validate": "ecs_vehicles.doctype_triggers.buying.purchase_order.purchase_order.validate",
		"on_submit": "ecs_vehicles.doctype_triggers.buying.purchase_order.purchase_order.on_submit",
		"on_cancel": "ecs_vehicles.doctype_triggers.buying.purchase_order.purchase_order.on_cancel",
		"on_update_after_submit": "ecs_vehicles.doctype_triggers.buying.purchase_order.purchase_order.on_update_after_submit",
		"before_save": "ecs_vehicles.doctype_triggers.buying.purchase_order.purchase_order.before_save",
		"before_cancel": "ecs_vehicles.doctype_triggers.buying.purchase_order.purchase_order.before_cancel",
		"on_update": "ecs_vehicles.doctype_triggers.buying.purchase_order.purchase_order.on_update",
	},
	"Request For Quotation": {
		"before_insert": "ecs_vehicles.doctype_triggers.buying.request_for_quotation.request_for_quotation.before_insert",
		"after_insert": "ecs_vehicles.doctype_triggers.buying.request_for_quotation.request_for_quotation.after_insert",
		"onload": "ecs_vehicles.doctype_triggers.buying.request_for_quotation.request_for_quotation.onload",
		"before_validate": "ecs_vehicles.doctype_triggers.buying.request_for_quotation.request_for_quotation.before_validate",
		"validate": "ecs_vehicles.doctype_triggers.buying.request_for_quotation.request_for_quotation.validate",
		"on_submit": "ecs_vehicles.doctype_triggers.buying.request_for_quotation.request_for_quotation.on_submit",
		"on_cancel": "ecs_vehicles.doctype_triggers.buying.request_for_quotation.request_for_quotation.on_cancel",
		"on_update_after_submit": "ecs_vehicles.doctype_triggers.buying.request_for_quotation.request_for_quotation.on_update_after_submit",
		"before_save": "ecs_vehicles.doctype_triggers.buying.request_for_quotation.request_for_quotation.before_save",
		"before_cancel": "ecs_vehicles.doctype_triggers.buying.request_for_quotation.request_for_quotation.before_cancel",
		"on_update": "ecs_vehicles.doctype_triggers.buying.request_for_quotation.request_for_quotation.on_update",
	},
	"Supplier": {
		"before_insert": "ecs_vehicles.doctype_triggers.buying.supplier.supplier.before_insert",
		"after_insert": "ecs_vehicles.doctype_triggers.buying.supplier.supplier.after_insert",
		"onload": "ecs_vehicles.doctype_triggers.buying.supplier.supplier.onload",
		"before_validate": "ecs_vehicles.doctype_triggers.buying.supplier.supplier.before_validate",
		"validate": "ecs_vehicles.doctype_triggers.buying.supplier.supplier.validate",
		"on_update_after_submit": "ecs_vehicles.doctype_triggers.buying.supplier.supplier.on_update_after_submit",
		"before_save": "ecs_vehicles.doctype_triggers.buying.supplier.supplier.before_save",
		"on_update": "ecs_vehicles.doctype_triggers.buying.supplier.supplier.on_update",
	},
	"Supplier Group": {
		"before_insert": "ecs_vehicles.doctype_triggers.buying.supplier_group.supplier_group.before_insert",
		"after_insert": "ecs_vehicles.doctype_triggers.buying.supplier_group.supplier_group.after_insert",
		"onload": "ecs_vehicles.doctype_triggers.buying.supplier_group.supplier_group.onload",
		"before_validate": "ecs_vehicles.doctype_triggers.buying.supplier_group.supplier_group.before_validate",
		"validate": "ecs_vehicles.doctype_triggers.buying.supplier_group.supplier_group.validate",
		"on_update_after_submit": "ecs_vehicles.doctype_triggers.buying.supplier_group.supplier_group.on_update_after_submit",
		"before_save": "ecs_vehicles.doctype_triggers.buying.supplier_group.supplier_group.before_save",
		"on_update": "ecs_vehicles.doctype_triggers.buying.supplier_group.supplier_group.on_update",
	},
	"Supplier Quotation": {
		"before_insert": "ecs_vehicles.doctype_triggers.buying.supplier_quotation.supplier_quotation.before_insert",
		"after_insert": "ecs_vehicles.doctype_triggers.buying.supplier_quotation.supplier_quotation.after_insert",
		"onload": "ecs_vehicles.doctype_triggers.buying.supplier_quotation.supplier_quotation.onload",
		"before_validate": "ecs_vehicles.doctype_triggers.buying.supplier_quotation.supplier_quotation.before_validate",
		"validate": "ecs_vehicles.doctype_triggers.buying.supplier_quotation.supplier_quotation.validate",
		"on_submit": "ecs_vehicles.doctype_triggers.buying.supplier_quotation.supplier_quotation.on_submit",
		"on_cancel": "ecs_vehicles.doctype_triggers.buying.supplier_quotation.supplier_quotation.on_cancel",
		"on_update_after_submit": "ecs_vehicles.doctype_triggers.buying.supplier_quotation.supplier_quotation.on_update_after_submit",
		"before_save": "ecs_vehicles.doctype_triggers.buying.supplier_quotation.supplier_quotation.before_save",
		"before_cancel": "ecs_vehicles.doctype_triggers.buying.supplier_quotation.supplier_quotation.before_cancel",
		"on_update": "ecs_vehicles.doctype_triggers.buying.supplier_quotation.supplier_quotation.on_update",
	},
	"Address": {
		"before_insert": "ecs_vehicles.doctype_triggers.crm.address.address.before_insert",
		"after_insert": "ecs_vehicles.doctype_triggers.crm.address.address.after_insert",
		"onload": "ecs_vehicles.doctype_triggers.crm.address.address.onload",
		"before_validate": "ecs_vehicles.doctype_triggers.crm.address.address.before_validate",
		"validate": "ecs_vehicles.doctype_triggers.crm.address.address.validate",
		"on_update_after_submit": "ecs_vehicles.doctype_triggers.crm.address.address.on_update_after_submit",
		"before_save": "ecs_vehicles.doctype_triggers.crm.address.address.before_save",
		"on_update": "ecs_vehicles.doctype_triggers.crm.address.address.on_update",
	},
	"Contact": {
		"before_insert": "ecs_vehicles.doctype_triggers.crm.contact.contact.before_insert",
		"after_insert": "ecs_vehicles.doctype_triggers.crm.contact.contact.after_insert",
		"onload": "ecs_vehicles.doctype_triggers.crm.contact.contact.onload",
		"before_validate": "ecs_vehicles.doctype_triggers.crm.contact.contact.before_validate",
		"validate": "ecs_vehicles.doctype_triggers.crm.contact.contact.validate",
		"on_update_after_submit": "ecs_vehicles.doctype_triggers.crm.contact.contact.on_update_after_submit",
		"before_save": "ecs_vehicles.doctype_triggers.crm.contact.contact.before_save",
		"on_update": "ecs_vehicles.doctype_triggers.crm.contact.contact.on_update",
	},
	"Lead": {
		"before_insert": "ecs_vehicles.doctype_triggers.crm.lead.lead.before_insert",
		"after_insert": "ecs_vehicles.doctype_triggers.crm.lead.lead.after_insert",
		"onload": "ecs_vehicles.doctype_triggers.crm.lead.lead.onload",
		"before_validate": "ecs_vehicles.doctype_triggers.crm.lead.lead.before_validate",
		"validate": "ecs_vehicles.doctype_triggers.crm.lead.lead.validate",
		"on_update_after_submit": "ecs_vehicles.doctype_triggers.crm.lead.lead.on_update_after_submit",
		"before_save": "ecs_vehicles.doctype_triggers.crm.lead.lead.before_save",
		"on_update": "ecs_vehicles.doctype_triggers.crm.lead.lead.on_update",
	},
	"Opportunity": {
		"before_insert": "ecs_vehicles.doctype_triggers.crm.opportunity.opportunity.before_insert",
		"after_insert": "ecs_vehicles.doctype_triggers.crm.opportunity.opportunity.after_insert",
		"onload": "ecs_vehicles.doctype_triggers.crm.opportunity.opportunity.onload",
		"before_validate": "ecs_vehicles.doctype_triggers.crm.opportunity.opportunity.before_validate",
		"validate": "ecs_vehicles.doctype_triggers.crm.opportunity.opportunity.validate",
		"on_update_after_submit": "ecs_vehicles.doctype_triggers.crm.opportunity.opportunity.on_update_after_submit",
		"before_save": "ecs_vehicles.doctype_triggers.crm.opportunity.opportunity.before_save",
		"on_update": "ecs_vehicles.doctype_triggers.crm.opportunity.opportunity.on_update",
	},
	"Employee": {
		"before_insert": "ecs_vehicles.doctype_triggers.hr.employee.employee.before_insert",
		"after_insert": "ecs_vehicles.doctype_triggers.hr.employee.employee.after_insert",
		"onload": "ecs_vehicles.doctype_triggers.hr.employee.employee.onload",
		"before_validate": "ecs_vehicles.doctype_triggers.hr.employee.employee.before_validate",
		"validate": "ecs_vehicles.doctype_triggers.hr.employee.employee.validate",
		"on_update_after_submit": "ecs_vehicles.doctype_triggers.hr.employee.employee.on_update_after_submit",
		"before_save": "ecs_vehicles.doctype_triggers.hr.employee.employee.before_save",
		"on_update": "ecs_vehicles.doctype_triggers.hr.employee.employee.on_update",
	},
	"Employee Checkin": {
		"before_insert": "ecs_vehicles.doctype_triggers.hr.employee_checkin.employee_checkin.before_insert",
		"after_insert": "ecs_vehicles.doctype_triggers.hr.employee_checkin.employee_checkin.after_insert",
		"onload": "ecs_vehicles.doctype_triggers.hr.employee_checkin.employee_checkin.onload",
		"before_validate": "ecs_vehicles.doctype_triggers.hr.employee_checkin.employee_checkin.before_validate",
		"validate": "ecs_vehicles.doctype_triggers.hr.employee_checkin.employee_checkin.validate",
		"on_update_after_submit": "ecs_vehicles.doctype_triggers.hr.employee_checkin.employee_checkin.on_update_after_submit",
		"before_save": "ecs_vehicles.doctype_triggers.hr.employee_checkin.employee_checkin.before_save",
		"on_update": "ecs_vehicles.doctype_triggers.hr.employee_checkin.employee_checkin.on_update",
	},
	"Salary Component": {
		"before_insert": "ecs_vehicles.doctype_triggers.hr.salary_component.salary_component.before_insert",
		"after_insert": "ecs_vehicles.doctype_triggers.hr.salary_component.salary_component.after_insert",
		"onload": "ecs_vehicles.doctype_triggers.hr.salary_component.salary_component.onload",
		"before_validate": "ecs_vehicles.doctype_triggers.hr.salary_component.salary_component.before_validate",
		"validate": "ecs_vehicles.doctype_triggers.hr.salary_component.salary_component.validate",
		"on_update_after_submit": "ecs_vehicles.doctype_triggers.hr.salary_component.salary_component.on_update_after_submit",
		"before_save": "ecs_vehicles.doctype_triggers.hr.salary_component.salary_component.before_save",
		"on_update": "ecs_vehicles.doctype_triggers.hr.salary_component.salary_component.on_update",
	},
	"Additional Salary": {
		"before_insert": "ecs_vehicles.doctype_triggers.hr.additional_salary.additional_salary.before_insert",
		"after_insert": "ecs_vehicles.doctype_triggers.hr.additional_salary.additional_salary.after_insert",
		"onload": "ecs_vehicles.doctype_triggers.hr.additional_salary.additional_salary.onload",
		"before_validate": "ecs_vehicles.doctype_triggers.hr.additional_salary.additional_salary.before_validate",
		"validate": "ecs_vehicles.doctype_triggers.hr.additional_salary.additional_salary.validate",
		"on_submit": "ecs_vehicles.doctype_triggers.hr.additional_salary.additional_salary.on_submit",
		"on_cancel": "ecs_vehicles.doctype_triggers.hr.additional_salary.additional_salary.on_cancel",
		"on_update_after_submit": "ecs_vehicles.doctype_triggers.hr.additional_salary.additional_salary.on_update_after_submit",
		"before_save": "ecs_vehicles.doctype_triggers.hr.additional_salary.additional_salary.before_save",
		"before_cancel": "ecs_vehicles.doctype_triggers.hr.additional_salary.additional_salary.before_cancel",
		"on_update": "ecs_vehicles.doctype_triggers.hr.additional_salary.additional_salary.on_update",
	},
	"Attendance": {
		"before_insert": "ecs_vehicles.doctype_triggers.hr.attendance.attendance.before_insert",
		"after_insert": "ecs_vehicles.doctype_triggers.hr.attendance.attendance.after_insert",
		"onload": "ecs_vehicles.doctype_triggers.hr.attendance.attendance.onload",
		"before_validate": "ecs_vehicles.doctype_triggers.hr.attendance.attendance.before_validate",
		"validate": "ecs_vehicles.doctype_triggers.hr.attendance.attendance.validate",
		"on_submit": "ecs_vehicles.doctype_triggers.hr.attendance.attendance.on_submit",
		"on_cancel": "ecs_vehicles.doctype_triggers.hr.attendance.attendance.on_cancel",
		"on_update_after_submit": "ecs_vehicles.doctype_triggers.hr.attendance.attendance.on_update_after_submit",
		"before_save": "ecs_vehicles.doctype_triggers.hr.attendance.attendance.before_save",
		"before_cancel": "ecs_vehicles.doctype_triggers.hr.attendance.attendance.before_cancel",
		"on_update": "ecs_vehicles.doctype_triggers.hr.attendance.attendance.on_update",
	},
	"Attendance Request": {
		"before_insert": "ecs_vehicles.doctype_triggers.hr.attendance_request.attendance_request.before_insert",
		"after_insert": "ecs_vehicles.doctype_triggers.hr.attendance_request.attendance_request.after_insert",
		"onload": "ecs_vehicles.doctype_triggers.hr.attendance_request.attendance_request.onload",
		"before_validate": "ecs_vehicles.doctype_triggers.hr.attendance_request.attendance_request.before_validate",
		"validate": "ecs_vehicles.doctype_triggers.hr.attendance_request.attendance_request.validate",
		"on_submit": "ecs_vehicles.doctype_triggers.hr.attendance_request.attendance_request.on_submit",
		"on_cancel": "ecs_vehicles.doctype_triggers.hr.attendance_request.attendance_request.on_cancel",
		"on_update_after_submit": "ecs_vehicles.doctype_triggers.hr.attendance_request.attendance_request.on_update_after_submit",
		"before_save": "ecs_vehicles.doctype_triggers.hr.attendance_request.attendance_request.before_save",
		"before_cancel": "ecs_vehicles.doctype_triggers.hr.attendance_request.attendance_request.before_cancel",
		"on_update": "ecs_vehicles.doctype_triggers.hr.attendance_request.attendance_request.on_update",
	},
	"Employee Advance": {
		"before_insert": "ecs_vehicles.doctype_triggers.hr.employee_advance.employee_advance.before_insert",
		"after_insert": "ecs_vehicles.doctype_triggers.hr.employee_advance.employee_advance.after_insert",
		"onload": "ecs_vehicles.doctype_triggers.hr.employee_advance.employee_advance.onload",
		"before_validate": "ecs_vehicles.doctype_triggers.hr.employee_advance.employee_advance.before_validate",
		"validate": "ecs_vehicles.doctype_triggers.hr.employee_advance.employee_advance.validate",
		"on_submit": "ecs_vehicles.doctype_triggers.hr.employee_advance.employee_advance.on_submit",
		"on_cancel": "ecs_vehicles.doctype_triggers.hr.employee_advance.employee_advance.on_cancel",
		"on_update_after_submit": "ecs_vehicles.doctype_triggers.hr.employee_advance.employee_advance.on_update_after_submit",
		"before_save": "ecs_vehicles.doctype_triggers.hr.employee_advance.employee_advance.before_save",
		"before_cancel": "ecs_vehicles.doctype_triggers.hr.employee_advance.employee_advance.before_cancel",
		"on_update": "ecs_vehicles.doctype_triggers.hr.employee_advance.employee_advance.on_update",
	},
	"Expense Claim": {
		"before_insert": "ecs_vehicles.doctype_triggers.hr.expense_claim.expense_claim.before_insert",
		"after_insert": "ecs_vehicles.doctype_triggers.hr.expense_claim.expense_claim.after_insert",
		"onload": "ecs_vehicles.doctype_triggers.hr.expense_claim.expense_claim.onload",
		"before_validate": "ecs_vehicles.doctype_triggers.hr.expense_claim.expense_claim.before_validate",
		"validate": "ecs_vehicles.doctype_triggers.hr.expense_claim.expense_claim.validate",
		"on_submit": "ecs_vehicles.doctype_triggers.hr.expense_claim.expense_claim.on_submit",
		"on_cancel": "ecs_vehicles.doctype_triggers.hr.expense_claim.expense_claim.on_cancel",
		"on_update_after_submit": "ecs_vehicles.doctype_triggers.hr.expense_claim.expense_claim.on_update_after_submit",
		"before_save": "ecs_vehicles.doctype_triggers.hr.expense_claim.expense_claim.before_save",
		"before_cancel": "ecs_vehicles.doctype_triggers.hr.expense_claim.expense_claim.before_cancel",
		"on_update": "ecs_vehicles.doctype_triggers.hr.expense_claim.expense_claim.on_update",
	},
	"Leave Application": {
		"before_insert": "ecs_vehicles.doctype_triggers.hr.leave_application.leave_application.before_insert",
		"after_insert": "ecs_vehicles.doctype_triggers.hr.leave_application.leave_application.after_insert",
		"onload": "ecs_vehicles.doctype_triggers.hr.leave_application.leave_application.onload",
		"before_validate": "ecs_vehicles.doctype_triggers.hr.leave_application.leave_application.before_validate",
		"validate": "ecs_vehicles.doctype_triggers.hr.leave_application.leave_application.validate",
		"on_submit": "ecs_vehicles.doctype_triggers.hr.leave_application.leave_application.on_submit",
		"on_cancel": "ecs_vehicles.doctype_triggers.hr.leave_application.leave_application.on_cancel",
		"on_update_after_submit": "ecs_vehicles.doctype_triggers.hr.leave_application.leave_application.on_update_after_submit",
		"before_save": "ecs_vehicles.doctype_triggers.hr.leave_application.leave_application.before_save",
		"before_cancel": "ecs_vehicles.doctype_triggers.hr.leave_application.leave_application.before_cancel",
		"on_update": "ecs_vehicles.doctype_triggers.hr.leave_application.leave_application.on_update",
	},
	"Loan": {
		"before_insert": "ecs_vehicles.doctype_triggers.hr.loan.loan.before_insert",
		"after_insert": "ecs_vehicles.doctype_triggers.hr.loan.loan.after_insert",
		"onload": "ecs_vehicles.doctype_triggers.hr.loan.loan.onload",
		"before_validate": "ecs_vehicles.doctype_triggers.hr.loan.loan.before_validate",
		"validate": "ecs_vehicles.doctype_triggers.hr.loan.loan.validate",
		"on_submit": "ecs_vehicles.doctype_triggers.hr.loan.loan.on_submit",
		"on_cancel": "ecs_vehicles.doctype_triggers.hr.loan.loan.on_cancel",
		"on_update_after_submit": "ecs_vehicles.doctype_triggers.hr.loan.loan.on_update_after_submit",
		"before_save": "ecs_vehicles.doctype_triggers.hr.loan.loan.before_save",
		"before_cancel": "ecs_vehicles.doctype_triggers.hr.loan.loan.before_cancel",
		"on_update": "ecs_vehicles.doctype_triggers.hr.loan.loan.on_update",
	},
	"Loan Application": {
		"before_insert": "ecs_vehicles.doctype_triggers.hr.loan_application.loan_application.before_insert",
		"after_insert": "ecs_vehicles.doctype_triggers.hr.loan_application.loan_application.after_insert",
		"onload": "ecs_vehicles.doctype_triggers.hr.loan_application.loan_application.onload",
		"before_validate": "ecs_vehicles.doctype_triggers.hr.loan_application.loan_application.before_validate",
		"validate": "ecs_vehicles.doctype_triggers.hr.loan_application.loan_application.validate",
		"on_submit": "ecs_vehicles.doctype_triggers.hr.loan_application.loan_application.on_submit",
		"on_cancel": "ecs_vehicles.doctype_triggers.hr.loan_application.loan_application.on_cancel",
		"on_update_after_submit": "ecs_vehicles.doctype_triggers.hr.loan_application.loan_application.on_update_after_submit",
		"before_save": "ecs_vehicles.doctype_triggers.hr.loan_application.loan_application.before_save",
		"before_cancel": "ecs_vehicles.doctype_triggers.hr.loan_application.loan_application.before_cancel",
		"on_update": "ecs_vehicles.doctype_triggers.hr.loan_application.loan_application.on_update",
	},
	"Loan Disbursement": {
		"before_insert": "ecs_vehicles.doctype_triggers.hr.loan_disbursement.loan_disbursement.before_insert",
		"after_insert": "ecs_vehicles.doctype_triggers.hr.loan_disbursement.loan_disbursement.after_insert",
		"onload": "ecs_vehicles.doctype_triggers.hr.loan_disbursement.loan_disbursement.onload",
		"before_validate": "ecs_vehicles.doctype_triggers.hr.loan_disbursement.loan_disbursement.before_validate",
		"validate": "ecs_vehicles.doctype_triggers.hr.loan_disbursement.loan_disbursement.validate",
		"on_submit": "ecs_vehicles.doctype_triggers.hr.loan_disbursement.loan_disbursement.on_submit",
		"on_cancel": "ecs_vehicles.doctype_triggers.hr.loan_disbursement.loan_disbursement.on_cancel",
		"on_update_after_submit": "ecs_vehicles.doctype_triggers.hr.loan_disbursement.loan_disbursement.on_update_after_submit",
		"before_save": "ecs_vehicles.doctype_triggers.hr.loan_disbursement.loan_disbursement.before_save",
		"before_cancel": "ecs_vehicles.doctype_triggers.hr.loan_disbursement.loan_disbursement.before_cancel",
		"on_update": "ecs_vehicles.doctype_triggers.hr.loan_disbursement.loan_disbursement.on_update",
	},
	"Loan Repayment": {
		"before_insert": "ecs_vehicles.doctype_triggers.hr.loan_repayment.loan_repayment.before_insert",
		"after_insert": "ecs_vehicles.doctype_triggers.hr.loan_repayment.loan_repayment.after_insert",
		"onload": "ecs_vehicles.doctype_triggers.hr.loan_repayment.loan_repayment.onload",
		"before_validate": "ecs_vehicles.doctype_triggers.hr.loan_repayment.loan_repayment.before_validate",
		"validate": "ecs_vehicles.doctype_triggers.hr.loan_repayment.loan_repayment.validate",
		"on_submit": "ecs_vehicles.doctype_triggers.hr.loan_repayment.loan_repayment.on_submit",
		"on_cancel": "ecs_vehicles.doctype_triggers.hr.loan_repayment.loan_repayment.on_cancel",
		"on_update_after_submit": "ecs_vehicles.doctype_triggers.hr.loan_repayment.loan_repayment.on_update_after_submit",
		"before_save": "ecs_vehicles.doctype_triggers.hr.loan_repayment.loan_repayment.before_save",
		"before_cancel": "ecs_vehicles.doctype_triggers.hr.loan_repayment.loan_repayment.before_cancel",
		"on_update": "ecs_vehicles.doctype_triggers.hr.loan_repayment.loan_repayment.on_update",
	},
	"Loan Type": {
		"before_insert": "ecs_vehicles.doctype_triggers.hr.loan_type.loan_type.before_insert",
		"after_insert": "ecs_vehicles.doctype_triggers.hr.loan_type.loan_type.after_insert",
		"onload": "ecs_vehicles.doctype_triggers.hr.loan_type.loan_type.onload",
		"before_validate": "ecs_vehicles.doctype_triggers.hr.loan_type.loan_type.before_validate",
		"validate": "ecs_vehicles.doctype_triggers.hr.loan_type.loan_type.validate",
		"on_submit": "ecs_vehicles.doctype_triggers.hr.loan_type.loan_type.on_submit",
		"on_cancel": "ecs_vehicles.doctype_triggers.hr.loan_type.loan_type.on_cancel",
		"on_update_after_submit": "ecs_vehicles.doctype_triggers.hr.loan_type.loan_type.on_update_after_submit",
		"before_save": "ecs_vehicles.doctype_triggers.hr.loan_type.loan_type.before_save",
		"before_cancel": "ecs_vehicles.doctype_triggers.hr.loan_type.loan_type.before_cancel",
		"on_update": "ecs_vehicles.doctype_triggers.hr.loan_type.loan_type.on_update",
	},
	"Payroll Entry": {
		"before_insert": "ecs_vehicles.doctype_triggers.hr.payroll_entry.payroll_entry.before_insert",
		"after_insert": "ecs_vehicles.doctype_triggers.hr.payroll_entry.payroll_entry.after_insert",
		"onload": "ecs_vehicles.doctype_triggers.hr.payroll_entry.payroll_entry.onload",
		"before_validate": "ecs_vehicles.doctype_triggers.hr.payroll_entry.payroll_entry.before_validate",
		"validate": "ecs_vehicles.doctype_triggers.hr.payroll_entry.payroll_entry.validate",
		"on_submit": "ecs_vehicles.doctype_triggers.hr.payroll_entry.payroll_entry.on_submit",
		"on_cancel": "ecs_vehicles.doctype_triggers.hr.payroll_entry.payroll_entry.on_cancel",
		"on_update_after_submit": "ecs_vehicles.doctype_triggers.hr.payroll_entry.payroll_entry.on_update_after_submit",
		"before_save": "ecs_vehicles.doctype_triggers.hr.payroll_entry.payroll_entry.before_save",
		"before_cancel": "ecs_vehicles.doctype_triggers.hr.payroll_entry.payroll_entry.before_cancel",
		"on_update": "ecs_vehicles.doctype_triggers.hr.payroll_entry.payroll_entry.on_update",
	},
	"Salary Slip": {
		"before_insert": "ecs_vehicles.doctype_triggers.hr.salary_slip.salary_slip.before_insert",
		"after_insert": "ecs_vehicles.doctype_triggers.hr.salary_slip.salary_slip.after_insert",
		"onload": "ecs_vehicles.doctype_triggers.hr.salary_slip.salary_slip.onload",
		"before_validate": "ecs_vehicles.doctype_triggers.hr.salary_slip.salary_slip.before_validate",
		"validate": "ecs_vehicles.doctype_triggers.hr.salary_slip.salary_slip.validate",
		"on_submit": "ecs_vehicles.doctype_triggers.hr.salary_slip.salary_slip.on_submit",
		"on_cancel": "ecs_vehicles.doctype_triggers.hr.salary_slip.salary_slip.on_cancel",
		"on_update_after_submit": "ecs_vehicles.doctype_triggers.hr.salary_slip.salary_slip.on_update_after_submit",
		"before_save": "ecs_vehicles.doctype_triggers.hr.salary_slip.salary_slip.before_save",
		"before_cancel": "ecs_vehicles.doctype_triggers.hr.salary_slip.salary_slip.before_cancel",
		"on_update": "ecs_vehicles.doctype_triggers.hr.salary_slip.salary_slip.on_update",
	},
	"Salary Structure": {
		"before_insert": "ecs_vehicles.doctype_triggers.hr.salary_structure.salary_structure.before_insert",
		"after_insert": "ecs_vehicles.doctype_triggers.hr.salary_structure.salary_structure.after_insert",
		"onload": "ecs_vehicles.doctype_triggers.hr.salary_structure.salary_structure.onload",
		"before_validate": "ecs_vehicles.doctype_triggers.hr.salary_structure.salary_structure.before_validate",
		"validate": "ecs_vehicles.doctype_triggers.hr.salary_structure.salary_structure.validate",
		"on_submit": "ecs_vehicles.doctype_triggers.hr.salary_structure.salary_structure.on_submit",
		"on_cancel": "ecs_vehicles.doctype_triggers.hr.salary_structure.salary_structure.on_cancel",
		"on_update_after_submit": "ecs_vehicles.doctype_triggers.hr.salary_structure.salary_structure.on_update_after_submit",
		"before_save": "ecs_vehicles.doctype_triggers.hr.salary_structure.salary_structure.before_save",
		"before_cancel": "ecs_vehicles.doctype_triggers.hr.salary_structure.salary_structure.before_cancel",
		"on_update": "ecs_vehicles.doctype_triggers.hr.salary_structure.salary_structure.on_update",
	},
	"BOM": {
		"before_insert": "ecs_vehicles.doctype_triggers.manufacturing.bom.bom.before_insert",
		"after_insert": "ecs_vehicles.doctype_triggers.manufacturing.bom.bom.after_insert",
		"onload": "ecs_vehicles.doctype_triggers.manufacturing.bom.bom.onload",
		"before_validate": "ecs_vehicles.doctype_triggers.manufacturing.bom.bom.before_validate",
		"validate": "ecs_vehicles.doctype_triggers.manufacturing.bom.bom.validate",
		"on_submit": "ecs_vehicles.doctype_triggers.manufacturing.bom.bom.on_submit",
		"on_cancel": "ecs_vehicles.doctype_triggers.manufacturing.bom.bom.on_cancel",
		"on_update_after_submit": "ecs_vehicles.doctype_triggers.manufacturing.bom.bom.on_update_after_submit",
		"before_save": "ecs_vehicles.doctype_triggers.manufacturing.bom.bom.before_save",
		"before_cancel": "ecs_vehicles.doctype_triggers.manufacturing.bom.bom.before_cancel",
		"on_update": "ecs_vehicles.doctype_triggers.manufacturing.bom.bom.on_update",
	},
	"Job Card": {
		"before_insert": "ecs_vehicles.doctype_triggers.manufacturing.job_card.job_card.before_insert",
		"after_insert": "ecs_vehicles.doctype_triggers.manufacturing.job_card.job_card.after_insert",
		"onload": "ecs_vehicles.doctype_triggers.manufacturing.job_card.job_card.onload",
		"before_validate": "ecs_vehicles.doctype_triggers.manufacturing.job_card.job_card.before_validate",
		"validate": "ecs_vehicles.doctype_triggers.manufacturing.job_card.job_card.validate",
		"on_submit": "ecs_vehicles.doctype_triggers.manufacturing.job_card.job_card.on_submit",
		"on_cancel": "ecs_vehicles.doctype_triggers.manufacturing.job_card.job_card.on_cancel",
		"on_update_after_submit": "ecs_vehicles.doctype_triggers.manufacturing.job_card.job_card.on_update_after_submit",
		"before_save": "ecs_vehicles.doctype_triggers.manufacturing.job_card.job_card.before_save",
		"before_cancel": "ecs_vehicles.doctype_triggers.manufacturing.job_card.job_card.before_cancel",
		"on_update": "ecs_vehicles.doctype_triggers.manufacturing.job_card.job_card.on_update",
	},
	"Work Order": {
		"before_insert": "ecs_vehicles.doctype_triggers.manufacturing.work_order.work_order.before_insert",
		"after_insert": "ecs_vehicles.doctype_triggers.manufacturing.work_order.work_order.after_insert",
		"onload": "ecs_vehicles.doctype_triggers.manufacturing.work_order.work_order.onload",
		"before_validate": "ecs_vehicles.doctype_triggers.manufacturing.work_order.work_order.before_validate",
		"validate": "ecs_vehicles.doctype_triggers.manufacturing.work_order.work_order.validate",
		"on_submit": "ecs_vehicles.doctype_triggers.manufacturing.work_order.work_order.on_submit",
		"on_cancel": "ecs_vehicles.doctype_triggers.manufacturing.work_order.work_order.on_cancel",
		"on_update_after_submit": "ecs_vehicles.doctype_triggers.manufacturing.work_order.work_order.on_update_after_submit",
		"before_save": "ecs_vehicles.doctype_triggers.manufacturing.work_order.work_order.before_save",
		"before_cancel": "ecs_vehicles.doctype_triggers.manufacturing.work_order.work_order.before_cancel",
		"on_update": "ecs_vehicles.doctype_triggers.manufacturing.work_order.work_order.on_update",
	},
	"Project": {
		"before_insert": "ecs_vehicles.doctype_triggers.projects.project.project.before_insert",
		"after_insert": "ecs_vehicles.doctype_triggers.projects.project.project.after_insert",
		"onload": "ecs_vehicles.doctype_triggers.projects.project.project.onload",
		"before_validate": "ecs_vehicles.doctype_triggers.projects.project.project.before_validate",
		"validate": "ecs_vehicles.doctype_triggers.projects.project.project.validate",
		"before_save": "ecs_vehicles.doctype_triggers.projects.project.project.before_save",
		"on_update": "ecs_vehicles.doctype_triggers.projects.project.project.on_update",
	},
	"Task": {
		"before_insert": "ecs_vehicles.doctype_triggers.projects.task.task.before_insert",
		"after_insert": "ecs_vehicles.doctype_triggers.projects.task.task.after_insert",
		"onload": "ecs_vehicles.doctype_triggers.projects.task.task.onload",
		"before_validate": "ecs_vehicles.doctype_triggers.projects.task.task.before_validate",
		"validate": "ecs_vehicles.doctype_triggers.projects.task.task.validate",
		"before_save": "ecs_vehicles.doctype_triggers.projects.task.task.before_save",
		"on_update": "ecs_vehicles.doctype_triggers.projects.task.task.on_update",
	},
	"Timesheet": {
		"before_insert": "ecs_vehicles.doctype_triggers.projects.timesheet.timesheet.before_insert",
		"after_insert": "ecs_vehicles.doctype_triggers.projects.timesheet.timesheet.after_insert",
		"onload": "ecs_vehicles.doctype_triggers.projects.timesheet.timesheet.onload",
		"before_validate": "ecs_vehicles.doctype_triggers.projects.timesheet.timesheet.before_validate",
		"validate": "ecs_vehicles.doctype_triggers.projects.timesheet.timesheet.validate",
		"before_save": "ecs_vehicles.doctype_triggers.projects.timesheet.timesheet.before_save",
		"on_update": "ecs_vehicles.doctype_triggers.projects.timesheet.timesheet.on_update",
	},
	"Customer": {
		"before_insert": "ecs_vehicles.doctype_triggers.selling.customer.customer.before_insert",
		"after_insert": "ecs_vehicles.doctype_triggers.selling.customer.customer.after_insert",
		"onload": "ecs_vehicles.doctype_triggers.selling.customer.customer.onload",
		"before_validate": "ecs_vehicles.doctype_triggers.selling.customer.customer.before_validate",
		"validate": "ecs_vehicles.doctype_triggers.selling.customer.customer.validate",
		"before_save": "ecs_vehicles.doctype_triggers.selling.customer.customer.before_save",
		"on_update": "ecs_vehicles.doctype_triggers.selling.customer.customer.on_update",
	},
	"Customer Group": {
		"before_insert": "ecs_vehicles.doctype_triggers.selling.customer_group.customer_group.before_insert",
		"after_insert": "ecs_vehicles.doctype_triggers.selling.customer_group.customer_group.after_insert",
		"onload": "ecs_vehicles.doctype_triggers.selling.customer_group.customer_group.onload",
		"before_validate": "ecs_vehicles.doctype_triggers.selling.customer_group.customer_group.before_validate",
		"validate": "ecs_vehicles.doctype_triggers.selling.customer_group.customer_group.validate",
		"before_save": "ecs_vehicles.doctype_triggers.selling.customer_group.customer_group.before_save",
		"on_update": "ecs_vehicles.doctype_triggers.selling.customer_group.customer_group.on_update",
	},
	"Pricing Rule": {
		"before_insert": "ecs_vehicles.doctype_triggers.selling.pricing_rule.pricing_rule.before_insert",
		"after_insert": "ecs_vehicles.doctype_triggers.selling.pricing_rule.pricing_rule.after_insert",
		"onload": "ecs_vehicles.doctype_triggers.selling.pricing_rule.pricing_rule.onload",
		"before_validate": "ecs_vehicles.doctype_triggers.selling.pricing_rule.pricing_rule.before_validate",
		"validate": "ecs_vehicles.doctype_triggers.selling.pricing_rule.pricing_rule.validate",
		"before_save": "ecs_vehicles.doctype_triggers.selling.pricing_rule.pricing_rule.before_save",
		"on_update": "ecs_vehicles.doctype_triggers.selling.pricing_rule.pricing_rule.on_update",
	},
	"Sales Partner": {
		"before_insert": "ecs_vehicles.doctype_triggers.selling.sales_partner.sales_partner.before_insert",
		"after_insert": "ecs_vehicles.doctype_triggers.selling.sales_partner.sales_partner.after_insert",
		"onload": "ecs_vehicles.doctype_triggers.selling.sales_partner.sales_partner.onload",
		"before_validate": "ecs_vehicles.doctype_triggers.selling.sales_partner.sales_partner.before_validate",
		"validate": "ecs_vehicles.doctype_triggers.selling.sales_partner.sales_partner.validate",
		"before_save": "ecs_vehicles.doctype_triggers.selling.sales_partner.sales_partner.before_save",
		"on_update": "ecs_vehicles.doctype_triggers.selling.sales_partner.sales_partner.on_update",
	},
	"Sales Person": {
		"before_insert": "ecs_vehicles.doctype_triggers.selling.sales_person.sales_person.before_insert",
		"after_insert": "ecs_vehicles.doctype_triggers.selling.sales_person.sales_person.after_insert",
		"onload": "ecs_vehicles.doctype_triggers.selling.sales_person.sales_person.onload",
		"before_validate": "ecs_vehicles.doctype_triggers.selling.sales_person.sales_person.before_validate",
		"validate": "ecs_vehicles.doctype_triggers.selling.sales_person.sales_person.validate",
		"before_save": "ecs_vehicles.doctype_triggers.selling.sales_person.sales_person.before_save",
		"on_update": "ecs_vehicles.doctype_triggers.selling.sales_person.sales_person.on_update",
	},
	"Quotation": {
		"before_insert": "ecs_vehicles.doctype_triggers.selling.quotation.quotation.before_insert",
		"after_insert": "ecs_vehicles.doctype_triggers.selling.quotation.quotation.after_insert",
		"onload": "ecs_vehicles.doctype_triggers.selling.quotation.quotation.onload",
		"before_validate": "ecs_vehicles.doctype_triggers.selling.quotation.quotation.before_validate",
		"validate": "ecs_vehicles.doctype_triggers.selling.quotation.quotation.validate",
		"on_submit": "ecs_vehicles.doctype_triggers.selling.quotation.quotation.on_submit",
		"on_cancel": "ecs_vehicles.doctype_triggers.selling.quotation.quotation.on_cancel",
		"on_update_after_submit": "ecs_vehicles.doctype_triggers.selling.quotation.quotation.on_update_after_submit",
		"before_save": "ecs_vehicles.doctype_triggers.selling.quotation.quotation.before_save",
		"before_cancel": "ecs_vehicles.doctype_triggers.selling.quotation.quotation.before_cancel",
		"on_update": "ecs_vehicles.doctype_triggers.selling.quotation.quotation.on_update",
	},
	"Sales Order": {
		"before_insert": "ecs_vehicles.doctype_triggers.selling.sales_order.sales_order.before_insert",
		"after_insert": "ecs_vehicles.doctype_triggers.selling.sales_order.sales_order.after_insert",
		"onload": "ecs_vehicles.doctype_triggers.selling.sales_order.sales_order.onload",
		"before_validate": "ecs_vehicles.doctype_triggers.selling.sales_order.sales_order.before_validate",
		"validate": "ecs_vehicles.doctype_triggers.selling.sales_order.sales_order.validate",
		"on_submit": "ecs_vehicles.doctype_triggers.selling.sales_order.sales_order.on_submit",
		"on_cancel": "ecs_vehicles.doctype_triggers.selling.sales_order.sales_order.on_cancel",
		"on_update_after_submit": "ecs_vehicles.doctype_triggers.selling.sales_order.sales_order.on_update_after_submit",
		"before_save": "ecs_vehicles.doctype_triggers.selling.sales_order.sales_order.before_save",
		"before_cancel": "ecs_vehicles.doctype_triggers.selling.sales_order.sales_order.before_cancel",
		"on_update": "ecs_vehicles.doctype_triggers.selling.sales_order.sales_order.on_update",
	},
	"Delivery Note": {
		"before_insert": "ecs_vehicles.doctype_triggers.stock.delivery_note.delivery_note.before_insert",
		"after_insert": "ecs_vehicles.doctype_triggers.stock.delivery_note.delivery_note.after_insert",
		"onload": "ecs_vehicles.doctype_triggers.stock.delivery_note.delivery_note.onload",
		"before_validate": "ecs_vehicles.doctype_triggers.stock.delivery_note.delivery_note.before_validate",
		"validate": "ecs_vehicles.doctype_triggers.stock.delivery_note.delivery_note.validate",
		"on_submit": "ecs_vehicles.doctype_triggers.stock.delivery_note.delivery_note.on_submit",
		"on_cancel": "ecs_vehicles.doctype_triggers.stock.delivery_note.delivery_note.on_cancel",
		"on_update_after_submit": "ecs_vehicles.doctype_triggers.stock.delivery_note.delivery_note.on_update_after_submit",
		"before_save": "ecs_vehicles.doctype_triggers.stock.delivery_note.delivery_note.before_save",
		"before_cancel": "ecs_vehicles.doctype_triggers.stock.delivery_note.delivery_note.before_cancel",
		"on_update": "ecs_vehicles.doctype_triggers.stock.delivery_note.delivery_note.on_update",
	},
	"Purchase Receipt": {
		"before_insert": "ecs_vehicles.doctype_triggers.stock.purchase_receipt.purchase_receipt.before_insert",
		"after_insert": "ecs_vehicles.doctype_triggers.stock.purchase_receipt.purchase_receipt.after_insert",
		"onload": "ecs_vehicles.doctype_triggers.stock.purchase_receipt.purchase_receipt.onload",
		"before_validate": "ecs_vehicles.doctype_triggers.stock.purchase_receipt.purchase_receipt.before_validate",
		"validate": "ecs_vehicles.doctype_triggers.stock.purchase_receipt.purchase_receipt.validate",
		"on_submit": "ecs_vehicles.doctype_triggers.stock.purchase_receipt.purchase_receipt.on_submit",
		"on_cancel": "ecs_vehicles.doctype_triggers.stock.purchase_receipt.purchase_receipt.on_cancel",
		"on_update_after_submit": "ecs_vehicles.doctype_triggers.stock.purchase_receipt.purchase_receipt.on_update_after_submit",
		"before_save": "ecs_vehicles.doctype_triggers.stock.purchase_receipt.purchase_receipt.before_save",
		"before_cancel": "ecs_vehicles.doctype_triggers.stock.purchase_receipt.purchase_receipt.before_cancel",
		"on_update": "ecs_vehicles.doctype_triggers.stock.purchase_receipt.purchase_receipt.on_update",
	},
	"Stock Entry": {
		"before_insert": "ecs_vehicles.doctype_triggers.stock.stock_entry.stock_entry.before_insert",
		"after_insert": "ecs_vehicles.doctype_triggers.stock.stock_entry.stock_entry.after_insert",
		"onload": "ecs_vehicles.doctype_triggers.stock.stock_entry.stock_entry.onload",
		"before_validate": "ecs_vehicles.doctype_triggers.stock.stock_entry.stock_entry.before_validate",
		"validate": "ecs_vehicles.doctype_triggers.stock.stock_entry.stock_entry.validate",
		"on_submit": "ecs_vehicles.doctype_triggers.stock.stock_entry.stock_entry.on_submit",
		"on_cancel": "ecs_vehicles.doctype_triggers.stock.stock_entry.stock_entry.on_cancel",
		"on_update_after_submit": "ecs_vehicles.doctype_triggers.stock.stock_entry.stock_entry.on_update_after_submit",
		"before_save": "ecs_vehicles.doctype_triggers.stock.stock_entry.stock_entry.before_save",
		"before_cancel": "ecs_vehicles.doctype_triggers.stock.stock_entry.stock_entry.before_cancel",
		"on_update": "ecs_vehicles.doctype_triggers.stock.stock_entry.stock_entry.on_update",
	},
	"Stock Reconciliation": {
		"before_insert": "ecs_vehicles.doctype_triggers.stock.stock_reconciliation.stock_reconciliation.before_insert",
		"after_insert": "ecs_vehicles.doctype_triggers.stock.stock_reconciliation.stock_reconciliation.after_insert",
		"onload": "ecs_vehicles.doctype_triggers.stock.stock_reconciliation.stock_reconciliation.onload",
		"before_validate": "ecs_vehicles.doctype_triggers.stock.stock_reconciliation.stock_reconciliation.before_validate",
		"validate": "ecs_vehicles.doctype_triggers.stock.stock_reconciliation.stock_reconciliation.validate",
		"on_submit": "ecs_vehicles.doctype_triggers.stock.stock_reconciliation.stock_reconciliation.on_submit",
		"on_cancel": "ecs_vehicles.doctype_triggers.stock.stock_reconciliation.stock_reconciliation.on_cancel",
		"on_update_after_submit": "ecs_vehicles.doctype_triggers.stock.stock_reconciliation.stock_reconciliation.on_update_after_submit",
		"before_save": "ecs_vehicles.doctype_triggers.stock.stock_reconciliation.stock_reconciliation.before_save",
		"before_cancel": "ecs_vehicles.doctype_triggers.stock.stock_reconciliation.stock_reconciliation.before_cancel",
		"on_update": "ecs_vehicles.doctype_triggers.stock.stock_reconciliation.stock_reconciliation.on_update",
	},
	"Item": {
		"before_insert": "ecs_vehicles.doctype_triggers.stock.item.item.before_insert",
		"after_insert": "ecs_vehicles.doctype_triggers.stock.item.item.after_insert",
		"onload": "ecs_vehicles.doctype_triggers.stock.item.item.onload",
		"before_validate": "ecs_vehicles.doctype_triggers.stock.item.item.before_validate",
		"validate": "ecs_vehicles.doctype_triggers.stock.item.item.validate",
		"before_save": "ecs_vehicles.doctype_triggers.stock.item.item.before_save",
		"on_update": "ecs_vehicles.doctype_triggers.stock.item.item.on_update",
	},
	"Item Group": {
		"before_insert": "ecs_vehicles.doctype_triggers.stock.item_group.item_group.before_insert",
		"after_insert": "ecs_vehicles.doctype_triggers.stock.item_group.item_group.after_insert",
		"onload": "ecs_vehicles.doctype_triggers.stock.item_group.item_group.onload",
		"before_validate": "ecs_vehicles.doctype_triggers.stock.item_group.item_group.before_validate",
		"validate": "ecs_vehicles.doctype_triggers.stock.item_group.item_group.validate",
		"before_save": "ecs_vehicles.doctype_triggers.stock.item_group.item_group.before_save",
		"on_update": "ecs_vehicles.doctype_triggers.stock.item_group.item_group.on_update",
	},
	"Item Price": {
		"before_insert": "ecs_vehicles.doctype_triggers.stock.item_price.item_price.before_insert",
		"after_insert": "ecs_vehicles.doctype_triggers.stock.item_price.item_price.after_insert",
		"onload": "ecs_vehicles.doctype_triggers.stock.item_price.item_price.onload",
		"before_validate": "ecs_vehicles.doctype_triggers.stock.item_price.item_price.before_validate",
		"validate": "ecs_vehicles.doctype_triggers.stock.item_price.item_price.validate",
		"before_save": "ecs_vehicles.doctype_triggers.stock.item_price.item_price.before_save",
		"on_update": "ecs_vehicles.doctype_triggers.stock.item_price.item_price.on_update",
	},
	"Website Item": {
		"before_insert": "ecs_vehicles.doctype_triggers.stock.website_item.website_item.before_insert",
		"after_insert": "ecs_vehicles.doctype_triggers.stock.website_item.website_item.after_insert",
		"onload": "ecs_vehicles.doctype_triggers.stock.website_item.website_item.onload",
		"before_validate": "ecs_vehicles.doctype_triggers.stock.website_item.website_item.before_validate",
		"validate": "ecs_vehicles.doctype_triggers.stock.website_item.website_item.validate",
		"before_save": "ecs_vehicles.doctype_triggers.stock.website_item.website_item.before_save",
		"on_update": "ecs_vehicles.doctype_triggers.stock.website_item.website_item.on_update",
	},
}
doctype_js = {
	"Journal Entry" : "ecs_vehicles/doctype_triggers/accounting/journal_entry/journal_entry.js",
	"Payment Entry" : "ecs_vehicles/doctype_triggers/accounting/payment_entry/payment_entry.js",
	"Purchase Invoice" : "ecs_vehicles/doctype_triggers/accounting/purchase_invoice/purchase_invoice.js",
	"Sales Invoice" : "ecs_vehicles/doctype_triggers/accounting/sales_invoice/sales_invoice.js",
	"Material Request" : "ecs_vehicles/doctype_triggers/buying/material_request/material_request.js",
	"Purchase Oder" : "doctype_triggers/buying/purchase_order/purchase_order.js",
	"Request For Quotation" : "ecs_vehicles/doctype_triggers/buying/request_for_quotation/request_for_quotation.js",
	"Supplier" : "ecs_vehicles/doctype_triggers/buying/supplier/supplier.js",
	"Supplier Group" : "ecs_vehicles/doctype_triggers/buying/supplier_group/supplier_group.js",
	"Supplier Quotation" : "ecs_vehicles/doctype_triggers/buying/supplier_quotation/supplier_quotation.js",
	"Address" : "ecs_vehicles/doctype_triggers/crm/address/address.js",
	"Contact" : "ecs_vehicles/doctype_triggers/crm/contact/contact.js",
	"Lead" : "ecs_vehicles/doctype_triggers/crm/lead/lead.js",
	"Oppurtunity" : "ecs_vehicles/doctype_triggers/crm/oppurtunity/oppurtunity.js",
	"Employee" : "ecs_vehicles/doctype_triggers/hr/employee/employee.js",
	"Employee Checkin" : "ecs_vehicles/doctype_triggers/hr/employee_checkin/employee_checkin.js",
	"Salary Component" : "ecs_vehicles/doctype_triggers/hr/salary_component/salary_component.js",
	"Additional Salary" : "ecs_vehicles/doctype_triggers/hr/additional_salary/additional_salary.js",
	"Attendance" : "ecs_vehicles/doctype_triggers/hr/attendance/attendance.js",
	"Attendance Request" : "ecs_vehicles/doctype_triggers/hr/attendance_request/attendance_request.js",
	"Employee Advance" : "ecs_vehicles/doctype_triggers/hr/employee_advance/employee_advance.js",
	"Expense Claim" : "ecs_vehicles/doctype_triggers/hr/expense_claim/expense_claim.js",
	"Leave Application" : "ecs_vehicles/doctype_triggers/hr/leave_application/leave_application.js",
	"Loan" : "ecs_vehicles/doctype_triggers/hr/loan/loan.js",
	"Loan Application" : "ecs_vehicles/doctype_triggers/hr/loan_application/loan_application.js",
	"Loan Disbursement" : "ecs_vehicles/doctype_triggers/hr/loan_disbursement/loan_disbursement.js",
	"Loan Repayment" : "ecs_vehicles/doctype_triggers/hr/loan_repayment/loan_repayment.js",
	"Loan Type" : "ecs_vehicles/doctype_triggers/hr/loan_type/loan_type.js",
	"Payroll Entry" : "ecs_vehicles/doctype_triggers/hr/payroll_entry/payroll_entry.js",
	"Salary Slip" : "ecs_vehicles/doctype_triggers/hr/salary_slip/salary_slip.js",
	"Salary Structure" : "ecs_vehicles/doctype_triggers/hr/salary_structure/salary_structure.js",
	"BOM" : "ecs_vehicles/doctype_triggers/manufacturing/bom/bom.js",
	"Job Card" : "ecs_vehicles/doctype_triggers/manufacturing/job_card/job_card.js",
	"Work Order" : "ecs_vehicles/doctype_triggers/manufacturing/work_order/work_order.js",
	"Project" : "ecs_vehicles/doctype_triggers/projects/project/project.js",
	"Task" : "ecs_vehicles/doctype_triggers/projects/task/task.js",
	"Timesheet" : "ecs_vehicles/doctype_triggers/projects/timesheet/timesheet.js",
	"Customer" : "ecs_vehicles/doctype_triggers/selling/customer/customer.js",
	"Customer Group" : "ecs_vehicles/doctype_triggers/selling/customer_group/customer_group.js",
	"Pricing Rule" : "ecs_vehicles/doctype_triggers/selling/pricing_rule/pricing_rule.js",
	"Sales Partner" : "ecs_vehicles/doctype_triggers/selling/sales_partner/sales_partner.js",
	"Sales Person" : "ecs_vehicles/doctype_triggers/selling/sales_person/sales_person.js",
	"Quotation" : "ecs_vehicles/doctype_triggers/selling/quotation/quotation.js",
	"Sales Order" : "ecs_vehicles/doctype_triggers/selling/sales_order/sales_order.js",
	"Delivery Note" : "ecs_vehicles/doctype_triggers/stock/delivery_note/delivery_note.js",
	"Purchase Receipt" : "ecs_vehicles/doctype_triggers/stock/purchase_receipt/purchase_receipt.js",
	"Stock Entry" : "ecs_vehicles/doctype_triggers/stock/stock_entry/stock_entry.js",
	"Stock Reconciliation" : "ecs_vehicles/doctype_triggers/stock/stock_reconciliation/stock_reconciliation.js",
	"Item" : "ecs_vehicles/doctype_triggers/stock/item/item.js",
	"Item Group" : "ecs_vehicles/doctype_triggers/stock/item_group/item_group.js",
	"Item Price" : "ecs_vehicles/doctype_triggers/stock/item_price/item_price.js",
	"Website Item" : "ecs_vehicles/doctype_triggers/stock/website_item/website_item.js",
}








scheduler_events = {
	 "all": [
 		"ecs_vehicles.scheduler_events.all.all"
	 ],
	 "daily": [
 		"ecs_vehicles.scheduler_events.daily.daily"
	 ],
 	"hourly": [
 		"ecs_vehicles.scheduler_events.hourly.hourly"
 	],
 	"weekly": [
 		"ecs_vehicles.scheduler_events.weekly.weekly"
 	],
 	"monthly": [
 		"ecs_vehicles.scheduler_events.monthly.monthly"
 	],
	"cron": {
        "*/30 * * * *": [
            "ecs_vehicles.scheduler_events.cron.cron"
        ]
    },
}


app_include_css = "/assets/ecs_vehicles/css/ecs_vehicles.css"
app_include_js = "/assets/ecs_vehicles/js/ecs_vehicles.js"
web_include_js = "/assets/js/web_ecs.min.js"
web_include_css = "/assets/js/web_ecs.min.css"
#app_css_right = "assets/ecs_vehicles/css/erpnext-rtl.css"

website_context = {
	"favicon": '/vec.emdad.local/public/files/markabat logoce3b5ed30c07d7831d.png',
	"splash_image": '/vec.emdad.local/public/files/markabat logoce3b5ed30c07d7831d.png',
}
# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/ecs_vehicles/css/ecs_vehicles.css"
# app_include_js = "/assets/ecs_vehicles/js/ecs_vehicles.js"

# include js, css files in header of web template
# web_include_css = "/assets/ecs_vehicles/css/ecs_vehicles.css"
# web_include_js = "/assets/ecs_vehicles/js/ecs_vehicles.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "ecs_vehicles/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "ecs_vehicles.install.before_install"
# after_install = "ecs_vehicles.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "ecs_vehicles.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"ecs_vehicles.tasks.all"
# 	],
# 	"daily": [
# 		"ecs_vehicles.tasks.daily"
# 	],
# 	"hourly": [
# 		"ecs_vehicles.tasks.hourly"
# 	],
# 	"weekly": [
# 		"ecs_vehicles.tasks.weekly"
# 	]
# 	"monthly": [
# 		"ecs_vehicles.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "ecs_vehicles.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "ecs_vehicles.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "ecs_vehicles.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


# User Data Protection
# --------------------

user_data_fields = [
	{
		"doctype": "{doctype_1}",
		"filter_by": "{filter_by}",
		"redact_fields": ["{field_1}", "{field_2}"],
		"partial": 1,
	},
	{
		"doctype": "{doctype_2}",
		"filter_by": "{filter_by}",
		"partial": 1,
	},
	{
		"doctype": "{doctype_3}",
		"strict": False,
	},
	{
		"doctype": "{doctype_4}"
	}
]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"ecs_vehicles.auth.validate"
# ]
fixtures = ["Print Format", "Custom Field", "Translation", "Workspace"]
