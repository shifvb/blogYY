document.addEventListener("DOMContentLoaded", function() {
    // 使用quill解释文章内容
    document.querySelectorAll(".article_content").forEach(function(x) {
        new Quill(x).setContents(JSON.parse(x.dataset.raw));
        x.removeAttribute("data-raw");
    });

    // 处理翻页按钮
    var total_page = Number(document.querySelector(".page_control").dataset.totalPage);
    // 处理可能出现的url参数
    var _arr = [];
    var current_page = 1; // 如果没有出现url参数，那么默认为第1页
    if (location.href.indexOf("?") >= 0) {
        var _params = location.href.split("?")[1].split("&");
        for (var i = 0; i < _params.length; ++i) {
            // 记录page_num参数的值至current_page，其余加入数组_arr
            if (_params[i].indexOf("page_num=") != -1) {
                var current_page = Number(_params[i].split("=")[1]);
            } else {
                _arr.push(_params[i]);
            }
        }
    }
    // 处理page_num参数
    _arr.push("page_num=")
    // 合成page_link变量
    var page_link = location.pathname + "?" + _arr.join("&");

    // 设置上一页按钮
    if (current_page >= 2) {
        var _prev_btn = document.querySelector(".prev_page > a");
        _prev_btn.setAttribute("href", page_link + String(current_page - 1))
        _prev_btn.classList.remove("page_link_disabled");
    }
    // 设置下一页按钮
    if (current_page < total_page) {
        var _next_btn = document.querySelector(".next_page > a");
        _next_btn.setAttribute("href", page_link + String(current_page + 1))
        _next_btn.classList.remove("page_link_disabled");
    }
    // 设置临近页按钮内容
    var offset = 0;
    if (current_page - 2 < 1) { // 讨论左边界对offset的影响
        offset += (1 - (current_page - 2));
    }
    if (current_page + 2 > total_page && total_page > 5) { // 讨论右边界对offset的影响
        offset -= (current_page + 2 - total_page);
    }
    document.querySelectorAll(".page_buttons > a").forEach(function(x, i) { // 应用offset
        var _ = current_page + i - 2 + offset;
        x.innerText = _;
        if (_ <= total_page) {
            x.classList.remove("page_link_disabled");
            x.setAttribute("href", page_link + _);
        }
        if (x.innerText == current_page) {
            x.classList.add("page_link_highlighted")
        }
    });
});