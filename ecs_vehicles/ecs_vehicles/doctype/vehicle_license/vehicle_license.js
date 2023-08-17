// Copyright (c) 2022, erpcloud.systems and contributors
// For license information, please see license.txt

frappe.ui.form.on("Vehicle License", {
    onload(frm) {
        if (!frm.doc.license_no || !frm.doc.license_no2 || !frm.doc.license_no3 || !frm.doc.license_no4 ){
            frappe.call({
                method: 'ecs_vehicles.ecs_vehicles.doctype.vehicle_license.vehicle_license.get_cards_no',
                freeze: true,
                callback: (r) => {
                    cur_frm.set_value("card_code", r.message.card_code);
                    cur_frm.set_value("card_code2", r.message.card_code);
                    cur_frm.set_value("card_code3", r.message.card_code);
                    cur_frm.set_value("card_code4", r.message.card_code);
                    cur_frm.set_value("license_no", r.message.card_no);
                    cur_frm.set_value("license_no2", r.message.card_no2);
                    cur_frm.set_value("license_no3", r.message.card_no3);
                    cur_frm.set_value("license_no4", r.message.card_no4);
                    frm.refresh()
    
                },
                error: (r) => {
                    console.log(r)
                }
            })
        }
       
    },

})
///// Vehicle 1 /////
frappe.ui.form.on('Vehicle License',"vehicle", function(frm) {
var license_duration = 0
license_duration = 365 * cur_frm.doc.license_duration +1;
cur_frm.set_value("to_date", frappe.datetime.add_days(frm.doc.from_date, license_duration));
if (frm.doc.validation) {
    license_duration = 30
    cur_frm.set_value("to_date", frappe.datetime.add_days(frm.doc.from_date, 30));
    // cur_frm.set_value("license_duration", "0");

    } else {
    license_duration = 365 * cur_frm.doc.license_duration +1;
    cur_frm.set_value("to_date", frappe.datetime.add_days(frm.doc.from_date, license_duration));
    frappe.call({ method: "frappe.client.get_value",
        args: {
            doctype: "Vehicles",
            fieldname: "group_shape",
            filters: {'name': cur_frm.doc.vehicle},
        },
        callback: function(r){
            if (r.message.group_shape == "ليموزين" || r.message.group_shape == "موتوسيكل" ) {
                cur_frm.set_value("license_duration", "3");
            }
            else {
                cur_frm.set_value("license_duration", "1");
            }
        }
    });
    }
});
frappe.ui.form.on('Vehicle License',"validation", function(frm) {
    var license_duration = 0

    if (frm.doc.validation) {
    license_duration = 30
    cur_frm.set_value("to_date", frappe.datetime.add_days(frm.doc.from_date, 30));
    // cur_frm.set_value("license_duration", "0");

    } else {
    license_duration = 365 * cur_frm.doc.license_duration +1;
    cur_frm.set_value("to_date", frappe.datetime.add_days(frm.doc.from_date, license_duration));
    frappe.call({ method: "frappe.client.get_value",
        args: {
            doctype: "Vehicles",
            fieldname: "group_shape",
            filters: {'name': cur_frm.doc.vehicle},
        },
        callback: function(r){
            if (r.message.group_shape == "ليموزين" || r.message.group_shape == "موتوسيكل" ) {
                cur_frm.set_value("license_duration", "3");
            }
            else {
                cur_frm.set_value("license_duration", "1");
            }
        }
    });
    }
    frm.refresh()
    });
frappe.ui.form.on('Vehicle License',"license_duration", function(frm) {
var license_duration = 0
license_duration = 365 * cur_frm.doc.license_duration +1;
cur_frm.set_value("to_date", frappe.datetime.add_days(frm.doc.from_date, license_duration));
});

