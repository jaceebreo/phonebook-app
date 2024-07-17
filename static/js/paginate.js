var paginate_form = $("#paginate-form");

$.fn.paginatePage = function () {
    $(this).on('change', function(){
        var self = $(this)
        var page_url = paginate_form.attr('action') + "?paginate_by=" + self.val()

        $.ajax({
            url: page_url,
            type: "GET",
            success: function (response) {
                window.location.replace(page_url);
            }
        })
    });
}