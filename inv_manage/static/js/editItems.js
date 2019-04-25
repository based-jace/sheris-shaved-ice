let quantityField = document.getElementById("quantity");
let costField = document.getElementById("cost");
let itemNames = document.getElementsByClassName("itemNames");
let items = document.getElementById("attname");
let orderList = document.getElementById("orderlist");
//The order that is currently being edited.
let selectedItem;

//update = 0
//delete = -1
//create new = -2

function additem(){
    let attindex = items.selectedIndex;
    let purchaseItem = {
        Attribute:items.options[attindex].value,
        Quantity:document.getElementById("quantity").value,
        Cost:document.getElementById("cost").value
    }
    let option = document.createElement("option");
    option.text = items.options[attindex].text;
    option.value = "-2," + purchaseItem.Attribute +","+ purchaseItem.Quantity +","+ purchaseItem.Cost + ",0";
    orderList.add(option);
    setUpOrderOptions();
}

function loadEditField(self){
    selectedItem = self;
    let data = selectedItem.value;
    let splitdata = data.split(",");
    for(let i = 0; i < itemNames.length;++i){
        if(itemNames[i].value == splitdata[1]){
            itemNames[i].selected = true;
        }
    }
    quantityField.value = parseInt(splitdata[2]);
    costField.value = parseFloat(splitdata[3]);
}

function setUpOrderOptions(){
    for(let i = 0;i < orderList.options.length;++i){
        orderList.options[i].ondblclick = function(){loadEditField(orderList.options[i])};
    }
}

function updateOrder(){
    let data = selectedItem.value;
    let splitData = data.split(",");
    let itemindex = items.selectedIndex;
    selectedItem.disabled = false;
    selectedItem.value = splitData[0] + "," + items.options[itemindex].value + "," + quantityField.value + "," + costField.value + ',0';
    selectedItem.text = items.options[itemindex].text;
}

//TODO change to work with ajax and remove from the database as well.
function removeItem(){
    for(let i = 0; i < orderList.options.length; i++){
        if (orderList.options[i].selected == true){
            orderList.options[i].disabled = true;
            splitdata = orderList.options[i].value.split(",");
            orderList.options[i].value = splitdata[0] + "," + splitdata[1] + "," + splitdata[2] + "," + splitdata[3] + ',-1';
            orderList.options[i].selected = false;
        }
    }
}

function selectItems(){
    for(let i = 0; i < orderList.options.length;i++){
        orderList.options[i].selected = true;
        orderList.options[i].disabled = false;
    }
}

setUpOrderOptions();
document.getElementById("update-btn").onclick = function(){updateOrder()}
document.getElementById("rmv-btn").onclick = function(){removeItem();setUpOrderOptions();}
document.getElementById("add-btn").onclick = function(){additem();}