frappe.ui.form.on('Vehicle License', 'vehicle', function(frm) {
    frappe.call({ 
        method: "frappe.client.get_value",
        args: {
            doctype: "Vehicle License Entries",
            fieldname: "license_state",
            filters: {'police_no': cur_frm.doc.police_no,
                        "is_current":"1"},
        },
        callback: function(r){
            console.log(r)

            if (r.message.license_state == "سارية" || r.message.license_state== "منتهية") {
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
            if (r.message.group_shape == "ليموزين" || r.message.group_shape == "موتوسيكل" ) {
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
    cur_frm.set_value("last_end_date", "");

    // call with all options
        frappe.call({
    method: 'ecs_vehicles.ecs_vehicles.doctype.vehicle_license.vehicle_license.history_vehicle1',
    args: {
        police_no: frm.doc.police_no
    },

    freeze: true,
    
    callback: (r) => {
        if(r.message){
            r.message.forEach((row, idx, array)=>{
                let vehicle_license_logs1 = frm.add_child("vehicle_license_logs");
                vehicle_license_logs1.license_no = row.license_no;
                vehicle_license_logs1.vehicle = row.vehicle;
                vehicle_license_logs1.note = frm.doc.vehicle != row.vehicle ? "<span style='color:red;'>رخصة على مركبة مختلفة</span>":"<span style='color:green;'>رخصة على نفس المركبة</span>";
                vehicle_license_logs1.issue_status = row.issue_status;
                vehicle_license_logs1.renewal_type = row.renewal_type;
                vehicle_license_logs1.license_duration = row.license_duration;
                vehicle_license_logs1.license_from_date = row.from_date;
                vehicle_license_logs1.license_to_date = row.to_date;
                vehicle_license_logs1.license_status = row.license_status;
                vehicle_license_logs1.entity = row.entity;
                vehicle_license_logs1.user = row.user;
                cur_frm.refresh_field("vehicle_license_logs");
            })

    cur_frm.set_value("last_end_date",  r.message[r.message.length -1].to_date.toString().toString());
    cur_frm.refresh_field("last_end_date");


        }
    },

})
 
});





///// Vehicle 2 /////
frappe.ui.form.on('Vehicle License',"vehicle2", function(frm) {
var license_duration = 0
license_duration = 365 * cur_frm.doc.license_duration2+1;
cur_frm.set_value("to_date2", frappe.datetime.add_days(frm.doc.from_date2, license_duration));
if (frm.doc.validation2) {
    license_duration = 30
    cur_frm.set_value("to_date2", frappe.datetime.add_days(frm.doc.from_date2, 30));
    // cur_frm.set_value("license_duration", "0");

    } else {
    license_duration = 365 * cur_frm.doc.license_duration2 +1;
    cur_frm.set_value("to_date2", frappe.datetime.add_days(frm.doc.from_date2, license_duration));
    frappe.call({ method: "frappe.client.get_value",
        args: {
            doctype: "Vehicles",
            fieldname: "group_shape",
            filters: {'name': cur_frm.doc.vehicle2},
        },
        callback: function(r){
            if (r.message.group_shape == "ليموزين" || r.message.group_shape == "موتوسيكل" ) {
                cur_frm.set_value("license_duration2", "3");
            }
            else {
                cur_frm.set_value("license_duration2", "1");
            }
        }
    });
    }
});
frappe.ui.form.on('Vehicle License',"validation2", function(frm) {
    var license_duration = 0
    if (frm.doc.validation2) {
    license_duration = 30
    cur_frm.set_value("to_date2", frappe.datetime.add_days(frm.doc.from_date2, 30));
    // cur_frm.set_value("license_duration", "0");

    } else {
    license_duration = 365 * cur_frm.doc.license_duration2 +1;
    cur_frm.set_value("to_date2", frappe.datetime.add_days(frm.doc.from_date2, license_duration));
    frappe.call({ method: "frappe.client.get_value",
        args: {
            doctype: "Vehicles",
            fieldname: "group_shape",
            filters: {'name': cur_frm.doc.vehicle2},
        },
        callback: function(r){
            if (r.message.group_shape == "ليموزين" || r.message.group_shape == "موتوسيكل" ) {
                cur_frm.set_value("license_duration2", "3");
            }
            else {
                cur_frm.set_value("license_duration2", "1");
            }
        }
    });
    }
    frm.refresh()
    });
frappe.ui.form.on('Vehicle License',"license_duration2", function(frm) {
var license_duration = 0
license_duration = 365 * cur_frm.doc.license_duration2 +1;
cur_frm.set_value("to_date2", frappe.datetime.add_days(frm.doc.from_date2, license_duration));
});

frappe.ui.form.on('Vehicle License', 'vehicle2', function(frm) {
    frappe.call({ method: "frappe.client.get_value",
    args: {
        doctype: "Vehicle License Entries",
        fieldname: "license_state",
        filters: {'police_no': cur_frm.doc.police_no2,
                    "is_current":"1"},
        },
        callback: function(r){
            console.log(r)

            if (r.message.license_state == "سارية" || r.message.license_state== "منتهية") {
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
            if (r.message.group_shape == "ليموزين" || r.message.group_shape == "موتوسيكل" ) {
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
    cur_frm.set_value("last_end_date2", "");

        // call with all options
        frappe.call({
            method: 'ecs_vehicles.ecs_vehicles.doctype.vehicle_license.vehicle_license.history_vehicle1',
            args: {
                police_no: frm.doc.police_no2
            },
        
            freeze: true,
            callback: (r) => {
                if(r.message){
                    r.message.forEach((row, idx, array)=>{
                        let vehicle_license_logs2 = frm.add_child("vehicle_license_logs2");
                        vehicle_license_logs2.license_no = row.license_no;
                        vehicle_license_logs2.issue_status = row.issue_status;
                        vehicle_license_logs2.vehicle = row.vehicle;
                        vehicle_license_logs2.note = frm.doc.vehicle2 != row.vehicle ? "<span style='color:red;'>رخصة على مركبة مختلفة</span>":"<span style='color:green;'>رخصة على نفس المركبة</span>";
                        vehicle_license_logs2.renewal_type = row.renewal_type;
                        vehicle_license_logs2.license_duration = row.license_duration;
                        vehicle_license_logs2.license_from_date = row.from_date;
                        vehicle_license_logs2.license_to_date = row.to_date;
                        vehicle_license_logs2.license_status = row.license_status;
                        vehicle_license_logs2.entity = row.entity;
                        vehicle_license_logs2.user = row.user;
                        cur_frm.refresh_field("vehicle_license_logs2");
                    })
            cur_frm.set_value("last_end_date2",  r.message[r.message.length -1].to_date.toString());
            cur_frm.refresh_field("last_end_date2");
        
        
                }
            },
        
        })
   
});


///// Vehicle 3 /////
frappe.ui.form.on('Vehicle License',"vehicle3", function(frm) {
var license_duration = 0
license_duration = 365 * cur_frm.doc.license_duration3 +1;
cur_frm.set_value("to_date3", frappe.datetime.add_days(frm.doc.from_date3, license_duration));
if (frm.doc.validation3) {
    license_duration = 30
    cur_frm.set_value("to_date3", frappe.datetime.add_days(frm.doc.from_date3, 30));
    // cur_frm.set_value("license_duration", "0");
    } else {
    license_duration = 365 * cur_frm.doc.license_duration3 +1;
    cur_frm.set_value("to_date3", frappe.datetime.add_days(frm.doc.from_date3, license_duration));
    frappe.call({ method: "frappe.client.get_value",
        args: {
            doctype: "Vehicles",
            fieldname: "group_shape",
            filters: {'name': cur_frm.doc.vehicle3},
        },
        callback: function(r){
            if (r.message.group_shape == "ليموزين" || r.message.group_shape == "موتوسيكل" ) {
                cur_frm.set_value("license_duration3", "3");
            }
            else {
                cur_frm.set_value("license_duration3", "1");
            }
        }
    });
    }
});
frappe.ui.form.on('Vehicle License',"validation3", function(frm) {
    var license_duration = 0
    if (frm.doc.validation3) {
    license_duration = 30
    cur_frm.set_value("to_date3", frappe.datetime.add_days(frm.doc.from_date3, 30));
    // cur_frm.set_value("license_duration", "0");
    } else {
    license_duration = 365 * cur_frm.doc.license_duration3 +1;
    cur_frm.set_value("to_date3", frappe.datetime.add_days(frm.doc.from_date3, license_duration));
    frappe.call({ method: "frappe.client.get_value",
        args: {
            doctype: "Vehicles",
            fieldname: "group_shape",
            filters: {'name': cur_frm.doc.vehicle3},
        },
        callback: function(r){
            if (r.message.group_shape == "ليموزين" || r.message.group_shape == "موتوسيكل" ) {
                cur_frm.set_value("license_duration3", "3");
            }
            else {
                cur_frm.set_value("license_duration3", "1");
            }
        }
    });
    }
    frm.refresh()
    });
frappe.ui.form.on('Vehicle License',"license_duration3", function(frm) {
var license_duration = 0
license_duration = 365 * cur_frm.doc.license_duration3 +1;
cur_frm.set_value("to_date3", frappe.datetime.add_days(frm.doc.from_date3, license_duration));
});

frappe.ui.form.on('Vehicle License', 'vehicle3', function(frm) {
    frappe.call({ method: "frappe.client.get_value",
    args: {
        doctype: "Vehicle License Entries",
        fieldname: "license_state",
        filters: {'police_no': cur_frm.doc.police_no3,
                    "is_current":"1"},
        },
        callback: function(r){
            console.log(r)

            if (r.message.license_state == "سارية" || r.message.license_state== "منتهية") {
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
            if (r.message.group_shape == "ليموزين" || r.message.group_shape == "موتوسيكل" ) {
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
    cur_frm.set_value("last_end_date3", "");

    frappe.call({
        method: 'ecs_vehicles.ecs_vehicles.doctype.vehicle_license.vehicle_license.history_vehicle1',
        args: {
            police_no: frm.doc.police_no3
        },
    
        freeze: true,
        callback: (r) => {
            if(r.message){
                r.message.forEach((row, idx, array)=>{
                    let vehicle_license_logs3 = frm.add_child("vehicle_license_logs3");
                    vehicle_license_logs3.license_no = row.license_no;
                    vehicle_license_logs3.issue_status = row.issue_status;
                    vehicle_license_logs3.vehicle = row.vehicle;
                    vehicle_license_logs3.note = frm.doc.vehicle3 != row.vehicle ? "<span style='color:red;'>رخصة على مركبة مختلفة</span>":"<span style='color:green;'>رخصة على نفس المركبة</span>";
                    vehicle_license_logs3.renewal_type = row.renewal_type;
                    vehicle_license_logs3.license_duration = row.license_duration;
                    vehicle_license_logs3.license_from_date = row.from_date;
                    vehicle_license_logs3.license_to_date = row.to_date;
                    vehicle_license_logs3.license_status = row.license_status;
                    vehicle_license_logs3.entity = row.entity;
                    vehicle_license_logs3.user = row.user;
                    cur_frm.refresh_field("vehicle_license_logs3");
                })
        cur_frm.set_value("last_end_date3",  r.message[r.message.length -1].to_date.toString());
        cur_frm.refresh_field("last_end_date3");
    
    
            }
        },
    
    })
   
});


///// Vehicle 4 /////
frappe.ui.form.on('Vehicle License',"vehicle4", function(frm) {
var license_duration = 0
license_duration = 365 * cur_frm.doc.license_duration4 +1;
cur_frm.set_value("to_date4", frappe.datetime.add_days(frm.doc.from_date4, license_duration));
if (frm.doc.validation4) {
    license_duration = 30
    cur_frm.set_value("to_date4", frappe.datetime.add_days(frm.doc.from_date4, 30));
} else {
    license_duration = 365 * cur_frm.doc.license_duration4 + 1
    cur_frm.set_value("to_date4", frappe.datetime.add_days(frm.doc.from_date4, license_duration));
    frappe.call({ method: "frappe.client.get_value",
        args: {
            doctype: "Vehicles",
            fieldname: "group_shape",
            filters: {'name': cur_frm.doc.vehicle4},
        },
        callback: function(r){
            if (r.message.group_shape == "ليموزين" || r.message.group_shape == "موتوسيكل" ) {
                cur_frm.set_value("license_duration4", "3");
            }
            else {
                cur_frm.set_value("license_duration4", "1");
            }
        }
    });
}
});
frappe.ui.form.on('Vehicle License',"validation4", function(frm) {
    var license_duration = 0
    if (frm.doc.validation4) {
        license_duration = 30
        cur_frm.set_value("to_date4", frappe.datetime.add_days(frm.doc.from_date4, 30));
    } else {
        license_duration = 365 * cur_frm.doc.license_duration4 + 1
        cur_frm.set_value("to_date4", frappe.datetime.add_days(frm.doc.from_date4, license_duration));
        frappe.call({ method: "frappe.client.get_value",
            args: {
                doctype: "Vehicles",
                fieldname: "group_shape",
                filters: {'name': cur_frm.doc.vehicle4},
            },
            callback: function(r){
                if (r.message.group_shape == "ليموزين" || r.message.group_shape == "موتوسيكل" ) {
                    cur_frm.set_value("license_duration4", "3");
                }
                else {
                    cur_frm.set_value("license_duration4", "1");
                }
            }
        });
    }
    frm.refresh()
    });
frappe.ui.form.on('Vehicle License',"license_duration4", function(frm) {
var license_duration = 0
license_duration = 365 * cur_frm.doc.license_duration4 +1; 
cur_frm.set_value("to_date4", frappe.datetime.add_days(frm.doc.from_date4, license_duration));
});

frappe.ui.form.on('Vehicle License', 'vehicle4', function(frm) {
    frappe.call({ method: "frappe.client.get_value",
    args: {
        doctype: "Vehicle License Entries",
        fieldname: "license_state",
        filters: {'police_no': cur_frm.doc.police_no4,
                    "is_current":"1"},
        },
        callback: function(r){
            console.log(r)
            if (r.message.license_state == "سارية" || r.message.license_state== "منتهية") {
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
            if (r.message.group_shape == "ليموزين" || r.message.group_shape == "موتوسيكل" ) {
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
    cur_frm.set_value("last_end_date4", "");
    frappe.call({
        method: 'ecs_vehicles.ecs_vehicles.doctype.vehicle_license.vehicle_license.history_vehicle1',
        args: {
            police_no: frm.doc.police_no4
        },
    
        freeze: true,
        callback: (r) => {
            if(r.message){
                r.message.forEach((row, idx, array)=>{
                    let vehicle_license_logs12 = frm.add_child("vehicle_license_logs4");
                    vehicle_license_logs12.license_no = row.license_no;
                    vehicle_license_logs12.issue_status = row.issue_status;
                    vehicle_license_logs12.vehicle = row.vehicle;
                    vehicle_license_logs12.note = frm.doc.vehicle4 != row.vehicle ? "<span style='color:red;'>رخصة على مركبة مختلفة</span>":"<span style='color:green;'>رخصة على نفس المركبة</span>";
                    vehicle_license_logs12.renewal_type = row.renewal_type;
                    vehicle_license_logs12.license_duration = row.license_duration;
                    vehicle_license_logs12.license_from_date = row.from_date;
                    vehicle_license_logs12.license_to_date = row.to_date;
                    vehicle_license_logs12.license_status = row.license_status;
                    vehicle_license_logs12.entity = row.entity;
                    vehicle_license_logs12.user = row.user;
                    cur_frm.refresh_field("vehicle_license_logs4");
                })
        cur_frm.set_value("last_end_date4",  r.message[r.message.length -1].to_date.toString());
        cur_frm.refresh_field("last_end_date4");
        cur_frm.refresh_field("last_end_date4");
    
    
            }
        },
    
    })

 
});


frappe.ui.form.on("Vehicle License", "card_front", function(frm){
	var myWin = window.open('/printview?doctype=Vehicle%20License&name='+ cur_frm.doc.name +'&trigger_print=1&format=وجه%20أمامي&no_letterhead=1&letterhead=No%20Letterhead&settings=%7B%7D&_lang=ar');	
	
});
frappe.ui.form.on("Vehicle License", "card_back", function(frm){
	var myWin = window.open('/printview?doctype=Vehicle%20License&name='+ cur_frm.doc.name +'&trigger_print=1&format=وجه%20خلفي&no_letterhead=1&letterhead=No%20Letterhead&settings=%7B%7D&_lang=ar');	
	
});