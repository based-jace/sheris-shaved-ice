let subButtons = document.getElementsByClassName('single-delete');
let groupDeleteButton = document.getElementById('delete-selected');
let checkAll = document.getElementById('check-all');
let numItemsSelected = $('#num-selected-items');

//Gets a cookie based on the cookies name
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

//gets all the selected checkboxes and returns them
function getSelectedCheckboxes(){
    let checkboxes = [];
    for(let i = 0; i < boxes.length;++i){
        if(boxes[i].checked == true){
            checkboxes.push(boxes[i].value);
        }
    }
    return checkboxes;
}

function removeItem(box){
    for(i in table_items){
        if(table_items[i]['id'] == box.value){
            table_items.splice(i,1); 
            num_items--;
            box.checked = false;
        }
    }
}

function removeItems(){
    for(i in boxes){
        if(boxes[i].checked == true){
            table_items.splice(i,1);   
            boxes[i].checked = false;
            num_items--;
        }
    }
}

//uses ajax to delete an item out of the database
function deleteItem(box){
    $.ajax({
        type:"POST",
        url:window.location.href,                
        data:{
            'checkbox[]':box.value,
            csrfmiddlewaretoken: getCookie('csrftoken')
        },
        success:function(data){
            removeItem(box);
            refreshTable();
    },
        failure:function(data){
            alert('Theres a problem');
        }
    })
}

function refreshTable(){
    updateVue();
    numerateRows();
    last_page = Math.floor(num_items / 10);
    checkPage();
}

function deleteItems(){
    checkboxes = getSelectedCheckboxes()
    $.ajax({
        type:"POST",
        url:window.location.href,                
        data:{
            'checkbox':checkboxes,
            csrfmiddlewaretoken: getCookie('csrftoken')
        },
        success:function(data){
            removeItems();
            refreshTable();
    },
        failure:function(data){
            alert('Theres a problem');
        }
    })
}

// The only way I could figure out how to get the boxes working without fucking up
function javascriptSucks(){
    $(numItemsSelected).text(getSelectedCheckboxes().length);
}

function makeBoxesWork(){
    for(box of boxes){
        box.addEventListener('click', javascriptSucks);
    }
}

//sets up all the buttons with their click events
function setUpButtons(){
    boxes = document.getElementsByName('checkbox');
    subButtons = document.getElementsByClassName('single-delete');
    groupDeleteButton = document.getElementById('delete-selected');

    for(let i = 0; i < subButtons.length;++i){
        subButtons[i].onclick = function(){
            deleteItem(boxes[i]);
        };
    }
    groupDeleteButton.onclick = deleteItems;    
}


checkAll.addEventListener('click', ()=>{
    if(checkAll.checked == true){
        for(box of boxes){
            box.checked = true;
        }
    }
    else{
        for(box of boxes){
            box.checked = false;
        }
    }
    javascriptSucks();
})

// Sets up checkboxes
for(b in 'button.pagination'){
    $('button.pagination').on('click', ()=>{
        $(numItemsSelected).text(0);
        setUpButtons();
        makeBoxesWork();
        checkAll.checked = false;
        for(box of boxes){
            box.checked = false;
        }
    });
}

makeBoxesWork();
setUpButtons();