frappe.ui.form.on('Vehicle Maintenance Process', {
	cancel_ezn: function (frm) {
		if (frm.doc.cancel_ezn == 1) {
			frm.scroll_to_field('cancellation_reason');
			frm.set_df_property("edit_ezn", "read_only", true);
			frm.set_df_property("renew_ezn", "read_only", true);
			frm.set_df_property("ezn_no", "read_only", true);
			frm.set_df_property("vehicles", "read_only", true);
			frm.set_df_property("fiscal_year", "read_only", true);
			frm.set_df_property("ezn_date", "read_only", true);
			frm.set_df_property("car_in_date", "read_only", true);
			frm.set_df_property("car_out_date", "read_only", true);
			frm.set_df_property("driver", "read_only", true);
			frm.set_df_property("notes", "read_only", true);
			frm.set_df_property("select_type", "hidden", true);
			frm.set_df_property("group_type", "hidden", true);
			frm.set_df_property("bundle", "hidden", true);
			frm.set_df_property("select_all_maintenance_method", "hidden", true);
			frm.set_df_property("select_all_maintenance_type", "hidden", true);
			frm.set_df_property("select_all_disc_percent", "hidden", true);
			frm.set_df_property("select_all_maintenance_order", "hidden", true);
			frm.set_df_property("kashf_ohda_item", "read_only", true);
			frm.set_df_property("pass_order", "read_only", true);
			frm.set_df_property("talb_date", "read_only", true);
			frm.set_df_property("fix_type", "read_only", true);
			frm.set_df_property("fix_description", "read_only", true);
			frm.set_df_property("accepted_supplier", "read_only", true);
			frm.set_df_property("talb_total_amount", "read_only", true);
			frm.set_df_property("talab_total_in_words", "read_only", true);
			frm.set_df_property("talb_oroud_asaar_item", "read_only", true);
			frm.set_df_property("edit_in_words", "hidden", true);
			frm.set_df_property("supplier_table", "read_only", true);
			frm.set_df_property("mozakira_date", "read_only", true);
			frm.set_df_property("mozakira_no", "read_only", true);
			frm.set_df_property("contract_date", "read_only", true);
			frm.set_df_property("contract_term", "read_only", true);
			frm.set_df_property("supplier", "read_only", true);
			frm.set_df_property("fix_period", "read_only", true);
			frm.set_df_property("pay_method", "read_only", true);
			frm.set_df_property("check_byname", "read_only", true);
			frm.set_df_property("mozakira_item", "read_only", true);
			frm.set_df_property("mozakira_total_amount", "read_only", true);
			frm.set_df_property("total_in_words", "read_only", true);
			frm.set_df_property("edit_in_words2", "hidden", true);
			frm.set_df_property("job_order_date", "read_only", true);
			frm.set_df_property("job_order_no", "read_only", true);
			frm.set_df_property("work_end_date", "read_only", true);
			frm.set_df_property("fix_perod", "read_only", true);
			frm.set_df_property("veh_rec_date", "read_only", true);
			frm.set_df_property("rec_name", "read_only", true);
			frm.set_df_property("supplier2", "read_only", true);
			frm.set_df_property("aamr_shoghl_status", "read_only", true);
			frm.set_df_property("vehicle_maintenance_process", "read_only", true);
			frm.set_df_property("aamr_shoghl_item", "read_only", true);
			frm.set_df_property("aamr_shoghl_total_amount", "read_only", true);
			frm.set_df_property("aamr_shoghl_total_in_words", "read_only", true);
			frm.set_df_property("edit_in_words3", "hidden", true);
			frm.set_df_property("purchase_invoices", "read_only", true);
			frm.set_df_property("invoice_no", "read_only", true);
			frm.set_df_property("add_maintenance_invoice", "hidden", true);
			frm.set_df_property("add_job_order", "hidden", true);
			frm.set_df_property("add_presentation_note_out", "hidden", true);
			frm.set_df_property("add_maintenance_rfq", "hidden", true);
			frm.refresh_fields();
		}
		if (frm.doc.cancel_ezn == 0) {
			frm.set_df_property("edit_ezn", "read_only", false);
			frm.set_df_property("renew_ezn", "read_only", false);
			frm.set_df_property("ezn_no", "read_only", false);
			frm.set_df_property("vehicles", "read_only", false);
			frm.set_df_property("fiscal_year", "read_only", false);
			frm.set_df_property("ezn_date", "read_only", false);
			frm.set_df_property("car_in_date", "read_only", false);
			frm.set_df_property("car_out_date", "read_only", false);
			frm.set_df_property("driver", "read_only", false);
			frm.set_df_property("notes", "read_only", false);
			frm.set_df_property("select_type", "hidden", false);
			frm.set_df_property("group_type", "hidden", false);
			frm.set_df_property("bundle", "hidden", false);
			frm.set_df_property("select_all_maintenance_method", "hidden", false);
			frm.set_df_property("select_all_maintenance_type", "hidden", false);
			frm.set_df_property("select_all_disc_percent", "hidden", false);
			frm.set_df_property("select_all_maintenance_order", "hidden", false);
			frm.set_df_property("kashf_ohda_item", "read_only", false);
			frm.set_df_property("pass_order", "read_only", false);
			frm.set_df_property("talb_date", "read_only", false);
			frm.set_df_property("fix_type", "read_only", false);
			frm.set_df_property("fix_description", "read_only", false);
			frm.set_df_property("accepted_supplier", "read_only", false);
			frm.set_df_property("talb_total_amount", "read_only", false);
			frm.set_df_property("talab_total_in_words", "read_only", false);
			frm.set_df_property("talb_oroud_asaar_item", "read_only", false);
			frm.set_df_property("edit_in_words", "hidden", false);
			frm.set_df_property("supplier_table", "read_only", false);
			frm.set_df_property("mozakira_date", "read_only", false);
			frm.set_df_property("mozakira_no", "read_only", false);
			frm.set_df_property("contract_date", "read_only", false);
			frm.set_df_property("contract_term", "read_only", false);
			frm.set_df_property("supplier", "read_only", false);
			frm.set_df_property("fix_period", "read_only", false);
			frm.set_df_property("pay_method", "read_only", false);
			frm.set_df_property("check_byname", "read_only", false);
			frm.set_df_property("mozakira_item", "read_only", false);
			frm.set_df_property("mozakira_total_amount", "read_only", false);
			frm.set_df_property("total_in_words", "read_only", false);
			frm.set_df_property("edit_in_words2", "hidden", false);
			frm.set_df_property("job_order_date", "read_only", false);
			frm.set_df_property("job_order_no", "read_only", false);
			frm.set_df_property("work_end_date", "read_only", false);
			frm.set_df_property("fix_perod", "read_only", false);
			frm.set_df_property("veh_rec_date", "read_only", false);
			frm.set_df_property("rec_name", "read_only", false);
			frm.set_df_property("supplier2", "read_only", false);
			frm.set_df_property("aamr_shoghl_status", "read_only", false);
			frm.set_df_property("vehicle_maintenance_process", "read_only", false);
			frm.set_df_property("aamr_shoghl_item", "read_only", false);
			frm.set_df_property("aamr_shoghl_total_amount", "read_only", false);
			frm.set_df_property("aamr_shoghl_total_in_words", "read_only", false);
			frm.set_df_property("edit_in_words3", "hidden", false);
			frm.set_df_property("invoice_no", "read_only", false);
			frm.set_df_property("add_maintenance_invoice", "hidden", false);
			frm.set_df_property("add_job_order", "hidden", false);
			frm.set_df_property("add_presentation_note_out", "hidden", false);
			frm.set_df_property("add_maintenance_rfq", "hidden", false);
			frm.refresh_fields();
		}
	},
	onload: function (frm) {
		if (frm.doc.cancel_ezn == 1) {
			frm.set_df_property("edit_ezn", "read_only", true);
			frm.set_df_property("renew_ezn", "read_only", true);
			frm.set_df_property("ezn_no", "read_only", true);
			frm.set_df_property("vehicles", "read_only", true);
			frm.set_df_property("fiscal_year", "read_only", true);
			frm.set_df_property("ezn_date", "read_only", true);
			frm.set_df_property("car_in_date", "read_only", true);
			frm.set_df_property("car_out_date", "read_only", true);
			frm.set_df_property("driver", "read_only", true);
			frm.set_df_property("notes", "read_only", true);
			frm.set_df_property("select_type", "hidden", true);
			frm.set_df_property("group_type", "hidden", true);
			frm.set_df_property("bundle", "hidden", true);
			frm.set_df_property("select_all_maintenance_method", "hidden", true);
			frm.set_df_property("select_all_maintenance_type", "hidden", true);
			frm.set_df_property("select_all_disc_percent", "hidden", true);
			frm.set_df_property("select_all_maintenance_order", "hidden", true);
			frm.set_df_property("kashf_ohda_item", "read_only", true);
			frm.set_df_property("pass_order", "read_only", true);
			frm.set_df_property("talb_date", "read_only", true);
			frm.set_df_property("fix_type", "read_only", true);
			frm.set_df_property("fix_description", "read_only", true);
			frm.set_df_property("accepted_supplier", "read_only", true);
			frm.set_df_property("talb_total_amount", "read_only", true);
			frm.set_df_property("talab_total_in_words", "read_only", true);
			frm.set_df_property("talb_oroud_asaar_item", "read_only", true);
			frm.set_df_property("edit_in_words", "hidden", true);
			frm.set_df_property("supplier_table", "read_only", true);
			frm.set_df_property("mozakira_date", "read_only", true);
			frm.set_df_property("mozakira_no", "read_only", true);
			frm.set_df_property("contract_date", "read_only", true);
			frm.set_df_property("contract_term", "read_only", true);
			frm.set_df_property("supplier", "read_only", true);
			frm.set_df_property("fix_period", "read_only", true);
			frm.set_df_property("pay_method", "read_only", true);
			frm.set_df_property("check_byname", "read_only", true);
			frm.set_df_property("mozakira_item", "read_only", true);
			frm.set_df_property("mozakira_total_amount", "read_only", true);
			frm.set_df_property("total_in_words", "read_only", true);
			frm.set_df_property("edit_in_words2", "hidden", true);
			frm.set_df_property("job_order_date", "read_only", true);
			frm.set_df_property("job_order_no", "read_only", true);
			frm.set_df_property("work_end_date", "read_only", true);
			frm.set_df_property("fix_perod", "read_only", true);
			frm.set_df_property("veh_rec_date", "read_only", true);
			frm.set_df_property("rec_name", "read_only", true);
			frm.set_df_property("supplier2", "read_only", true);
			frm.set_df_property("aamr_shoghl_status", "read_only", true);
			frm.set_df_property("vehicle_maintenance_process", "read_only", true);
			frm.set_df_property("aamr_shoghl_item", "read_only", true);
			frm.set_df_property("aamr_shoghl_total_amount", "read_only", true);
			frm.set_df_property("aamr_shoghl_total_in_words", "read_only", true);
			frm.set_df_property("edit_in_words3", "hidden", true);
			frm.set_df_property("purchase_invoices", "read_only", true);
			frm.set_df_property("invoice_no", "read_only", true);
			frm.set_df_property("add_maintenance_invoice", "hidden", true);
			frm.set_df_property("add_job_order", "hidden", true);
			frm.set_df_property("add_presentation_note_out", "hidden", true);
			frm.set_df_property("add_maintenance_rfq", "hidden", true);
			frm.refresh_fields();
		}
		if (frm.doc.cancel_ezn == 0) {
			frm.set_df_property("edit_ezn", "read_only", false);
			frm.set_df_property("renew_ezn", "read_only", false);
			frm.set_df_property("ezn_no", "read_only", false);
			frm.set_df_property("vehicles", "read_only", false);
			frm.set_df_property("fiscal_year", "read_only", false);
			frm.set_df_property("ezn_date", "read_only", false);
			frm.set_df_property("car_in_date", "read_only", false);
			frm.set_df_property("car_out_date", "read_only", false);
			frm.set_df_property("driver", "read_only", false);
			frm.set_df_property("notes", "read_only", false);
			frm.set_df_property("select_type", "hidden", false);
			frm.set_df_property("group_type", "hidden", false);
			frm.set_df_property("bundle", "hidden", false);
			frm.set_df_property("select_all_maintenance_method", "hidden", false);
			frm.set_df_property("select_all_maintenance_type", "hidden", false);
			frm.set_df_property("select_all_disc_percent", "hidden", false);
			frm.set_df_property("select_all_maintenance_order", "hidden", false);
			frm.set_df_property("kashf_ohda_item", "read_only", false);
			frm.set_df_property("pass_order", "read_only", false);
			frm.set_df_property("talb_date", "read_only", false);
			frm.set_df_property("fix_type", "read_only", false);
			frm.set_df_property("fix_description", "read_only", false);
			frm.set_df_property("accepted_supplier", "read_only", false);
			frm.set_df_property("talb_total_amount", "read_only", false);
			frm.set_df_property("talab_total_in_words", "read_only", false);
			frm.set_df_property("talb_oroud_asaar_item", "read_only", false);
			frm.set_df_property("edit_in_words", "hidden", false);
			frm.set_df_property("supplier_table", "read_only", false);
			frm.set_df_property("mozakira_date", "read_only", false);
			frm.set_df_property("mozakira_no", "read_only", false);
			frm.set_df_property("contract_date", "read_only", false);
			frm.set_df_property("contract_term", "read_only", false);
			frm.set_df_property("supplier", "read_only", false);
			frm.set_df_property("fix_period", "read_only", false);
			frm.set_df_property("pay_method", "read_only", false);
			frm.set_df_property("check_byname", "read_only", false);
			frm.set_df_property("mozakira_item", "read_only", false);
			frm.set_df_property("mozakira_total_amount", "read_only", false);
			frm.set_df_property("total_in_words", "read_only", false);
			frm.set_df_property("edit_in_words2", "hidden", false);
			frm.set_df_property("job_order_date", "read_only", false);
			frm.set_df_property("job_order_no", "read_only", false);
			frm.set_df_property("work_end_date", "read_only", false);
			frm.set_df_property("fix_perod", "read_only", false);
			frm.set_df_property("veh_rec_date", "read_only", false);
			frm.set_df_property("rec_name", "read_only", false);
			frm.set_df_property("supplier2", "read_only", false);
			frm.set_df_property("aamr_shoghl_status", "read_only", false);
			frm.set_df_property("vehicle_maintenance_process", "read_only", false);
			frm.set_df_property("aamr_shoghl_item", "read_only", false);
			frm.set_df_property("aamr_shoghl_total_amount", "read_only", false);
			frm.set_df_property("aamr_shoghl_total_in_words", "read_only", false);
			frm.set_df_property("edit_in_words3", "hidden", false);
			// frm.set_df_property("invoice_no", "read_only", false);
			frm.set_df_property("add_maintenance_invoice", "hidden", false);
			frm.set_df_property("add_job_order", "hidden", false);
			frm.set_df_property("add_presentation_note_out", "hidden", false);
			frm.set_df_property("add_maintenance_rfq", "hidden", false);
			frm.refresh_fields();
		}
	},
})

