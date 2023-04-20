// Copyright (c) 2022, erpcloud.systems and contributors
// For license information, please see license.txt
frappe.ui.form.on('Vouchers Review', {
    refresh:function(frm){
        frm.set_df_property("review_vouchers_table", "cannot_delete_rows", true);
        frm.set_df_property("review_vouchers_table", "cannot_add_rows", true);
    }
});

frappe.ui.form.on('Vouchers Review', {
   setup: function(frm) {
       frm.set_query("received_voucher", function() {
           return {
               filters: [
                   ["Received Vouchers", "docstatus", "=", 1],
                   ["Received Vouchers","company_name", "=", frm.doc.company_name]
               ]
           };
       });
   }
});

frappe.ui.form.on("Vouchers Review", "barcode", function(frm, cdt, cdn) {
    $.each(frm.doc.review_vouchers_table || [], function(i, d) {
        if (d.barcode_no == cur_frm.doc.barcode) {
            cur_frm.doc.barcode = "";
            cur_frm.refresh_field('barcode');
            frappe.throw(" البون " + d.barcode_no + " تم إضافته من قبل في الصف رقم " + d.idx);
        }
    });
});


frappe.ui.form.on("Vouchers Review", "barcode", function(frm) {
    frappe.call({ method: "frappe.client.get_value", args: {
        doctype: "Voucher",
        fieldname: ["barcode_no","entity","voucher_type","serial_no","release_date","disabled","reviewed","voucher_review"],
        filters: { 'barcode_no': cur_frm.doc.barcode, }},
        callback: function(r) {
            if (cur_frm.doc.counter == cur_frm.doc.group_count){
                cur_frm.doc.barcode = "";
                cur_frm.refresh_field('barcode');
                frappe.throw("عدد البونات المدخلة تجاوز إجمالي المجموعة");
            }
            if (r.message.barcode_no && r.message.disabled === 0 && r.message.entity && r.message.reviewed === 0) {
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
            if (r.message.disabled == 1) {
                cur_frm.doc.barcode = "";
                cur_frm.refresh_field('barcode');
                frappe.throw(" البون " + r.message.barcode_no + " معطل ");
            }
            if (r.message.reviewed == 1) {
                cur_frm.doc.barcode = "";
                cur_frm.refresh_field('barcode');
                frappe.throw(" البون " + r.message.barcode_no + " تم مراجعته من قبل في المستند رقم " + r.message.voucher_review);
            }
            if (!r.message.barcode_no) {
                var y = cur_frm.doc.barcode;
                cur_frm.doc.barcode = "";
                cur_frm.refresh_field('barcode');
                frappe.throw(":لا يوجد بون بهذا الباركود " + y);
            }
            if (!r.message.entity) {
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


