// Copyright (c) 2022, erpcloud.systems and contributors
// For license information, please see license.txt

frappe.ui.form.on("Liquid Vouchers Issuing", "print", function (frm) {
    var myWin = window.open('/printpreview?doctype=Liquid+Vouchers+Issuing&name=' + cur_frm.doc.name + '&trigger_print=1&print_format=Vouchers+Issuing&no_letterhead=1&letterhead=No%20Letterhead&settings=%7B%7D&_lang=ar');
});

frappe.ui.form.on("Liquid Vouchers Issuing", "onload", function (frm) {
    frappe.call({
        doc: frm.doc,
        method: "set_today_date",
        callback: function (r) {
            frm.refresh_field("issue_date");
        }
    });
});

// frappe.ui.form.on('Liquid Vouchers Issuing', {
//     refresh: function (frm) {
//         frm.set_df_property("qty_per_liquid", "cannot_add_rows", true);
//     },
//     // validate: (frm) => {
//     //     frm.doc.qty_per_liquid.forEach((row, idx, array) => {
//     //         if (row.notebook_count === undefined || row.notebook_count <= 0) {
//     //             frm.doc.qty_per_liquid.splice(idx, 1);
//     //         }

//     //     })
//     // }
// });

frappe.ui.form.on('Liquid Vouchers Issuing', {
    setup: function (frm) {
        frm.set_query("liquids_issuing", function () {
            if (frm.doc.type == "صرفية شهرية") {
                return {
                    filters: [
                        ["Liquids Issuing", "entity", "=", frm.doc.entity],
                        ["Liquids Issuing", "submitted", "=", 1],
                        ["Liquids Issuing", "issue_to", "=", "جهة"],
                        ["Liquids Issuing", "issue_type", "=", frm.doc.issue_type]
                    ]
                };
            }
            if (frm.doc.type == "صرفية لمركبات") {
                return {
                    filters: [
                        ["Liquids Issuing", "entity", "=", frm.doc.entity],
                        ["Liquids Issuing", "submitted", "=", 1],
                        ["Liquids Issuing", "issue_to", "=", "مركبة أو مجموعة مركبات"],
                        ["Liquids Issuing", "issue_type", "=", frm.doc.issue_type]
                    ]
                };
            }
        });
    }
});


frappe.ui.form.on("Liquid Vouchers Issuing", "entity", function () {
    cur_frm.doc.liquids_issuing = "";
    cur_frm.doc.from_date = "";
    cur_frm.doc.to_date = "";
    cur_frm.refresh_field('liquids_issuing');
    cur_frm.refresh_field('from_date');
    cur_frm.refresh_field('to_date');
});


frappe.ui.form.on("Liquid Vouchers Issuing", "type", function () {
    cur_frm.doc.entity = "";
    cur_frm.doc.liquids_issuing = "";
    cur_frm.doc.from_date = "";
    cur_frm.doc.to_date = "";
    cur_frm.refresh_field('entity');
    cur_frm.refresh_field('liquids_issuing');
    cur_frm.refresh_field('from_date');
    cur_frm.refresh_field('to_date');
});


frappe.ui.form.on("Liquid Vouchers Issuing", "liquids_issuing", function (frm) {
    if (frm.doc.liquids_issuing && frm.doc.type == "صرفية شهرية") {
        frappe.model.with_doc("Liquids Issuing", frm.doc.liquids_issuing, function () {
            var tabletransfer = frappe.model.get_doc("Liquids Issuing", frm.doc.liquids_issuing);
            cur_frm.clear_table("qty_per_liquid");
            $.each(tabletransfer.qty_per_liquid, function (d, row) {
                if (row.qty > 0) {
                    d = frm.add_child("qty_per_liquid");
                    d.liquid = row.liquid;
                    d.vehicles_count = row.vehicles_count;
                    d.qty = row.qty;
                    d.in_words = row.in_words;
                    d.notebook_count = 0;
                    d.voucher_qty = 0;
                    cur_frm.refresh_field("qty_per_liquid");
                }
            });
        });
    }
});

