// Copyright (c) 2022, erpcloud.systems and contributors
// For license information, please see license.txt

frappe.ui.form.on('Buying Order', {
	// refresh: function(frm) {

	// }
});
frappe.ui.form.on('Buying Order', {
	add_purchase_order: function(frm) {
			   frappe.call({
				   doc: frm.doc,
				   method: "add_purchase_order",
				   callback: function(r) {
					   frm.refresh_fields();
					   frm.refresh();
				   }
			   });
	   }
   });

   frappe.ui.form.on('Buying Order', {
	add_financial_approval: function(frm) {
			   frappe.call({
				   doc: frm.doc,
				   method: "add_financial_approval",
				   callback: function(r) {
					   frm.refresh_fields();
					   frm.refresh();
				   }
			   });
	   }
   });

   frappe.ui.form.on('Buying Order', {
	add_presentation_note: function(frm) {
			   frappe.call({
				   doc: frm.doc,
				   method: "add_presentation_note",
				   callback: function(r) {
					   frm.refresh_fields();
					   frm.refresh();
				   }
			   });
	   }
   });

   frappe.ui.form.on('Buying Order', {
	add_technical_clearance: function(frm) {
			   frappe.call({
				   doc: frm.doc,
				   method: "add_technical_clearance",
				   callback: function(r) {
					   frm.refresh_fields();
					   frm.refresh();
				   }
			   });
	   }
   });

   frappe.ui.form.on('Buying Order', {
	add_financial_clearance: function(frm) {
			   frappe.call({
				   doc: frm.doc,
				   method: "add_financial_clearance",
				   callback: function(r) {
					   frm.refresh_fields();
					   frm.refresh();
				   }
			   });
	   }
   });

   frappe.ui.form.on('Buying Order', "refresh", function(){
	document.querySelectorAll("[data-fieldname='add_purchase_order']")[1].style.color = "red";
	});
	