$(function(){
    // 使用quill解释文章内容
    document.querySelectorAll(".article_content").forEach(function(x) {
        new Quill(x).setContents(JSON.parse(x.dataset.raw));
        x.removeAttribute("data-raw");
    });

    // 处理翻页按钮
    var _page_data = document.querySelector(".page_control").dataset;
    var current_page = Number(_page_data.currentPage);
    var total_page = Number(_page_data.totalPage);
    var page_link = _page_data.pageLink + "?page_num=";
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
        var _ = String(current_page + i - 2 + offset);
        x.innerText = _;
        x.setAttribute("href", page_link + _)
    });
    // 设置临近页按钮样式
    document.querySelectorAll(".page_buttons > a").forEach(function(x) {
        if (Number(x.innerText) <= total_page) {
            x.classList.remove("page_link_disabled");
        }
        if (Number(x.innerText) == current_page) {
            x.classList.add("page_link_highlighted")
        }
    });
});