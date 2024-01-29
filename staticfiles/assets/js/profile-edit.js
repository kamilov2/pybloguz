let profile_edit_clear = document.querySelectorAll(".profile_edit-clear")
profile_edit_clear.forEach(clearer => {
    clearer.addEventListener("click", () => {
        input = clearer.parentElement.nextElementSibling
        clearer.classList.remove("changed")
        input.value = ""
    })
});
let all_inputs = document.querySelectorAll(".profile_edit-social_item input")

all_inputs.forEach(input => {
    input.addEventListener("keyup", () => {
        clearer = input.previousElementSibling.lastElementChild
        if (input.value) {
            clearer.classList.add("changed")
        } else {
            clearer.classList.remove("changed")
        }
    })
})

window.addEventListener("load", () => {
    all_inputs.forEach(input => {
        clearer = input.previousElementSibling.lastElementChild
        if (input.value) {
            clearer.classList.add("changed")
        } else {
            clearer.classList.remove("changed")
        }
    })
})