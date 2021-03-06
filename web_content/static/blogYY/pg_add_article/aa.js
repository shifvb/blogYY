$(function(){
    // 初始化文本编辑器
    var quill = new Quill("#article_content_editor", {
        modules: {
            toolbar: "#article_content_toolbar"
        },
        theme: "snow"
    });
    var _content = document.querySelector("#article_content_editor").dataset.raw
    if (_content) {
        quill.setContents(JSON.parse(_content));
    }


    // 提交用户输入的文章内容
    document.querySelector("#submit_btn").onclick = function() {
        var data = {
            title: document.querySelector("#article_title").value,
            create_time_str: document.querySelector("#article_create_time_str").value,
            content: JSON.stringify(quill.getContents()),
            category_id: document.querySelector("#category_id").value,
        };
        $.post({
            "url": document.querySelector("#submit_btn").dataset.submitUrl,
            "type": "POST",
            "headers": {
                "X-CSRFToken": document.querySelector("meta[name=csrf-token]").getAttribute("content")
            },
            "data": data,
            "success": function(rsp) {
                location.href = document.querySelector("#submit_btn").dataset.redirectUrl;
            },
            "error": function(rsp) {
                alert("error");
            }
        });
    };
});