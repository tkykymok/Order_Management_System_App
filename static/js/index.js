console.log('ok');

var csrfToken = $('input[name=csrfmiddlewaretoken]').val();


$(document).ready(function () {
    //"createOrderNumber" ---------------------------
    $('#orderNumber').keypress(function (event) {
        if (event.keyCode === 13) {
            $('input[name="suppDelDate"]').focus();
        }
    });
    $('input[name="suppDelDate"]').keypress(function (event) {
        if (event.keyCode === 13) {
            var date1 = $('input[name="suppDelDate"]').val();
            if (date1.length === 8) {
                var year1 = date1.slice(0, 4);
                var month1 = date1.slice(4, 6);
                var day1 = date1.slice(6, 8);
                var validated1 = `${year1}-${month1}-${day1}`;
                $('input[name="suppDelDate"]').val(validated1);
                $('input[name="custDelDate"]').focus();
            } else {
                alert('Validation Error!');
            }
        }
    });
    $('input[name="custDelDate"]').keypress(function (event) {
        if (event.keyCode === 13) {
            var date2 = $('input[name="custDelDate"]').val();
            if (date2.length === 8) {
                var year2 = date2.slice(0, 4);
                var month2 = date2.slice(4, 6);
                var day2 = date2.slice(6, 8);
                var validated2 = `${year2}-${month2}-${day2}`;
                $('input[name="custDelDate"]').val(validated2);
                $('#enter1').focus();
            } else {
                alert('Validation Error!');
            }
        }
    });
    $('#enter1').click(function () {
        var serializedData = $('#createOrderNumber').serialize();
        $.ajax({
            url: '/order-number-create/',
            data: serializedData,
            type: 'post',
            dataType: 'json',
            success: function (response) {
                $('#item1').focus();
                $('#orderNumber').prop("disabled", true);
                $('input[name="suppDelDate"]').prop("disabled", true);
                $('input[name="custDelDate"]').prop("disabled", true);
                $('#enter1').hide();
            },
            error: function () {
                alert("Please input valid Order Number.");
            }
        });
    });
    // end ---------------------------
    $('#item1').keypress(function () {
        if (event.keyCode === 13) {
            itemInfoGet('pName1', 'pNo1', 'sp1', 'bp1', 'qty1');
        }
    });
    $('#qty1').keypress(function () {
        if (event.keyCode === 13) {
            $('#item2').focus();
            $('#item1').prop("disabled", true);

        }
    });
    $('#item2').keypress(function () {
        if (event.keyCode === 13) {
            itemInfoGet('pName2', 'pNo2', 'sp2', 'bp2', 'qty2');
        }
    });
    $('#qty2').keypress(function () {
        if (event.keyCode === 13) {
            $('#item3').focus();
            $('#item2').prop("disabled", true);
        }
    });
    $('#item3').keypress(function () {
        if (event.keyCode === 13) {
            itemInfoGet('pName3', 'pNo3', 'sp3', 'bp3', 'qty3');
        }
    });
    $('#qty3').keypress(function () {
        if (event.keyCode === 13) {
            $('#item4').focus();
            $('#item3').prop("disabled", true);
        }
    });
    $('#item4').keypress(function () {
        if (event.keyCode === 13) {
            itemInfoGet('pName4', 'pNo4', 'sp4', 'bp4', 'qty4');
        }
    });
    $('#qty4').keypress(function () {
        if (event.keyCode === 13) {
            $('#item5').focus();
            $('#item4').prop("disabled", true);
        }
    });
    $('#item5').keypress(function () {
        if (event.keyCode === 13) {
            itemInfoGet('pName5', 'pNo5', 'sp5', 'bp5', 'qty5');
        }
    });
    $('#qty5').keypress(function () {
        if (event.keyCode === 13) {
            $('#item5').focus();
            $('#item5').prop("disabled", true);
        }
    });


    function itemInfoGet(pName, pNo, sp, bp, qty) {
        var serializedData = $('#orderContentForm').serialize();
        $.ajax({
            url: '/item-info-get/',
            type: 'post',
            data: serializedData,
            dataType: 'json',
            success: function (response) {
                console.log(response.item_info);
                $(`#${pName}`).val(response.item_info.parts_name).prop("disabled", true);
                $(`#${pNo}`).val(response.item_info.parts_number).prop("disabled", true);
                $(`#${sp}`).val(response.item_info.sell_price).prop("disabled", true);
                $(`#${bp}`).val(response.item_info.buy_price).prop("disabled", true);
                $(`#${qty}`).focus();
            },
            error: function () {
                alert("Please input valid Item Code.");
            }
        });
    };

    




});
