frappe.ui.form.on('Vouchers Review', {
    refresh: function (frm) {
        // frm.set_df_property("review_vouchers_table", "cannot_delete_rows", true);
        frm.set_df_property("review_vouchers_table", "cannot_add_rows", true);
    }
});

frappe.ui.form.on("Vouchers Review", "onload", function (frm) {
    frappe.call({
        doc: frm.doc,
        method: "set_today_date",
        callback: function (r) {
            frm.refresh_field("date");
        }
    });
});


frappe.ui.form.on("Vouchers Review", {
    refresh: function (frm, cdt, cdn) {
        if (frm.doc.docstatus == 1) {
            frm.add_custom_button(__("تكرار"), function () {
                var child = locals[cdt][cdn];
                frappe.route_options = {
                    "company_name": frm.doc.company_name,
                    "fiscal_year": frm.doc.fiscal_year,
                    "date": frm.doc.date,
                    "received_voucher": frm.doc.received_voucher,
                    "batch_no": frm.doc.batch_no,
                };
                frappe.new_doc("Vouchers Review");
            },);
        }
    }
});

frappe.ui.form.on('Vouchers Review', {
    setup: function (frm) {
        frm.set_query("received_voucher", function () {
            return {
                filters: [
                    ["Received Vouchers", "docstatus", "=", 1],
                    ["Received Vouchers", "company_name", "=", frm.doc.company_name],
                    ["Received Vouchers", "fiscal_year", "=", frm.doc.fiscal_year]
                ]
            };
        });
    }
});



frappe.ui.form.on('Vouchers Review', {
    group_no: function (frm) {
        frappe.call({
            doc: frm.doc,
            method: "check_group_no",
            callback: function (r) {
            }
        });
    }
});

frappe.ui.form.on("Vouchers Review", "copy_barcode", function (frm) {
    frm.set_value("barcode", frm.doc.manual_barcode);
    cur_frm.doc.manual_barcode = "";
    cur_frm.refresh_field('manual_barcode');
});

frappe.ui.form.on('Review Vouchers Table', {
    review_vouchers_table_remove(frm, cdt, cdn) {
        cur_frm.doc.counter = cur_frm.doc.review_vouchers_table.length;
        cur_frm.refresh_field('counter');
    }
});


frappe.ui.form.on("Vouchers Review", "barcode", function (frm, cdt, cdn) {
    $.each(frm.doc.review_vouchers_table || [], function (i, d) {
        if (d.barcode_no == cur_frm.doc.barcode && cur_frm.doc.review === 0) {
            cur_frm.doc.barcode = "";
            cur_frm.refresh_field('barcode');
            frappe.throw(" البون " + d.barcode_no + " تم إضافته من قبل في الصف رقم " + d.idx);
        }

        if (d.barcode_no == cur_frm.doc.barcode && cur_frm.doc.review == 1) {
            d.reviewed = 1
            cur_frm.doc.barcode = "";
            cur_frm.refresh_field('review_vouchers_table');
            cur_frm.refresh_field('barcode');
        }
    });
    frappe.call({
        method: "frappe.client.get_value", args: {
            doctype: "Voucher",
            fieldname: ["barcode_no", "entity", "voucher_type", "serial_no", "release_date", "disabled", "lost", "reviewed", "voucher_review", "batch_no", "group_no", "review_date"],
            filters: { 'barcode_no': cur_frm.doc.barcode, }
        },
        callback: function (r) {
            if (cur_frm.doc.counter == cur_frm.doc.group_count && cur_frm.doc.docstatus != 1) {
                cur_frm.doc.barcode = "";
                cur_frm.refresh_field('barcode');
                frappe.throw("عدد البونات المدخلة تجاوز إجمالي المجموعة");
            }
            if (r.message.barcode_no && r.message.disabled === 0 && r.message.lost === 0 && r.message.entity && r.message.reviewed === 0 && cur_frm.doc.docstatus != 1) {
                var d = frm.add_child("review_vouchers_table");
                d.entity = r.message.entity;
                d.voucher_type = r.message.voucher_type;
                d.serial_no = r.message.serial_no;
                d.barcode_no = r.message.barcode_no;
                d.release_date = r.message.release_date;
                cur_frm.refresh_field("review_vouchers_table");
                cur_frm.doc.barcode = "";
                cur_frm.refresh_field('barcode');
                cur_frm.doc.counter = cur_frm.doc.review_vouchers_table.length;
                cur_frm.refresh_field('counter');
            }
            if (r.message.disabled == 1 && cur_frm.doc.barcode) {
                cur_frm.doc.barcode = "";
                cur_frm.refresh_field('barcode');
                frappe.throw(" البون " + r.message.barcode_no + " معطل ");
            }
            if (r.message.reviewed == 1 && cur_frm.doc.barcode) {
                cur_frm.doc.barcode = "";
                cur_frm.refresh_field('barcode');
                frappe.throw(" البون " + r.message.barcode_no + " تم صرفه لجهة " + r.message.entity + " وتم تسويته بدفعة " + r.message.batch_no + " ومجموعة " + r.message.group_no + " بتاريخ " + r.message.review_date);
            }
            if (r.message.lost == 1 && cur_frm.doc.barcode) {
                cur_frm.doc.barcode = "";
                cur_frm.refresh_field('barcode');
                frappe.throw(" البون " + r.message.barcode_no + " مفقود ");
            }
            if (!r.message.barcode_no && cur_frm.doc.barcode) {
                var y = cur_frm.doc.barcode;
                cur_frm.doc.barcode = "";
                cur_frm.refresh_field('barcode');
                frappe.throw("لا يوجد بون بهذا الباركود " + y);
            }
            if (!r.message.entity && cur_frm.doc.barcode) {
                cur_frm.doc.barcode = "";
                cur_frm.refresh_field('barcode');
                frappe.throw(" البون " + r.message.barcode_no + " لم يتم صرفه إلى أى جهة ");
            }
            else {
                cur_frm.doc.barcode = "";
                cur_frm.refresh_field('barcode');
            }
        }
    });
});