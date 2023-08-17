// Copyright (c) 2022, erpcloud.systems and contributors
// For license information, please see license.txt
frappe.ui.form.on("Presentation Note", "print_mozakira_purchase", function (frm) {
	var myWin = window.open('/printview?doctype=Presentation%20Note&name=' + cur_frm.doc.name + '&trigger_print=1&format=Direct%20Order%20Purchase%20Note&no_letterhead=1&letterhead=No%20Letterhead&settings=%7B%7D&_lang=ar');
});

frappe.ui.form.on('Presentation Note', {
	refresh: (frm) => {
		frm.set_query("item_code", "presentation_note_item", () => {
			return {
				filters: [
					["Item", "is_stock_item", "=", 1],
					["Item", "item_category", "=", "صيانة"],
				],
			};
		});
	},
});
frappe.ui.form.on('Presentation Note', {
	setup: function (frm) {
		frm.set_query("request_for_quotations", function () {
			return {
				filters: [
					["Vehicle Maintenance Process", "fiscal_year", "=", frm.doc.fiscal_year]
				]
			};
		});
	},
	fiscal_year: function (frm) {
		frm.set_query("request_for_quotations", function () {
			return {
				filters: [
					["Vehicle Maintenance Process", "fiscal_year", "=", frm.doc.fiscal_year]
				]
			};
		});
	},
	request_for_quotations: function (frm) {
		frappe.call({
			doc: frm.doc,
			method: "get_data",
			callback: function (r) {
				frm.doc.request_for_quotations = ""
				frm.refresh_fields();
				frm.refresh();
			}
		});
	},
	create_purchase_import_order: function (frm) {
		frappe.call({
			doc: frm.doc,
			method: "create_purchase_import_order",
			callback: function (r) {

			}
		});
	}
});

frappe.ui.form.on("Presentation Note Item", "qty", function (frm, cdt, cdn) {
	let item = locals[cdt][cdn];
	item.amount = item.qty * item.rate
	let total_amount = 0
	frm.doc.presentation_note_item.forEach((element, idx, array) => {
		total_amount += (element.qty * element.rate)
	})
	frm.doc.total = total_amount
	frm.refresh()

});

frappe.ui.form.on("Presentation Note Item", "rate", function (frm, cdt, cdn) {
	let item = locals[cdt][cdn];
	item.amount = item.qty * item.rate
	let total_amount = 0
	frm.doc.presentation_note_item.forEach((element, idx, array) => {
		total_amount += (element.qty * element.rate)
	})
	frm.doc.total = total_amount
	frm.refresh()

});

frappe.ui.form.on('Presentation Note', {
	add_po: function (frm) {
		frappe.call({
			method: "ecs_vehicles.ecs_vehicles.doctype.presentation_note.presentation_note.add_po_f",
			args: {
				"name": frm.doc.name,
				"supplier": frm.doc.supplier,
				"request_for_quotations": frm.doc.request_for_quotations,
			},
			callback: function (r) {
				frm.save();
				frm.refresh_fields();
				frm.refresh();
			}
		});
	}
});
