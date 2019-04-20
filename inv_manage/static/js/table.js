let num_items = items.count;
let current_items = items.slice(0,10);

let quantWidth = window.matchMedia("(max-width: 760px)");

//TODO: Add pagination and the ability to sort descending
let sort_columns = document.getElementsByClassName("sort-column");

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

// I fucking hate javascript
function sortClick(column){
    return function(){
        function compare(a, b){
            console.log(a[$(column).attr('sort-name')])
            if (a[$(column).attr('sort-name')] > b[$(column).attr('sort-name')]){
                return 1;
            }
            if (a[$(column).attr('sort-name')] < b[$(column).attr('sort-name')]){
                return -1;
            }
            return 0;
        };
        items.sort(compare);
        vue.items = items.slice(0,10);
    }
}

for(column of sort_columns){
    console.log(column);
    column.addEventListener('click', sortClick(column))
};

window.addEventListener('resize', replaceQuant)