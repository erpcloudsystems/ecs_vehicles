// Copyright (c) 2022, erpcloud.systems and contributors
// For license information, please see license.txt


frappe.ui.form.on("Purchase Invoices", {
	onload: function (frm) {
		if (frm.doc.order_no) {
			frappe.call({
				doc: frm.doc,
				method: "get_job_order_stat",
				callback: function (r) {
					frm.refresh_fields("vehicle_maintenance_status");


				}
			});
		}
		frm.set_query("item_code", "purchase_invoices_table", () => {
			return {
				filters: [
					["Item", "is_stock_item", "=", 1],
					["Item", "item_category", "=", "صيانة"],
				],
			};
		});




	},
	maintenance_order: function (frm) {
		frappe.call({
			doc: frm.doc,
			method: "get_data",
			callback: function (r) {
				frm.refresh_fields();
				frm.refresh();
				frm.save();

			}
		});
	}
});

frappe.ui.form.on("Purchase Invoices", "setup", function (frm) {
	frm.set_value("check_date", frm.doc.date);
});

frappe.ui.form.on("Purchase Invoices", "date", function (frm) {
	frm.set_value("check_date", frm.doc.date);
});


frappe.ui.form.on("Purchase Invoices", "print_format1", function (frm) {
	var myWin = window.open('/printview?doctype=Purchase%20Invoices&name=' + cur_frm.doc.name + '&trigger_print=1&format=محضر%20فحص%20اصلاح%20مركبه&no_letterhead=1&letterhead=No%20Letterhead&settings=%7B%7D&_lang=ar');
});

frappe.ui.form.on("Purchase Invoices", "print_format2", function (frm) {

	if (!frm.doc.tawreed_no){
		var myWin = window.open('/printview?doctype=Purchase%20Invoices&name=' + cur_frm.doc.name + '&trigger_print=1&format=%D8%A5%D8%B0%D9%86%20%D8%B5%D8%B1%D9%81&no_letterhead=1&letterhead=No%20Letterhead&settings=%7B%7D&_lang=ar');
	} else {

	var myWin = window.open('/printview?doctype=Purchase%20Invoices&name=' + cur_frm.doc.name + '&trigger_print=1&format=Tawreed%20Order&no_letterhead=1&letterhead=No%20Letterhead&settings=%7B%7D&_lang=ar');
	}
});

frappe.ui.form.on("Purchase Invoices", "print_format3", function (frm) {
	var myWin = window.open('/printview?doctype=Purchase%20Invoices&name=' + cur_frm.doc.name + '&trigger_print=1&format=%D8%A5%D8%B0%D9%86%20%D8%A5%D8%B1%D8%AA%D8%AC%D8%A7%D8%B9&no_letterhead=1&letterhead=No%20Letterhead&settings=%7B%7D&_lang=ar');
});

