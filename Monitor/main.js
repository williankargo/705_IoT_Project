// main.js

// Get User Media
navigator.getUserMedia =
  navigator.getUserMedia ||
  navigator.webkitGetUserMedia ||
  navigator.mozGetUserMedia ||
  navigator.msGetUserMedia;

var video;
var webcamStream;
var isSnapshotTaken = false;

const apiAddr = "http://127.0.0.1:5100/";

var canvas, ctx;

function init() {
  canvas = document.getElementById("myCanvas");
  ctx = canvas.getContext("2d");
  startWebcam();
}

function startWebcam() {
  if (navigator.getUserMedia) {
    navigator.getUserMedia(
      { video: true, audio: false },
      function (localMediaStream) {
        video = document.querySelector("video");
        video.srcObject = localMediaStream;
        webcamStream = localMediaStream;
      },
      function (err) {
        console.log("The following error occurred: " + err);
      }
    );
  } else {
    console.log("getUserMedia not supported");
  }
}

function snapshot() {
  if (video) {
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
    document.getElementById("submitBtn").style.display = "block";
    document.getElementById("snapshotBtn").disabled = true;
    document.getElementById("restartBtn").style.display = "block";
    isSnapshotTaken = true;
  }
}

function restart() {
  if (webcamStream) {
    const tracks = webcamStream.getTracks();
    tracks.forEach((track) => track.stop());
  }
  startWebcam();
  document.getElementById("submitBtn").style.display = "none";
  document.getElementById("snapshotBtn").disabled = false;
  document.getElementById("restartBtn").style.display = "none";
  clearCanvas();
}

function clearCanvas() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
}

function stopWebcam() {
  if (webcamStream) {
    const tracks = webcamStream.getTracks();
    tracks.forEach((track) => track.stop());
    video.srcObject = null;
  }
}

function submitFace() {
  if (isSnapshotTaken) {
    var imageData = canvas.toDataURL("image/jpeg");
    var formData = new FormData();
    formData.append("img2", imageData);

    fetch(apiAddr + "verify", {
      method: "POST",
      body: JSON.stringify({ img2: imageData }),
      headers: {
        "Content-Type": "application/json",
      },
    })
    .then((response) => response.json())
    .then((data) => {
      console.log("API Response:", data);
      if (data.verified === "True") {
        alert("Face is recognized!");
        stopWebcam();
        showOTPInput();
      } else {
        if (data.error) {
          alert(data.error);
        } else {
          alert("Face Not Recognised !");
        }
        restart();
      }
    })
    .catch((error) => {
      console.error("Error:", error);
    });
  } else {
    console.log("No snapshot taken.");
  }
}

function showOTPInput() {
  var pageContent = document.body;
  pageContent.innerHTML = `
    <h1>Step 2: Enter OTP</h1>
    <input type="text" id="otpInput" placeholder="Enter OTP" />
    <button id="submitOTPBtn" onclick="submitOTP()">Submit OTP</button>
  `;
}


// Submit OTP to an OTP API
// TODO: If wrong OTP, show wrong OTP and trigger Restart()
function submitOTP() {
  var otpInput = document.getElementById("otpInput").value;
  var otpObject = {
    otp: otpInput,
  };

  fetch(apiAddr + "validate_otp", {
    method: "POST",
    body: JSON.stringify(otpObject),
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((response) => response.json())
    .then((data) => {
      console.log("OTP Submission Response:", data);
      if (data.message === "OTP is valid") {
        alert("OTP is valid!");
        alert("Door is Unlocked! Welcome!! ");
      } else {
        // Wrong Face, display message and Restart button
        if (data.error) {
          alert(data.error);
        } else {
          alert("Invalid OTP!");
        }
      } 
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}
// function submitOTP() {
//   var otpInput = document.getElementById("otpInput").value;
//   if (otpInput.length === 6) {
//     alert("OTP is valid!");
//     alert("Door is Unlocked! Welcome!! ");
//     // showUnlockedMessage();
//   } else {
//     alert("Please enter a valid 6-digit OTP.");
//   }
// }

