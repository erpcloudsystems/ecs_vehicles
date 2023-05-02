// Copyright (c) 2022, ERP CLOUD SYSTEMS and contributors
// For license information, please see license.txt

frappe.ui.form.on("Liquids Issuing", "onload", function(frm) {
    const start_day = frappe.datetime.month_start();
    const last_day = frappe.datetime.month_end();
    if ((cur_frm.doc.month_count == 1) && (cur_frm.doc.issue_to == "جهة") && (!cur_frm.doc.from_date) && (!cur_frm.doc.to_date)){
        cur_frm.set_value("from_date", frappe.datetime.add_months(start_day, 1));
        cur_frm.set_value("to_date", frappe.datetime.add_months(last_day, 1));
    }
});

frappe.ui.form.on("Liquids Issuing", "issue_to", function(frm) {
    if (cur_frm.doc.issue_to == "مركبة أو مجموعة مركبات"){
        cur_frm.set_value("from_date", frappe.datetime.get_today());
    }
    if (cur_frm.doc.issue_to == "جهة"){
        const start_day = frappe.datetime.month_start();
        const last_day = frappe.datetime.month_end();
        cur_frm.set_value("from_date", frappe.datetime.add_months(start_day, 1));
        cur_frm.set_value("to_date", frappe.datetime.add_months(last_day, frm.doc.month_count));
    }
});

frappe.ui.form.on("Liquids Issuing", "month_count", function(frm) {
    const start_day = frappe.datetime.month_start();
    const last_day = frappe.datetime.month_end();
    if (cur_frm.doc.issue_to == "جهة"){
        cur_frm.set_value("from_date", frappe.datetime.add_months(start_day, 1));
        cur_frm.set_value("to_date", frappe.datetime.add_months(last_day, frm.doc.month_count));
    }
});

frappe.ui.form.on("Liquids Issuing", "from_date", function(frm) {
    const start_day = frappe.datetime.month_start();
    const last_day = frappe.datetime.month_end();
    if (cur_frm.doc.issue_to == "جهة" && cur_frm.doc.edit_from_date == 0){
        cur_frm.set_value("from_date", frappe.datetime.add_months(start_day, 1));
        cur_frm.set_value("to_date", frappe.datetime.add_months(last_day, frm.doc.month_count));
    }
});

frappe.ui.form.on("Liquids Issuing", "month_count", function(frm) {
    if (cur_frm.doc.issue_to == "مركبة أو مجموعة مركبات"){
        const added_months = frappe.datetime.add_months(frm.doc.from_date, frm.doc.month_count - 1)
        const f_day = new Date(added_months.split("-")[0],added_months.split("-")[1],0)
        cur_frm.set_value("to_date", f_day.getFullYear() + "-" + (f_day.getMonth() + 1) + "-" + f_day.getDate());
    }
});

frappe.ui.form.on("Liquids Issuing", "from_date", function(frm) {
//    if (cur_frm.doc.issue_to == "مركبة أو مجموعة مركبات"){
        const added_months = frappe.datetime.add_months(frm.doc.from_date, frm.doc.month_count - 1)
        const f_day = new Date(added_months.split("-")[0],added_months.split("-")[1],0)
        cur_frm.set_value("to_date", f_day.getFullYear() + "-" + (f_day.getMonth() + 1) + "-" + f_day.getDate());
//    }
});


frappe.ui.form.on("Liquids Issuing", "from_date", function(frm) {
    cur_frm.set_value("issue_days", frappe.datetime.get_day_diff(cur_frm.doc.to_date , cur_frm.doc.from_date));
});

frappe.ui.form.on("Liquids Issuing", "to_date", function(frm) {
    cur_frm.set_value("issue_days", frappe.datetime.get_day_diff(cur_frm.doc.to_date , cur_frm.doc.from_date));
});

frappe.ui.form.on("Liquids Issuing", "validate", function(frm) {
    cur_frm.set_value("issue_days", frappe.datetime.get_day_diff(cur_frm.doc.to_date , cur_frm.doc.from_date));
});

frappe.ui.form.on('Liquids Issuing',{
    setup: function(frm) {
        cur_frm.fields_dict['specified_vehicles_issuing_table'].grid.get_field("vehicle").get_query = function(doc, cdt, cdn){
            const added_vehicles = frm.doc.specified_vehicles_issuing_table.map((r) => r.vehicle);
            return {
                filters:[
                    ["Vehicles","entity_name", "=", frm.doc.entity],
                    ["Vehicles","vehicle_status", "=", "صالحة"],
                    ["name", "not in", added_vehicles],
                ]
            };
        };
    }
});

frappe.ui.form.on('Liquids Issuing', {
    refresh:function(frm){
        frm.set_df_property("vehicles_issuing_table", "cannot_add_rows", true);
        frm.set_df_property("vehicles_issuing_table", "cannot_delete_rows", true);
    }
 });

// frappe.ui.form.on("Liquids Issuing", "validate", function(frm) {
//     frappe.show_progress('جاري تجهيز الصرفية..', '70 %', '100 %', 'برجاء الإنتظار يا حاج سعيد');
// });