const deleteNote = (noteId) => {
    fetch("/delete-note", {
        method: "POST",
        body: JSON.stringify({note_id: noteId}),
    }).then((response)=>{
        window.location.href = "/";
    });
}

const list = document.querySelectorAll('.list');
var loc = window.location.pathname;

function activeLink(){
    list.forEach((item) =>
    item.classList.remove('active'));
    
}
list.forEach((item) =>
item.addEventListener('click', activeLink));

if (loc == '/')
{
    var element = document.getElementById("nav-home");
    element.classList.add("active");
}
else if(loc == '/upload')
{
    var element = document.getElementById("nav-upload");
    element.classList.add("active");
}
else if(loc == '/search')
{
    var element = document.getElementById("nav-search");
    element.classList.add("active");
}
else if(loc == '/account')
{
    var element = document.getElementById("nav-account");
    element.classList.add("active");
}
else if(loc == '/logout')
{
    var element = document.getElementById("nav-logout");
    element.classList.add("active");
}
else if(loc == '/sigin')
{
    var element = document.getElementById("nav-login");
    element.classList.add("active");
}
else if(loc == '/signup')
{
    var element = document.getElementById("nav-register");
    element.classList.add("active");
}

var filename;
document.getElementById('inputGroupFile01').onchange = function () {
   filename = this.value.split(String.fromCharCode(92));
   document.getElementById("chooseFile").innerHTML = filename[filename.length-1];
};