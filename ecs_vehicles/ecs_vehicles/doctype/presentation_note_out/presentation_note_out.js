// Copyright (c) 2023, erpcloud.systems and contributors
// For license information, please see license.txt

frappe.ui.form.on('Presentation Note Out', {
	// refresh: function(frm) {

	// }
});
frappe.ui.form.on('Presentation Note Out', {
	create_job_order: function(frm) {
				frappe.call({
					doc: frm.doc,
					method: "create_job_order",
					callback: function(r) {
						frm.refresh_fields();
						frm.refresh();
					}
				});
		}
	});