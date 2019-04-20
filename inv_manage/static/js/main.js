// Hide parent of clicked item
$('.close-parent').on('click', function(){
    $(this).parent().addClass('hide');
    $(this).addClass('hide');
}) 

if(make_active){
    $('#' + make_active).addClass('active');
}
