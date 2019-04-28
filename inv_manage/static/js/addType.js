let typeInput = document.getElementById("new-type-input");
let types = document.getElementById("type_id");

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

function addOption(data){
    let option = document.createElement("option");
    option.value = data.id;
    option.text = data.name;
    types.add(option);
}

function addType(){
    $.ajax({
        type:"POST",
        url:'/addtype',                
        data:{
            'name':typeInput.value,
            csrfmiddlewaretoken: getCookie('csrftoken')
        },
        success:function(data){
            addOption(data);
            hideNewTypeModal();
            showMessage('success', data.message)
    },
        failure:function(data){
            alert('Unable to add type');
        }
    })
}

document.getElementById("#submit-type").onclick = function(){addType();}