frappe.ui.form.on('Vehicle Maintenance Process', {
	onload_post_render: function (frm) {
		frm.get_field("kashf_ohda_item").grid.set_multiple_add("item_code");
	},
	onload: function (frm) {
		let state = ""
		if (frm.doc.ezn_egraa_item.length > 0) {
			state = "إجراء إصلاح"
		}
		if (frm.doc.talb_oroud_asaar_item.length > 0) {
			state = "طلب عروض أسعار"
		}
		if (frm.doc.mozakira_item.length > 0) {
			state = "مذكرة عرض"
		}
		if (frm.doc.aamr_shoghl_item.length > 0) {
			state = "أمر شغل"
		}
		if (frm.doc.purchase_invoices) {
			state = "فاتورة صيانة"
		}
		if (frm.doc.cancel_ezn) {
			state = "ملغي"
		}
		frm.set_value("vehicle_maintenance_status", state);
		if (frm.doc.vehicle_maintenance_status === "فاتورة صيانة") {
			frm.set_df_property("renew_ezn", "hidden", true);
			frm.set_df_property("edit_ezn", "hidden", true);

			// frappe.throw(`${frm.doc.invoice_no} لا يمكن تجديد الإذن نظرا لوجود فاتورة صيانة برقم`)

		} else if (frm.doc.vehicle_maintenance_status === "أمر شغل") {
			frm.set_df_property("renew_ezn", "hidden", true);
			frm.set_df_property("edit_ezn", "hidden", true);

			// frappe.throw(`${frm.doc.job_order_no} لا يمكن تجديد الإذن نظرا لوجود أمر شغل برقم`)
		}
		frm.refresh_fields("vehicle_maintenance_status");
		// frm.scroll_to_field('vehicle_maintenance_status');


	},
	add_maintenance_invoice: function (frm) {
		frappe.call({
			doc: frm.doc,
			method: "add_maintenance_invoice",
			freeze: 1,
			callback: function (r) {
				// frm.scroll_to_field('inv_no');
				frm.refresh_fields();
				frm.refresh();
			}
		});
	},
	setup: function (frm) {
		frm.set_query("vehicles", function () {
			return {
				filters: [
					["Vehicles", "vehicle_status", "in", ["عاطلة", "صالحة"]],
				]
			};
		});
	},
	bundle: function (frm) {
		// frappe.msgprint("جاري تحميل مجموعات متوافقة" +  " " + frm.doc.bundle.toString())
		frappe.call({
			doc: frm.doc,
			method: "update_table",
			freeze: 1,
			callback: function (r) {
				frm.doc.bundle = ""
				frm.refresh_fields();
				frm.refresh();
			}
		});
	},
	add_maintenance_rfq: function (frm) {
		frappe.call({
			doc: frm.doc,
			method: "add_maintenance_rfq",
			freeze: 1,
			callback: function (r) {
				frm.scroll_to_field('accepted_supplier');

				frm.refresh_fields();
				frm.refresh();
			}
		});
	},
	add_presentation_note_out: function (frm) {
		frappe.call({
			doc: frm.doc,
			method: "add_presentation_note_out",
			freeze: 1,

			callback: function (r) {
				frm.scroll_to_field('mozakira_no');

				frm.refresh_fields();
				frm.refresh();
			}
		});
	},

	add_job_order: function (frm) {
		frappe.call({
			doc: frm.doc,
			method: "add_job_order",
			freeze: 1,
			callback: function (r) {
				frm.scroll_to_field('aamr_shoghl_total_amount');

				frm.refresh_fields();
				frm.refresh();
			}
		});
	},

	// create_purchase_order_request: function (frm) {
	// 	frappe.call({
	// 		doc: frm.doc,
	// 		method: "create_purchase_order_request",
	// 		freeze: 1,
	// 		callback: function (r) {
	// 			frm.scroll_to_field('mister');
	// 			frm.refresh_fields();
	// 			frm.refresh();
	// 		}
	// 	});
	// },



	group_type: function (frm) {
		// frm.doc.custody_report_item = []
		if (frm.doc.select_type == "مجموعات فرعية" && frm.doc.group_type == "اطارات داخلية و خارجية") {
			// frappe.msgprint("جاري تحميل مجموعات فرعية"  + " " + frm.doc.group_type.toString())

			frappe.call({
				doc: frm.doc,
				method: "wheels_update_table",
				freeze: 1,
				callback: function (r) {
					frm.refresh_fields();
					frm.refresh();
					console.log(last_sarf_date)
					// if (!r.length) {
					// 	frappe.msgprint({
					// 		title: ('تنبيه'),
					// 		indicator: 'red',
					// 		message: ('المركبة لم تصرف اطارات من قبل')
					// 	});
					// }
				}
			});
		}
		if (frm.doc.select_type === "مجموعات فرعية" && frm.doc.group_type === "البطاريات") {
			// frappe.msgprint("جاري تحميل مجموعات فرعية" + " " +  frm.doc.group_type.toString())

			frappe.call({
				doc: frm.doc,
				method: "battaries_update_table",
				freeze: 1,
				callback: function (r) {
					frm.refresh_fields();
					frm.refresh();
					// if (!r.length) {
					// 	frappe.msgprint({
					// 		title: ('تنبيه'),
					// 		indicator: 'red',
					// 		message: ('المركبة لم تصرف بطاريات من قبل')
					// 	});
					// }
				}
			});
		}
		frm.doc.select_type = ""



	},
	//    validate: function(frm) {
	// 	if (frm.doc.ezn_egraa_item === undefined) {

	// 		frm.doc.ezn_egraa_item = []
	// 	}
	// 	let names = add_maintenance_order_item(frm.doc.kashf_ohda_item, frm.doc, frm)
	// 	let toggel_include_maintenance_order = toggel_include_maintenance(frm.doc.kashf_ohda_item, frm.doc, frm)
	// 	let delete_row = delete_row_maintenance_order_item(frm.doc.ezn_egraa_item, frm.doc, frm)
	// 	// let update_table = update_row_maintenance_order_item(frm.doc.ezn_egraa_item, frm.doc, frm)
	//    },
});

