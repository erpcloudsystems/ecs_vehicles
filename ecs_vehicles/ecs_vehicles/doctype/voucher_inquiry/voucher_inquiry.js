// Copyright (c) 2023, erpcloud.systems and contributors
// For license information, please see license.txt

frappe.ui.form.on("Voucher Inquiry", 'refresh', function(frm){
	frm.disable_save();
});

frappe.ui.form.on("Voucher Inquiry", 'clear_voucher', function(frm){
	cur_frm.doc.barcode = "";
	cur_frm.refresh_fields();
});

frappe.ui.form.on("Voucher Inquiry", "barcode", function(frm) {
    frappe.call({ method: "frappe.client.get_value", args: {
        doctype: "Voucher",
        fieldname: ["barcode_no","voucher_type","release_date","issue_date","entity","review_date","username","company_name",
			"fiscal_year","batch_no","group_no","police_no","entity_name","private_no","motor_no","chassis_no",
			"vehicle_fuel_type","vehicle_shape","vehicle_brand","vehicle_style","vehicle_model","vehicle_color","processing_type"],
        filters: { 'barcode_no': cur_frm.doc.barcode, }},
        callback: function(r) {
			cur_frm.doc.voucher_type = r.message.voucher_type;
			cur_frm.doc.release_date = r.message.release_date;
			cur_frm.doc.issue_date = r.message.issue_date;
			cur_frm.doc.entity = r.message.entity;
			cur_frm.doc.review_date = r.message.review_date;
			cur_frm.doc.username = r.message.username;
			cur_frm.doc.company_name = r.message.company_name;
			cur_frm.doc.fiscal_year = r.message.fiscal_year;
			cur_frm.doc.batch_no = r.message.batch_no;
			cur_frm.doc.group_no = r.message.group_no;
			cur_frm.doc.police_no = r.message.police_no;
			cur_frm.doc.entity_name = r.message.entity_name;
			cur_frm.doc.private_no = r.message.private_no;
			cur_frm.doc.motor_no = r.message.motor_no;
			cur_frm.doc.chassis_no = r.message.chassis_no;
			cur_frm.doc.vehicle_fuel_type = r.message.vehicle_fuel_type;
			cur_frm.doc.vehicle_shape = r.message.vehicle_shape;
			cur_frm.doc.vehicle_brand = r.message.vehicle_brand;
			cur_frm.doc.vehicle_style = r.message.vehicle_style;
			cur_frm.doc.vehicle_model = r.message.vehicle_model;
			cur_frm.doc.vehicle_color = r.message.vehicle_color;
			cur_frm.doc.processing_type = r.message.processing_type;
			cur_frm.refresh_fields();
		}
	});
});