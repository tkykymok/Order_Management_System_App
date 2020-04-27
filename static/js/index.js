// let csrfToken = $('input[name=csrfmiddlewaretoken]').val();
$(document).ready(function () {
    var csrfToken = $('input[name=csrfmiddlewaretoken]').val();

    let mode = "1"; // 1:new 2:change 3:delete
    
    console.log(mode);

    //"Check Box" ---------------------------
    $('#chkbox1').on('click', function () { 
        if ($('#chkbox2').prop('checked') === true || $('#chkbox3').prop('checked')===true ) {
            $('#chkbox2').prop('checked', false); 
            $('#chkbox3').prop('checked', false); 
            $('#prjCode').prop('readonly', false);
            $('#suppDate').prop('readonly', false);
            $('#custDate').prop('readonly', false);
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
        } else {
            return false
        }
    });
    
    $('#check-box').on('click','input[name="chkbox"]', function () { 
        mode = $(this).val();
        console.log(mode);
    });

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
            modeChkBoxDiabled();
            let serializedData = $('#createOrderNumber').serialize();
            $.ajax({
                url: '/order-number-create/',
                data: serializedData,
                type: 'post',
                dataType: 'json',
                success: function (response) {
                    let orderNumber = $('#orderNumber').val();
                    let prjCode = $('#prjCode').val();
                    let lineCount = 0;

                    $('#orderNumCopy').val(orderNumber);
                    $('#prjCodeCopy').val(prjCode);

                    $('#orderNumber').prop("readonly", true);
                    $('input[name="suppDelDate"]').prop("readonly", true);
                    $('input[name="custDelDate"]').prop("readonly", true);
                    $('#enter1').hide();
                    newLineAdd(lineCount);
                    lineCount += 5;

                    $('#lineAdd').css('display','block');
                    $('#lineDelete').css('display','block');
                
                    $('#lineAdd').click(function () {
                        newLineAdd(lineCount);
                        lineCount += 5;
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
                modeChkBoxDiabled();
                let serializedData = $('#createOrderNumber').serialize();
    
                $.ajax({
                    url: '/order-update-info-get/',
                    type: 'post',
                    data: serializedData,
                    dataType: 'json',
                    success: function (response) {
                        let orderNumber = $('#orderNumber').val();
                        let prjCode = $('#prjCode').val();
                        $('#orderNumCopy').val(orderNumber);
                        $('#prjCodeCopy').val(prjCode);
                        $('#enter1').hide();
    
                        console.log(response.order_list)
                        let data = response.order_list
                        let dataLength = Object.keys(response.order_list.id).length;
                        console.log(dataLength);
    
                        if (dataLength === 0) {
                            alert("This Order No does not exist.")
                            location.reload()
                        } else {
                            for (let i = 0; i < dataLength; i++){
                                $("#orderCreateTable > tbody:last-child").append(`
                                <tr id=${i}>
                                    <input id="order-${i}"  type="hidden" name="orderId"  maxlength="5">
                                    <td class="delete-check-box"><input id="deleteCheck-${i}" class="check-box" type="checkbox" name="deleteCheck" disabled=True maxlength="5"></td>
                                    <td><input id="item-${i}" class="form-control" type="text" name="item" maxlength="5" readonly=True></td>
                                    <td><input id="suppDate-${i}" class="form-control" type="text" name="suppDate" maxlength="10"></td>
                                    <td><input id="custDate-${i}" class="form-control" type="text" name="custDate" maxlength="10"></td>
                                    <td><input id="pName-${i}" class="form-control form-control" type="text" readonly=True></td>
                                    <td><input id="pNo-${i}" class="form-control" type="text" readonly=True></td>
                                    <td><input id="sp-${i}" class="form-control" type="text" readonly=True></td>
                                    <td><input id="bp-${i}" class="form-control" type="text" readonly=True></td>
                                    <td><input id="qty-${i}" class="form-control"  type="text" name="qty" data-id="${i}"></th>
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
                modeChkBoxDiabled();
                let serializedData = $('#createOrderNumber').serialize();
    
                $.ajax({
                    url: '/order-update-info-get/',
                    type: 'post',
                    data: serializedData,
                    dataType: 'json',
                    success: function (response) {
                        let orderNumber = $('#orderNumber').val();
                        let prjCode = $('#prjCode').val();
                        $('#orderNumCopy').val(orderNumber);
                        $('#prjCodeCopy').val(prjCode);
                        $('#enter1').hide();
    
                        console.log(response.order_list)
                        let data = response.order_list
                        let dataLength = Object.keys(response.order_list.id).length;
                        console.log(dataLength);
    
                        if (dataLength === 0) {
                            alert("This Order No does not exist.")
                            location.reload()
                        } else {
                            for (let i = 0; i < dataLength; i++){
                                $("#orderCreateTable > tbody:last-child").append(`
                                <tr id=${i}>
                                    <input id="order-${i}"  type="hidden" name="orderId"  maxlength="5">
                                    <td class="delete-check-box"><input id="deleteCheck-${i}" class="check-box" type="checkbox" name="deleteCheck" maxlength="5"></td>
                                    <td><input id="item-${i}" class="form-control" type="text" name="item" maxlength="5" readonly=True></td>
                                    <td><input id="suppDate-${i}" class="form-control" type="text" name="suppDate" maxlength="10"></td>
                                    <td><input id="custDate-${i}" class="form-control" type="text" name="custDate" maxlength="10"></td>
                                    <td><input id="pName-${i}" class="form-control form-control" type="text" readonly=True></td>
                                    <td><input id="pNo-${i}" class="form-control" type="text" readonly=True></td>
                                    <td><input id="sp-${i}" class="form-control" type="text" readonly=True></td>
                                    <td><input id="bp-${i}" class="form-control" type="text" readonly=True></td>
                                    <td><input id="qty-${i}" class="form-control"  type="text" name="qty" data-id="${i}"></th>
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
                            // "Order Delete confirm" ---------------------------
                            $('#confirm').click(function () {
                                    if (!confirm('Do you Delete Checked Order?')) {
                                        return false;
                                    } else {
                                        let dataLength = $('#orderCreateTable > tbody').children().length;
                                        // unchecked Line Delete --------------------------
                                        for (let i = 0; i < dataLength; i++) {
                                            if ($(`#orderCreateTable tr#${i} input[name="deleteCheck"]`).prop('checked') === false) {
                                                $(`#orderCreateTable tr#${i}`).remove()
                                            }
                                        }
                                        let serializedData = $('#orderContentForm').serialize();
                                        // -------------------------------------
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
    



    // "Item Info Get / Order Create" ----------------------
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
    // -------------------------------------
    
    // new Line add ----------------------------
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
    // -------------------------------------

    // Line Delete --------------------------
    $('#lineDelete').click(function () {
        let dataLength = $('#orderCreateTable > tbody').children().length;
        for (let i = 0; i < dataLength; i++) {
            if ($(`#orderCreateTable tr#${i} input[name="deleteCheck"]`).prop('checked') === true) {
                $(`#orderCreateTable tr#${i}`).remove()
            }
        }
    });
    // -------------------------------------

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

    // "Cancel and reload" -----------------------
    $('#cancel').click(function () {
        if (!confirm('Are you sure you want to Cancel?')) {
            return false;
        } else {
            location.reload(); 
        }
    });


    // modal close and modal content delete 停止
    $('#close').click(function () {
        $("#orderUpdateTable tbody").empty();
    });
    // modal close and modal content delete 停止
    $('#close').click(function () {
        $("#orderConfirmTable tbody").empty();
    });



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

                    $('#shipDate').on('input',function (event) {
                        let shipDate = $('input[name="shipDate"]');
                        let next3 = $('#enter2');
                        dateValidation(shipDate, next3);
                    });
                    let dataLength = response.order_data.length;
                    $('#enter2').click(function () {
                        let isOrderExit = 0;
                        for (i = 0; i < dataLength; i++) {
                            if (response.order_data[i].balance === 0) {
                                isOrderExit += 1;
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
                                    <td><input id="shipQty-${i}" class="form-control"  type="text" name="shipQty" data-id="${i}"></td>
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

                        if (dataLength - isOrderExit === 0) {
                            alert("No remaining Order Exit.")
                            location.reload();
                        } else {
                            $('#enter2').hide();
                        }

                        $('input[name="shipQty"]').on('focus', function () {
                            let dataId = $(this).data('id')
                         
                            $(`#shipQty-${dataId}`).on('input', function () { 
                                if (parseInt($(`#orderBal-${dataId}`).val()) < parseInt($(`#shipQty-${dataId}`).val())) {
                                    alert("Ship Qty must be less than PO Balance.");
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
    // -------------------------------------




    // Sorting Order Information ------------
    $('#sortOrderDateS').on('input',function (event) {
        let date = $('#sortOrderDateS');
        let next = $('#sortOrderDateE');
        dateValidation(date, next);          
    });
    
    $('#sortOrderDateE').on('input',function (event) {
        let date = $('#sortOrderDateE');
        let next = $('#enter3');
        dateValidation(date, next);
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
            return false
        }
    };
    //--------------------------------------

    function modeChkBoxDiabled() {
        $('#chkbox1').prop('disabled', true);
        $('#chkbox2').prop('disabled', true);
        $('#chkbox3').prop('disabled', true);
    }



});