frappe.ui.form.on("Vehicle Maintenance Process", {
	refresh: (frm) => {
		frm.set_query("scrapped_vehicle", "kashf_ohda_item", () => {
			return {
				filters: [
					["Vehicles", "vehicle_status", "=", "مخردة"]
				],
			};
		});
	},
});


frappe.ui.form.on('Vehicle Maintenance Process', 'renew_ezn', function (frm, cdt, cdn) {
	if (cur_frm.doc.renew_ezn == 1) {
		frm.set_value("old_ezn_no", frm.doc.ezn_no);
		frm.set_value("old_ezn_date", frm.doc.ezn_date);
		frm.set_value("old_fiscal_year", frm.doc.fiscal_year);
		frm.set_value("ezn_no", "");
		frappe.call({
			"method": "frappe.client.get_value",
			"args": {
				"doctype": "Global Defaults",
				"fieldname": "current_fiscal_year",
			},
			callback: function (r) {
				frm.set_value("fiscal_year", r.message.current_fiscal_year);
				frm.set_value("ezn_date", frappe.datetime.nowdate());
			}
		});
		frm.set_value("edit_ezn", 1);
		frm.refresh();
	}

	else {
		frm.set_value("ezn_no", frm.doc.old_ezn_no);
		frm.set_value("ezn_date", frm.doc.old_ezn_date);
		frm.set_value("fiscal_year", frm.doc.old_fiscal_year);
		frm.set_value("edit_ezn", 0);
		frm.set_value("old_ezn_no", "");
		frm.set_value("old_fiscal_year", "");
		frm.refresh();
	}
});

frappe.ui.form.on("Vehicle Maintenance Process", {
	refresh: (frm) => {
		frm.set_query("item_code", "kashf_ohda_item", () => {
			return {
				filters: [
					["Item", "is_stock_item", "=", 1],
					["Item", "item_category", "=", "صيانة"],
				],
			};
		});
	},
});


frappe.ui.form.on("Vehicle Maintenance Process", "select_all_maintenance_type", function (frm) {
	let maintenance_order_items = []
	frm.doc.kashf_ohda_item.forEach(element => {
		element.maintenance_method == "إصلاح خارجي" && element.include_in_maintenance_order ? element.maintenance_type = frm.doc.select_all_maintenance_type : element.maintenance_type = ""
		// element.maintenance_type = frm.doc.select_all_maintenance_type 
		maintenance_order_items.push(element)
	});
	frm.doc.kashf_ohda_item = maintenance_order_items
	frm.doc.select_all_maintenance_type = ""
	frm.refresh_fields();
	frm.refresh();

});

frappe.ui.form.on("Vehicle Maintenance Process", "select_all_maintenance_method", function (frm) {
	let maintenance_order_items = []
	frm.doc.kashf_ohda_item.forEach(element => {
		element.include_in_maintenance_order ? element.maintenance_method = frm.doc.select_all_maintenance_method : element.maintenance_method = element.maintenance_method
		// element.maintenance_method = frm.doc.select_all_maintenance_method
		maintenance_order_items.push(element)
	});
	frm.doc.kashf_ohda_item = maintenance_order_items
	frm.doc.select_all_maintenance_method = ""
	frm.refresh_fields();
	frm.refresh();

});

frappe.ui.form.on("Vehicle Maintenance Process", "select_all_disc_percent", function (frm) {
	let maintenance_order_items22 = []
	frm.doc.kashf_ohda_item.forEach(element => {
		element.include_in_maintenance_order ? element.disc = frm.doc.select_all_disc_percent : element.disc = element.disc
		// element.disc = eval(frm.doc.select_all_disc_percent)
		// console.log( element.disc)
		maintenance_order_items22.push(element)
	});
	frm.doc.kashf_ohda_item = maintenance_order_items22
	// frm.doc.select_all_disc_percent =""
	frm.refresh_fields();
	frm.refresh();

});

