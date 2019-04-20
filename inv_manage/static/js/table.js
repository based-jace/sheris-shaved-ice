let num_items = table_items.length; // Total number of items
let current_items = table_items.slice(0,10); // Items shown in table

// Width that changes the 'quantity' column label to '#'
let quantWidth = window.matchMedia("(max-width: 760px)");

// For pagination
// Buttons that clicking on changes the table page
let left_pag_buttons = document.getElementsByClassName("left-table-page");
let right_pag_buttons = document.getElementsByClassName("right-table-page"); 
let curr_page = 0; // First page

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
    if (quantWidth.matches){
        qc.text("#");
    }
    else{
        qc.text("quantity");
    }
}
window.addEventListener('resize', replaceQuant) // 

// returns a function that sorts by the column you clicked on
// I fucking hate javascript
function sortClick(column){
    return function(){
        col_name = [$(column).attr('sort-name')].toString(); // Column name to sort by

        // sort comparison function
        function compare(a, b){
            a = a[col_name];
            b = b[col_name];
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
    }
}

// Adds table sort method to columns
for(column of sort_columns){
    column.addEventListener('click', sortClick(column))
};

// Allows pagination from left page buttons
for(btn of left_pag_buttons){
    btn.addEventListener('click', ()=>{
        if(curr_page > 0){ // If greater than first page
            curr_page--; // Go back a page
            let item_start = curr_page * 10; // Items to start from
            vue.items = table_items.slice(item_start, item_start + 10) // Sets table rows to show
        }
    })
}

// Allows pagination from right page buttons
for(btn of right_pag_buttons){
    btn.addEventListener('click', ()=>{
        if(curr_page < Math.floor(num_items / 10)){ // If less than last page
            curr_page++; // Go up a page
            let item_start = curr_page * 10; // Items to start from
            vue.items = table_items.slice(item_start, item_start + 10) // Sets table rows to show
        }
    })
}

