frappe.ui.form.on("Liquids Issuing", {
    refresh: function (frm, cdt, cdn) {
        if (frm.doc.issue_state == 'جاري تحضير الصرفية ومراجعتها') {
            frm.add_custom_button(__("جاري تجهيــــز الصرفيـــة ومراجعتهــــا")).addClass("btn-primary").css({ 'color': 'white', 'font-weight': 'bold' });
        }
        if (frm.doc.issue_state == 'تم صرف البونات من خزينة السوائل') {
            frm.add_custom_button(__("تم صرف البونـــات من خزينــــة السوائــــل")).addClass("btn-danger").css({ 'color': 'white', 'font-weight': 'bold' });
        }
        if (!frm.doc.__islocal) {
            frm.add_custom_button(__("تحضيــــر صرفيـــــة جديــــدة"), function () {
                frappe.new_doc("Liquids Issuing");
            },);
        }
    }
});

frappe.ui.form.on("Liquids Issuing", "print", function (frm) {
    var myWin = window.open('/printview?doctype=Liquids%20Issuing&name=' + cur_frm.doc.name + '&trigger_print=1&format=%D9%86%D9%85%D9%88%D8%B0%D8%AC%20%D8%B5%D8%B1%D9%81%20%D8%A7%D9%84%D8%B3%D9%88%D8%A7%D8%A6%D9%84&no_letterhead=1&letterhead=No%20Letterhead&settings=%7B%7D&_lang=ar');
});

frappe.ui.form.on("Liquids Issuing", "print_vehicles_entity", function (frm) {
    if (frm.doc.issue_type == 'وقود') {
        var myWin = window.open('/printview?doctype=Liquids%20Issuing&name=' + cur_frm.doc.name + '&trigger_print=1&format=Vehicles%20Entity%20Print&no_letterhead=1&letterhead=No%20Letterhead&settings=%7B%7D&_lang=ar');
    } else {
        var myWin = window.open('/printview?doctype=Liquids%20Issuing&name=' + cur_frm.doc.name + '&trigger_print=1&format=Vehicles%20Entity%20Print%20Oil&no_letterhead=1&letterhead=No%20Letterhead&settings=%7B%7D&_lang=ar');
    }
});
frappe.ui.form.on("Liquids Issuing", "veh_no", function (frm) {
    var myWin = window.open('/query-report/Vehicle%20Liquid%20History?name=' + cur_frm.doc.veh_no + '&issue_type=وقود');

});

frappe.ui.form.on("Liquids Issuing", "print_broken_vehicles", function (frm) {
    var myWin = window.open('/printview?doctype=Liquids%20Issuing&name=' + cur_frm.doc.name + '&trigger_print=1&format=Invalid%20Vehicles%20Entity&no_letterhead=1&letterhead=No%20Letterhead&settings=%7B%7D&_lang=ar');
});

frappe.ui.form.on("Liquids Issuing", "print_valid_vehicles", function (frm) {
    var myWin = window.open('/printview?doctype=Liquids%20Issuing&name=' + cur_frm.doc.name + '&trigger_print=1&format=Valid%20Vehicles%20Entity&no_letterhead=1&letterhead=No%20Letterhead&settings=%7B%7D&_lang=ar');
});

frappe.ui.form.on("Liquids Issuing", "print_vehicles_entity_changes", function (frm) {
    if (frm.doc.compare_with_date) {
        var myWin = window.open('/printview?doctype=Liquids%20Issuing&name=' + cur_frm.doc.name + '&trigger_print=1&format=Liquids%20Issuing%20Changes&no_letterhead=1&letterhead=No%20Letterhead&settings=%7B%7D&_lang=ar');

    } else {
        frappe.msgprint("برجاء إدخال تاريخ مقارنة الصرفية")
    }
});

frappe.ui.form.on("Liquids Issuing", "onload", function (frm) {

    frappe.call({
        doc: frm.doc,
        method: "set_today_date",
        callback: function (r) {
            frm.refresh_field("issue_date");
        }
    });


    if (frm.doc.issue_to == "جهة" && frm.doc.issue_type == "وقود") {
        cur_frm.set_value("from_date", frappe.datetime.add_months(start_day, 1));
        cur_frm.set_value("to_date", frappe.datetime.add_months(last_day, 1));
    }

});