frappe.ui.form.on("Vehicle Maintenance Process", "select_all_maintenance_order", function (frm) {
	let maintenance_order_items = []
	var maintenance_order = 0
	if (frm.doc.select_all_maintenance_order == "إنشاء إجراء إصلاح للكل") {
		maintenance_order = 1
	};
	if (frm.doc.select_all_maintenance_order == "إلغاء إجراء إصلاح للكل") {
		maintenance_order = 0
	};
	frm.doc.kashf_ohda_item.forEach(element => {
		element.maintenance_method == "إصلاح خارجي" ? element.include_in_maintenance_order = 0 : element.include_in_maintenance_order = maintenance_order
		// element.include_in_maintenance_order = maintenance_order
		maintenance_order_items.push(element)
	});
	frm.doc.kashf_ohda_item = maintenance_order_items
	frm.doc.select_all_maintenance_order = ""
	frm.refresh_fields();
	frm.refresh();
});

frappe.ui.form.on("Vehicle Maintenance Process", "karta", function (frm) {
	var myWin = window.open('/app/query-report/Car%20Card?vic_serial=' + cur_frm.doc.vehicles);
});


// frappe.ui.form.on("Vehicle Maintenance Process", "print_internal_ezn", function(frm, cdt, cdn){
// 	let is_printed = 0;
// 	$.each(cur_frm.doc.maintenance_print_logs || [], function(i, d) {
// 		if (cur_frm.doc.enable_print === 0 && d.format_name == "كشف عهدة" && d.format_no == cur_frm.doc.print_templete1){
// 			is_printed = 1;
// 		}
// 	})
// 	if (is_printed == 1){
// 		frappe.throw(" لقد تم طباعة نموذج رقم " + (cur_frm.doc.print_templete1) + " من قبل ولا يمكن طباعته مرة أخرى ... برجاء الرجوع للإدارة ")
// 	}
// 	if (is_printed == 0){
// 		var myWin = window.open('/printview?doctype=Vehicle%20Maintenance%20Process&name='+ frm.doc.name +'&trigger_print=1&format=Internal%20Maintenance%20Print&no_letterhead=1&letterhead=No%20Letterhead&settings=%7B%7D&_lang=ar');
// 	}	
// 	frappe.call({
// 		doc: frm.doc,
// 		method: "print_internal_ezn",
// 		callback: function(r) {
// 			frm.refresh_fields();
// 			frm.refresh();
// 		}
// 	});
// });


frappe.ui.form.on("Vehicle Maintenance Process", "print_internal_ezn", function (frm, cdt, cdn) {
	var myWin = window.open('/printview?doctype=Vehicle%20Maintenance%20Process&name=' + frm.doc.name + '&trigger_print=1&format=Internal%20Maintenance%20Print&no_letterhead=1&letterhead=No%20Letterhead&settings=%7B%7D&_lang=ar');
	frm.doc.enable_print = 0
	frappe.call({
		doc: frm.doc,
		method: "print_internal_ezn",
		callback: function (r) {
			frm.refresh_fields();
			frm.refresh();
		}
	});
});

frappe.ui.form.on("Vehicle Maintenance Process", "preview_internal_ezn", function (frm) {
	var myWin = window.open('/printview?doctype=Vehicle%20Maintenance%20Process&name=' + cur_frm.doc.name + '&trigger_print=1&format=Internal%20Maintenance%20Preview&no_letterhead=1&letterhead=No%20Letterhead&settings=%7B%7D&_lang=ar');
});

// frappe.ui.form.on("Vehicle Maintenance Process", "print_external_ezn", function(frm){
// 	let is_printed = 0;
// 	$.each(cur_frm.doc.maintenance_print_logs || [], function(i, d) {
// 		if (cur_frm.doc.enable_print === 0 && d.format_name == "إذن إصلاح خارجي" && d.format_no == cur_frm.doc.print_templete2){
// 			is_printed = 1;
// 		}
// 	})
// 	if (is_printed == 1){
// 		frappe.throw(" لقد تم طباعة نموذج رقم " + (cur_frm.doc.print_templete2) + " من قبل ولا يمكن طباعته مرة أخرى ... برجاء الرجوع للإدارة ")
// 	}
// 	if (is_printed == 0){
// 		var myWin = window.open('/printview?doctype=Vehicle%20Maintenance%20Process&name='+ cur_frm.doc.name +'&trigger_print=1&format=External%20Maintenance%20Print&no_letterhead=1&letterhead=No%20Letterhead&settings=%7B%7D&_lang=ar');	
// 	}	
// 	frappe.call({
// 		doc: frm.doc,
// 		method: "print_external_ezn",
// 		callback: function(r) {
// 			frm.refresh_fields();
// 			frm.refresh();
// 		}
// 	});
// });

frappe.ui.form.on("Vehicle Maintenance Process", "print_external_ezn", function (frm) {
	window.open('/printview?doctype=Vehicle%20Maintenance%20Process&name=' + cur_frm.doc.name + '&trigger_print=1&format=External%20Maintenance%20Print&no_letterhead=1&letterhead=No%20Letterhead&settings=%7B%7D&_lang=ar');
	frm.doc.enable_print = 0
	frappe.call({
		doc: frm.doc,
		method: "print_external_ezn",
		callback: function (r) {
			frm.refresh_fields();
			frm.refresh();
		}
	});
});


frappe.ui.form.on("Vehicle Maintenance Process", "preview_external_ezn", function (frm) {
	var myWin = window.open('/printview?doctype=Vehicle%20Maintenance%20Process&name=' + cur_frm.doc.name + '&trigger_print=1&format=External%20Maintenance%20Preview&no_letterhead=1&letterhead=No%20Letterhead&settings=%7B%7D&_lang=ar');
});

// frappe.ui.form.on("Vehicle Maintenance Process", "print_external_ezn_on_entity", function(frm){
// 	let is_printed = 0;
// 	$.each(cur_frm.doc.maintenance_print_logs || [], function(i, d) {
// 		if (cur_frm.doc.enable_print === 0 && d.format_name == "إصلاح خارجي على الجهة" && d.format_no == cur_frm.doc.print_templete2){
// 			is_printed = 1;
// 		}
// 	})
// 	if (is_printed == 1){
// 		frappe.throw(" لقد تم طباعة نموذج رقم " + (cur_frm.doc.print_templete2) + " من قبل ولا يمكن طباعته مرة أخرى ... برجاء الرجوع للإدارة ")
// 	}
// 	if (is_printed == 0){
// 		var myWin = window.open('/printview?doctype=Vehicle%20Maintenance%20Process&name='+ cur_frm.doc.name +'&trigger_print=1&format=External%20Maintenance%20On%20Entity%20Print&no_letterhead=1&letterhead=No%20Letterhead&settings=%7B%7D&_lang=ar');	
// 	}	
// 	frappe.call({
// 		doc: frm.doc,
// 		method: "print_external_ezn_on_entity",
// 		callback: function(r) {
// 			frm.refresh_fields();
// 			frm.refresh();
// 		}
// 	});
// });


frappe.ui.form.on("Vehicle Maintenance Process", "print_external_ezn_on_entity", function (frm) {
	var myWin = window.open('/printview?doctype=Vehicle%20Maintenance%20Process&name=' + cur_frm.doc.name + '&trigger_print=1&format=External%20Maintenance%20On%20Entity%20Print&no_letterhead=1&letterhead=No%20Letterhead&settings=%7B%7D&_lang=ar');
	frm.doc.enable_print = 0
	frappe.call({
		doc: frm.doc,
		method: "print_external_ezn_on_entity",
		callback: function (r) {
			frm.refresh_fields();
			frm.refresh();
		}
	});
});


frappe.ui.form.on("Vehicle Maintenance Process", "preview_external_ezn_on_entity", function (frm) {
	var myWin = window.open('/printview?doctype=Vehicle%20Maintenance%20Process&name=' + cur_frm.doc.name + '&trigger_print=1&format=External%20Maintenance%20On%20Entity%20Preview&no_letterhead=1&letterhead=No%20Letterhead&settings=%7B%7D&_lang=ar');
});

// frappe.ui.form.on("Vehicle Maintenance Process", "print_purchase_wallet", function(frm){
// 	let is_printed = 0;
// 	$.each(cur_frm.doc.maintenance_print_logs || [], function(i, d) {
// 		if (cur_frm.doc.enable_print === 0 && d.format_name == "حافظة مشتريات" && d.format_no == cur_frm.doc.print_templete2){
// 			is_printed = 1;
// 		}
// 	})
// 	if (is_printed == 1){
// 		frappe.throw(" لقد تم طباعة نموذج رقم " + (cur_frm.doc.print_templete2) + " من قبل ولا يمكن طباعته مرة أخرى ... برجاء الرجوع للإدارة ")
// 	}
// 	if (is_printed == 0){
// 		var myWin = window.open('/printview?doctype=Vehicle%20Maintenance%20Process&name='+ cur_frm.doc.name +'&trigger_print=1&format=Purchase%20Wallet%20Print&no_letterhead=1&letterhead=No%20Letterhead&settings=%7B%7D&_lang=ar');	
// 	}	
// 	frappe.call({
// 		doc: frm.doc,
// 		method: "print_purchase_wallet",
// 		callback: function(r) {
// 			frm.refresh_fields();
// 			frm.refresh();
// 		}
// 	});
// });

