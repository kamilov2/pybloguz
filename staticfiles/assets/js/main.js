let user_switcher = document.querySelector(".header-user_switcher"),
    icon = document.querySelector(".header-user_switcher i"),
    header_close = document.querySelector(".header-close"),
    header_search_inner = document.querySelector(".header-search_inner"),
    header_search_opener = document.querySelector(".header-search_opener"),
    header_search_wrapper = document.querySelector(".header-search_wrapper"),
    header_res_wrapper = document.querySelector(".header-res_wrapper"),
    header_search_bg = document.querySelector(".header-search_bg"),
    top_tag_item_icon = document.querySelector(".hero-top_tag_item.icon"),
    content_bottom_detail_tooltip = document.querySelector(".hero-content_bottom_detail_tooltip")



window.addEventListener("DOMContentLoaded", () => {
    mode = localStorage.getItem("mode")
    icon_class = localStorage.getItem("icon_class")
    if (mode) {
        document.querySelector('html').classList.toggle(`${mode}`)
        icon.classList.remove("fa-sun")
        icon.classList.remove("fa-moon")
        icon.classList.add(`${icon_class}`)
    } else {
        icon.classList.remove("fa-sun")
        icon.classList.add("fa-moon")
    }
})

user_switcher.addEventListener("click", () => {
    document.querySelector('html').classList.toggle("dark")
    if (document.querySelector('html').className == "dark") {
        localStorage.setItem("mode", "dark")
        localStorage.setItem("icon_class", "fa-sun")
    } else {
        localStorage.setItem("mode", "")
        localStorage.setItem("icon_class", "fa-moon")
    }
    icon.classList.toggle("fa-sun")
    icon.classList.toggle("fa-moon")
})

header_close.addEventListener("click", () => {
    header_close.parentElement.classList.add("cleared")
    setTimeout(() => {
        header_close.parentElement.classList.add("noned")
    }, 300)
})

header_search_inner.addEventListener("click", () => {
    header_close.parentElement.classList.remove("noned")
    setTimeout(() => {
        header_close.parentElement.classList.remove("cleared")
    }, 300)
})

header_search_opener.addEventListener("click", () => {
    header_search_wrapper.classList.add("opened")
    header_res_wrapper.classList.add("opened")
    header_search_bg.classList.add("opened")
})

header_search_bg.addEventListener("click", () => {
    header_search_wrapper.classList.remove("opened")
    header_res_wrapper.classList.remove("opened")
    header_search_bg.classList.remove("opened")
})

let message = document.querySelector(".message")

let post_add_closer = document.querySelector(".post_add-closer")

if (post_add_closer) {
    post_add_closer.addEventListener("click", () => {
        post_add_closer.parentElement.classList.add("noned")

        setTimeout(() => {
            post_add_closer.parentElement.classList.add("displayed")
        }, 300);
    })
}


// POST REACTION
function postReact(post_id, react) {
    let url = "/react/" + `?post_id=${post_id}&react=${react}`;
  
    fetch(url)
      .then((res) => res.json())
      .then((data) => {
        if (data["status"] == 200) {
            message.classList.add("opened")
            message.children[0].textContent = data["wtf"]
  
          setInterval(() => {
            message.classList.remove("opened");
          }, 4000);
        }
      });
  }


  function clearMessage(el){
    el.parentElement.classList.remove("opened")
  }