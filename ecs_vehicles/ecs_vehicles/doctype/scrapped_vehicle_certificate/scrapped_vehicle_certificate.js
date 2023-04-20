// Copyright (c) 2023, erpcloud.systems and contributors
// For license information, please see license.txt

frappe.ui.form.on('Scrapped Vehicle Certificate', {
	onload: function(frm) {
		frm.set_query("vehicle", function() {
			return {
				filters: {
					"vehicle_status": "مخردة"
				}
			}
		});
		cur_frm.refresh_field('option');
	}
});