frappe.ui.form.on("Liquid Vouchers Issuing", "liquids_issuing", function (frm) {
    if (frm.doc.liquids_issuing && frm.doc.type == "صرفية لمركبات") {
        frappe.model.with_doc("Liquids Issuing", frm.doc.liquids_issuing, function () {
            var tabletransfer = frappe.model.get_doc("Liquids Issuing", frm.doc.liquids_issuing);
            cur_frm.clear_table("qty_per_liquid");
            $.each(tabletransfer.qty_per_liquid, function (d, row) {
                if (row.qty > 0) {
                    d = frm.add_child("qty_per_liquid");
                    d.liquid = row.liquid;
                    d.vehicles_count = row.vehicles_count;
                    d.qty = row.qty;
                    d.in_words = row.in_words;
                    d.notebook_count = 0;
                    d.voucher_qty = 0;
                    cur_frm.refresh_field("qty_per_liquid");
                }
            });
        });
    }
});


frappe.ui.form.on("Vouchers Issued Per Liquid", "notebook_count", function (frm, cdt, cdn) {
    function frappe_call(doctype_name, filters, fieldnames) {
        let status = 0
        frappe.call({
            method: 'frappe.client.get_value',
            args: {
                'doctype': doctype_name,
                'filters': filters,
                'fieldname': fieldnames,
            },

            callback: function (r) {
                if (r.message) {

                    let item = locals[cdt][cdn];
                    if (fieldnames.pop() === "gas_count") {
                        r.message["litre_count"] = r.message.gas_count
                    }
                    item.voucher_qty = (item.notebook_count * 25) * r.message.litre_count
                    frm.refresh_field('qty_per_liquid');
                    status = 1


                }
            }
        });
        return status
    }
    let item = locals[cdt][cdn];
    let liquid_types = ["بنزين 80", "بنزين 92", "بنزين 95", "سولار", "غاز طبيعي"]

    if (!(liquid_types.includes(item.liquid))) {
        item.voucher_qty = item.notebook_count * 25
        frm.refresh_field('qty_per_liquid');
    }
    else if (liquid_types.slice(0, -1).includes(item.liquid)) {
        let filters = { "fuel_type": item.liquid }
        let doctype_name = "Fuel Voucher"
        let fieldnames = [
            'name',
            "litre_count",
        ]

        frappe_call(doctype_name, filters, fieldnames)
    }
    else if (liquid_types.pop().includes(item.liquid)) {
        let filters = { "gas_name": item.liquid }
        let doctype_name = "Gas Voucher"
        let fieldnames = [
            'name',
            "gas_count",
        ]
        frappe_call(doctype_name, filters, fieldnames)

    }
});





frappe.ui.form.on("Vouchers Issued Per Liquid", "voucher_qty", function (frm, cdt, cdn) {
    function frappe_call(doctype_name, filters, fieldnames) {
        let status = 0
        console.log("iam here")
        frappe.call({
            method: 'frappe.client.get_value',
            args: {
                'doctype': doctype_name,
                'filters': filters,
                'fieldname': fieldnames,
            },

            callback: function (r) {
                console.log(r)
                if (r.message) {
                    console.log(r.message)

                    let item = locals[cdt][cdn];
                    if (fieldnames.pop() === "gas_count") {
                        r.message["litre_count"] = r.message.gas_count
                    }
                    console.log(r.message.litre_count)
                    item.notebook_count = (item.voucher_qty / 25) / r.message.litre_count
                    frm.refresh_field('qty_per_liquid');
                    status = 1


                }
            }
        });
        return status
    }
    let item = locals[cdt][cdn];
    let liquid_types = ["بنزين 80", "بنزين 92", "بنزين 95", "سولار", "غاز طبيعي"]

    if (!(liquid_types.includes(item.liquid))) {
        item.notebook_count = item.voucher_qty / 25
        frm.refresh_field('qty_per_liquid');
    }
    else if (liquid_types.slice(0, -1).includes(item.liquid)) {
        let filters = { "fuel_type": item.liquid }
        let doctype_name = "Fuel Voucher"
        let fieldnames = [
            'name',
            "litre_count",
        ]

        frappe_call(doctype_name, filters, fieldnames)
    }
    else if (liquid_types.pop().includes(item.liquid)) {
        let filters = { "gas_name": item.liquid }
        let doctype_name = "Gas Voucher"
        let fieldnames = [
            'name',
            "gas_count",
        ]
        frappe_call(doctype_name, filters, fieldnames)

    }
});


