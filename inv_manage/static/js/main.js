// Hide parent of clicked item
$('.close-parent').on('click', function(){
    $(this).parent().addClass('hide');
}) 

function showNewTypeModal(){
    let type_modal = $("#new-type-modal");
    $(type_modal).removeClass("hide");
    $(type_modal).parent().removeClass('hide hidden')
}

function hideNewTypeModal(){
    let type_modal = $("#new-type-modal");
    $(type_modal).addClass("hide");
    $(type_modal).parent().addClass('hide hidden')
}

function showMessage(messageType, message){
    let ajm = $('#ajax-message');
    $(ajm).parent().removeClass('hide hidden');
    $(ajm).addClass('message-' + messageType)
    $(ajm).text(message);
}

if(make_active){
    $('#' + make_active).addClass('active');
}

$('.close-modal').on('click', function(){
        $('.modal-cont').addClass('hide');
        setTimeout(()=>{
            $('.modal-cont').addClass('hidden');
        }, 300);
})

$("#add-type").on('click', showNewTypeModal)