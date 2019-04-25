// Hide parent of clicked item
$('.close-parent').on('click', function(){
    $(this).parent().addClass('hide');
    $(this).addClass('hide');
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
