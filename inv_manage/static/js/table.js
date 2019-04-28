let boxes = document.getElementsByName('checkbox');

let num_items = table_items.length; // Total number of items
let current_items = table_items.slice(0,10); // Items shown in table

// Width that changes the 'quantity' column label to '#'
let quantWidth = 440;
let quantWatch = window.matchMedia("(max-width: " + quantWidth + "px)");

// For pagination
// Buttons that clicking on changes the table page
let left_pag_buttons = document.getElementsByClassName("left-table-page");
let right_pag_buttons = document.getElementsByClassName("right-table-page"); 
let curr_page = 0; // First page
let last_page = Math.floor(num_items / 10);

// For sorting
let sort_columns = document.getElementsByClassName("sort-column"); // columns to sort by
let curr_column = ''; // column currently sorting by
let ascend = true; // Sort ascending

// Allows table columns to be resizeable (from js colResizable)
table = $(function(){
    $("#data-table").colResizable({
        liveDrag: true,
        minWidth: 30
    })
});

// Vue Setup
vue = new Vue({
    delimiters: ['[[', ']]'],
    el: '#data-table',
    data: {
        items: current_items,
    }
});

// Function that changes quantity column label
function replaceQuant(){
    let qc = $('.quantity-column');
    if (quantWatch.matches){
        qc.text("Q");
    }
    else{
        qc.text("Quantity");
    }
}

// returns a function that sorts by the column you clicked on
// I fucking hate javascript
function sortClick(column){
    return function(){
        col_name = [$(column).attr('sort-name')].toString(); // Column name to sort by

        // sort comparison function
        function compare(a, b){
            a = a[col_name];
            b = b[col_name];
            if(a == null || b == null){
                if(a == null){
                    return -1;
                }
                else if (b == null){
                    return 1;
                }
                return 0;
            }

            if(typeof(a) != 'string'){
                if (a > b){
                    return 1;
                }
                if (a < b){
                    return -1;
                }
            }
            else{
                if (a.toLowerCase() > b.toLowerCase()){
                    return 1;
                }
                if (a.toLowerCase() < b.toLowerCase()){
                    return -1;
                }
            }
            return 0;
        };
        table_items.sort(compare);

        if(curr_column == col_name){ // If already sorting by
            if(ascend == true){ // If already sorting in ascending order
                ascend = false; // Now sort descending
                table_items = table_items.reverse() // ^
            }
            else{
                ascend = true;
            }
        }
        else{
            curr_column = col_name;
            ascend = true;
        }
        curr_page = 0; // Reset to first page
        vue.items = table_items.slice(curr_page, curr_page + 10); // Show first 10 items
        checkPage();
        numerateRows();
    }
}

// Adds table sort method to columns
for(column of sort_columns){
    column.addEventListener('click', sortClick(column))
};

function howManyItems(){
    return num_items == current_items[9].number;
}

function disablePagination(btn){
    btn.classList.add('disabled');
}
function enablePagination(btn){
    btn.classList.remove('disabled')
}
function checkPage(){
    for(page_number of $(".table-page-number")){
        $(page_number).text(curr_page + 1);
    }
    if(curr_page == 0){
        for(btn of left_pag_buttons){
            disablePagination(btn);
        }
    }
    else{
        for(btn of left_pag_buttons){
            enablePagination(btn);
        }
    }
    if(curr_page == last_page || howManyItems()){
        for(btn of right_pag_buttons){
            disablePagination(btn);
        }
    }
    else if(!howManyItems()){
        for(btn of right_pag_buttons){
            enablePagination(btn);
        }
    }
    
}

 // Sets table rows to show
function updateVue(){
    let item_start = curr_page * 10; // Items to start from
    vue.items = table_items.slice(item_start, item_start + 10)
}

function changePage(norp){
    if(norp > 0){
        curr_page++; // Go up a page
        updateVue();
    }
    else if(norp < 0){
        curr_page--; // Go back a page
        updateVue();
    }
    checkPage();
    numerateRows();
    document.getElementsByName('checkbox');
}

// Numerates Rows (C'mon, man)
function numerateRows(){
    temp_items = [];
    for(i in vue['items']){
        temp_items[i] = vue.items[i];
        temp_items[i]['number'] = (curr_page + 1) * 10 - 9 + Number(i); // Again, I hate javascript
    }
    vue.items = temp_items;
}

// ** INIT **

// Allows pagination from left page buttons
for(btn of left_pag_buttons){
    btn.addEventListener('click', ()=>{
        if(curr_page > 0){
            enablePagination(btn);
        }
        if(!btn.classList.contains('disabled')){
            if(curr_page > 0){ // If greater than first page
                changePage(-1);
            }
        }
    })
}

// Allows pagination from right page buttons
for(btn of right_pag_buttons){
    btn.addEventListener('click', ()=>{
        if(curr_page < last_page && !howManyItems()){
            enablePagination(btn);
        }

        if(!btn.classList.contains('disabled')){
            console.log(howManyItems());
            if(curr_page < last_page && !howManyItems()){ // If less than last page
                changePage(1);
            }
        }
    })
}

if ($(window).width() <= quantWidth){
    replaceQuant();
}
window.addEventListener('resize', replaceQuant) // 
numerateRows();
checkPage();
