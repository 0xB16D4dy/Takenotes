const deleteNote = (noteId) => {
    fetch("/delete-note", {
        method: "POST",
        body: JSON.stringify({note_id: noteId}),
    }).then( (response)=>{
        window.location.href = "/";
    });
}

const enterSearch = function() {
    fetch("/search", {
        method: "GET",
        body: JSON.stringify({note_id: noteId}),
    }).then( (response)=>{
        window.location.href = "/";
    });
}