frappe.ui.form.on("Liquids Issuing", "issue_to", function (frm) {
    if (cur_frm.doc.issue_to == "مركبة أو مجموعة مركبات") {
        cur_frm.set_value("from_date", frappe.datetime.get_today());
    }
    if (cur_frm.doc.issue_to == "جهة" && cur_frm.doc.issue_type == "وقود") {
        const start_day = frappe.datetime.month_start();
        const last_day = frappe.datetime.month_end();
        cur_frm.set_value("from_date", frappe.datetime.add_months(start_day, 1));
        cur_frm.set_value("to_date", frappe.datetime.add_months(last_day, frm.doc.month_count));
    }
});

frappe.ui.form.on("Liquids Issuing", "month_count", function (frm) {
    const start_day = frappe.datetime.month_start();
    const last_day = frappe.datetime.month_end();
    if (cur_frm.doc.issue_to == "جهة" && cur_frm.doc.issue_type == "وقود") {
        cur_frm.set_value("from_date", frappe.datetime.add_months(start_day, 1));
        cur_frm.set_value("to_date", frappe.datetime.add_months(last_day, frm.doc.month_count));
    }
});

frappe.ui.form.on("Liquids Issuing", "from_date", function (frm) {
    const start_day = frappe.datetime.month_start();
    const last_day = frappe.datetime.month_end();
    if (cur_frm.doc.issue_to == "جهة" && cur_frm.doc.edit_from_date == 0 && cur_frm.doc.issue_type == "وقود") {
        cur_frm.set_value("from_date", frappe.datetime.add_months(start_day, 1));
        cur_frm.set_value("to_date", frappe.datetime.add_months(last_day, frm.doc.month_count));
    }
});

frappe.ui.form.on("Liquids Issuing", "month_count", function (frm) {
    if (cur_frm.doc.issue_to == "مركبة أو مجموعة مركبات" && cur_frm.doc.issue_type == "وقود") {
        const added_months = frappe.datetime.add_months(frm.doc.from_date, frm.doc.month_count - 1)
        const f_day = new Date(added_months.split("-")[0], added_months.split("-")[1], 0)
        cur_frm.set_value("to_date", f_day.getFullYear() + "-" + (f_day.getMonth() + 1) + "-" + f_day.getDate());
    }
});

frappe.ui.form.on("Liquids Issuing", "from_date", function (frm) {
    //    if (cur_frm.doc.issue_to == "مركبة أو مجموعة مركبات"){
    const added_months = frappe.datetime.add_months(frm.doc.from_date, frm.doc.month_count - 1)
    const f_day = new Date(added_months.split("-")[0], added_months.split("-")[1], 0)
    cur_frm.set_value("to_date", f_day.getFullYear() + "-" + (f_day.getMonth() + 1) + "-" + f_day.getDate());
    //    }
});


frappe.ui.form.on("Liquids Issuing", "from_date", function (frm) {
    cur_frm.set_value("issue_days", frappe.datetime.get_day_diff(cur_frm.doc.to_date, cur_frm.doc.from_date));
});

frappe.ui.form.on("Liquids Issuing", "to_date", function (frm) {
    cur_frm.set_value("issue_days", frappe.datetime.get_day_diff(cur_frm.doc.to_date, cur_frm.doc.from_date));
});

frappe.ui.form.on("Liquids Issuing", "validate", function (frm) {
    cur_frm.set_value("issue_days", frappe.datetime.get_day_diff(cur_frm.doc.to_date, cur_frm.doc.from_date));
});

