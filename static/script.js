function validateForm() {
    const youtubeRegex = new RegExp(
        "^(https?://)?(www.)?(youtube.com|youtu.?be)/.+$"
    );
    let videolink = document.getElementById("link").value
    
     if (videolink.length == 0) {
        alert("please enter a youtube video link! (your link is empty)");
        return false;
    } else {
        if (youtubeRegex.test(videolink)) {
          return true;
        } else {
          alert("please enter a valid youtube video link! (your link is mistaken)");
          return false;
        }
    }
}