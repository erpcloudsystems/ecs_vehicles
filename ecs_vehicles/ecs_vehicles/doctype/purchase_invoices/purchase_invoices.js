// Copyright (c) 2022, erpcloud.systems and contributors
// For license information, please see license.txt

frappe.ui.form.on('Purchase Invoices', {
	// refresh: function(frm) {

	// }
});
frappe.ui.form.on("Purchase Invoices", {
	maintenance_order: function(frm) {
			   frappe.call({
				   doc: frm.doc,
				   method: "get_data",
				   callback: function(r) {
					   frm.refresh_fields();
					   frm.refresh();
					   frm.save();
					   
				   }
			   });
	   }
   });
   