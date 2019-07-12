async function likeCafes(){
    let response = await axios.get(`/api/likes?cafe_id=${window.location.pathname.split("/")[2]}`)
    if (response.data.likes){
        $("#liked").text("Liked")
        $("#liked").addClass("btn-primary")
    } else {
        $("#liked").text("Like")
        $("#liked").addClass("btn-outline-primary")
    }
}

likeCafes();

async function likeNewCafe(){
    let response = await axios.post("/api/like", {"cafe_id": window.location.pathname.split("/")[2]})
    if (response.data.liked){
        $("#liked").removeClass("btn-outline-primary")
        $("#liked").text("Liked")
        $("#liked").addClass("btn-primary")
    }
}


async function unLikeCafe(){
    let response = await axios.post("/api/unlike", {"cafe_id": window.location.pathname.split("/")[2]})
    $("#liked").removeClass("btn-primary")
    if (response.data.unliked){
        $("#liked").removeClass("btn-primary")
        $("#liked").text("Like")
        $("#liked").addClass("btn-outline-primary")
    }    
}



$("#liked").on('click', function(evt){
    // debugger;
    if($("#liked").text() === "Like"){
        likeNewCafe()
    } else {
        unLikeCafe()
    }
})