frappe.ui.form.on('Liquids Issuing', {
    setup: function (frm) {
        cur_frm.fields_dict['specified_vehicles_issuing_table'].grid.get_field("vehicle").get_query = function (doc, cdt, cdn) {
            const added_vehicles = frm.doc.specified_vehicles_issuing_table.map((r) => r.vehicle);
            return {
                filters: [
                    ["Vehicles", "entity_name", "=", frm.doc.entity],
                    ["Vehicles", "vehicle_status", "=", "صالحة"],
                    ["name", "not in", added_vehicles],
                ]
            };
        };
    },
    issue_date: function (frm) {
        const issue_date = frappe.datetime.add_months(frm.doc.issue_date, 1);
        function padTo2Digits(num) {

            return num.toString().padStart(2, '0');
        }

        function formatDate(date) {
            return [
                date.getFullYear(),
                padTo2Digits(date.getMonth()),
                padTo2Digits(date.getDate()),
            ].join('-');
        }
        if ((frm.doc.issue_to == "جهة" && cur_frm.doc.issue_type == "وقود")) {
            let date = new Date(issue_date)
            console.log(issue_date)
            // first day of next month
            let firstDay = new Date(date.getFullYear(), date.getMonth() + frm.doc.month_count, 1);
            // last day of next month
            let lastDay = new Date(date.getFullYear(), date.getMonth() + frm.doc.month_count + 1, 0);
            frm.set_value("from_date", formatDate(firstDay));
            frm.set_value("to_date", formatDate(lastDay));
            frm.refresh_fields();
        } else if (cur_frm.doc.issue_type === "زيت") {
            const start_day = frappe.datetime.month_start();
            const last_day = frappe.datetime.month_end();
            cur_frm.set_value("month_count", 2);
            cur_frm.set_value("from_date", frappe.datetime.add_months(start_day, 0));
            cur_frm.set_value("to_date", frappe.datetime.add_months(last_day, frm.doc.month_count - 1));
            frm.refresh_fields();

        } else if (cur_frm.doc.issue_type === "غسيل") {
            const start_day = frappe.datetime.month_start();
            const last_day = frappe.datetime.month_end();
            cur_frm.set_value("month_count", 3);
            cur_frm.set_value("from_date", frappe.datetime.add_months(start_day, 0));
            cur_frm.set_value("to_date", frappe.datetime.add_months(last_day, frm.doc.month_count - 1));
            frm.refresh_fields();
        }
    }


});

frappe.ui.form.on("Liquids Issuing", 'refresh', function (frm) {
    frm.set_df_property("specified_vehicles_issuing_table", "cannot_add_rows", true);
    const start_day = frappe.datetime.month_start();
    const last_day = frappe.datetime.month_end();
    // cur_frm.set_value("compare_with_date", frappe.datetime.add_months(start_day, -1));
});

