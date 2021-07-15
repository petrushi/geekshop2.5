window.onload = function () {
    $('.basket_list').on('change', 'input[type="number"]', function () {
        var t_href = event.target;

        $.ajax({
            url: "/basket/edit/" + t_href.name + "/" + t_href.value + "/",

            success: (data) => {
                $('.basket_preview').html(data.menu_result);
                $('.basket_list').html(data.list_result)
            },
        });
        event.preventDefault();
    });
}