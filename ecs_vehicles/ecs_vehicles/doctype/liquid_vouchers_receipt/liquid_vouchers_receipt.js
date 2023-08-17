// Copyright (c) 2022, erpcloud.systems and contributors
// For license information, please see license.txt

frappe.ui.form.on("Liquid Vouchers Receipt", "onload", function(frm) {
	frappe.call({
		doc: frm.doc,
		method: "set_today_date",
		callback: function(r) {
			frm.refresh_field("receipt_date");
		}
	});
});