// Copyright (c) 2022, erpcloud.systems and contributors
// For license information, please see license.txt

frappe.ui.form.on('Job Order', {
	// refresh: function(frm) {

	// }
});
frappe.ui.form.on("Job Order", {
	create_invoice: function(frm) {
			   frappe.call({
				   doc: frm.doc,
				   method: "create_invoice",
				   callback: function(r) {
					   frm.refresh_fields();
					   frm.refresh();
				   }
			   });
	   }
   });
   