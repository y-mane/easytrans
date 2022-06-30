
const Allbtnsucess = document.querySelectorAll(".btn-success")
const Allbtnsdanger = document.querySelectorAll(".btn-danger")
const Allbtnsprimary = document.querySelectorAll(".btn-assign")
const voyageInput = document.getElementById("voyage")
console.log(Allbtnsucess)


Allbtnsucess.forEach((btnsuccess) => {
    btnsuccess.addEventListener("click",function(){
        swal("Bon travail!", "commande validée !", "success");
        
      
    })
})





Allbtnsdanger.forEach((btndanger) => {
    btndanger.addEventListener("click",function(e){
        const voyage_id = e.target.attributes.getNamedItem('data-voyage_id').value
        swal({
            title: "Voulez-vous supprimé cette commande?",
            text: "",
            icon: "warning",
            buttons:["annuler","oui"],
            dangerMode: true,
          })
          .then((willDelete) => {
            if (willDelete) {
                
              swal("Poof! Your imaginary file has been deleted!", {
                icon: "success",
              });
            } else {
                console.log("annulé")
            //   swal("Your imaginary file is safe!");
            }
          });
    })
})

/*let button_valide = document.querySelector(".btn-valid ");
let button_decline = document.querySelector(".btn-decline");
button.disabled = true;
button_valide.addEventListener("change", stateHandle);
function stateHandle() {
  if (document.querySelector(".btn-valid").value === "") {
    button_decline.disabled = true; 
  } else {
    button_decline.disabled = false;
  }
}*/