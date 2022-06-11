// var btnDelete = document.getElementById("btnDelete")

const deleteNote = (noteId) => {
    fetch("/delete-note", {
        method: "POST",
        body: JSON.stringify({note_id: noteId}),
    }).then((response)=>{
        window.location.href = "/";
    });
}

const updateNote = (noteId) => {
    fetch("/update-note",{
        method: "POST",
        body: JSON.stringify({})
    }).then((response) =>{
        window.location.href = "/";
    });
}

