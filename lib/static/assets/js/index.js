const deleteNote = (noteId) => {
    fetch("/delete-note", {
        method: "POST",
        body: JSON.stringify({note_id: noteId}),
    }).then((response)=>{
        window.location.href = "/";
    });
<<<<<<< HEAD
}
=======
}


>>>>>>> 5e3d23b38fcb820341669c53871a5d5b0ad8fc3b
