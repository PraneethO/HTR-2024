
// Source: https://dev.to/dalalrohit/live-stream-your-webcam-to-html-page-3ehf
window.onload = () => {
  let socket = io.connect();

  socket.on("plastic", (result) => {
    console.log(window.location.search);
    
    if (result.plastic) {
      let end = window.location.search ? window.location.search + "&message='Successfully detected plastic'" : "?message='Successfully detected plastic'";
      document.location.href = '/add/20' + end;
    } else {
      let end = window.location.search ? window.location.search + "&message='Could not detect plastic'" : "?message='Could not detect plastic'";
      document.location.href = '/tracker' + window.location.search;

    }
  });

const video = document.querySelector('#stream');
const canvas = document.querySelector('#canvas');
const submit = document.querySelector('#submit');
let streaming = false;
let width = 500;
let height = 0;

window.navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {

        console.log(stream);

        video.srcObject = stream;
        video.onloadedmetadata = (e) => {
            video.play();
        };

       video.addEventListener(
        "canplay",
        (ev) => {
          if (!streaming) {
            height = (video.videoHeight / video.videoWidth) * width;

            video.setAttribute("width", width);
            video.setAttribute("height", height);
            canvas.setAttribute("width", width);
            canvas.setAttribute("height", height);
            streaming = true;
          }
        },
        false,
      );

        submit.addEventListener(
          "click",
          (ev) => {
            const context = canvas.getContext("2d");
            canvas.width = width;
            canvas.height = height;
            context.drawImage(video, 0, 0, width, height);

            const data = canvas.toDataURL("image/png");
            socket.emit("image", { url: data });
            console.log(data);
            // photo.setAttribute("src", data);
            ev.preventDefault();
          },
          false,
        );

    })
    .catch( () => {
        alert('Allow camera permissions');
    });
}
// Source: https://developer.mozilla.org/en-US/docs/Web/API/Media_Capture_and_Streams_API/Taking_still_photos
/*
function takepicture() {
  const context = canvas.getContext("2d");
  if (width && height) {
    canvas.width = width;
    canvas.height = height;
    context.drawImage(video, 0, 0, width, height);

    const data = canvas.toDataURL("image/png");
    photo.setAttribute("src", data);
  } else {
    clearphoto();
  }
}

*/