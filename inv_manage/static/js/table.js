let num_items = items.count;
let current_items = items.slice(0,10);

let quantWidth = window.matchMedia("(max-width: 760px)");

//TODO: Add pagination
let sort_columns = document.getElementsByClassName("sort-column"); // columns to sort by
let curr_column = ''; // column currently sorting by
let ascend = true; // Sort ascending

table = $(function(){
    $("#data-table").colResizable({
        liveDrag: true,
        minWidth: 30
    })
});

vue = new Vue({
    delimiters: ['[[', ']]'],
    el: '#data-table',
    data: {
        items: current_items,
    }
});

function replaceQuant(){
    let qc = $('.quantity-column');
    if (quantWidth.matches){
        qc.text("#");
    }
    else{
        qc.text("quantity");
    }
}

// returns a function that sorts by the column you clicked on
// I fucking hate javascript
function sortClick(column){
    return function(){
        col_name = [$(column).attr('sort-name')].toString();

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
        items.sort(compare);
        if(curr_column == col_name){
            if(ascend == true){
                ascend = false;
                items = items.reverse()
            }
            else{
                ascend = true;
            }
        }
        else{
            curr_column = col_name;
            ascend = true;
        }

        vue.items = items.slice(0,10);
    }
}

for(column of sort_columns){
    column.addEventListener('click', sortClick(column))
};

window.addEventListener('resize', replaceQuant)