frappe.ui.form.on("Vehicle Maintenance Process", "print_purchase_wallet", function (frm) {
	var myWin = window.open('/printview?doctype=Vehicle%20Maintenance%20Process&name=' + cur_frm.doc.name + '&trigger_print=1&format=Purchase%20Wallet%20Print&no_letterhead=1&letterhead=No%20Letterhead&settings=%7B%7D&_lang=ar');
	frm.doc.enable_print = 0
	frappe.call({
		doc: frm.doc,
		method: "print_purchase_wallet",
		callback: function (r) {
			frm.refresh_fields();
			frm.refresh();
		}
	});
});


frappe.ui.form.on("Vehicle Maintenance Process", "preview_purchase_wallet", function (frm) {
	var myWin = window.open('/printview?doctype=Vehicle%20Maintenance%20Process&name=' + cur_frm.doc.name + '&trigger_print=1&format=Purchase%20Wallet%20Preview&no_letterhead=1&letterhead=No%20Letterhead&settings=%7B%7D&_lang=ar');
});

frappe.ui.form.on("Vehicle Maintenance Process", "print_issue_return", function (frm) {
	let is_printed = 0;
	$.each(frm.doc.maintenance_print_logs || [], function (i, d) {
		if (frm.doc.enable_print === 0 && d.format_name == "إذن صرف وإرتجاع" && d.format_no == frm.doc.print_templete2) {
			is_printed = 1;
		}
	})
	if (is_printed == 1) {
		frappe.throw(" لقد تم طباعة نموذج رقم " + (frm.doc.print_templete2) + " من قبل ولا يمكن طباعته مرة أخرى ... برجاء الرجوع للإدارة ")
	}
	if (is_printed == 0) {
		var myWin = window.open('/printview?doctype=Vehicle%20Maintenance%20Process&name=' + cur_frm.doc.name + '&trigger_print=1&format=Issue%20And%20Return%20Print&no_letterhead=1&letterhead=No%20Letterhead&settings=%7B%7D&_lang=ar');
	}
	frm.doc.enable_print = 0
	frappe.call({
		doc: frm.doc,
		method: "print_issue_return",
		callback: function (r) {
			frm.refresh_fields();
			frm.refresh();
		}
	});
});

frappe.ui.form.on("Vehicle Maintenance Process", "preview_issue_return", function (frm) {
	var myWin = window.open('/printview?doctype=Vehicle%20Maintenance%20Process&name=' + cur_frm.doc.name + '&trigger_print=1&format=Issue%20And%20Return%20Preview&no_letterhead=1&letterhead=No%20Letterhead&settings=%7B%7D&_lang=ar');
});


frappe.ui.form.on("Vehicle Maintenance Process", "print_certificate", function (frm) {
	let is_printed = 0;
	$.each(cur_frm.doc.maintenance_print_logs || [], function (i, d) {
		if (cur_frm.doc.enable_print === 0 && d.format_name == "شهادة إدارية" && d.format_no == cur_frm.doc.print_templete2) {
			is_printed = 1;
		}
	})
	if (is_printed == 1) {
		frappe.throw(" لقد تم طباعة نموذج رقم " + (cur_frm.doc.print_templete2) + " من قبل ولا يمكن طباعته مرة أخرى ... برجاء الرجوع للإدارة ")
	}
	if (is_printed == 0) {
		var myWin = window.open('/printview?doctype=Vehicle%20Maintenance%20Process&name=' + cur_frm.doc.name + '&trigger_print=1&format=Certificate%20Print&no_letterhead=1&letterhead=No%20Letterhead&settings=%7B%7D&_lang=ar');
	}
	frm.doc.enable_print = 0
	frappe.call({
		doc: frm.doc,
		method: "print_certificate",
		callback: function (r) {
			frm.refresh_fields();
			frm.refresh();
		}
	});
});

frappe.ui.form.on("Vehicle Maintenance Process", "preview_exchange_certificate", function (frm) {
	var myWin = window.open('/printview?doctype=Vehicle%20Maintenance%20Process&name=' + cur_frm.doc.name + '&trigger_print=1&format=Certificate%20Exchange%20Preview&no_letterhead=1&letterhead=No%20Letterhead&settings=%7B%7D&_lang=ar');
});


frappe.ui.form.on("Vehicle Maintenance Process", "print_exchange_certificate", function (frm) {
	let is_printed = 0;
	$.each(cur_frm.doc.maintenance_print_logs || [], function (i, d) {
		if (cur_frm.doc.enable_print === 0 && d.format_name == "شهادة إستبدال" && d.format_no == cur_frm.doc.print_templete2) {
			is_printed = 1;
		}
	})
	if (is_printed == 1) {
		frappe.throw(" لقد تم طباعة نموذج رقم " + (cur_frm.doc.print_templete2) + " من قبل ولا يمكن طباعته مرة أخرى ... برجاء الرجوع للإدارة ")
	}
	if (is_printed == 0) {
		var myWin = window.open('/printview?doctype=Vehicle%20Maintenance%20Process&name=' + cur_frm.doc.name + '&trigger_print=1&format=Certificate%20Exchange%20Print&no_letterhead=1&letterhead=No%20Letterhead&settings=%7B%7D&_lang=ar');
	}
	frm.doc.enable_print = 0
	frappe.call({
		doc: frm.doc,
		method: "print_exchange_certificate",
		callback: function (r) {
			frm.refresh_fields();
			frm.refresh();
		}
	});
});

frappe.ui.form.on("Vehicle Maintenance Process", "preview_certificate", function (frm) {
	var myWin = window.open('/printview?doctype=Vehicle%20Maintenance%20Process&name=' + cur_frm.doc.name + '&trigger_print=1&format=Certificate%20Preview&no_letterhead=1&letterhead=No%20Letterhead&settings=%7B%7D&_lang=ar');
});



// frappe.ui.form.on("Vehicle Maintenance Process", "print_maintenance_rfq", function(frm){
// 	let is_printed = 0;
// 	$.each(cur_frm.doc.maintenance_print_logs || [], function(i, d) {
// 		if (cur_frm.doc.enable_print === 0 && d.format_name == "طلب عروض أسعار"){
// 			is_printed = 1;
// 		}
// 	})
// 	if (is_printed == 1){
// 		frappe.throw(" لقد تم طباعة طلب عروض الأسعار من قبل ولا يمكن طباعته مرة أخرى ... برجاء الرجوع للإدارة ")
// 	}
// 	if (is_printed == 0){
// 		var myWin = window.open('/printview?doctype=Vehicle%20Maintenance%20Process&name='+ cur_frm.doc.name +'&trigger_print=1&format=Maintenance%20RFQ%20Print&no_letterhead=1&letterhead=No%20Letterhead&settings=%7B%7D&_lang=ar');	
// 	}	
// 	frappe.call({
// 		doc: frm.doc,
// 		method: "print_maintenance_rfq",
// 		callback: function(r) {
// 			frm.refresh_fields();
// 			frm.refresh();
// 		}
// 	});
// });


frappe.ui.form.on("Vehicle Maintenance Process", "print_maintenance_rfq", function (frm) {
	var myWin = window.open('/printview?doctype=Vehicle%20Maintenance%20Process&name=' + cur_frm.doc.name + '&trigger_print=1&format=Maintenance%20RFQ%20Print&no_letterhead=1&letterhead=No%20Letterhead&settings=%7B%7D&_lang=ar');
	frm.doc.enable_print = 0
	frappe.call({
		doc: frm.doc,
		method: "print_maintenance_rfq",
		callback: function (r) {
			frm.refresh_fields();
			frm.refresh();
		}
	});
});


