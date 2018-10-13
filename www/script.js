function init() {
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
           a = JSON.parse(xhr.responseText)
           for (var i = 0; i < a.length; i++) {
                temp = document.createElement("option")
                temp.text = a[i]["name"];
                temp.value = "pl_id=" + a[i]["id"] + "&pl_name=" + a[i]["name"]
                document.getElementById("playlists").add(temp)
           }
        }
    }
    xhr.open("GET", "/playlists", true);
    xhr.send()
}


function add() {
    text = document.getElementById("song_text").value;
    pl_data = document.getElementById("playlists").value;
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
           document.getElementById("output").innerHTML = xhr.responseText;
        }
    }
    xhr.open("POST", "/add", true);
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    text = "query=" + text + "&" + pl_data
    xhr.send(text);
}

function search() {
    text = document.getElementById("song_text").value;
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            output = JSON.parse(xhr.responseText)
            for (var i = 0; i < output.length; i++){
                document.getElementById("output").innerHTML += output[i] + "</br>"
            }
        }
    }
    xhr.open("POST", "/search", true);
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    text = "query=" + text
    xhr.send(text);
}