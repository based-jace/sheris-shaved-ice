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
    for(let i = 0; i < orderList.options.length; ++i){
        splitdata = orderList.options[i].value.split(",");
        if(splitdata[1] == purchaseItem.Attribute){
            alert("Please update the item that's alread in the order.")
            return 0;
        }
    }

    if(purchaseItem.Quantity != "" && purchaseItem.Cost != ""){
        let option = document.createElement("option");
        option.text = items.options[attindex].text;
        option.value = "-2," + purchaseItem.Attribute +","+ purchaseItem.Quantity +","+ purchaseItem.Cost + ",0";
        orderList.add(option);
        setUpOrderOptions();
        return 0;
    }
    else{
        alert("Please fill out both the cost and quantity fields before adding or updating an item.");
        return -1;
    }
        
    
}

function loadEditField(){
    let selectedIndex = orderList.selectedIndex;
    selectedItem = orderList.options[selectedIndex];
    let data = selectedItem.value;
    let splitdata = data.split(",");
    for(let i = 0; i < itemNames.length;++i){
        if(itemNames[i].value == splitdata[1]){
            itemNames[i].selected = true;
        }
    }
    quantityField.value = parseInt(splitdata[2]);
    costField.value = parseFloat(splitdata[3]);
    // let data = self;
    // let splitdata = data.split(",");
    // for(let i = 0; i < itemNames.length;++i){
    //     if(itemNames[i].value == splitdata[1]){
    //         itemNames[i].selected = true;
    //     }
    // }
    // items.value = itemNames[splitdata[1] - 1].text;
    // quantityField.value = parseInt(splitdata[2]);
    // costField.value = parseFloat(splitdata[3]);
}

function setUpOrderOptions(){
    document.getElementById("submit-btn").onclick = function(){selectItems();}
    for(let i = 0;i < orderList.options.length;++i){
        orderList.options[i].onclick = function(){loadEditField()};
    }
}

function clearFields(){
    quantityField.value = "";
    costField.value = "";
}

function updateOrder(){
    let data = selectedItem.value;
    let splitData = data.split(",");
    let itemindex = items.selectedIndex;
    for(let i = 0; i < orderList.options.length; ++i){
        splitdata = orderList.options[i].value.split(",");
        if(splitdata[1] == items.options[itemindex].value && selectedItem != orderList.options[i]){
            alert("Please remove this item and update the item that is already in the order.")
            return 0;
        }
    }
    if(quantityField.value != "" && costField.value != ""){
        selectedItem.disabled = false;
        selectedItem.value = splitData[0] + "," + items.options[itemindex].value + "," + quantityField.value + "," + costField.value + ',0';
        selectedItem.text = items.options[itemindex].text;
        items.options[itemindex].selected = false;
    }
    else{
        alert("Please fill out both the cost and quantity fields before adding or updating an item.");
    }    
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
        orderList.options[i].disabled = false;
        orderList.options[i].selected = true;

    }
}

setUpOrderOptions();
document.getElementById("update-btn").onclick = function(){updateOrder()}
document.getElementById("rmv-btn").onclick = function(){removeItem();}
document.getElementById("add-btn").onclick = function(){additem();}
// document.getElementById("view-item-btn").addEventListener('click', ()=>{
//     loadEditField();
// });