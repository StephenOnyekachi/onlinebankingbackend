
mini_menu = document.querySelector('.mini_menu');
// menu = document.querySelector('.menu');
// mini_menu.addEventListener("click", e =>{
//     if(menu.style.display === "none"){
//         menu.style.display = "block";
//     }
//     else{
//         menu.style.display = "none";
//     }
// })

mini_menu.onclick = function(){
    menu = document.querySelector('.menu_links')
    menu.classList.toggle('active')
}