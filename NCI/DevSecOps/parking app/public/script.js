function myFunction() {
    let input, filter, tr, td, i, txtValue;
    input = document.getElementById("myInput");
    filter = input.value.toUpperCase();
    tr = document.querySelectorAll(".table tr");
    
    for (i = 1; i < tr.length; i++) {
        td = tr[i].getElementsByTagName("td")[0];
        if (td) {
            txtValue = td.textContent || td.innerText;
            if (txtValue.toUpperCase().indexOf(filter) > -1) {
                tr[i].style.display = "";
            } else {
                tr[i].style.display = "none";
            }
        }
    }
}

let buttonPro = document.querySelector("button.Pro");
buttonPro.addEventListener("click", function() {
    aftercheckout.style.display = "none";
    block.style.display = "";
    pay.style.display = "";
});