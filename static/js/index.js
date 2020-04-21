
var csrfToken = $('input[name=csrfmiddlewaretoken]').val();


$(document).ready(function () {

    //"PrjCodeGet" ---------------------------
    $('#prjCode').keypress(function (event) {
        if (event.keyCode === 13) {
            var serializedData = $('#createOrderNumber').serialize();
            $.ajax({
                url: '/prj-code-get/',
                data: serializedData,
                type: 'post',
                dataType: 'json',
                success: function (response) {
                    var customerCode = response.customer_info.customer_code 
                    var customerName =response.customer_info.name
                    $('#customer').val(customerCode + '/' + customerName )
                    $('#orderNumber').focus();
                    $('#prjCode').prop("readonly", true);
                },
                error: function () {
                    alert("Please input valid PRJ Code.");
                }
            });
        }
    });
    
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
                var orderNumber = $('#orderNumber').val();
                var prjCode = $('#prjCode').val();
                $('#orderNumCopy').val(orderNumber);
                $('#prjCodeCopy').val(prjCode);

                $('#item1').prop("disabled", false).focus();
                $('#orderNumber').prop("readonly", true);
                $('input[name="suppDelDate"]').prop("readonly", true);
                $('input[name="custDelDate"]').prop("readonly", true);
                $('#enter1').hide();
            },
            error: function () {
                alert("Please input valid Order Number.");
            }
        });
    });

    // "Item Info Get" ---------------------------
    $('#item1').keypress(function () {
        if (event.keyCode === 13) {
            itemInfoGet('pName1', 'pNo1', 'sp1', 'bp1', 'qty1');
        }
    });
    $('#qty1').keypress(function () {
        if (event.keyCode === 13) {
            $('#item2').prop("disabled", false).focus();
            $('#item1').prop('readonly', true);
        }
    });
    $('#item2').keypress(function () {
        if (event.keyCode === 13) {
            itemInfoGet('pName2', 'pNo2', 'sp2', 'bp2', 'qty2');
        }
    });
    $('#qty2').keypress(function () {
        if (event.keyCode === 13) {
            $('#item3').prop("disabled", false).focus();
            $('#item2').prop('readonly', true);
       
        }
    });
    $('#item3').keypress(function () {
        if (event.keyCode === 13) {
            itemInfoGet('pName3', 'pNo3', 'sp3', 'bp3', 'qty3');
        }
    });
    $('#qty3').keypress(function () {
        if (event.keyCode === 13) {
            $('#item4').prop("disabled", false).focus();
            $('#item3').prop('readonly', true);
        }
    });
    $('#item4').keypress(function () {
        if (event.keyCode === 13) {
            itemInfoGet('pName4', 'pNo4', 'sp4', 'bp4', 'qty4');
        }
    });
    $('#qty4').keypress(function () {
        if (event.keyCode === 13) {
            $('#item5').prop("disabled", false).focus();
            $('#item4').prop('readonly', true);
        }
    });
    $('#item5').keypress(function () {
        if (event.keyCode === 13) {
            itemInfoGet('pName5', 'pNo5', 'sp5', 'bp5', 'qty5');
        }
    });
    $('#qty5').keypress(function () {
        if (event.keyCode === 13) {
            $('#item5').focusout();
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
                if ($('#prjCodeCopy').val() === response.prj) {
                    $(`#${pName}`).val(response.item_info.parts_name).prop("disabled", true);
                    $(`#${pNo}`).val(response.item_info.parts_number).prop("disabled", true);
                    $(`#${sp}`).val(response.item_info.sell_price).prop("disabled", true);
                    $(`#${bp}`).val(response.item_info.buy_price).prop("disabled", true);
                    $(`#${qty}`).prop('disabled', false).focus();
                } else {
                    alert(`Please input valid Item Code. This Item Code is registered as ${response.prj}`);
                }
            },
            error: function () {
                alert("Please input valid Item Code.");
            }
        });
    };

    // "Order Confirm modal" ---------------------------
    let item, qty
    let order = {}; 
    $('#create').click(function () {
        for (i = 1; i <= 5; i++) {
            if ($(`#item${i}`).val() !== "" && $(`#qty${i}`).val() !== "") {
                item = $(`#item${i}`).val();
                qty = $(`#qty${i}`).val();
                order[i] = [item, qty];
                
                $("#orderConfirmTable > tbody:last-child").append(`
                    <tr>
                        <td width="50%">${item}</td>
                        <td width="50%">${qty}</td>
                    </tr>
                `);
            } else if (Object.keys(order).length === 0){
                $("#orderConfirmTable > tbody:last-child").append(`
                <tr>
                    <td width="50%">No Order</td>
                    <td width="50%">No Order</td>
                </tr>
                 `);
                break
            } else {
                break
            }
        }
        console.log(order);
    });
    $('#close').click(function () {
        $("#orderConfirmTable tbody").empty();
    });
    
    
    // "Order final confirm" ---------------------------
    $('#confirm').click(function () {
        var serializedData = $('#orderContentForm').serialize();

        $.ajax({
            url: '/order-confirm-create/',
            type: 'post',
            data: serializedData,
            dataType: 'json',
            success: function (response) {
                console.log(response.result);
                location.reload();
            },
            error: function () {
                alert("error");
            }
        });
    });

    // "Cancel Button" ---------------------------
    $('#cancel').click(function () {
        location.reload(); 
    });
    

});