// frappe.ui.form.on("Vehicle Maintenance Process", "print_mozakira", function(frm){
// 	let is_printed = 0;
// 	$.each(cur_frm.doc.maintenance_print_logs || [], function(i, d) {
// 		if (cur_frm.doc.enable_print === 0 && d.format_name == "مذكرة عرض"){
// 			is_printed = 1;
// 		}
// 	})
// 	if (is_printed == 1){
// 		frappe.throw(" لقد تم طباعة مذكرة العرض من قبل ولا يمكن طباعتها مرة أخرى ... برجاء الرجوع للإدارة ")
// 	}
// 	if (is_printed == 0){
// 		var myWin = window.open('/printview?doctype=Vehicle%20Maintenance%20Process&name='+ cur_frm.doc.name +'&trigger_print=1&format=Mozakira%20Print&no_letterhead=1&letterhead=No%20Letterhead&settings=%7B%7D&_lang=ar');	
// 	}	
// 	frappe.call({
// 		doc: frm.doc,
// 		method: "print_mozakira",
// 		callback: function(r) {
// 			frm.refresh_fields();
// 			frm.refresh();
// 		}
// 	});
// });


frappe.ui.form.on("Vehicle Maintenance Process", "print_mozakira", function (frm) {
	var myWin = window.open('/printview?doctype=Vehicle%20Maintenance%20Process&name=' + cur_frm.doc.name + '&trigger_print=1&format=Mozakira%20Print&no_letterhead=1&letterhead=No%20Letterhead&settings=%7B%7D&_lang=ar');
	frm.doc.enable_print = 0
	frappe.call({
		doc: frm.doc,
		method: "print_mozakira",
		callback: function (r) {
			frm.refresh_fields();
			frm.refresh();
		}
	});
});


// frappe.ui.form.on("Vehicle Maintenance Process", "print_job_order", function(frm){
// 	let is_printed = 0;
// 	$.each(cur_frm.doc.maintenance_print_logs || [], function(i, d) {
// 		if (cur_frm.doc.enable_print === 0 && d.format_name == "أمر شغل"){
// 			is_printed = 1;
// 		}
// 	})
// 	if (is_printed == 1){
// 		frappe.throw(" لقد تم طباعة أمر الشغل من قبل ولا يمكن طباعته مرة أخرى ... برجاء الرجوع للإدارة ")
// 	}
// 	if (is_printed == 0){
// 		var myWin = window.open('/printview?doctype=Vehicle%20Maintenance%20Process&name='+ cur_frm.doc.name +'&trigger_print=1&format=Job%20Order%20Print&no_letterhead=1&letterhead=No%20Letterhead&settings=%7B%7D&_lang=ar');	
// 	}	
// 	frappe.call({
// 		doc: frm.doc,
// 		method: "print_job_order",
// 		callback: function(r) {
// 			frm.refresh_fields();
// 			frm.refresh();
// 		}
// 	});
// });

frappe.ui.form.on("Vehicle Maintenance Process", "print_job_order", function (frm) {
	var myWin = window.open('/printview?doctype=Vehicle%20Maintenance%20Process&name=' + cur_frm.doc.name + '&trigger_print=1&format=Job%20Order%20Print&no_letterhead=1&letterhead=No%20Letterhead&settings=%7B%7D&_lang=ar');
	frm.doc.enable_print = 0
	frappe.call({
		doc: frm.doc,
		method: "print_job_order",
		callback: function (r) {
			frm.refresh_fields();
			frm.refresh();
		}
	});
});


frappe.ui.form.on("Vehicle Maintenance Process", "print_templete1", function (frm) {
	frm.save();
});

frappe.ui.form.on("Vehicle Maintenance Process", "print_templete2", function (frm) {
	frm.save();
});


frappe.ui.form.on("Vehicle Maintenance Process", "print_mahdar_fahs", function (frm) {
	var myWin = window.open('/printview?doctype=Vehicle%20Maintenance%20Process&name=' + cur_frm.doc.name + '&trigger_print=1&format=Mahdar%20Fahs%20Print&no_letterhead=1&letterhead=No%20Letterhead&settings=%7B%7D&_lang=ar');
});

frappe.ui.form.on("Vehicle Maintenance Process", "print_ezn_sarf", function (frm) {
	var myWin = window.open('/printview?doctype=Vehicle%20Maintenance%20Process&name=' + cur_frm.doc.name + '&trigger_print=1&format=Ezn%20Sarf%20Print&no_letterhead=1&letterhead=No%20Letterhead&settings=%7B%7D&_lang=ar');
});

frappe.ui.form.on("Vehicle Maintenance Process", "print_ezn_ertgaa", function (frm) {
	var myWin = window.open('/printview?doctype=Vehicle%20Maintenance%20Process&name=' + cur_frm.doc.name + '&trigger_print=1&format=Ezn%20Ertgaa%20Print&no_letterhead=1&letterhead=No%20Letterhead&settings=%7B%7D&_lang=ar');
});


// frappe.ui.form.on("Vehicle Maintenance Process", "print_request_for_quotations", function (frm) {
// 	var myWin = window.open('/printview?doctype=Vehicle%20Maintenance%20Process&name=' + cur_frm.doc.name + '&trigger_print=1&format=Request%20Order%20for%20Quotation%20Items&no_letterhead=1&letterhead=No%20Letterhead&settings=%7B%7D&_lang=ar');
// });
// frappe.ui.form.on("Vehicle Maintenance Process", "print_mozakira_purchase", function (frm) {
// 	var myWin = window.open('/printview?doctype=Vehicle%20Maintenance%20Process&name=' + cur_frm.doc.name + '&trigger_print=1&format=Direct%20Order%20Purchase&no_letterhead=1&letterhead=No%20Letterhead&settings=%7B%7D&_lang=ar');
// });
// frappe.ui.form.on("Vehicle Maintenance Process", "print_purchase_order", function (frm) {
// 	var myWin = window.open('/printview?doctype=Vehicle%20Maintenance%20Process&name=' + cur_frm.doc.name + '&trigger_print=1&format=Purchase%20Import&no_letterhead=1&letterhead=No%20Letterhead&settings=%7B%7D&_lang=ar');
// });


// frappe.ui.form.on("Kashf Ohda Item", "item_code", function(frm, cdt, cdn) {
// 	let item = locals[cdt][cdn];
// 	if (!frm.doc.vehicles){
// 		item.include_in_maintenance_order=0
// 		frm.refresh_fields("kashf_ohda_item");

// 		frappe.throw({
// 			title: ('تنبيه'),
// 			indicator: 'red',
// 			message: ('قم بإختيار رقم مركبة أولا'),
// 		})
// 	}
// 		frappe.call({
// 			method: "ecs_vehicles.ecs_vehicles.doctype.vehicle_maintenance_process.vehicle_maintenance_process.get_last_sarf_detail",
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
// 		// frm.doc.ezn_egraa_item.forEach((egraa,idx, array)=>{
// 		// 	if (egraa.custody_report_item.toString() === item.name.toString()) {
// 		// 		frm.doc.ezn_egraa_item[idx].item_code = item.item_code
// 		// 		frm.doc.ezn_egraa_item[idx].item_name = item.item_name
// 		// 		frm.doc.ezn_egraa_item[idx].item_group = item.item_group
// 		// 		frm.doc.ezn_egraa_item[idx].description = item.description
// 		// 		frm.doc.ezn_egraa_item[idx].qty = item.qty
// 		// 		frm.doc.ezn_egraa_item[idx].default_unit_of_measure = item.default_unit_of_measure
// 		// 		if (item.maintenance_method === "إذن صرف وإرتجاع") {

// 		// 			let karta_name = update_karta(frm.doc.ezn_egraa_item[idx].kle, item.item_code, item.qty)
// 		// 		}

// 		// 		frm.refresh_field("ezn_egraa_item")
// 		// 		frm.refresh();


// 		// 	}
// 		// })
// });


