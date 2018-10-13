var maps, loc, me, mark, text = [];
var infoWindow
var song;
var hf;
var audio_context;
var recorder;
var markers = []
function startUserMedia(stream) {
        var input = audio_context.createMediaStreamSource(stream);
        __log('Media stream created.');
recorder = new Recorder(input);
__log('Recorder initialised.');
}

        
function init() {
    populate_drop_down()
    infoWindow = new google.maps.InfoWindow();
    maps = new google.maps.Map(document.getElementById('map'), {
      center: {lat: 42.4062336, lng: -71.1166001},
      zoom: 15, mapTypeControl: false, fullscreenControl: false
    });
    navigate()
}


function populate_drop_down() {
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

function navigate()
{
    if (navigator.geolocation)
    {
        navigator.geolocation.getCurrentPosition(function(position){
            loc = {lat: position.coords.latitude, lng: position.coords.longitude};
            maps.panTo(loc);
            add_markers()
        });
    }
    else
    {
        alert("Sorry! Your browser doesn't support geolocation");
    }
    
}

function add_markers() {
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
           a = JSON.parse(xhr.responseText)
           console.log(a)
           locations = []
           a.forEach(function(object){
              var location = new google.maps.LatLng(object.lat, object.long);
              var is_found = locations.find(function(x){
                return x.equals(location)
              });
              if (is_found){
                console.log("found repeat")
              }else {
                locations.push(location);
                //console.log("pushing " + location)
              }
                //console.log(locations);
           })
           console.log("second "+ locations);
           console.log(locations.length);

           a.forEach(function(object){
            var location = new google.maps.LatLng(object.lat, object.long);
            var index = 0
            for (var i = 0; i < locations.length; i++) {
                  if (location.equals(locations[i])) {
                    console.log("FOUND")
                    index = i
                  }
              }
              if(!text[i])
                text[i] = "<a href = 'https://open.spotify.com/playlist/"+object.pl_id+"'>"+object.pl_name+"</a> <br>";
              else
                text[i] += "<a href = 'https://open.spotify.com/playlist/"+object.pl_id+"'>"+object.pl_name+"</a> <br>" ;
           })

           console.log("here text " + text);
           console.log("text.length " + text.length)
           for (var i = 0; i < text.length; i++)
                text[i] = text[i+1]
            text.pop()
            console.log("text.length " + text.length)

           for (var i = 0; i < locations.length; i++) {
                console.log(text);
                var mark = new google.maps.Marker({position: locations[i], map: maps})
                markers.push(mark)
                add_info()
           }
           // a.forEach(function(object) {
           //      var location = new google.maps.LatLng(object.lat, object.long)
           //      var mark = new google.maps.Marker({position: location, map: maps})
           //      google.maps.event.addListener(mark, 'click', function(){
           //          infoWindow.setContent("<a href = 'https://open.spotify.com/playlist/"+object.pl_id+"'>"+object.pl_name+"</a>")
           //          infoWindow.open(maps, mark)
           //      })
           // })
        }
    }
    xhr.open("GET", "/locations", true);
    xhr.send()

}

function add_info() {
    markers.forEach(function(marker, index){
        google.maps.event.addListener(marker, 'click', function(){
            console.log("making marker")
            console.log(text[index])
            console.log(index)
            infoWindow.setContent(text[index])
            infoWindow.open(maps, marker)
        })
    })
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
    text = "query=" + text + "&" + pl_data + "&lat=" + loc.lat + "&long=" + loc.lng
    xhr.send(text);
}

function new_playlist() {
    text = document.getElementById("playlist_name").value;
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
           new_pl = JSON.parse(xhr.responseText);
           console.log(new_pl)
            temp = document.createElement("option")
            temp.text = new_pl["p_name"];
            temp.value = "pl_id=" + new_pl["p_id"] + "&pl_name=" + new_pl["p_name"]
            document.getElementById("playlists").add(temp)
        }
    }
    xhr.open("POST", "/new_playlist", true);
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    text = "query=" + text + "&lat=" + loc.lat + "&long=" + loc.lng
    xhr.send(text);
}

function search() {
    text = document.getElementById("song_text").value;
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            output = JSON.parse(xhr.responseText)
            var temp = ''
            output.forEach(function(out){
                temp += '<option value="' + out[1]+' - ' +out[0]+ '"/>';
            })
            document.getElementById("searchables").innerHTML = temp
            temp = ''
        }
    }
    xhr.open("POST", "/search", true);
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    text = "query=" + text
    xhr.send(text);
}

function __log(e, data) {
                console.log( "\n" + e + " " + (data || ''));
        }
function startRecording(button) {
        recorder && recorder.record();
        button.disabled = true;
        button.nextElementSibling.disabled = false;
        __log('Recording...');
}
function stopRecording(button) {
  recorder && recorder.stop();
  button.disabled = true;
  button.previousElementSibling.disabled = false;
  __log('Stopped recording.');
        createDownloadLink();
        recorder.clear();
}   
function createDownloadLink() {
        recorder && recorder.exportWAV(function(blob) {
        console.log(blob)
        var xhr = new XMLHttpRequest();
        xhr.open("POST", "/musicin", true);
        xhr.setRequestHeader("Content-Type", "audio/wav");
        
        xhr.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                music = JSON.parse(xhr.responseText)
                if (music['status']['msg'] == 'Success') {
                    track = music['metadata']['music'][0]['external_metadata']['spotify']['track']['name']
                    artist = music['metadata']['music'][0]['artists'][0]['name']
                    document.getElementById('song_text').value = track + " " + artist
                }
            }
        }
        xhr.send(blob);
    });
}

window.onload = function ini() { 
    try {
            // webkit shim
            window.AudioContext = window.AudioContext || window.webkitAudioContext;
            navigator.getUserMedia = navigator.getUserMedia || navigator.webkitGetUserMedia;
            window.URL = window.URL || window.webkitURL;
            
            audio_context = new AudioContext;
            __log('Audio context set up.');
            __log('navigator.getUserMedia ' + (navigator.getUserMedia ? 'available.' : 'not present!'));
    } catch (e) {
            alert('No web audio support in this browser!');
    }
    navigator.getUserMedia({audio: true}, startUserMedia, function(e) {
            __log('No live audio input: ' + e);
    });
};