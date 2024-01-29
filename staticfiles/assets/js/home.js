top_tag_item_icon.addEventListener("click", () => {
    top_tag_item_icon.firstElementChild.classList.toggle("opened")
    let top_tag_more = document.querySelector(".hero-top_tag_more")

    if (top_tag_more.getBoundingClientRect().height) {
        top_tag_more.style.maxHeight = null
        top_tag_more.style.maxHeight = `0px`

        top_tag_more.style.margin = `0px`

    } else {
        top_tag_more.style.margin = `5px 0px`
        top_tag_more.style.maxHeight = `${top_tag_more.scrollHeight}px`
    }
})

let hero_top_closer = document.querySelectorAll(".hero-top_closer")
let hero_top_closer_bg = document.querySelector(".hero-top_closer.bg")
let hero_top_menu = document.querySelector(".hero-top_menu")

let top_sort_item_menu = document.querySelector(".hero-top_sort_item.menu")


hero_top_closer.forEach(closer => {
    closer.addEventListener("click", () => {
        hero_top_menu.classList.remove("opened")
        document.querySelector('body').style.overflowY = "scroll"
        hero_top_closer_bg.classList.remove("opened")
    })
});

top_sort_item_menu.addEventListener("click", () => {
    hero_top_menu.classList.add("opened")
    document.querySelector('body').style.overflowY = "hidden"
    hero_top_closer_bg.classList.add("opened")
})

hero_top_closer_bg.addEventListener("click", () => {
    hero_top_menu.classList.remove("opened")
    document.querySelector('body').style.overflowY = "scroll"
    hero_top_closer_bg.classList.remove("opened")
})


// Dynamic emoji 
let index = 0;
let emoji = document.querySelector("#emoji");
let emojies = ["fas fa-heart", "fas fa-thumbs-up", "fas fa-thumbs-down", "fas fa-bolt", "fas fa-fire", "fas fa-star"];
let colors = ["red","#6ea7e0","#6ea7e0", "orange", "orange", "orange"]
setInterval(function(){
    if(index == emojies.length){
        index = 0
    }
    emoji.style.transition = "all 0.3s"
    emoji.className = emojies[index];
    emoji.style.color = colors[index]
    index++
},3000)


let btns = document.querySelectorAll(".hero-top_sort_item");
let path = location.href.split("/")[location.href.split("/").length-1]





if(path == "new"){
    btns[0].classList.add("selected")
}else if(path == "fire"){
    btns[1].classList.add("selected")
}else if(path == "reactions"){
    btns[2].classList.add("selected")
}else if(path == "top"){
    btns[3].classList.add("selected")
}else{
    btns[0].classList.add("selected")
    btns[0].style.cursor = "not-allowed"
}