const update_row_maintenance_order_item = (maintenance_order_items, doc, frm) => {
	// sleep(2000)

	// let ezn_egraa_item2 = []
	// 	frm.doc.ezn_egraa_item.forEach((egraa,idx, array)=>{
	// 		ezn_egraa_item2.push(egraa.custody_report_item.toString())
	// 	})
	let ezn_3ohdaa_items = []
	frm.doc.kashf_ohda_item.forEach((kashf, idx, array) => {
		ezn_3ohdaa_items.push(kashf)
	})
	maintenance_order_items.forEach((item, idx, array) => {
		frm.doc.kashf_ohda_item.forEach((kashf, idx, array) => {
			if (kashf.name.toString() === item.custody_report_item) {
				ezn_3ohdaa_items.push(kashf)
			}
		})

	})

	frm.refresh_field('ezn_egraa_item');

}
const toggel_include_maintenance = (kashf_al3ohda_items, doc, frm) => {
	let ezn_egraa_items = []
	frm.doc.ezn_egraa_item.forEach((egraa, idx, array) => {
		ezn_egraa_items.push(egraa.custody_report_item.toString())
	})
	let ezn_3ohdaa_items = []
	frm.doc.kashf_ohda_item.forEach((kashf, idx, array) => {
		ezn_3ohdaa_items.push(kashf.name.toString())
	})
	console.log(ezn_egraa_items)
	console.log("here")
	kashf_al3ohda_items.forEach((item, idx, array) => {
		console.log("here2")
		console.log(ezn_egraa_items.includes(item.name.toString()))
		console.log(item.include_in_maintenance_order)
		if (ezn_egraa_items.includes(item.name.toString()) && !item.include_in_maintenance_order) {
			console.log("here3")
			frm.doc.ezn_egraa_item.forEach((row, idx, array) => {
				if (row.custody_report_item.toString() === item.name.toString()) {
					let new_ezn_egraa_item = frm.doc.ezn_egraa_item
					if (row.kle) {
						delete_karta_ledger_entry(row.kle)
					}
					new_ezn_egraa_item.splice(idx, 1);
					frm.doc.ezn_egraa_item = new_ezn_egraa_item
				}
			})
		}

	})

	frm.refresh_field('ezn_egraa_item');
}
const delete_row_maintenance_order_item = (maintenance_order_items, doc, frm) => {
	// sleep(2000)

	let ezn_egraa_item2 = []
	frm.doc.ezn_egraa_item.forEach((egraa, idx, array) => {
		ezn_egraa_item2.push(egraa.custody_report_item.toString())
	})
	let ezn_3ohdaa_items = []
	frm.doc.kashf_ohda_item.forEach((kashf, idx, array) => {
		ezn_3ohdaa_items.push(kashf.name.toString())
	})
	maintenance_order_items.forEach((item, idx, array) => {

		if (!ezn_3ohdaa_items.includes(item.custody_report_item.toString())) {
			frm.doc.ezn_egraa_item.forEach((row, idx, array) => {
				if (row.custody_report_item.toString() === item.custody_report_item.toString()) {
					let new_ezn_egraa_itemsss = frm.doc.ezn_egraa_item
					console.log(new_ezn_egraa_itemsss)
					if (row.kle) {
						delete_karta_ledger_entry(row.kle)
					}
					new_ezn_egraa_itemsss.splice(idx, 1);
					console.log(new_ezn_egraa_itemsss)

					frm.doc.ezn_egraa_item = new_ezn_egraa_itemsss

				}
			})

			// if (new_ezn_egraa_item.length > 0) {

			// 	frm.doc.ezn_egraa_item = new_ezn_egraa_item
			// }
		}
		// removeUnwanted(unwantedNames, wantedNames, frm)

	})

	frm.refresh_field('ezn_egraa_item');

}


const add_maintenance_order_item = (maintenance_order_items, doc, frm) => {
	// sleep(2000)

	let ezn_egraa_item2 = []
	frm.doc.ezn_egraa_item.forEach((egraa, idx, array) => {
		ezn_egraa_item2.push(egraa.custody_report_item.toString())
	})
	let ezn_3ohdaa_items = []
	frm.doc.kashf_ohda_item.forEach((kashf, idx, array) => {
		ezn_3ohdaa_items.push(kashf.name.toString())
	})
	maintenance_order_items.forEach((item, idx, array) => {
		let unwantedNames = []
		let wantedNames = [item.name]
		if (item.include_in_maintenance_order && !ezn_egraa_item2.includes(item.name.toString()) && item.maintenance_method === "إذن صرف وإرتجاع" && !item.kle) {
			let karta_name = create_karta_ledger_entry(item, doc, frm)
		}
		else if (item.include_in_maintenance_order && !ezn_egraa_item2.includes(item.name.toString())) {
			let esla7_table = fill_egra2at_elasla7_table(item, doc, frm)
		}
		// else if (!item.include_in_maintenance_order && ezn_egraa_item2.includes(item.name.toString())){
		// 	let new_ezn_egraa_item = []
		// 	new_ezn_egraa_item.push(item.name)
		// 	frm.doc.ezn_egraa_item.forEach((row,idx, array)=>{
		// 		if (row.custody_report_item.toString() === item.name.toString()) {
		// 			let new_ezn_egraa_itemsss = frm.doc.ezn_egraa_item
		// 			if (row.kle) {
		// 				delete_karta_ledger_entry(row.kle)
		// 			}
		// 			new_ezn_egraa_itemsss.splice(idx, 1);
		// 			frm.doc.ezn_egraa_item = new_ezn_egraa_itemsss
		// 		}
		// 	})

		// 	// if (new_ezn_egraa_item.length > 0) {

		// 	// 	frm.doc.ezn_egraa_item = new_ezn_egraa_item
		// 	// }
		// }
		// removeUnwanted(unwantedNames, wantedNames, frm)

	})

	frm.refresh_field('ezn_egraa_item');

}
const fill_egra2at_elasla7_table = (item, doc, frm) => {
	let ezn_egraa_item = frm.add_child("ezn_egraa_item");
	ezn_egraa_item.maintenance_method = item.maintenance_method
	ezn_egraa_item.maintenance_type = item.maintenance_type
	ezn_egraa_item.consumption_type = item.consumption_type
	ezn_egraa_item.item_code = item.item_code
	ezn_egraa_item.item_group = item.item_group
	ezn_egraa_item.description = item.description
	ezn_egraa_item.qty = item.qty
	ezn_egraa_item.default_unit_of_measure = item.default_unit_of_measure
	ezn_egraa_item.brand = item.brand
	ezn_egraa_item.disc = item.disc
	ezn_egraa_item.last_issue_detail = item.last_issue_detail
	ezn_egraa_item.namozg_no2 = item.namozag_no
	ezn_egraa_item.action_date = frappe.datetime.nowdate()

	ezn_egraa_item.quality = item.quality
	ezn_egraa_item.namozg_no2 = item.namozag_no
	ezn_egraa_item.prt_prc = item.prt_prc

	ezn_egraa_item.store_code = item.store_code
	ezn_egraa_item.last_sarf_qty = item.last_sarf_qty
	// ezn_egraa_item.custody_report=item.debit_credit
	ezn_egraa_item.custody_report_item = item.name
	// ezn_egraa_item.kle=r.message
}

const create_karta_ledger_entry = (item, doc, frm) => {
	frappe.call({
		method: "ecs_vehicles.ecs_vehicles.doctype.vehicle_maintenance_process.vehicle_maintenance_process.create_karta_ledger_entry_method",
		args: {
			"item": item,
			"vehicles": doc.vehicles,
			"ezn_no": doc.ezn_no,
			"date": doc.ezn_date,
			"entity_name": doc.entity_name,
			"fis_year": doc.fiscal_year,
		},
		callback: function (r) {
			// console.log(r)
			if (r) {
				let ezn_egraa_item = frm.add_child("ezn_egraa_item");
				ezn_egraa_item.maintenance_method = item.maintenance_method
				ezn_egraa_item.maintenance_type = item.maintenance_type
				ezn_egraa_item.consumption_type = item.consumption_type
				ezn_egraa_item.item_code = item.item_code
				ezn_egraa_item.item_group = item.item_group
				ezn_egraa_item.description = item.description
				ezn_egraa_item.qty = item.qty
				ezn_egraa_item.default_unit_of_measure = item.default_unit_of_measure
				ezn_egraa_item.brand = item.brand
				ezn_egraa_item.disc = item.disc
				ezn_egraa_item.last_issue_detail = item.last_issue_detail
				ezn_egraa_item.namozg_no2 = item.namozag_no
				ezn_egraa_item.quality = item.quality
				ezn_egraa_item.namozg_no2 = item.namozag_no
				ezn_egraa_item.prt_prc = item.prt_prc
				ezn_egraa_item.action_date = frappe.datetime.nowdate()
				ezn_egraa_item.store_code = item.store_code
				ezn_egraa_item.disc = item.disc
				ezn_egraa_item.last_sarf_qty = item.last_sarf_qty
				// ezn_egraa_item.custody_report=item.debit_credit
				ezn_egraa_item.custody_report_item = item.name
				ezn_egraa_item.kle = r.message

			}
		}
	});
}



