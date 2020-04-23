$(function(){
    // 将innerHTML按照markdown格式进行解释
    var converter = new showdown.Converter();
    document.querySelectorAll(".article > .article_content").forEach(function(x) {
        x.innerHTML = converter.makeHtml(x.innerHTML)
    });

    // 删除article按钮鼠标单击事件绑定
    $(".article .delete_article_btn").on("click", function() {
        if (!confirm("确定删除？")) {
            return false; // 停止链接跳转
        }
        $.ajax({
            "url": $(this).attr("href"),
            "type": "POST",
            "success": function(rsp) {
                alert("删除成功！");
                location.href = "/blogYY/article/"
            },
            "error": function(rsp) {
                alert("请求错误，请稍后再试！");
            }
        })
        return false; // 停止链接跳转
    });

    // todo: 编辑article按钮鼠标单击事件绑定



});