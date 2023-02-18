//
set_rtl: function () {
    if (["ar", "he", "fa"].indexOf(frappe.boot.lang) >= 0) {
    var ls = document.createElement('link');
    ls.rel="stylesheet";
    ls.href= "assets/css/frappe-rtl.css";
    document.getElementsByTagName('head')[0].appendChild(ls);
    $('body').addClass('frappe-rtl')
    $("*").css('fontFamily', "B Baran");
    }
    }