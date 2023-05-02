frappe.ui.form.on('Custody Report', {
	refresh(frm) {
		// your code here
	}
})
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
			frm.doc.custody_report_item = []
			if (frm.doc.select_type == "مجموعات فرعية" && frm.doc.group_type == "اطارات خارجية"){
				frappe.call({
					doc: frm.doc,
					method: "wheels_update_table",
					freeze:1,
					callback: function(r) {
						console.log("return");
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
						console.log("return")

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
				callback: function(r) {
					frm.refresh_fields();
					frm.refresh();
				}
			});
	}
});