frappe.ui.form.on('Liquids Issuing', {
    refresh: function (frm) {
        frm.set_df_property("vehicles_issuing_table", "cannot_add_rows", true);
        frm.set_df_property("vehicles_issuing_table", "cannot_delete_rows", true);
    },
    entity: function (frm) {
        if (frm.doc.entity) {

            frappe.call({
                doc: frm.doc,
                method: "get_total_vehicles",
                freeze: 0,
                callback: function (r) {
                    if (r.message) {
                        frm.set_value("total_vehicles_count_main", r.message[0].toString());
                        frm.set_value("valid_vehicles_count_main", r.message[1].toString());
                        frm.set_value("invalid_vehicles_count_main", r.message[2].toString());
                        frm.set_value("plates_only_count_main", r.message[3].toString());
                    }
                    frm.scroll_to_field('contact_person');

                    frm.refresh_fields();
                    frm.refresh();
                }
            });

        }

    },
    refresh_entity: function (frm) {
        if (frm.doc.entity) {
            frappe.call({
                doc: frm.doc,
                method: "get_total_vehicles",
                freeze: 0,
                callback: function (r) {
                    if (r.message) {
                        frm.set_value("total_vehicles_count_main", r.message[0].toString());
                        frm.set_value("valid_vehicles_count_main", r.message[1].toString());
                        frm.set_value("invalid_vehicles_count_main", r.message[2].toString());
                        frm.set_value("plates_only_count_main", r.message[3].toString());
                    }

                    frm.refresh_fields();
                    frm.refresh();
                }
            });

        }

    },
    issue_type: function (frm) {
        if (frm.doc.entity) {

            frappe.call({
                doc: frm.doc,
                method: "get_total_vehicles",
                freeze: 0,
                callback: function (r) {
                    if (r.message) {
                        frm.set_value("total_vehicles_count_main", r.message[0].toString());
                        frm.set_value("valid_vehicles_count_main", r.message[1].toString());
                        frm.set_value("invalid_vehicles_count_main", r.message[2].toString());
                        frm.set_value("plates_only_count_main", r.message[3].toString());
                    }

                    frm.refresh_fields();
                    frm.refresh();
                }
            });

        }

    },
    refresh: function (frm) {
        if (!(frm.doc.__islocal)) {
            frm.disable_save();
        }

    },
    post_liquid_issuing: function (frm) {
        frappe.call({
            doc: frm.doc,
            method: "post_liquid_issuing",
            freeze: 1,
            freeze_message: (' جاري ترحيل الصرفية ... برجاء الإنتظار '),
            callback: function (r) {
                frm.refresh_field("submitted");
                frm.refresh_fields();
                frm.refresh()
            }
        });
    },
    empty_pages: function (frm) {
        frappe.call({
            doc: frm.doc,
            method: "get_empty_pages",
            callback: function (r) {
                frm.refresh_field("empty_pages");
                frm.refresh_fields();
                frm.refresh()
            }
        });
    },
    fuel_type: function (frm) {
        frappe.call({
            doc: frm.doc,
            method: "get_fuel_type",
            callback: function (r) {
                frm.refresh_field("fuel_type");
                frm.refresh_fields();
                frm.refresh()
            }
        });
    },
    cylinder_count: function (frm) {
        frappe.call({
            doc: frm.doc,
            method: "get_cylinder_count",
            callback: function (r) {
                frm.refresh_field("cylinder_count");
                frm.refresh_fields();
                frm.refresh()
            }
        });
    },
    litre_count: function (frm) {
        frappe.call({
            doc: frm.doc,
            method: "get_litre_count",
            callback: function (r) {
                frm.refresh_field("litre_count");
                frm.refresh_fields();
                frm.refresh()
            }
        });
    },
    compare_with_date: function (frm) {

        frappe.call({
            doc: frm.doc,
            method: "get_compare_with_date",
            callback: function (r) {
                frm.refresh_field("compare_with_date");
                frm.refresh_fields();
                frm.refresh()
            }
        });

    },
});


frappe.ui.form.on("Liquids Issuing", "get_vehicle_data", function (frm, cdt, cdn) {
    if (frm.doc.vehicle_no) {
        frappe.call({
            doc: frm.doc,
            method: "get_searched_vehicles",
            freeze: 1,
            callback: function (r) {
                frm.set_value("vehicle_no", "");
                cur_frm.refresh_fields();
                frm.scroll_to_field('vehicle_no');
            }
        });
        frm.refresh_fields();
    }
});

frappe.ui.form.on("Liquids Issuing", "issue_type", function (frm) {
    const start_dayyy = frappe.datetime.month_start();
    const last_dayyy = frappe.datetime.month_end();

    if (cur_frm.doc.issue_to == "جهة" && frm.doc.issue_type == "زيت") {
        cur_frm.set_value("month_count", 2);
        cur_frm.set_value("from_date", frappe.datetime.add_months(start_dayyy, 0));
        cur_frm.set_value("to_date", frappe.datetime.add_months(last_dayyy, frm.doc.month_count - 1));

    } else if (frm.doc.issue_type == "وقود") {
        cur_frm.set_value("month_count", 1);
        cur_frm.set_value("from_date", frappe.datetime.add_months(start_dayyy, 0));
        cur_frm.set_value("to_date", frappe.datetime.add_months(last_dayyy, frm.doc.month_count));
    } else if (frm.doc.issue_type == "غسيل") {

        cur_frm.set_value("month_count", 3);
        cur_frm.set_value("from_date", frappe.datetime.add_months(start_dayyy, 0));
        cur_frm.set_value("to_date", frappe.datetime.add_months(last_dayyy, frm.doc.month_count - 1));
    }
});