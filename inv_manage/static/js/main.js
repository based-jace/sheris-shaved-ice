// Hide parent of clicked item
$('.close-parent').on('click', function(){
    $(this).parent().addClass('hide');
}) 

if(make_active){
    $('#' + make_active).addClass('active');
}

$('.close-modal').on('click', function(){
        $('.modal-cont').addClass('hide');
        setTimeout(()=>{
            $('.modal-cont').addClass('hidden');
        }, 300);
})

$("#add-type").on('click', ()=>{
    let type_modal = $("#new-type-modal");
    $(type_modal).removeClass("hide");
    $(type_modal).parent().removeClass('hide hidden')
})