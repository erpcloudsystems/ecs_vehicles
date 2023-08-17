frappe.ui.form.on('Custody Report', {
	onload_post_render: function(frm) {
		frm.get_field("custody_report_item").grid.set_multiple_add("item_code");
	},
});

frappe.ui.form.on('Custody Report', {
    setup: function(frm) {
        frm.set_query("vehicles", function() {
			return {
				filters: [
					["Vehicles","vehicle_status", "in", ["عاطلة", "صالحة"]]
				]
			};
        });
    }
});

frappe.ui.form.on('Custody Report', {
 bundle: function(frm) {
			frappe.call({
				doc: frm.doc,
				method: "update_table",
				callback: function(r) {
					frm.refresh_fields();
					frm.refresh();
				}
			});
	}
});

frappe.ui.form.on('Custody Report', {
	select_type: function(frm) {
			// frm.doc.custody_report_item = []
			frm.refresh_fields();
			frm.refresh();
			  
	   }
   });

frappe.ui.form.on('Custody Report', {
	group_type: function(frm) {
			// frm.doc.custody_report_item = []
			if (frm.doc.select_type == "مجموعات فرعية" && frm.doc.group_type == "اطارات خارجية"){
				frappe.call({
					doc: frm.doc,
					method: "wheels_update_table",
					freeze:1,
					callback: function(r) {
						frm.refresh_fields();
						frm.refresh();
					}
				});
			}
			if (frm.doc.select_type === "مجموعات فرعية" && frm.doc.group_type === "البطاريات"){
				frappe.call({
					doc: frm.doc,
					method: "battaries_update_table",
					freeze:1,
					callback: function(r) {
						frm.refresh_fields();

						frm.refresh();
					}
				});
			}
			

			  
	   }
   });
frappe.ui.form.on('Custody Report', {
 add_maintenance_order: function(frm) {
    
			frappe.call({
				doc: frm.doc,
				method: "add_maintenance_order",
				freeze:1,
				callback: function(r) {
					frm.refresh_fields();
					frm.refresh();
				}
			});
	}
});



// frappe.ui.form.on("Custody Report Item", "item_code", function(frm, cdt, cdn) {
// 	let item = locals[cdt][cdn];
// 	if (item.item_code ){
// 		frappe.call({
// 			method: "ecs_vehicles.ecs_vehicles.doctype.custody_report.custody_report.get_last_sarf_detail",
// 			args: {
// 				"vehicles": frm.doc.vehicles,
// 				"item_code": item.item_code,
// 			},
// 			callback: function(r) {
// 				if (r.message == "لم يسبق") {
// 					item.last_issue_detail = "لم يسبق"
// 					item.last_sarf_qty = 0

// 				}else {
// 					item.last_issue_detail = r.message[0]
// 					item.last_sarf_qty = r.message[1]
// 				}

// 				frm.refresh_fields();
// 				frm.refresh();
// 			}
// 		});
// 	}
// });


frappe.ui.form.on("Custody Report", "select_all_maintenance_order", function(frm) {
	let maintenance_order_items = []
	var maintenance_order = 0
	if (frm.doc.select_all_maintenance_order == "إنشاء إجراء إصلاح للكل"){
		maintenance_order = 1
	};
	if (frm.doc.select_all_maintenance_order == "إلغاء إجراء إصلاح للكل"){
		maintenance_order = 0
	};
	frm.doc.custody_report_item.forEach(element => {
		element.include_in_maintenance_order = maintenance_order
		maintenance_order_items.push(element)
	});
	frm.doc.custody_report_item = maintenance_order_items
	frm.doc.select_all_maintenance_order = ""
	frm.refresh_fields();
	frm.refresh();
});
