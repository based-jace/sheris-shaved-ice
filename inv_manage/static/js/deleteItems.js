let subButtons = document.getElementsByClassName('single-delete');
let groupDeleteButton = document.getElementById('delete-selected');
let boxes = document.getElementsByName('checkbox');

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
    let elem = box.parentElement.parentElement;
    elem.parentNode.removeChild(elem);
}



function removeItems(){
    let elements = [];
    for(let i = boxes.length-1; i >= 0;--i){
        if(boxes[i].checked == true){
            let elem = boxes[i].parentElement.parentElement;
            elem.parentNode.removeChild(elem);                   
        }
    }
}

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
            setUpButtons();
    },
        failure:function(data){
            alert('Theres a problem');
        }
    })
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
            
    },
        failure:function(data){
            alert('Theres a problem');
        }
    })
}

function setUpButtons(){
    subButtons = document.getElementsByClassName('single-delete');
    groupDeleteButton = document.getElementById('delete-selected');
    boxes = document.getElementsByName('checkbox');

    for(let i = 0; i < subButtons.length;++i){
        subButtons[i].onclick = function(){deleteItem(boxes[i]);};
    }
    groupDeleteButton.onclick = deleteItems;    
}

setUpButtons();