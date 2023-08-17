// Copyright (c) 2022, erpcloud.systems and contributors
// For license information, please see license.txt

frappe.ui.form.on("Maintenance Order", "onload", function(frm) {
	frappe.call({
		doc: frm.doc,
		method: "set_today_date",
		callback: function(r) {
			frm.refresh_field("date");
		}
	});
});


frappe.ui.form.on("Maintenance Order Item", "maintenance_method", function(frm, cdt, cdn) {
	let item = locals[cdt][cdn];
	if (item.maintenance_method == "إصلاح خارجي"){
		frappe.call({
			method: "ecs_vehicles.ecs_vehicles.doctype.maintenance_order.maintenance_order.pass_order_function",
			args: {
				"vehicles": frm.doc.vehicles,
				"fis_year": frm.doc.fis_year,
				"pass_order": frm.doc.pass_order,
			},
			callback: function(r) {
				frm.refresh_fields();
				frm.refresh();
			}
		});
	}
});

frappe.ui.form.on("Maintenance Order", "select_all_maintenance_type", function(frm) {
	let maintenance_order_items = []
	frm.doc.maintenance_order_item.forEach(element => {
		!element.maintenance_type ? element.maintenance_type = frm.doc.select_all_maintenance_type : element.maintenance_type = element.maintenance_type
		maintenance_order_items.push(element)
	});
	frm.doc.maintenance_order_item = maintenance_order_items
	frm.refresh_fields();
	frm.refresh();
	
});

frappe.ui.form.on("Maintenance Order", "select_all_maintenance_method", function(frm) {
	let maintenance_order_items = []
	frm.doc.maintenance_order_item.forEach(element => {
		!element.maintenance_method ? element.maintenance_method = frm.doc.select_all_maintenance_method : element.maintenance_method = element.maintenance_method
		maintenance_order_items.push(element)
	});
	frm.doc.maintenance_order_item = maintenance_order_items
	frm.refresh_fields();
	frm.refresh();
	
});