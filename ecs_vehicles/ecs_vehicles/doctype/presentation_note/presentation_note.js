// Copyright (c) 2022, erpcloud.systems and contributors
// For license information, please see license.txt

frappe.ui.form.on('Presentation Note', {
	// refresh: function(frm) {

	// }
});
frappe.ui.form.on('Presentation Note', {
	request_for_quotations: function(frm) {
			   frappe.call({
				   doc: frm.doc,
				   method: "get_data",
				   callback: function(r) {
					   frm.save();
					   frm.refresh_fields();
					   frm.refresh();
				   }
			   });
	   }
   });
   


   frappe.ui.form.on('Presentation Note', {
	add_po: function(frm) {
			   frappe.call({
				   doc: frm.doc,
				   method: "add_po",
				   callback: function(r) {
					   frm.save();
					   frm.refresh_fields();
					   frm.refresh();
				   }
			   });
	   }
   });
   