const update_karta = (kle, item_code, qty) => {
	frappe.call({
		method: "ecs_vehicles.ecs_vehicles.doctype.vehicle_maintenance_process.vehicle_maintenance_process.update_karta_method",
		args: {
			"kle": kle,
			"part_universal_code": item_code,
			"qty": qty,

		},
		callback: function (r) {
			// console.log(r)

		}
	});
}
const delete_karta_ledger_entry = (kle) => {
	frappe.call({
		method: "ecs_vehicles.ecs_vehicles.doctype.vehicle_maintenance_process.vehicle_maintenance_process.delete_flag_karta_ledger_entry_method",
		args: {
			"kle": kle,
		},
		callback: function (r) {
		}
	});
}

const removeUnwanted = (unwantedNames, wantedNames, frm) => {
	let unwanted_items = []
	frm.doc.ezn_egraa_item.forEach(element => {
		wantedNames.includes(element.custody_report_item) ? unwanted_items.push(element) : console.log(element)
		frm.doc.ezn_egraa_item = unwanted_items
		// delete_flag_karta_ledger_entry(frm, element.kle)
	});

	frm.refresh_fields();
	frm.refresh();
}
function sleep(ms) {
	return new Promise(resolve => setTimeout(resolve, ms));
}




// frappe.ui.form.on("Kashf Ohda Item", "qty", function(frm, cdt, cdn) {
// 	let item = locals[cdt][cdn];
// 	frm.doc.ezn_egraa_item.forEach((egraa,idx, array)=>{
// 		if (egraa.custody_report_item.toString() === item.name.toString()) {
// 			frm.doc.ezn_egraa_item[idx].item_code = item.item_code
// 			frm.doc.ezn_egraa_item[idx].item_name = item.item_name
// 			frm.doc.ezn_egraa_item[idx].item_group = item.item_group
// 			frm.doc.ezn_egraa_item[idx].description = item.description
// 			frm.doc.ezn_egraa_item[idx].qty = item.qty
// 			frm.doc.ezn_egraa_item[idx].default_unit_of_measure = item.default_unit_of_measure
// 			if (item.maintenance_method === "إذن صرف وإرتجاع") {

// 				let karta_name = update_karta(frm.doc.ezn_egraa_item[idx].kle, item.item_code, item.qty)
// 			}

// 			frm.refresh_field("ezn_egraa_item")
// 			frm.refresh();


// 		}
// 	})

// });







// frappe.ui.form.on("Kashf Ohda Item", "namozag_no", function(frm, cdt, cdn) {
// 	let item = locals[cdt][cdn];
// 	frm.doc.ezn_egraa_item.forEach((egraa,idx, array)=>{
// 		if (egraa.custody_report_item.toString() === item.name.toString()) {
// 			frm.doc.ezn_egraa_item[idx].item_code = item.item_code
// 			frm.doc.ezn_egraa_item[idx].item_name = item.item_name
// 			frm.doc.ezn_egraa_item[idx].item_group = item.item_group
// 			frm.doc.ezn_egraa_item[idx].description = item.description
// 			frm.doc.ezn_egraa_item[idx].qty = item.qty
// 			frm.doc.ezn_egraa_item[idx].default_unit_of_measure = item.default_unit_of_measure
// 			frm.doc.ezn_egraa_item[idx].namozg_no2 = item.namozag_no
// 			if (item.maintenance_method === "إذن صرف وإرتجاع") {

// 				let karta_name = update_karta(frm.doc.ezn_egraa_item[idx].kle, item.item_code, item.qty)
// 			}

// 			frm.refresh_field("ezn_egraa_item")
// 			frm.refresh();


// 		}
// 	})

// });



// frappe.ui.form.on("Kashf Ohda Item", "default_unit_of_measure", function(frm, cdt, cdn) {
// 	let item = locals[cdt][cdn];
// 	frm.doc.ezn_egraa_item.forEach((egraa,idx, array)=>{
// 		if (egraa.custody_report_item.toString() === item.name.toString()) {
// 			frm.doc.ezn_egraa_item[idx].item_code = item.item_code
// 			frm.doc.ezn_egraa_item[idx].item_name = item.item_name
// 			frm.doc.ezn_egraa_item[idx].item_group = item.item_group
// 			frm.doc.ezn_egraa_item[idx].description = item.description
// 			frm.doc.ezn_egraa_item[idx].qty = item.qty
// 			frm.doc.ezn_egraa_item[idx].default_unit_of_measure = item.default_unit_of_measure
// 			frm.doc.ezn_egraa_item[idx].namozg_no2 = item.namozag_no
// 			if (item.maintenance_method === "إذن صرف وإرتجاع") {

// 				let karta_name = update_karta(frm.doc.ezn_egraa_item[idx].kle, item.item_code, item.qty)
// 			}

// 			frm.refresh_field("ezn_egraa_item")
// 			frm.refresh();


// 		}
// 	})

// });



// frappe.ui.form.on("Kashf Ohda Item", "maintenance_method", function(frm, cdt, cdn) {
// 	let item = locals[cdt][cdn];
// 	frm.doc.ezn_egraa_item.forEach((egraa,idx, array)=>{
// 		if (egraa.custody_report_item.toString() === item.name.toString()) {
// 			frm.doc.ezn_egraa_item[idx].item_code = item.item_code
// 			frm.doc.ezn_egraa_item[idx].item_name = item.item_name
// 			frm.doc.ezn_egraa_item[idx].item_group = item.item_group
// 			frm.doc.ezn_egraa_item[idx].description = item.description
// 			frm.doc.ezn_egraa_item[idx].qty = item.qty
// 			frm.doc.ezn_egraa_item[idx].default_unit_of_measure = item.default_unit_of_measure
// 			frm.doc.ezn_egraa_item[idx].namozg_no2 = item.namozag_no
// 			frm.doc.ezn_egraa_item[idx].maintenance_method = item.maintenance_method
// 			frm.doc.ezn_egraa_item[idx].maintenance_type = item.maintenance_type
// 			if (item.maintenance_method === "إذن صرف وإرتجاع") {

// 				let karta_name = update_karta(frm.doc.ezn_egraa_item[idx].kle, item.item_code, item.qty)
// 			}

// 			frm.refresh_field("ezn_egraa_item")
// 			frm.refresh();


// 		}
// 	})

// });


// frappe.ui.form.on("Kashf Ohda Item", "maintenance_type", function(frm, cdt, cdn) {
// 	let item = locals[cdt][cdn];
// 	frm.doc.ezn_egraa_item.forEach((egraa,idx, array)=>{
// 		if (egraa.custody_report_item.toString() === item.name.toString()) {
// 			frm.doc.ezn_egraa_item[idx].item_code = item.item_code
// 			frm.doc.ezn_egraa_item[idx].item_name = item.item_name
// 			frm.doc.ezn_egraa_item[idx].item_group = item.item_group
// 			frm.doc.ezn_egraa_item[idx].description = item.description
// 			frm.doc.ezn_egraa_item[idx].qty = item.qty
// 			frm.doc.ezn_egraa_item[idx].default_unit_of_measure = item.default_unit_of_measure
// 			frm.doc.ezn_egraa_item[idx].namozg_no2 = item.namozag_no
// 			frm.doc.ezn_egraa_item[idx].maintenance_method = item.maintenance_method
// 			frm.doc.ezn_egraa_item[idx].maintenance_type = item.maintenance_type
// 			if (item.maintenance_method === "إذن صرف وإرتجاع") {

// 				let karta_name = update_karta(frm.doc.ezn_egraa_item[idx].kle, item.item_code, item.qty)
// 			}

// 			frm.refresh_field("ezn_egraa_item")
// 			frm.refresh();


// 		}
// 	})

// });








frappe.ui.form.on("Kashf Ohda Item", "maintenance_method", function (frm, cdt, cdn) {
	let item = locals[cdt][cdn];
	frappe.call({
		doc: frm.doc,
		method: "opened_job_order",
		freeze: 1,
		callback: function (r) {
			if (r.message) {
				item.maintenance_method = ""
				frappe.throw(r.message)

			}
			frm.refresh_fields();
			frm.refresh();
		}
	});

});


frappe.ui.form.on("Kashf Ohda Item", "include_in_maintenance_order", function (frm, cdt, cdn) {
	let item = locals[cdt][cdn];
	frappe.call({
		doc: frm.doc,
		method: "opened_job_order",
		freeze: 1,
		callback: function (r) {
			if (r.message) {
				item.include_in_maintenance_order = 0
				frappe.throw(r.message)

			}
			frm.refresh_fields();
			frm.refresh();
		}
	});

});