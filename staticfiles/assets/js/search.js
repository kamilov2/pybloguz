const result_wrapper = document.querySelector('.header-res_wrapper');
const result_title = document.querySelector(".header-res_heading");

function hideDefaultPosts(){
  let posts  = document.querySelectorAll("#default_posts")
  for(let i of posts){
    i.style.display = "none"
  }
}
function showDefaultPosts(){
  let posts  = document.querySelectorAll("#default_posts")
  for(let i of posts){
    i.style.display = "block"
  }
}

function hidePosts(){
  for(let el of result_wrapper.children){
    if(el.classList.contains("header-res_item")){
      el.style.display = 'none'
    }
  }
}

function fetchQueryData(query){
    let url = `/search/?query=${query}`
    if(query.length >= 0){
      fetch(url)
      .then(res => res.json())
      .then(data=>{
  
          if(data.data){
            hidePosts()
              for(let i=0; i<data.data.length;i++){
                let div = document.createElement('div'); div.className = 'header-res_item';
                let a = document.createElement('a'); a.className = 'header-res_item_link';  
                a.href = `/post/${data.data[i].slug}`;
                let img = document.createElement('img'); 
                img.className='header-res_item_img';
                img.src = `https://pyblog.uz/pybloguz/mediafiles/${data.data[i].image}`;
                let span = document.createElement("span")
                span.textContent = `${data.data[i].title}`;
                a.append(img)
                a.append(span)
                div.append(a)
  
                result_title.textContent = "Qidiruv natijalari"
                result_wrapper.appendChild(div)
              }            
          }else{
            let resultPosts = document.querySelectorAll('.header-res_item');
            resultPosts.forEach(el => {
              if(el.hasAttribute("id")){
                // pass 
              }else{
                el.style.display = "none" 
                hideDefaultPosts()              
                showDefaultPosts()
                result_title.textContent = "Yangi maqolalar"
              }
            })
          }
      })
    } // check query length

}