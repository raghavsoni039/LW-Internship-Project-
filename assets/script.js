// Webcam Access
navigator.mediaDevices.getUserMedia({ video: true }).then(stream => {
  document.getElementById("video").srcObject = stream;
});

function capturePhoto() {
  const video = document.getElementById("video");
  const canvas = document.getElementById("canvas");
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  canvas.getContext("2d").drawImage(video, 0, 0);
  alert("Photo captured!");
}

function sendPhoto() {
  const dataURL = document.getElementById("canvas").toDataURL();
  // Use EmailJS or backend API to send `dataURL` as attachment
  alert("Sending photo via email... (hook with EmailJS)");
}

// Record Video
let recorder, videoData = [];

function startRecording() {
  navigator.mediaDevices.getUserMedia({ video: true, audio: true }).then(stream => {
    recorder = new MediaRecorder(stream);
    recorder.ondataavailable = e => videoData.push(e.data);
    recorder.onstop = () => {
      const blob = new Blob(videoData, { type: 'video/webm' });
      const videoURL = URL.createObjectURL(blob);
      document.getElementById("recordedVideo").src = videoURL;
      alert("Send video using Email API backend");
      videoData = [];
    };
    recorder.start();
    alert("Recording started...");
  });
}

function stopRecording() {
  recorder.stop();
}

// WhatsApp
function sendWhatsApp() {
  const number = document.getElementById("wa-number").value;
  const message = document.getElementById("wa-msg").value;
  window.open(`https://wa.me/${number}?text=${encodeURIComponent(message)}`);
}

// SMS via API
function sendSMS() {
  alert("Hook this to a backend using Twilio API to send SMS.");
}

// Geolocation
function getLocation() {
  navigator.geolocation.getCurrentPosition(pos => {
    const { latitude, longitude } = pos.coords;
    document.getElementById("locationInfo").textContent = `Latitude: ${latitude}, Longitude: ${longitude}`;
    showMap(latitude, longitude);
  });
}

function showMap(lat, lng) {
  const mapDiv = document.getElementById("map");
  mapDiv.innerHTML = `<iframe width="100%" height="300" src="https://maps.google.com/maps?q=${lat},${lng}&z=15&output=embed"></iframe>`;
}

// Product Tracking
let viewCount = {};

function trackView(product) {
  viewCount[product] = (viewCount[product] || 0) + 1;
  alert(`${product} viewed`);
}

function showRecommended() {
  const top = Object.entries(viewCount).sort((a, b) => b[1] - a[1])[0];
  document.getElementById("recommendation").textContent = top ? `Recommended: ${top[0]}` : "No products viewed.";
}

// Get IP
function getIP() {
  fetch("https://api.ipify.org?format=json")
    .then(res => res.json())
    .then(data => {
      fetch(`https://ipapi.co/${data.ip}/json/`)
        .then(res => res.json())
        .then(loc => {
          document.getElementById("ipInfo").textContent =
            `Your IP is ${data.ip} and your location is ${loc.city}, ${loc.region}, ${loc.country_name}`;
        });
    });
}
