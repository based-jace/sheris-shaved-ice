let atts = document.getElementById("attname");
let orderlist = document.getElementById("orderlist");
let orderItems = [];
index = 0;

function additem(){
    let attindex = document.getElementById("attname").selectedIndex;
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

function removeItem(){
    let orderindex = document.getElementById("orderlist");
    for(let i = 0; i < orderindex.options.length; i++){
        if (orderindex.options[i].selected == true){
            orderindex.remove(orderindex.options.selectedIndex)
        }
    }
}

//document.getElementById("add-btn").onclick = additem; <- removed for form validation
document.getElementById("rmv-btn").onclick = removeItem;

// form validation
function checkForBlank() {
    if (document.getElementById('quantity').value == 0 || document.getElementById('cost').value == 0) {
        alert('Please enter an amount.');
    }
    else additem();
}