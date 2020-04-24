// let csrfToken = $('input[name=csrfmiddlewaretoken]').val();

$(document).ready(function () {
    //"PrjCodeInput" ---------------------------
    $('#prjCode').keypress(function (event) {
        if (event.keyCode === 13) {
            let serializedData = $('#createOrderNumber').serialize();
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
                    $('#pic').val(personIncharge)
                    $('input[name="suppDelDate"]').focus();
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
            $('#prjCode').focus();
        }
    });
    // suppDelDate Validation -----------------------------
    $('input[name="suppDelDate"]').keypress(function (event) {
        let date1 = $('input[name="suppDelDate"]');
        let next1 = $('input[name="custDelDate"]');
        if (event.keyCode === 13) {
            dateValidation(date1, next1);
            $('#suppDateCopy').val(date1);
        }
    });
    // custDelDate Validation -----------------------------
    $('input[name="custDelDate"]').keypress(function (event) {
        let date2 = $('input[name="custDelDate"]');
        let next2 = $('#enter1');
        if (event.keyCode === 13) {
            dateValidation(date2, next2);
            $('#custDateCopy').val(date2);
        }
    });
    // Order Number Create ---------------------------
    $('#enter1').click(function () {
        let serializedData = $('#createOrderNumber').serialize();
        $.ajax({
            url: '/order-number-create/',
            data: serializedData,
            type: 'post',
            dataType: 'json',
            success: function (response) {
                let orderNumber = $('#orderNumber').val();
                let prjCode = $('#prjCode').val();
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
    // "Order Confirm modal" ---------------------------
    $('#create').click(function () {
        let item, qty, suppDate, custDate
        let order = {}; 
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
    // "Order final confirm" ---------------------------
    $('#confirm').click(function () {
        let serializedData = $('#orderContentForm').serialize();
        if (!confirm('Do you Create Order?')) {
            return false;
        } else {
            $.ajax({
                url: '/order-confirm-create/',
                type: 'post',
                data: serializedData,
                dataType: 'json',
                success: function (response) {
                    if (response.result) {
                        location.reload();
                    }
                },
                error: function () {
                    alert("error");
                }
            });
        }
    });
    // "Cancel and reload" -----------------------
    $('#cancel').click(function () {
        if (!confirm('Are you sure you want to Cancel?')) {
            return false;
        } else {
            location.reload(); 
        }
    });
    // modal close and modal content delete
    $('#close').click(function () {
        $("#orderUpdateTable tbody").empty();
    });
    // modal close and modal content delete
    $('#close').click(function () {
        $("#orderConfirmTable tbody").empty();
    });
    // "Order Update " ---------------------------
    $('button.update').click(function () {
        console.log($('#form-delete').val());
        let tr_id = $(this).data('id');
        console.log(tr_id);
        $.ajax({
            url: `/order-update/${tr_id}/`,
            type: 'get',
            dataType: 'json',
            success: function (response) {
                console.log(response.cur_order);
                $("#orderUpdateTable > tbody:last-child").append(`
                
                <tr>
                    <td><input class="form-control" id="form-id" type="" name="formId" readonly=True/></td>
                    <td><input id="form-suppDelDate" class="form-control" type="text" name="suppDelDate" /></td>
                    <td><input id="form-custDelDate" class="form-control" type="text" name="custDelDate" /></td>
                    <td><input id="form-qty" class="form-control" type="text" name="qty" /></td>
                    <td><input id="form-delete" class="form-control" type="checkbox"  name="deleteCheck" value="0" /></td>
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
    });
    // Save Change or Delete -------------------------
    $('#updateConfirm').click(function () {      
        // Delete--------------------------------------
        if ($('#form-delete').val() === "1") {
            if (!confirm('Are you sure you want to delete this Order?')) {
                return false;
            } else {
                let tr_id = $('#form-id').val();
                $.ajax({
                    url: '/order-delete/',
                    type: 'get',
                    data: {
                        'id': tr_id
                    },
                    dataType: 'json',
                    success: function (data) {
                        if (data.deleted) {
                            $(`#orderListTable #order-${tr_id}`).remove();
                        }
                    },
                    error: function () {
                        alert("error");
                    }
                }); 
            }
        // Update Save----------------------------------
        } else if ($('#form-delete').val() === "0") {
            let serializedData = $('#orderUpdateForm').serialize();
            $.ajax({
                url: '/order-list/',
                type: 'post',
                data: serializedData,
                dataType: 'json',
                success: function (response) {
                    
                    // modified data reflected with red color
                    dataId = response.new_order.id;
                    let curSuppDelDate = $(`#suppDelDate-${dataId}`);
                    let curCustDelDate = $(`#custDelDate-${dataId}`);
                    let curQty = $(`#qty-${dataId}`);
    
                    let newSuppDelDate = response.new_order.supplier_delivery_date;
                    let newCustDelDate = response.new_order.customer_delivery_date;
                    let newQty = response.new_order.quantity;
                    
                    if (curSuppDelDate.text() !== newSuppDelDate) {
                        curSuppDelDate.text(newSuppDelDate).addClass('changed');  
                    }
                    if (curCustDelDate.text() !== newCustDelDate) {
                        curCustDelDate.text(newCustDelDate).addClass('changed');
                    }
                    if (curQty.text() !== newQty.toLocaleString()) {
                        curQty.text(newQty.toLocaleString()).addClass('changed');
                    } 
                },
                error: function () {
                    alert("error");
                }
            });    
        } 
        $("#orderUpdateTable tbody").empty();
    });


    // Delete CheckBox Value Check ---------
    $(function(){
        $(document).on('change', '#form-delete', function () {
            if ($(this).val() === "0") {
                $(this).val("1")
            } else {
                $(this).val("0")
            }
        }); 
    });
    //--------------------------------------

    // Order Entry Item info reflect -------
    function itemInfoGet(suppDate, custDate, pName, pNo, sp, bp, qty) {
        let suppDelDate = $('#suppDate').val();
        let custDelDate = $('#custDate').val();    
        let serializedData = $('#orderContentForm').serialize();
        $.ajax({
            url: '/item-info-get/',
            type: 'post',
            data: serializedData,
            dataType: 'json',
            success: function (response) {
                if ($('#prjCodeCopy').val() === response.prj) {
                    $(`#${suppDate}`).val(suppDelDate).prop("readonly", false);
                    $(`#${custDate}`).val(custDelDate).prop("readonly", false);
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
    // -------------------------------------


    // Ship Data Get ---------------------
    $('#shipOrderNumber').keypress(function (event) {
        let shipOrderNumber = $('#shipOrderNumber').val();
        if (event.keyCode === 13) {
            $.ajax({
                url: '/shipment-data-get/',
                type: 'get',
                data: {
                    'shipOrderNumber': shipOrderNumber
                },
                dataType: 'json',
                success: function (response) {
                    let orderNumber = $('#shipOrderNumber').val();
                    $('#orderNumCopy').val(orderNumber);
                    $('#shipPrjCode').val(response.prj_code.prj_code);
                    $('#shipCustomer').val(response.customer.name);
                    $('#shipPic').val(response.pic.username);
                    $('#shipOrderNumber').prop('readonly', true)
                    $('#shipDate').focus();
                    $('#shipDate').keypress(function (event) {
                        if (event.keyCode === 13) {
                            let shipDate = $('input[name="shipDate"]');
                            let next3 = $('#enter2');
                            dateValidation(shipDate, next3);
                        }
                    });

                    let dataLength = response.order_data.length;
                    $('#enter2').click(function () {
                        for (i = 0; i < dataLength; i++) {
                            if (response.order_data[i].balance === 0) {
                                continue
                            } else {
                                $("#shipmentEntryTable > tbody:last-child").append(`  
                                <tr>
                                    <input id="orderId-${i}" class="form-control" type="hidden" name="orderId" readonly=True >
                                    <td><input id="shipItem-${i}" class="form-control" type="text" name="shipItem" maxlength="5" readonly=True ></td>
                                    <td><input id="shipDate-${i}" class="form-control" type="text" name="shipDate2" maxlength="10"></td>
                                    <td><input id="shipPName-${i}" class="form-control form-control" type="text" readonly=True></td>
                                    <td><input id="shipPNo-${i}" class="form-control" type="text" readonly=True></td>
                                    <td><input id="shipSp-${i}" class="form-control" type="text" readonly=True></td>
                                    <td><input id="orderBal-${i}" class="form-control" type="text" readonly=True></td>
                                    <td><input id="shipQty-${i}" class="form-control"  type="text" name="shipQty"></td>
                                </tr>
                                `)
                                $(`#orderId-${i}`).val(response.order_data[i].id);
                                $(`#shipItem-${i}`).val(response.item_data[i].item_code);
                                $(`#shipDate-${i}`).val($('#shipDate').val());
                                $(`#shipPName-${i}`).val(response.item_data[i].parts_name);
                                $(`#shipPNo-${i}`).val(response.item_data[i].parts_number);
                                $(`#shipSp-${i}`).val(response.item_data[i].sell_price);
                                $(`#orderBal-${i}`).val(response.order_data[i].balance);    
                            }
                        }
                        $('#enter2').hide();
                        $(`#shipQty-0`).focus();
                        
                        qtyValCheck(0);
                        qtyValCheck(1);
                        qtyValCheck(2);
                        qtyValCheck(3);
                        qtyValCheck(4);
                        qtyValCheck(5);
           
                        function qtyValCheck(n) {
                            $(`#shipQty-${n}`).keypress(function (event) {
                                if (event.keyCode === 13) {
                                    if ( $(`#orderBal-${n}`).val() < $(`#shipQty-${n}`).val()) {
                                        alert("Ship Qty must be less than PO Balance.");
                                    } else {
                                        if ($(`#shipQty-${n + 1}`).length === 1) {
                                            $(`#shipQty-${n + 1}`).focus();
                                            n += 1;
                                        } else {
                                            $('#shipConfirm').focus();
                                        }          
                                    }
                                }
                            });
                        }
                    });
                },
                error: function () {
                    alert("Please input valid Order Number.");
                }
            });
        }
    });
    // -------------------------------------


    // Shipment Confirm --------------------
    $(function(){
        $('#shipConfirm').click(function () {
            let serializedData = $('#shipmentEntryForm').serialize();        
            if (!confirm('Do you Proceed?')) {
                return false;
            } else {
                $.ajax({
                    url: '/shipment-complete/',
                    data: serializedData,
                    type: 'post',
                    dataType: 'json',
                    success: function (response) {
                        if (response.result) {
                            location.reload();
                        }
                    },
                    error: function () {
                        alert("error");
                    }
                });  
            }
        });
    });
    // -------------------------------------


    // date validation ---------------------
    function dateValidation(date,next) {
        if (date.val().length === 8) {
            let year = date.val().slice(0, 4);
            let month = date.val().slice(4, 6);
            let day = date.val().slice(6, 8);
            let validated = `${year}-${month}-${day}`;
            date.val(validated);
            next.focus();
        }  else {
            alert('Validation Error!');
        }
    };
    //--------------------------------------
});


// $("#orderConfirmTable > tbody:last-child").append(`