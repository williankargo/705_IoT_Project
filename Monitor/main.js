// Get User Media
navigator.getUserMedia =
  navigator.getUserMedia ||
  navigator.webkitGetUserMedia ||
  navigator.mozGetUserMedia ||
  navigator.msGetUserMedia;

var video;
var webcamStream;
var isSnapshotTaken = false;

// todo: change the address
const apiAddr = "http://10.4.11.21:5100/";

// Init code
var canvas, ctx;
function init() {
  canvas = document.getElementById("myCanvas");
  ctx = canvas.getContext("2d");
  startWebcam();
}

// Take a snapshot
function snapshot() {
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;

  ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
  document.getElementById("submitBtn").style.display = "block";
  document.getElementById("snapshotBtn").disabled = true;
  document.getElementById("restartBtn").style.display = "block"; // Display the Restart button

  isSnapshotTaken = true;
}

// Retake Photo
function restart() {
  isSnapshotTaken = false;
  startWebcam();
  document.getElementById("submitBtn").style.display = "none";
  document.getElementById("snapshotBtn").disabled = false;
  document.getElementById("restartBtn").style.display = "none"; // Hide the Restart button
  clearCanvas();
}

function clearCanvas() {
  var canvas = document.getElementById("myCanvas");
  var ctx = canvas.getContext("2d");
  ctx.clearRect(0, 0, canvas.width, canvas.height);
}

// Start Camera
function startWebcam() {
  if (navigator.getUserMedia) {
    navigator.getUserMedia(
      {
        video: true,
        audio: false,
      },

      // successCallback
      function (localMediaStream) {
        video = document.querySelector("video");
        video.srcObject = localMediaStream;
        webcamStream = localMediaStream;
      },

      // errorCallback
      function (err) {
        console.log("The following error occurred: " + err);
      }
    );
  } else {
    console.log("getUserMedia not supported");
  }
}

// Stop Camera
function stopWebcam() {
  if (webcamStream) {
    const tracks = webcamStream.getTracks();
    tracks.forEach((track) => track.stop());
    video.srcObject = null; // Clear the video source to stop displaying the webcam feed
  }
}

// Submit the captured face to Face API
function submitFace() {
  if (isSnapshotTaken) {
    var canvas = document.getElementById("myCanvas");
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
          // Verified, show OTP input
          stopWebcam();
          showOTPInput();
        } else {
          // Wrong Face, display message and Restart button
          if (data.error) {
            alert(data.error);
          } else {
            alert("Wrong Face!");
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

// display OTP input and submit button
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
// TODO: send email?
function submitOTP() {
  var otpInput = document.getElementById("otpInput").value;
  var otpObject = {
    otp: otpInput,
  };

  fetch("https://example.com/api/submitotp", {
    method: "POST",
    body: JSON.stringify(otpObject),
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((response) => response.json())
    .then((data) => {
      console.log("OTP Submission Response:", data);
      // TODO: handle further actions based on the OTP submission response
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}
