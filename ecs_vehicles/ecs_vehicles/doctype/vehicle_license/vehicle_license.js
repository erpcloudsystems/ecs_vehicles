// Copyright (c) 2022, erpcloud.systems and contributors
// For license information, please see license.txt


///// Vehicle 1 /////
frappe.ui.form.on('Vehicle License',"vehicle", function(frm) {
var license_duration = 0
license_duration = 365 * cur_frm.doc.license_duration;
cur_frm.set_value("to_date", frappe.datetime.add_days(frm.doc.from_date, license_duration));
});

frappe.ui.form.on('Vehicle License',"license_duration", function(frm) {
var license_duration = 0
license_duration = 365 * cur_frm.doc.license_duration;
cur_frm.set_value("to_date", frappe.datetime.add_days(frm.doc.from_date, license_duration));
});

frappe.ui.form.on('Vehicle License', 'vehicle', function(frm) {
    frappe.call({ method: "frappe.client.get_value",
        args: {
            doctype: "Vehicles",
            fieldname: "license_no",
            filters: {'name': cur_frm.doc.vehicle},
        },
        callback: function(r){
            if (r.message.license_no) {
                cur_frm.set_value("issue_status", "تجديد");
            }
            else {
                cur_frm.set_value("issue_status", "ترخيص أول مرة");
            }
        }
    });
});

frappe.ui.form.on('Vehicle License', 'vehicle', function(frm) {
    frappe.call({ method: "frappe.client.get_value",
        args: {
            doctype: "Vehicles",
            fieldname: "group_shape",
            filters: {'name': cur_frm.doc.vehicle},
        },
        callback: function(r){
            if (r.message.group_shape == "ليموزين") {
                cur_frm.set_value("license_duration", "3");
            }
            else {
                cur_frm.set_value("license_duration", "1");
            }
        }
    });
});

frappe.ui.form.on('Vehicle License', 'vehicle', function(frm) {
    cur_frm.set_value("vehicle_license_logs", "");
    frappe.model.with_doc("Vehicles", frm.doc.vehicle, function() {
        var tabletransfer= frappe.model.get_doc("Vehicles", frm.doc.vehicle);
        $.each(tabletransfer.vehicle_license_logs, function(d, row){
            d = frm.add_child("vehicle_license_logs");
            d.license_no = row.license_no;
			d.issue_status = row.issue_status;
			d.renewal_type = row.renewal_type;
			d.license_duration = row.license_duration;
			d.license_from_date = row.license_from_date;
			d.license_to_date = row.license_to_date;
			d.license_status = row.license_status;
			d.user = row.user;
            cur_frm.refresh_field("vehicle_license_logs");
        });
    });
});


///// Vehicle 2 /////
frappe.ui.form.on('Vehicle License',"vehicle2", function(frm) {
var license_duration = 0
license_duration = 365 * cur_frm.doc.license_duration2;
cur_frm.set_value("to_date2", frappe.datetime.add_days(frm.doc.from_date2, license_duration));
});

frappe.ui.form.on('Vehicle License',"license_duration2", function(frm) {
var license_duration = 0
license_duration = 365 * cur_frm.doc.license_duration2;
cur_frm.set_value("to_date2", frappe.datetime.add_days(frm.doc.from_date2, license_duration));
});

frappe.ui.form.on('Vehicle License', 'vehicle2', function(frm) {
    frappe.call({ method: "frappe.client.get_value",
        args: {
            doctype: "Vehicles",
            fieldname: "license_no",
            filters: {'name': cur_frm.doc.vehicle2},
        },
        callback: function(r){
            if (r.message.license_no) {
                cur_frm.set_value("issue_status2", "تجديد");
            }
            else {
                cur_frm.set_value("issue_status2", "ترخيص أول مرة");
            }
        }
    });
});

frappe.ui.form.on('Vehicle License', 'vehicle2', function(frm) {
    frappe.call({ method: "frappe.client.get_value",
        args: {
            doctype: "Vehicles",
            fieldname: "group_shape",
            filters: {'name': cur_frm.doc.vehicle2},
        },
        callback: function(r){
            if (r.message.group_shape == "ليموزين") {
                cur_frm.set_value("license_duration2", "3");
            }
            else {
                cur_frm.set_value("license_duration2", "1");
            }
        }
    });
});

frappe.ui.form.on('Vehicle License', 'vehicle2', function(frm) {
    cur_frm.set_value("vehicle_license_logs2", "");
    frappe.model.with_doc("Vehicles", frm.doc.vehicle2, function() {
        var tabletransfer= frappe.model.get_doc("Vehicles", frm.doc.vehicle2);
        $.each(tabletransfer.vehicle_license_logs, function(d, row){
            d = frm.add_child("vehicle_license_logs2");
            d.license_no = row.license_no;
			d.issue_status = row.issue_status;
			d.renewal_type = row.renewal_type;
			d.license_duration = row.license_duration;
			d.license_from_date = row.license_from_date;
			d.license_to_date = row.license_to_date;
			d.license_status = row.license_status;
			d.user = row.user;
            cur_frm.refresh_field("vehicle_license_logs2");
        });
    });
});


