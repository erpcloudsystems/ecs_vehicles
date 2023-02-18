// Copyright (c) 2022, erpcloud.systems and contributors
// For license information, please see license.txt

frappe.ui.form.on('Maintenance Request for Quotations', {
	// refresh: function(frm) {

	// }
});
frappe.ui.form.on('Maintenance Request for Quotations', {
	maintenance_order: function(frm) {
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

frappe.ui.form.on('Maintenance Request for Quotations', {
	create_presentation_note_out: function(frm) {
				frappe.call({
					doc: frm.doc,
					method: "create_Presentation",
					callback: function(r) {
						frm.refresh_fields();
						frm.refresh();
					}
				});
		}
	});
	
//    frappe.ui.form.on("Maintenance Request for Quotations", "refresh", function(frm){
// 	if (cur_frm.doc.docstatus == 1) {
// 	  frm.add_custom_button("انشاء مذكرة عرض", function(){
// 		  frappe.call({
// 		method: "ecs_vehicles.ecs_vehicles.doctype.maintenance_request_for_quotations.maintenance_request_for_quotations.create_Presentation_note_out",
// 		args: {
// 				  'name': frm.doc.name
// 		},
// 		callback: function(r) {
// 			}
// 	  });
// 	});
// 	}
// 	});

