$(function(){
    $addArticleForm = $("form");
    $addArticleForm.submit(function(e) {
        $.post({
            "url": "/blogYY/api/v1/add_article",
            "type": "POST",
            "data": $addArticleForm.serializeArray(),
            "success": function(rsp) {
                location.href = "/blogYY/article"
            },
            "error": function(rsp) {
                alert("error");
            }
        });
        e.preventDefault(); // 阻止表单自动提交
    });
});