///// Vehicle 3 /////
frappe.ui.form.on('Vehicle License',"vehicle3", function(frm) {
var license_duration = 0
license_duration = 365 * cur_frm.doc.license_duration3;
cur_frm.set_value("to_date3", frappe.datetime.add_days(frm.doc.from_date3, license_duration));
});

frappe.ui.form.on('Vehicle License',"license_duration3", function(frm) {
var license_duration = 0
license_duration = 365 * cur_frm.doc.license_duration3;
cur_frm.set_value("to_date3", frappe.datetime.add_days(frm.doc.from_date3, license_duration));
});

frappe.ui.form.on('Vehicle License', 'vehicle3', function(frm) {
    frappe.call({ method: "frappe.client.get_value",
        args: {
            doctype: "Vehicles",
            fieldname: "license_no",
            filters: {'name': cur_frm.doc.vehicle3},
        },
        callback: function(r){
            if (r.message.license_no) {
                cur_frm.set_value("issue_status3", "تجديد");
            }
            else {
                cur_frm.set_value("issue_status3", "ترخيص أول مرة");
            }
        }
    });
});

frappe.ui.form.on('Vehicle License', 'vehicle3', function(frm) {
    frappe.call({ method: "frappe.client.get_value",
        args: {
            doctype: "Vehicles",
            fieldname: "group_shape",
            filters: {'name': cur_frm.doc.vehicle3},
        },
        callback: function(r){
            if (r.message.group_shape == "ليموزين") {
                cur_frm.set_value("license_duration3", "3");
            }
            else {
                cur_frm.set_value("license_duration3", "1");
            }
        }
    });
});

frappe.ui.form.on('Vehicle License', 'vehicle3', function(frm) {
    cur_frm.set_value("vehicle_license_logs3", "");
    frappe.model.with_doc("Vehicles", frm.doc.vehicle3, function() {
        var tabletransfer= frappe.model.get_doc("Vehicles", frm.doc.vehicle3);
        $.each(tabletransfer.vehicle_license_logs, function(d, row){
            d = frm.add_child("vehicle_license_logs3");
            d.license_no = row.license_no;
			d.issue_status = row.issue_status;
			d.renewal_type = row.renewal_type;
			d.license_duration = row.license_duration;
			d.license_from_date = row.license_from_date;
			d.license_to_date = row.license_to_date;
			d.license_status = row.license_status;
			d.user = row.user;
            cur_frm.refresh_field("vehicle_license_logs3");
        });
    });
});


///// Vehicle 4 /////
frappe.ui.form.on('Vehicle License',"vehicle4", function(frm) {
var license_duration = 0
license_duration = 365 * cur_frm.doc.license_duration4;
cur_frm.set_value("to_date4", frappe.datetime.add_days(frm.doc.from_date4, license_duration));
});

frappe.ui.form.on('Vehicle License',"license_duration4", function(frm) {
var license_duration = 0
license_duration = 365 * cur_frm.doc.license_duration4;
cur_frm.set_value("to_date4", frappe.datetime.add_days(frm.doc.from_date4, license_duration));
});

frappe.ui.form.on('Vehicle License', 'vehicle4', function(frm) {
    frappe.call({ method: "frappe.client.get_value",
        args: {
            doctype: "Vehicles",
            fieldname: "license_no",
            filters: {'name': cur_frm.doc.vehicle4},
        },
        callback: function(r){
            if (r.message.license_no) {
                cur_frm.set_value("issue_status4", "تجديد");
            }
            else {
                cur_frm.set_value("issue_status4", "ترخيص أول مرة");
            }
        }
    });
});

frappe.ui.form.on('Vehicle License', 'vehicle4', function(frm) {
    frappe.call({ method: "frappe.client.get_value",
        args: {
            doctype: "Vehicles",
            fieldname: "group_shape",
            filters: {'name': cur_frm.doc.vehicle4},
        },
        callback: function(r){
            if (r.message.group_shape == "ليموزين") {
                cur_frm.set_value("license_duration4", "3");
            }
            else {
                cur_frm.set_value("license_duration4", "1");
            }
        }
    });
});

frappe.ui.form.on('Vehicle License', 'vehicle4', function(frm) {
    cur_frm.set_value("vehicle_license_logs4", "");
    frappe.model.with_doc("Vehicles", frm.doc.vehicle4, function() {
        var tabletransfer= frappe.model.get_doc("Vehicles", frm.doc.vehicle4);
        $.each(tabletransfer.vehicle_license_logs, function(d, row){
            d = frm.add_child("vehicle_license_logs4");
            d.license_no = row.license_no;
			d.issue_status = row.issue_status;
			d.renewal_type = row.renewal_type;
			d.license_duration = row.license_duration;
			d.license_from_date = row.license_from_date;
			d.license_to_date = row.license_to_date;
			d.license_status = row.license_status;
			d.user = row.user;
            cur_frm.refresh_field("vehicle_license_logs4");
        });
    });
});