// let csrfToken = $('input[name=csrfmiddlewaretoken]').val();
$(document).ready(function () {

// Common Function ////////////////////////////////////////////////////////////////////////////////////
    var csrfToken = $('input[name=csrfmiddlewaretoken]').val();
    // date validation ---------------------
    function dateValidation(date,next) {
        if (date.val().length === 8) {
            let year = date.val().slice(0, 4);
            let month = date.val().slice(4, 6);
            let day = date.val().slice(6, 8);
            let validated = `${year}-${month}-${day}`;
            date.val(validated);
            next.focus();
        } else if (date.val().length > 8){
            date.val('')
        } else {
            return false
        }
    };
    //--------------------------------------

    let mode = "1"; // 1:new 2:change 3:delete
    console.log(mode);

    function modeBlock() {
        $('#chkbox1').prop('disabled',true)
        $('#chkbox2').prop('disabled',true)
        $('#chkbox3').prop('disabled',true)
    }

    function btnShowUp() {
        $('.confirm-btn').css('display','block')
        $('.cancel-btn').css('display','block')
    }
    
    function btnShowUp2() {
        $('#lineAdd').css('display','block');
        $('#lineDelete').css('display','block');
    }

    function deleteCheck() {
        $('input[name="deleteCheck"]').on('click', function () {
            let dataId = $(this).data('id')
            if ($(this).val() === "0") {
                $(this).val("1")
                $(`#deleteCheckNum-${dataId}`).val("1")
            } else {
                $(this).val("0")
                $(`#deleteCheckNum-${dataId}`).val("0")
            }
        });
    }

    //"Check Box" -------------------------
    $('#chkbox1').on('click', function () { 
        if ($('#chkbox2').prop('checked') === true || $('#chkbox3').prop('checked')===true ) {
            $('#chkbox2').prop('checked', false); 
            $('#chkbox3').prop('checked', false); 
            $('#prjCode').prop('readonly', false);
            $('#suppDate').prop('readonly', false);
            $('#custDate').prop('readonly', false);
            $('#shipDate').prop('readonly', false);
            $('#acceptDate').prop('readonly', false);
            $('#orderId').prop('readonly', true);
        } else {
            return false
        }
    });

    $('#chkbox2').on('click', function () { 
        if ($('#chkbox1').prop('checked') === true || $('#chkbox3').prop('checked')===true ) {
            $('#chkbox1').prop('checked', false); 
            $('#chkbox3').prop('checked', false); 
            $('#prjCode').prop('readonly', true);
            $('#suppDate').prop('readonly', true);
            $('#custDate').prop('readonly', true);
            $('#shipDate').prop('readonly', true);
            $('#acceptDate').prop('readonly', true);
            $('#orderId').prop('readonly', false);
        } else {
            return false
        }
    });

    $('#chkbox3').on('click', function () { 
        if ($('#chkbox1').prop('checked') === true || $('#chkbox2').prop('checked')===true ) {
            $('#chkbox1').prop('checked', false); 
            $('#chkbox2').prop('checked', false); 
            $('#prjCode').prop('readonly', true);
            $('#suppDate').prop('readonly', true);
            $('#custDate').prop('readonly', true);
            $('#shipDate').prop('readonly', true);
            $('#acceptDate').prop('readonly', true);
            $('#orderId').prop('readonly', false);
        } else {
            return false
        }
    });
    
    $('input[name="chkbox"]').on('click', function () { 
        mode = $(this).val();
        console.log(mode);
    });

    // "Item Info Get / Order Create" ------
    function itemInfoGet(item, suppDate, custDate, pName, pNo, sp, bp, qty) {
        let suppDelDate = $('#suppDate').val();
        let custDelDate = $('#custDate').val(); 
        $.ajax({
            url: '/item-info-get/',
            type: 'post',
            data: {
                csrfmiddlewaretoken: csrfToken,
                'item': item,
            },
            dataType: 'json',
            success: function (response) {
                if ($('#prjCodeCopy').val() === response.prj) {
                    $(`#${suppDate}`).val(suppDelDate).prop("readonly", false);
                    $(`#${custDate}`).val(custDelDate).prop("readonly", false);
                    $(`#${pName}`).val(response.item_info.parts_name).prop("disabled", true);
                    $(`#${pNo}`).val(response.item_info.parts_number).prop("disabled", true);
                    $(`#${sp}`).val(response.item_info.sell_price).prop("disabled", true);
                    $(`#${bp}`).val(response.item_info.buy_price).prop("disabled", true);
                    $(`#${qty}`).focus();
                } else {
                    alert(`Please input valid Item Code. This Item Code is registered as ${response.prj}`);
                }
            },
            error: function () {
                alert("Please input valid Item Code.");
            }
        });
    };
 
    
    // new Line add ------------------------
    function newLineAdd(n) {
        for (let i = 0; i < 5; i++){
            $("#orderCreateTable > tbody:last-child").append(`
            <tr id="${n+i}" >
                <td class="delete-check-box"><input id="deleteCheck-${i}" class="check-box" type="checkbox" name="deleteCheck" value="${i}" maxlength="5"></td>
                <td><input id="item-${n+i}" class="form-control" type="text" name="item" data-id="${n+i}" maxlength="5"></td>
                <td><input id="suppDate-${n+i}" class="form-control" type="text" name="suppDate" maxlength="10" readonly=True></td>
                <td><input id="custDate-${n+i}" class="form-control" type="text" name="custDate" maxlength="10" readonly=True></td>
                <td><input id="pName-${n+i}" class="form-control form-control" type="text" readonly=True></td>
                <td><input id="pNo-${n+i}" class="form-control" type="text" readonly=True></td>
                <td><input id="sp-${n+i}" class="form-control" type="text" readonly=True></td>
                <td><input id="bp-${n+i}" class="form-control" type="text" readonly=True></td>
                <td><input id="qty-${n+i}" class="form-control"  type="text" name="qty" data-id="${n+i}"></th>
            </tr>
            `);
        }
    }


    // Line Delete --------------------------
    $('#lineDelete').click(function () {
        for (let i = 0; i < 50; i++) {
            if ($(`#orderCreateTable tr#${i} input[name="deleteCheck"]`).prop('checked') === true) {
                $(`#orderCreateTable tr#${i}`).remove()
            }
        }
    });


    // "Cancel and reload" -----------------
    $('#cancel').click(function () {
        if (!confirm('Are you sure you want to Cancel?')) {
            return false;
        } else {
            location.reload(); 
        }
    });



// Order ////////////////////////////////////////////////////////////////////////////////////
    //"inputOrderNumber" ---------------------------
    $('#orderNumber').keypress(function (event) {
        if (event.keyCode === 13) {
            if (mode === "2" || mode === "3") {
                $('#enter1').focus();
            } else {
                $('#prjCode').focus();
            }
        }
    });

    // Order Create ---------------------------
    $('#enter1').click(function () {
        if (mode === "1") {

            let serializedData = $('#createOrderNumber').serialize();
            $.ajax({
                url: '/order-number-create/',
                data: serializedData,
                type: 'post',
                dataType: 'json',
                success: function (response) {
                    modeBlock();
                    btnShowUp();
                    btnShowUp2();

                    let orderNumber = $('#orderNumber').val();
                    let prjCode = $('#prjCode').val();
                    let lineCount = 0;
                    $('#orderNumCopy').val(orderNumber);
                    $('#prjCodeCopy').val(prjCode);
                    $('#orderNumber').prop("readonly", true);
                    $('input[name="suppDelDate"]').prop("readonly", true);
                    $('input[name="custDelDate"]').prop("readonly", true);
                    $('#enter1').hide();
                    $("#orderCreateTable > thead").prepend(`
                    <tr class="text-center">
                        <th colspan="2">Item Code</th>
                        <th width="13%">Supplier Delivery date</th>
                        <th width="13%">Customer Delivery date</th>
                        <th width="15%">Description</th>
                        <th width="20%">Maker P/N</th>
                        <th>S/P</th>
                        <th>B/P</th>
                        <th>QTY</th>
                    </tr>
                    `)
                    
                    newLineAdd(lineCount);
                    lineCount += 5;

                    $('#lineAdd').click(function () {
                        if (lineCount < 50) {
                            newLineAdd(lineCount);
                            lineCount += 5;
                        } else {
                            alert("You can not add line any more. Maximum number of line is 50.")
                            return false
                        }
                    });
                    // Order Entry Item info reflect & input-------
                    $('#orderCreateTable').on('keypress', 'input[name="item"]', function (event) {
                        if (event.keyCode === 13) {
                            let dataId = $(this).data('id');
                            let item = $(this).val();
                            let suppDate = `suppDate-${dataId}`;
                            let custDate = `custDate-${dataId}`;
                            let pName = `pName-${dataId}`;
                            let pNo = `pNo-${dataId}`;
                            let sp = `sp-${dataId}`;
                            let bp = `bp-${dataId}`;
                            let qty = `qty-${dataId}`;
                            itemInfoGet(item, suppDate, custDate, pName, pNo, sp, bp, qty);
                        }
                    });

                    $('#orderCreateTable').on('keypress', 'input[name="qty"]', function (event) {
                        if (event.keyCode === 13) {
                            let dataId = $(this).data('id');
                            console.log($(`#item-${dataId + 1}`));
                            // $(`#copyItem${dataId}`).val(`item-`)
                            if ($(`#item-${dataId + 1}`).length === 1) {
                                $(`#item-${dataId + 1}`).focus();
                            } else {
                                $('#confirm').focus();
                            }
                        }
                    });
                    // "Order create confirm" ---------------------------
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
                },
                error: function () {
                    alert("Please input valid Order Number.");
                }
            });
        } else {
            return false
        }
    });

    //"PrjCodeInput" ---------------------------
    $('#prjCode').keypress(function (event) {
        if (event.keyCode === 13) {
            let prjCode = $(this).val().toUpperCase();
            $(this).val(prjCode);
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

    // suppDelDate Validation -----------------------------
    $('input[name="suppDelDate"]').on('input',function (event) {
        let date1 = $('input[name="suppDelDate"]');
        let next1 = $('input[name="custDelDate"]');
        dateValidation(date1, next1);
        $('#suppDateCopy').val(date1);
    
    });
    // custDelDate Validation -----------------------------
    $('input[name="custDelDate"]').on('input',function (event) {
        let date2 = $('input[name="custDelDate"]');
        let next2 = $('#enter1');
        dateValidation(date2, next2);
        $('#custDateCopy').val(date2);
    });

    // "Order update ---------------------------
    $('#enter1').click(function () {
        if (mode === "2") {
            let serializedData = $('#createOrderNumber').serialize();

            $.ajax({
                url: '/order-update-data-get/',
                type: 'post',
                data: serializedData,
                dataType: 'json',
                success: function (response) {
                    let orderNumber = $('#orderNumber').val();
                    let prjCode = $('#prjCode').val();


                    console.log(response.order_list)
                    let data = response.order_list
                    let dataLength = Object.keys(response.order_list.id).length;
                    console.log(dataLength);

                    if (dataLength === 0) {
                        alert("This Order No does not exist.")
                        location.reload()
                    } else {
                        modeBlock();
                        btnShowUp();
                        $('#orderNumber').prop("readonly", true);
                        $('#orderNumCopy').val(orderNumber);
                        $('#prjCodeCopy').val(prjCode);
                        $('#enter1').hide();

                        $("#orderCreateTable > thead").prepend(`
                        <tr class="text-center">
                            <th>Item Code</th>
                            <th width="13%">Supplier Delivery date</th>
                            <th width="13%">Customer Delivery date</th>
                            <th width="15%">Description</th>
                            <th width="20%">Maker P/N</th>
                            <th>S/P</th>
                            <th>B/P</th>
                            <th>QTY</th>
                        </tr>
                        `)
                        for (let i = 0; i < dataLength; i++){
                            $("#orderCreateTable > tbody:last-child").append(`
                            <tr id=${i}>
                                <input id="order-${i}"  type="hidden" name="orderId"  maxlength="5">
                                <td><input id="item-${i}" class="form-control" type="text" name="item" maxlength="5" readonly=True></td>
                                <td><input id="suppDate-${i}" class="form-control" type="text" name="suppDate" maxlength="10"></td>
                                <td><input id="custDate-${i}" class="form-control" type="text" name="custDate" maxlength="10"></td>
                                <td><input id="pName-${i}" class="form-control form-control" type="text" readonly=True></td>
                                <td><input id="pNo-${i}" class="form-control" type="text" readonly=True></td>
                                <td><input id="sp-${i}" class="form-control" type="text" readonly=True></td>
                                <td><input id="bp-${i}" class="form-control" type="text" readonly=True></td>
                                <td><input id="qty-${i}" class="form-control"  type="text" name="qty" data-id="${i}" readonly=True></th>
                            </tr>
                            `);
                            $(`#order-${i}`).val(data.id[i]);
                            $(`#item-${i}`).val(data.item_code[i]);
                            $(`#suppDate-${i}`).val(data.supplier_delivery_date[i]);
                            $(`#custDate-${i}`).val(data.customer_delivery_date[i]);
                            $(`#pName-${i}`).val(data.parts_name[i]);
                            $(`#pNo-${i}`).val(data.parts_number[i]);
                            $(`#sp-${i}`).val(data.sell_price[i]);
                            $(`#bp-${i}`).val(data.buy_price[i]);
                            $(`#qty-${i}`).val(data.quantity[i]);
                        }
                        
                        $('#orderCreateTable').on('keypress', 'input[name="qty"]', function (event) {
                            if (event.keyCode === 13) {
                                let dataId = $(this).data('id');
                                if ($(`#qty-${dataId + 1}`).length === 1) {
                                    $(`#qty-${dataId + 1}`).focus();
                                } else {
                                    $('#confirm').focus();
                                }
                            }
                        });
    
                        // "Order update confirm" ---------------------------
                        $('#confirm').click(function () {
                                let serializedData = $('#orderContentForm').serialize();
                                if (!confirm('Do you Update Order?')) {
                                    return false;
                                } else {
                                    $.ajax({
                                        url: '/order-update-confirm/',
                                        type: 'post',
                                        data: serializedData,
                                        dataType: 'json',
                                        success: function (response) {
                                            if (response.result) {
                                                location.reload();
                                            } else {
                                                alert("This order cannot be changed");
                                            }
                                        },
                                        error: function () {
                                            alert("error");
                                        }
                                    });
                                }    
                        });
                    }
                },
                error: function () {
                    alert("Please input valid Order No.");
                }
            });
        }
    });
    
    // "Order Delete ---------------------------
    $('#enter1').click(function () {
        if (mode === "3") {
            let serializedData = $('#createOrderNumber').serialize();

            $.ajax({
                url: '/order-update-data-get/',
                type: 'post',
                data: serializedData,
                dataType: 'json',
                success: function (response) {
                    let data = response.order_list
                    let dataLength = Object.keys(response.order_list.id).length;


                    if (dataLength === 0) {
                        alert("This Order No does not exist.")
                        location.reload()
                    } else {
                        modeBlock();
                        btnShowUp();
                        let orderNumber = $('#orderNumber').val();
                        let prjCode = $('#prjCode').val();
                        $('#orderNumCopy').val(orderNumber);
                        $('#prjCodeCopy').val(prjCode);
                        $('#orderNumber').prop("readonly", true);
                        $('#enter1').hide();
                        $("#orderCreateTable > thead").prepend(`
                        <tr class="text-center">
                            <th colspan="2">Item Code</th>
                            <th width="13%">Supplier Delivery date</th>
                            <th width="13%">Customer Delivery date</th>
                            <th width="15%">Description</th>
                            <th width="20%">Maker P/N</th>
                            <th>S/P</th>
                            <th>B/P</th>
                            <th>QTY</th>
                        </tr>
                        `)

                        for (let i = 0; i < dataLength; i++){
                            $("#orderCreateTable > tbody:last-child").append(`
                            <tr id=${i}>
                                <input id="order-${i}"  type="hidden" name="orderId"  maxlength="5">
                                <input id="deleteCheckNum-${i}" type="hidden" name="deleteCheckNum" value="0">
                                <td class="delete-check-box"><input id="deleteCheck-${i}" class="check-box" type="checkbox" data-id="${i}" name="deleteCheck" value="0"></td>
                                <td><input id="item-${i}" class="form-control" type="text" name="item" maxlength="5" readonly=True></td>
                                <td><input id="suppDate-${i}" class="form-control" type="text" name="suppDate" maxlength="10" readonly=True ></td>
                                <td><input id="custDate-${i}" class="form-control" type="text" name="custDate" maxlength="10" readonly=True ></td>
                                <td><input id="pName-${i}" class="form-control form-control" type="text" readonly=True></td>
                                <td><input id="pNo-${i}" class="form-control" type="text" readonly=True></td>
                                <td><input id="sp-${i}" class="form-control" type="text" readonly=True></td>
                                <td><input id="bp-${i}" class="form-control" type="text" readonly=True></td>
                                <td><input id="qty-${i}" class="form-control"  type="text" name="qty" data-id="${i}" readonly=True></th>
                            </tr>
                            `);
    
                            $(`#order-${i}`).val(data.id[i]);
                            $(`#item-${i}`).val(data.item_code[i]);
                            $(`#suppDate-${i}`).val(data.supplier_delivery_date[i]);
                            $(`#custDate-${i}`).val(data.customer_delivery_date[i]);
                            $(`#pName-${i}`).val(data.parts_name[i]);
                            $(`#pNo-${i}`).val(data.parts_number[i]);
                            $(`#sp-${i}`).val(data.sell_price[i]);
                            $(`#bp-${i}`).val(data.buy_price[i]);
                            $(`#qty-${i}`).val(data.quantity[i]);
                        }
                        deleteCheck();
                        $('#orderCreateTable').on('keypress', 'input[name="qty"]', function (event) {
                            if (event.keyCode === 13) {
                                let dataId = $(this).data('id');
                                if ($(`#qty-${dataId + 1}`).length === 1) {
                                    $(`#qty-${dataId + 1}`).focus();
                                } else {
                                    $('#confirm').focus();
                                }
                            }
                        });
                        // "Order Delete confirm" ---------------------------
                        $('#confirm').click(function () {
                                if (!confirm('Do you Delete Checked Order?')) {
                                    return false;
                                } else {
                                    let serializedData = $('#orderContentForm').serialize();
                                    $.ajax({
                                        url: '/order-delete-confirm/',
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
                    }
                },
                error: function () {
                    alert("Please input valid Order No.");
                }
            });
        }
    });
    

// Shipment ////////////////////////////////////////////////////////////////////////////////////
    $('#shipOrderNumber').keypress(function (event) {
        if (event.keyCode === 13) {
            if (mode === "1") {        
                $('#shipDate').focus();
                $('#shipDate').on('input',function (event) {
                    let shipDate = $('input[name="shipDate"]');
                    let next3 = $('#enter2');
                    dateValidation(shipDate, next3);
                });        
            } else if (mode === "2" || mode === "3") {       
                $('#orderId').focus();
                $('#orderId').keypress(function (event) {
                    if (event.keyCode === 13) {
                        $('#enter2').focus();
                    }
                });
            } 
        }
    });
    
    // Shipment New ---------------------
    $('#enter2').click(function () {
        if (mode === "1") {
            let shipOrderNumber = $('#shipOrderNumber').val();
            $('#orderNumCopy').val(shipOrderNumber);
            $.ajax({
                url: '/shipment-data-get/',
                type: 'get',
                data: {
                    'shipOrderNumber': shipOrderNumber
                },
                dataType: 'json',
                success: function (response) {

                    let dataLength = Object.keys(response.ship_order_list.id).length;
                    let isStockExit = 0;

                    if (dataLength === 0) {
                        alert("Please input valid Order Number.");
                    } else {
                        for (i = 0; i < dataLength; i++) {
                            if (response.ship_order_list.stock[i] === 0) {
                                isStockExit += 1;
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
                                    <td><input id="stock-${i}" class="form-control" type="text" readonly=True></td>
                                    <td><input id="shipQty-${i}" class="form-control"  type="text" name="shipQty" data-id="${i}"></td>
                                </tr>
                                `)
                                $(`#orderId-${i}`).val(response.ship_order_list.id[i]);
                                $(`#shipItem-${i}`).val(response.ship_order_list.item_code[i]);
                                $(`#shipDate-${i}`).val($('#shipDate').val());
                                $(`#shipPName-${i}`).val(response.ship_order_list.parts_name[i]);
                                $(`#shipPNo-${i}`).val(response.ship_order_list.parts_number[i]);
                                $(`#shipSp-${i}`).val(response.ship_order_list.sell_price[i]);
                                $(`#stock-${i}`).val(response.ship_order_list.stock[i]);
                            }
                        }
                        if (dataLength - isStockExit === 0) {
                            alert("No remaining Stock Exit.")
                            location.reload();
                        } else {
                            $('#enter2').hide();
                            modeBlock();
                            btnShowUp();
                            $('#enter2').hide();
                            $('#shipOrderNumber').prop("readonly", true);
                            $('#shipDate').prop('readonly', true);
                            $('#shipPrjCode').val(response.ship_order_list.prj_code[0]);
                            $('#shipCustomer').val(response.ship_order_list.customer[0]);
                            
                            $("#shipmentEntryTable > thead").prepend(`
                            <tr class="text-center">
                                <th>Item Code</th>
                                <th width="13%">Ship Date</th>
                                <th width="15%">Description</th>
                                <th width="20%">Maker P/N</th>
                                <th>S/P</th>
                                <th>Stock</th>
                                <th>Ship Qty</th>
                            </tr>
                            `)
                        }
    
                        $('input[name="shipQty"]').on('focus', function () {
                            let dataId = $(this).data('id')
                            $(`#shipQty-${dataId}`).on('input', function () {
                                if (parseInt($(`#stock-${dataId}`).val()) < parseInt($(`#shipQty-${dataId}`).val())) {
                                    alert("Ship Qty must be less than Stock Qty.");
                                    $(this).val("");
                                } else {
                                    return false
                                }
                            });
    
                            $(`#shipQty-${dataId}`).keypress(function (event) {
                                if (event.keyCode === 13) {
                                    if ($(`#shipQty-${dataId + 1}`).length === 1) {
                                        $(`#shipQty-${dataId + 1}`).focus();
                                    } else {
                                        $('#shipConfirm').focus();
                                    }
                                }
                            });
                        });
                    }
                },
                error: function () {
                    alert("Please input valid Order Number.");
                }
            });
        }
    });

    // Shipment Update ---------------------
    $('#enter2').click(function () {
        if (mode === "2") {
            let shipOrderNumber = $('#shipOrderNumber').val();
            let orderId = $('#orderId').val();
            $('#orderNumCopy').val(shipOrderNumber);
            $.ajax({
                url: '/shipment-update-data-get/',
                type: 'get',
                data: {
                    'shipOrderNumber': shipOrderNumber,
                    'orderId': orderId
                },
                dataType: 'json',
                success: function (response) {
                    let dataLength = Object.keys(response.shipment_list.id_x).length;
                    if (response.shipment_list.order_number[0] != shipOrderNumber) {
                        alert("Input Order No and ID does not match.");
                    } else if (dataLength === 0) {
                        alert("Please input valid Order ID.");
                    } else {
                        modeBlock();
                        btnShowUp();
                        $('#enter2').hide();
                        $('#shipOrderNumber').prop("readonly", true);
                        $('#orderId').prop("readonly", true);
    
                        $('#shipPrjCode').val(response.shipment_list.prj_code[0]);
                        $('#shipCustomer').val(response.shipment_list.customer[0]);
                        
                        $("#shipmentEntryTable > thead").prepend(`
                        <tr class="text-center">
                            <th width="5%">ID</th>
                            <th>Item Code</th>
                            <th width="13%">Ship Date</th>
                            <th width="15%">Description</th>
                            <th width="20%">Maker P/N</th>
                            <th>S/P</th>
                            <th>Ship Qty</th>
                        </tr>
                        `)
                        for (i = 0; i < dataLength; i++) {
                            $("#shipmentEntryTable > tbody:last-child").append(`  
                            <tr>
                                <input id="orderId-${i}" class="form-control" type="hidden" name="orderId" readonly=True >
                                <td><input id="id-${i}" class="form-control" type="text" name="shipId" readonly=True></td>
                                <td><input id="shipItem-${i}" class="form-control" type="text" name="shipItem" maxlength="5" readonly=True ></td>
                                <td><input id="shipDate-${i}" class="form-control" type="text" name="shipDate2" maxlength="10"></td>
                                <td><input id="shipPName-${i}" class="form-control form-control" type="text" readonly=True></td>
                                <td><input id="shipPNo-${i}" class="form-control" type="text" readonly=True></td>
                                <td><input id="shipSp-${i}" class="form-control" type="text" readonly=True></td>
                                <td><input id="shipQty-${i}" class="form-control"  type="text" name="shipQty" data-id="${i}"></td>
                            </tr>
                            `)
                            $(`#orderId-${i}`).val(response.shipment_list.id_y[i]);
                            $(`#id-${i}`).val(response.shipment_list.id_x[i]);
                            $(`#shipItem-${i}`).val(response.shipment_list.item_code[i]);
                            $(`#shipDate-${i}`).val(response.shipment_list.shipped_date[i])
                            $(`#shipPName-${i}`).val(response.shipment_list.parts_name[i]);
                            $(`#shipPNo-${i}`).val(response.shipment_list.parts_number[i]);
                            $(`#shipSp-${i}`).val(response.shipment_list.sell_price[i]);
                            $(`#shipQty-${i}`).val(response.shipment_list.shipment_qty[i]);
                        }
                        $('input[name="shipQty"]').on('focus', function () {
                            let dataId = $(this).data('id')
                            $(`#shipQty-${dataId}`).on('input', function () {
                                if ( parseInt(response.shipment_list.shipment_qty[dataId]) < parseInt($(`#shipQty-${dataId}`).val())) {
                                    alert("Changed Qty must be less than Original Qty.");
                                    $(this).val("");
                                } else {
                                    return false
                                }
                            });
                            $(`#shipQty-${dataId}`).keypress(function (event) {
                                if (event.keyCode === 13) {
                                    if ($(`#shipQty-${dataId + 1}`).length === 1) {
                                        $(`#shipQty-${dataId + 1}`).focus();
                                    } else {
                                        $('#shipConfirm').focus();
                                    }
                                }
                            });
                        });
                    }
                },
                error: function () {
                    alert("Please input valid Order Number.");
                }
            });
        }
    });
    
    // Shipment Delete ---------------------
    $('#enter2').click(function () {
        if (mode === "3") {
            let shipOrderNumber = $('#shipOrderNumber').val();
            let orderId = $('#orderId').val();
            $('#orderNumCopy').val(shipOrderNumber);
            $.ajax({
                url: '/shipment-update-data-get/',
                type: 'get',
                data: {
                    'shipOrderNumber': shipOrderNumber,
                    'orderId': orderId
                },
                dataType: 'json',
                success: function (response) {
                    let dataLength = Object.keys(response.shipment_list.id_x).length;
                    if (dataLength === 0) {
                        alert("Please input valid Order ID. Shipment Data Does not exist.");
                    } else if (response.shipment_list.order_number[0] != shipOrderNumber) {
                        alert("Input Order No and ID does not match.");
                    } else {
                        modeBlock();
                        btnShowUp();
                        $('#enter2').hide();
                        $('#shipOrderNumber').prop("readonly", true);
                        $('#orderId').prop("readonly", true);

                        $('#shipPrjCode').val(response.shipment_list.prj_code[0]);
                        $('#shipCustomer').val(response.shipment_list.customer[0]);
                        
                        $("#shipmentEntryTable > thead").prepend(`
                        <tr class="text-center">
                            <th colspan="2" width="5%">ID</th>
                            <th>Item Code</th>
                            <th width="13%">Ship Date</th>
                            <th width="15%">Description</th>
                            <th width="20%">Maker P/N</th>
                            <th>S/P</th>
                            <th>Ship Qty</th>
                        </tr>
                        `)
                        for (i = 0; i < dataLength; i++) {
                            $("#shipmentEntryTable > tbody:last-child").append(`  
                            <tr id=${i}>
                                <input id="orderId-${i}" class="form-control" type="hidden" name="orderId" readonly=True>
                                <input id="deleteCheckNum-${i}" type="hidden" name="deleteCheckNum" value="0">
                                <td class="delete-check-box"><input id="deleteCheck-${i}" class="check-box" type="checkbox" data-id="${i}" name="deleteCheck" value="0"></td>
                                <td><input id="id-${i}" class="form-control" type="text" name="shipId" readonly=True></td>
                                <td><input id="shipItem-${i}" class="form-control" type="text" name="shipItem" maxlength="5" readonly=True ></td>
                                <td><input id="shipDate-${i}" class="form-control" type="text" name="shipDate2" maxlength="10" readonly=True></td>
                                <td><input id="shipPName-${i}" class="form-control form-control" type="text" readonly=True></td>
                                <td><input id="shipPNo-${i}" class="form-control" type="text" readonly=True></td>
                                <td><input id="shipSp-${i}" class="form-control" type="text" readonly=True></td>
                                <td><input id="shipQty-${i}" class="form-control"  type="text" name="shipQty" data-id="${i}" readonly=True></td>
                            </tr>
                            `)
                            $(`#orderId-${i}`).val(response.shipment_list.id_y[i]);
                            $(`#id-${i}`).val(response.shipment_list.id_x[i]);
                            $(`#shipItem-${i}`).val(response.shipment_list.item_code[i]);
                            $(`#shipDate-${i}`).val(response.shipment_list.shipped_date[i])
                            $(`#shipPName-${i}`).val(response.shipment_list.parts_name[i]);
                            $(`#shipPNo-${i}`).val(response.shipment_list.parts_number[i]);
                            $(`#shipSp-${i}`).val(response.shipment_list.sell_price[i]);
                            $(`#shipQty-${i}`).val(response.shipment_list.shipment_qty[i]);
                        }
                        deleteCheck();
                    }
                },
                error: function () {
                    alert("Please input valid Order Number.");
                }
            });
        }
    });
                        

    // Shipment Confirm --------------------
    $('#shipConfirm').click(function () {
        if (mode === "1") {
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
        } else if (mode === "2") {
            let serializedData = $('#shipmentEntryForm').serialize();        
            if (!confirm('Do you Proceed?')) {
                return false;
            } else {
                $.ajax({
                    url: '/shipment-update-confirm/',
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
        } else if (mode === "3") {       
            if (!confirm('Do you Delete Checked Line?')) {
                return false;
            } else {
                let serializedData = $('#shipmentEntryForm').serialize();
                $.ajax({
                    url: '/shipment-delete-confirm/',
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
        }
    });
    // -------------------------------------


// Acceptance ////////////////////////////////////////////////////////////////////////////////////
    $('#acceptOrderNumber').keypress(function (event) {
        if (event.keyCode === 13) {
            if (mode === "1") {        
                $('#acceptDate').focus();
                $('#acceptDate').on('input',function (event) {
                    let acceptDate = $('input[name="acceptDate"]');
                    let next = $('#enter4');
                    dateValidation(acceptDate, next);
                });        
            } else if (mode === "2" || mode === "3") {    
                $('#orderId').focus();
                $('#orderId').keypress(function (event) {
                    if (event.keyCode === 13) {
                        $('#enter4').focus();
                    }
                });
            } 
        }
    });

    // Acceptance New ---------------------
    $('#enter4').click(function () {
        if (mode === "1") {
            let acceptOrderNumber = $('#acceptOrderNumber').val();
            let supplier = $('#supplier').val();
            $('#orderNumCopy').val(acceptOrderNumber);
            $.ajax({
                url: '/acceptance-data-get/',
                type: 'get',
                data: {
                    'acceptOrderNumber': acceptOrderNumber,
                    'supplier': supplier
                },
                dataType: 'json',
                success: function (response) {
                    let dataLength = Object.keys(response.accept_order_list.id).length;
                    let isBalExit = 0;
                    $('#acceptPrjCode').val(response.accept_order_list.prj_code[0]);
                    
                    if (dataLength === 0) {
                        alert("Please input valid Order Number.");
                    } else {
                        for (i = 0; i < dataLength; i++) {
                            if (response.accept_order_list.balance[i] === 0) {
                                isBalExit += 1;
                                continue
                            } else {
                                $("#acceptanceEntryTable > tbody:last-child").append(`  
                                <tr>
                                    <input id="orderId-${i}" class="form-control" type="hidden" name="orderId" readonly=True >
                                    <td><input id="acceptItem-${i}" class="form-control" type="text" name="acceptItem" maxlength="5" readonly=True ></td>
                                    <td><input id="supplier-${i}" class="form-control" type="text" name="supplier" maxlength="" readonly=True ></td>
                                    <td><input id="acceptDate-${i}" class="form-control" type="text" name="acceptDate2" maxlength="10"></td>
                                    <td><input id="acceptPName-${i}" class="form-control form-control" type="text" readonly=True></td>
                                    <td><input id="acceptPNo-${i}" class="form-control" type="text" readonly=True></td>
                                    <td><input id="acceptBp-${i}" class="form-control" type="text" readonly=True></td>
                                    <td><input id="poBalance-${i}" class="form-control" type="text" readonly=True></td>
                                    <td><input id="acceptQty-${i}" class="form-control"  type="text" name="acceptQty" data-id="${i}"></td>
                                </tr>
                                `)
                                $(`#orderId-${i}`).val(response.accept_order_list.id[i]);
                                $(`#acceptItem-${i}`).val(response.accept_order_list.item_code[i]);
                                $(`#supplier-${i}`).val(response.accept_order_list.supplier[i]);
                                $(`#acceptDate-${i}`).val($('#acceptDate').val());
                                $(`#acceptPName-${i}`).val(response.accept_order_list.parts_name[i]);
                                $(`#acceptPNo-${i}`).val(response.accept_order_list.parts_number[i]);
                                $(`#acceptBp-${i}`).val(response.accept_order_list.sell_price[i]);
                                $(`#poBalance-${i}`).val(response.accept_order_list.balance[i]);
                            }
                        }

                        if (dataLength - isBalExit === 0) {
                            alert("No remaining PO Balance Exit.")
                            location.reload();
                        } else {
                            modeBlock();
                            btnShowUp();
                            $('#acceptOrderNumber').prop("readonly", true);
                            $('#acceptDate').prop("readonly", true);

                            $("#acceptanceEntryTable > thead").prepend(`
                            <tr class="text-center">
                                <th width="10%">Item Code</th>
                                <th width="15%">Supplier</th>
                                <th width="13%">Accept Date</th>
                                <th width="15%">Description</th>
                                <th width="20%">Maker P/N</th>
                                <th>B/P</th>
                                <th width="10%">PO Bal</th>
                                <th width="10%">Accept Qty</th>
                            </tr>
                            `)
                            $('#enter4').hide();
                        }

                        $('input[name="acceptQty"]').on('focus', function () {
                            let dataId = $(this).data('id')
                            $(`#acceptQty-${dataId}`).on('input', function () {
                                if (parseInt(response.accept_order_list.balance[dataId]) < parseInt($(`#acceptQty-${dataId}`).val())) {
                                    alert("Accept Qty must be less than PO Balance.");
                                    $(this).val("");
                                } else {
                                    return false
                                }
                            });
                            $(`#acceptQty-${dataId}`).keypress(function (event) {
                                if (event.keyCode === 13) {
                                    if ($(`#acceptQty-${dataId + 1}`).length === 1) {
                                        $(`#acceptQty-${dataId + 1}`).focus();
                                    } else {
                                        $('#acceptConfirm').focus();
                                    }
                                }
                            });
                        });
                    }
                },
                error: function () {
                    alert("Please input valid Order Number.");
                }
            });
        }
    });

    // Acceptance Update ---------------------
    $('#enter4').click(function () {
        if (mode === "2") {
            let acceptOrderNumber = $('#acceptOrderNumber').val();
            let orderId = $('#orderId').val();
            $('#orderNumCopy').val(acceptOrderNumber);
            $.ajax({
                url: '/acceptance-update-data-get/',
                type: 'get',
                data: {
                    'acceptOrderNumber': acceptOrderNumber,
                    'orderId': orderId
                },
                dataType: 'json',
                success: function (response) {
                    let dataLength = Object.keys(response.acceptance_list.id_x).length;
                    $('#acceptPrjCode').val(response.acceptance_list.prj_code[0]);
                    if (response.acceptance_list.order_number[0] != acceptOrderNumber) {
                        alert("Input Order No and ID does not match.");
                    } else if (dataLength === 0) {
                        alert("Please input valid Order ID.");
                    } else {
                        modeBlock();
                        btnShowUp();
                        $('#enter4').hide();
                        $('#acceptOrderNumber').prop("readonly", true);
                        $('#orderId').prop("readonly", true);

                        $("#acceptanceEntryTable > thead").prepend(`
                        <tr class="text-center">
                            <th width="5%">ID</th>
                            <th width="10%">Item Code</th>
                            <th width="15%">Supplier</th>
                            <th width="15%">Accept Date</th>
                            <th width="15%">Description</th>
                            <th width="15%">Maker P/N</th>
                            <th width="10%">B/P</th>
                            <th width="10%">Accept Qty</th>
                        </tr>
                        `)
                        for (i = 0; i < dataLength; i++) {
                            $("#acceptanceEntryTable > tbody:last-child").append(`  
                            <tr>
                                <input id="orderId-${i}" class="form-control" type="hidden" name="orderId" readonly=True >
                                <td><input id="id-${i}" class="form-control" type="text" name="acceptId" readonly=True></td>
                                <td><input id="acceptItem-${i}" class="form-control" type="text" name="acceptItem" maxlength="5" readonly=True ></td>
                                <td><input id="supplier-${i}" class="form-control" type="text" name="supplier" maxlength="" readonly=True ></td>
                                <td><input id="acceptDate-${i}" class="form-control" type="text" name="acceptDate2" maxlength="10"></td>
                                <td><input id="acceptPName-${i}" class="form-control form-control" type="text" readonly=True></td>
                                <td><input id="acceptPNo-${i}" class="form-control" type="text" readonly=True></td>
                                <td><input id="acceptBp-${i}" class="form-control" type="text" readonly=True></td>
                                <td><input id="acceptQty-${i}" class="form-control"  type="text" name="acceptQty" data-id="${i}"></td>
                            </tr>
                            `)
                            $(`#orderId-${i}`).val(response.acceptance_list.id_y[i]);
                            $(`#id-${i}`).val(response.acceptance_list.id_x[i]);
                            $(`#acceptItem-${i}`).val(response.acceptance_list.item_code[i]);
                            $(`#supplier-${i}`).val(response.acceptance_list.supplier[i]);
                            $(`#acceptDate-${i}`).val(response.acceptance_list.accepted_date[i])
                            $(`#acceptPName-${i}`).val(response.acceptance_list.parts_name[i]);
                            $(`#acceptPNo-${i}`).val(response.acceptance_list.parts_number[i]);
                            $(`#acceptBp-${i}`).val(response.acceptance_list.buy_price[i]);
                            $(`#acceptQty-${i}`).val(response.acceptance_list.acceptance_qty[i]);
                        }


                        $('input[name="acceptQty"]').on('focus', function () {
                            let dataId = $(this).data('id')
                            $(`#acceptQty-${dataId}`).on('input', function () {
                                let acceptedQty = parseInt(response.acceptance_list.acceptance_qty[dataId]);
                                let poBal = parseInt(response.acceptance_list.balance[dataId]);
                                let changedQty = parseInt($(`#acceptQty-${dataId}`).val());
                                if ( acceptedQty < changedQty) {
                                    if ((poBal + acceptedQty) < changedQty) {
                                        alert("Changed Qty must be less than remaining PO Bal.");
                                        $(this).val("");
                                    }
                                    //     else {
                                    //     alert("Changed Qty must be less than remaining Original Qty.");
                                    //     $(this).val("");
                                    // }   
                                } else {
                                    return false
                                }
                            });
                            $(`#acceptQty-${dataId}`).keypress(function (event) {
                                if (event.keyCode === 13) {
                                    if ($(`#acceptQty-${dataId + 1}`).length === 1) {
                                        $(`#acceptQty-${dataId + 1}`).focus();
                                    } else {
                                        $('#acceptConfirm').focus();
                                    }
                                }
                            });
                        });
                    }
                },
                error: function () {
                    alert("Please input valid Order Number.");
                }
            });
        }
    });

    // Acceptance Delete --------------------
    $('#enter4').click(function () {
        if (mode === "3") {
            let acceptOrderNumber = $('#acceptOrderNumber').val();
            let orderId = $('#orderId').val();
            $('#orderNumCopy').val(acceptOrderNumber);
            $.ajax({
                url: '/acceptance-update-data-get/',
                type: 'get',
                data: {
                    'acceptOrderNumber': acceptOrderNumber,
                    'orderId': orderId
                },
                dataType: 'json',
                success: function (response) {
                    let dataLength = Object.keys(response.acceptance_list.id_x).length;
                    $('#acceptPrjCode').val(response.acceptance_list.prj_code[0]);
                    if (dataLength === 0) {
                        alert("Please input valid Order ID. Acceptance Data Does not exist"); 
                    } else if (response.acceptance_list.order_number[0] != acceptOrderNumber) {
                        alert("Input Order No and ID does not match.");
                    } else {
                        modeBlock();
                        btnShowUp();
                        $('#enter4').hide();
                        $('#acceptOrderNumber').prop("readonly", true);
                        $('#orderId').prop("readonly", true);

                        $("#acceptanceEntryTable > thead").prepend(`
                        <tr class="text-center">
                            <th colspan="2" width="5%">ID</th>
                            <th width="10%">Item Code</th>
                            <th width="15%">Supplier</th>
                            <th width="15%">Accept Date</th>
                            <th width="15%">Description</th>
                            <th width="15%">Maker P/N</th>
                            <th width="10%">B/P</th>
                            <th width="10%">Accept Qty</th>
                        </tr>
                        `)
                        for (i = 0; i < dataLength; i++) {
                            $("#acceptanceEntryTable > tbody:last-child").append(`  
                            <tr id=${i}>
                                <input id="orderId-${i}" class="form-control" type="hidden" name="orderId" readonly=True>
                                <input id="deleteCheckNum-${i}" type="hidden" name="deleteCheckNum" value="0">
                                <td class="delete-check-box"><input id="deleteCheck-${i}" class="check-box" type="checkbox" data-id="${i}" name="deleteCheck" value="0"></td>
                                <td><input id="id-${i}" class="form-control" type="text" name="acceptId" readonly=True></td>
                                <td><input id="acceptItem-${i}" class="form-control" type="text" name="acceptItem" maxlength="5" readonly=True ></td>
                                <td><input id="supplier-${i}" class="form-control" type="text" name="supplier" maxlength="" readonly=True ></td>
                                <td><input id="acceptDate-${i}" class="form-control" type="text" name="acceptDate2" maxlength="10" readonly=True></td>
                                <td><input id="acceptPName-${i}" class="form-control form-control" type="text" readonly=True></td>
                                <td><input id="acceptPNo-${i}" class="form-control" type="text" readonly=True></td>
                                <td><input id="acceptBp-${i}" class="form-control" type="text" readonly=True></td>
                                <td><input id="acceptQty-${i}" class="form-control"  type="text" name="acceptQty" data-id="${i}" readonly=True></td>
                            </tr>
                            `)
                            $(`#orderId-${i}`).val(response.acceptance_list.id_y[i]);
                            $(`#id-${i}`).val(response.acceptance_list.id_x[i]);
                            $(`#acceptItem-${i}`).val(response.acceptance_list.item_code[i]);
                            $(`#supplier-${i}`).val(response.acceptance_list.supplier[i]);
                            $(`#acceptDate-${i}`).val(response.acceptance_list.accepted_date[i])
                            $(`#acceptPName-${i}`).val(response.acceptance_list.parts_name[i]);
                            $(`#acceptPNo-${i}`).val(response.acceptance_list.parts_number[i]);
                            $(`#acceptBp-${i}`).val(response.acceptance_list.buy_price[i]);
                            $(`#acceptQty-${i}`).val(response.acceptance_list.acceptance_qty[i]);
                        }
                        deleteCheck();
                    }
                },
                error: function () {
                    alert("Please input valid Order Number.");
                }
            });
        }
    });


    // Acceptance Confirm --------------------
    $('#acceptConfirm').click(function () {
        if (mode === "1") {
            let serializedData = $('#acceptanceEntryForm').serialize();        
            if (!confirm('Do you Proceed?')) {
                return false;
            } else {
                $.ajax({
                    url: '/acceptance-complete/',
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
        } else if (mode === "2") {
            let serializedData = $('#acceptanceEntryForm').serialize();        
            if (!confirm('Do you Proceed?')) {
                return false;
            } else {
                $.ajax({
                    url: '/acceptance-update-confirm/',
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
        } else if (mode === "3") {
            if (!confirm('Do you Delete Checked Line?')) {
                return false;
            } else {
                let serializedData = $('#acceptanceEntryForm').serialize();
                $.ajax({
                    url: '/acceptance-delete-confirm/',
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
        }
    });
    // -------------------------------------

// Order Info ////////////////////////////////////////////////////////////////////////////////////
    // Sorting Order Information ------------
    $('#dateS').on('input', function (event) {
        let date = $('#dateS');
        let next = $('#dateE');
        dateValidation(date, next);          
    });
    
    $('#dateE').on('input',function (event) {
        let date = $('#dateE');
        let next = $('#enter3');
        dateValidation(date, next);
    });

});



    /*
    // "Order Confirm modal" 停止---------------------------
    $('#create').click(function () {
        let item, qty, suppDate, custDate
        let order = {}; 
        for (i = 1; i <= 5; i++) {
            if ($(`#item-${i}`).val() !== "" && $(`#qty-${i}`).val() !== "") {
                item = $(`#item-${i}`).val();
                qty = $(`#qty-${i}`).val();
                suppDate = $(`#suppDate-${i}`).val();
                custDate = $(`#custDate-${i}`).val();
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
    */



    /*
    // modal close and modal content delete 停止
    $('#close').click(function () {
        $("#orderUpdateTable tbody").empty();
    });
    // modal close and modal content delete 停止
    $('#close').click(function () {
        $("#orderConfirmTable tbody").empty();
    });
    */



 /* 停止
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
                url: '/order-info/',
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
*/

/* 停止
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
*/