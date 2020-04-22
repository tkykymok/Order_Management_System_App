
var csrfToken = $('input[name=csrfmiddlewaretoken]').val();


$(document).ready(function () {

    //"PrjCodeInput" ---------------------------
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
                    var customerName = response.customer_info.name
                    var personIncharge = response.person_incharge.username
                    $('#customer').val(customerCode + '/' + customerName )
                    $('#pic').val(personIncharge )
                    $('#orderNumber').focus();
                    $('#prjCode').prop("disabled", true);
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
                $('#suppDateCopy').val(date1);
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
                $('#custDateCopy').val(date2);
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
            itemInfoGet('suppDate1', 'custDate1', 'pName1', 'pNo1', 'sp1', 'bp1', 'qty1');
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
            itemInfoGet('suppDate2','custDate2','pName2', 'pNo2', 'sp2', 'bp2', 'qty2');
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
            itemInfoGet('suppDate3','custDate3','pName3', 'pNo3', 'sp3', 'bp3', 'qty3');
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
            itemInfoGet('suppDate4','custDate4','pName4', 'pNo4', 'sp4', 'bp4', 'qty4');
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
            itemInfoGet('suppDate5','custDate5','pName5', 'pNo5', 'sp5', 'bp5', 'qty5');
        }
    });
    $('#qty5').keypress(function () {
        if (event.keyCode === 13) {
            $('#item5').focusout();
            dateGet('suppDate5', 'custDate5');
        }
    });


 


    function itemInfoGet(suppDate, custDate, pName, pNo, sp, bp, qty) {
        let suppDelDate = $('#suppDate').val();
        let custDelDate = $('#custDate').val();    
        var serializedData = $('#orderContentForm').serialize();
        $.ajax({
            url: '/item-info-get/',
            type: 'post',
            data: serializedData,
            dataType: 'json',
            success: function (response) {
                if ($('#prjCodeCopy').val() === response.prj) {
                    $(`#${suppDate}`).val(suppDelDate);
                    $(`#${custDate}`).val(custDelDate);
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
    let item, qty, suppDate, custDate
    let order = {}; 
    $('#create').click(function () {
        for (i = 1; i <= 5; i++) {
            if ($(`#item${i}`).val() !== "" && $(`#qty${i}`).val() !== "") {
                item = $(`#item${i}`).val();
                qty = $(`#qty${i}`).val();
                suppDate = $(`#suppDate${i}`).val();
                custDate = $(`#custDate${i}`).val();
                order[i] = [item, qty, suppDate, custDate];
                
                $("#orderConfirmTable > tbody:last-child").append(`
                    <tr>
                        <td width="20%">${item}</td>
                        <td width="20%">${qty}</td>
                        <td width="30%">${suppDate}</td>
                        <td width="30%">${custDate}</td>
                    </tr>
                `);
            } else if (Object.keys(order).length === 0){
                $("#orderConfirmTable > tbody:last-child").append(`
                <tr>
                    <td width="20%">No Order</td>
                    <td width="20%">No Order</td>
                    <td width="30%">No Order</td>
                    <td width="30%">No Order</td>
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



     // "Order Update " ---------------------------
    $('button.update').click(function () {
        var tr_id = $(this).data('id');
        console.log(tr_id);
        $.ajax({
            url: `/order-update/${tr_id}/`,
            type: 'get',
            dataType: 'json',
            success: function (response) {
                console.log(response.cur_order);
                console.log(response.order_number);
                $("#orderUpdateTable > tbody:last-child").append(`
                
                <tr>
                    <td><input class="form-control" id="form-id" type="" name="formId" readonly=True/></td>
                    <td><input id="form-suppDelDate" class="form-control" type="text" name="suppDelDate" /></td>
                    <td><input id="form-custDelDate" class="form-control" type="text" name="custDelDate" /></td>
                    <td><input id="form-qty" class="form-control" type="text" name="qty" /></td>
                </tr>
                `);
                
                $('#form-id').val(response.cur_order.id);
                $('#form-suppDelDate').val(response.cur_order.supplier_delivery_date);
                $('#form-custDelDate').val(response.cur_order.customer_delivery_date);
                $('#form-qty').val(response.cur_order.quantity);
            },
            error: function () {
                console.log("error");
            }
        });
        
        $('#close').click(function () {
            $("#orderUpdateTable tbody").empty();
        });

        $('#updateConfirm').click(function () {
            var serializedData = $('#orderUpdateForm').serialize();
            $.ajax({
                url: '/order-list/',
                type: 'post',
                data: serializedData,
                dataType: 'json',
                success: function (response) {
                    dataId = response.cur_order.id;
                    let curSuppDelDate = $(`#suppDelDate-${dataId}`);
                    let curCustDelDate = $(`#custDelDate-${dataId}`);
                    let curQty = $(`#qty-${dataId}`);

                    let newSuppDelDate = response.cur_order.supplier_delivery_date
                    let newCustDelDate = response.cur_order.customer_delivery_date
                    let newQty = response.cur_order.quantity
                    
                    
                    if (curSuppDelDate.text() !== newSuppDelDate) {
                        curSuppDelDate.text(newSuppDelDate).addClass('changed');  
                    }
                    if (curCustDelDate.text() !== newCustDelDate) {
                        curCustDelDate.text(newCustDelDate).addClass('changed');
                    }
                    if (curQty.text() !== newQty) {
                        curQty.text(newQty).addClass('changed');
                    } 
                    
                    console.log(curSuppDelDate.text() == newSuppDelDate)
                    console.log(curCustDelDate.text() == newCustDelDate) 
                    console.log((curQty.text() === newQty));
                    
                    $("#orderUpdateTable tbody").empty();
                },
                error: function () {
                    alert("error");
                }
            });

        });
    });
    



    

});
