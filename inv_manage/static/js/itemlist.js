let atts = document.getElementById("attname");
let orderlist = document.getElementById("orderlist");
let orderItems = [];
index = 0;

function additem(){
    attindex = document.getElementById("attname").selectedIndex;
    let purchaseItem = {
        Attribute:atts.options[attindex].value,
        Quantity:document.getElementById("quantity").value,
        Cost:document.getElementById("cost").value
    }
    orderItems[index] = purchaseItem;
    let option = document.createElement("option");
    option.text = atts.options[attindex].text;
    option.value = purchaseItem.Attribute +","+ purchaseItem.Quantity +","+ purchaseItem.Cost;
    orderlist.add(option);
    index++;
}

function selectItems(){
    orderlist = document.getElementById("orderlist");
    for(let i = 0; i < orderlist.options.length;i++){
        orderlist.options[i].selected = true;
    }
}

document.getElementById("add-btn").onclick = additem;
document.getElementById("submit-btn").onsubmit = selectItems;