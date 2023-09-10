// Copyright (c) 2023, erpcloud.systems and contributors
// For license information, please see license.txt
frappe.ui.form.on('Add To Karta', {
	refresh: (frm) => {
		frm.set_query("item_code", "items", () => {
			return {
				filters: [
					["Item", "is_stock_item", "=", 1],
					["Item", "item_category", "=", "صيانة"],
				],
			};
		});
	},
});

frappe.ui.form.on('Add To Karta', {
	onload_post_render: function (frm) {
		frm.get_field("items").grid.set_multiple_add("item_code");
	},
	setup: function (frm) {
		frm.set_query("vehicles", function () {
			return {
				filters: [
					["Vehicles", "vehicle_status", "in", ["عاطلة", "صالحة"]]
				]
			};
		});
	}
});

frappe.ui.form.on("Add To Karta", "karta", function (frm) {
	var myWin = window.open('/app/query-report/Car%20Card?vic_serial=' + cur_frm.doc.vehicles);
});