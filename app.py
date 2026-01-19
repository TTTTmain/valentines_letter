import os

from flask import Flask, Response, send_from_directory

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


@app.get("/")
def index() -> Response:
    html = """<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Valentine Letter</title>
    <style>
      :root {
        --bg: #fff5f8;
        --pink: #ff6b9c;
        --deep: #e63b6a;
        --paper: #fffdf7;
        --shadow: rgba(0, 0, 0, 0.12);
      }

      * {
        box-sizing: border-box;
      }

      body {
        margin: 0;
        min-height: 100vh;
        display: grid;
        place-items: center;
        font-family: "Segoe UI", system-ui, -apple-system, sans-serif;
        background: radial-gradient(circle at top, #ffe8f0, var(--bg));
        color: #5a2c3a;
        overflow: hidden;
      }

      .scene {
        position: relative;
        width: min(80vw, 420px);
        height: min(70vh, 520px);
        display: grid;
        place-items: center;
      }

      .gif-modal {
        position: fixed;
        inset: 0;
        background: rgba(255, 245, 248, 0.92);
        display: grid;
        place-items: center;
        opacity: 0;
        pointer-events: none;
        transition: opacity 0.3s ease;
        z-index: 10;
        padding: 24px;
      }

      .gif-modal.open {
        opacity: 1;
        pointer-events: auto;
      }

      .gif-card {
        width: min(420px, 92vw);
        background: #fff;
        border-radius: 18px;
        padding: 18px 16px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.18);
        text-align: center;
        position: relative;
      }

      .gif-card h2 {
        margin: 0 0 12px;
        font-size: 1.2rem;
        color: #b23a5c;
      }

      .gif-overlay {
        position: absolute;
        right: 18px;
        bottom: 18px;
        width: 90px;
        height: auto;
        border-radius: 10px;
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.18);
        opacity: 0;
        pointer-events: none;
      }

      .gif-overlay.show {
        animation: fadeIn 1.8s ease forwards;
      }

      @keyframes fadeIn {
        from {
          opacity: 0;
          transform: translateY(6px);
        }
        to {
          opacity: 1;
          transform: translateY(0);
        }
      }

      .prompt {
        position: absolute;
        left: 24px;
        bottom: 28px;
        font-size: 0.95rem;
        letter-spacing: 0.24em;
        color: #8b4b5e;
        text-transform: uppercase;
        pointer-events: none;
        transition: opacity 0.3s ease;
        z-index: 4;
      }

      .envelope {
        position: relative;
        width: 340px;
        height: 225px;
        background: linear-gradient(145deg, #ffe3ee 0%, #ffc1d6 100%);
        border-radius: 16px;
        box-shadow: 0 25px 40px var(--shadow);
        cursor: pointer;
        transition: transform 0.35s ease;
      }

      .envelope:active {
        transform: scale(0.98);
      }

      .envelope .back {
        position: absolute;
        inset: 0;
        background: linear-gradient(160deg, #ffe3ee 0%, #ffb3cb 100%);
        border-radius: 16px;
      }

      .envelope .flap {
        position: absolute;
        left: 0;
        right: 0;
        top: 0;
        height: 52%;
        background: linear-gradient(180deg, #ffb5ce 0%, #ff8fb5 100%);
        transform-origin: top center;
        clip-path: polygon(0 0, 50% 100%, 100% 0);
        border-radius: 16px 16px 0 0;
        transition: transform 0.6s ease;
      }

      .envelope .front {
        position: absolute;
        inset: 0;
        border-radius: 16px;
        overflow: hidden;
      }

      .envelope .front::before,
      .envelope .front::after {
        content: "";
        position: absolute;
        width: 100%;
        height: 100%;
        background: #ffd1e1;
        clip-path: polygon(0 100%, 50% 45%, 100% 100%, 100% 100%, 0 100%);
        top: 0;
        left: 0;
      }

      .envelope .front::after {
        background: #ffb3cb;
        clip-path: polygon(0 100%, 50% 55%, 100% 100%, 100% 100%, 0 100%);
      }

      .front-details {
        position: absolute;
        inset: 12px;
        border-radius: 12px;
        border: 2px solid rgba(255, 255, 255, 0.6);
        padding: 16px;
        display: grid;
        grid-template-columns: 1fr auto;
        grid-template-rows: auto 1fr auto;
        gap: 12px;
        z-index: 2;
      }

      .stamp {
        width: 56px;
        height: 70px;
        background: linear-gradient(160deg, #ffd7e7, #ff9fc1);
        border-radius: 8px;
        box-shadow: inset 0 0 0 2px rgba(255, 255, 255, 0.7);
        position: relative;
      }

      .stamp::after {
        content: "♥";
        position: absolute;
        inset: 0;
        display: grid;
        place-items: center;
        color: #e63b6a;
        font-size: 1.6rem;
      }

      .address {
        display: grid;
        gap: 8px;
        align-content: end;
        color: #8b4b5e;
        font-size: 0.9rem;
        letter-spacing: 0.04em;
      }

      .address span {
        display: block;
        height: 8px;
        width: 70%;
        background: rgba(139, 75, 94, 0.25);
        border-radius: 999px;
      }

      .seal {
        position: absolute;
        bottom: 40px;
        right: 36px;
        width: 48px;
        height: 48px;
        background: radial-gradient(circle at top left, #ff7ea8, #d62c5c);
        border-radius: 50%;
        box-shadow: 0 6px 14px rgba(214, 44, 92, 0.35);
        display: grid;
        place-items: center;
        color: #fff0f4;
        font-size: 1.2rem;
        letter-spacing: 0.02em;
        z-index: 3;
      }

      .letter {
        position: absolute;
        bottom: 12px;
        left: 50%;
        transform: translateX(-50%) translateY(40%);
        width: 88%;
        height: 86%;
        background: linear-gradient(180deg, #fffdf8 0%, #fff4f0 100%);
        border-radius: 14px;
        box-shadow: 0 12px 28px rgba(0, 0, 0, 0.12);
        display: grid;
        place-items: center;
        padding: 20px;
        transition: transform 0.7s ease, opacity 0.4s ease;
        opacity: 0;
      }

      .letter::before {
        content: "";
        position: absolute;
        top: 10px;
        left: 10px;
        right: 10px;
        height: 10px;
        border-radius: 999px;
        background: rgba(230, 59, 106, 0.15);
      }

      .message {
        font-size: clamp(1.6rem, 3vw + 1rem, 2.6rem);
        font-weight: 700;
        text-transform: lowercase;
        text-align: center;
        color: #cf2f5c;
        text-shadow: 0 6px 14px rgba(207, 47, 92, 0.2);
      }

      .cta {
        position: absolute;
        bottom: -56px;
        left: 50%;
        transform: translateX(-50%) translateY(10px);
        display: flex;
        gap: 16px;
        justify-content: center;
        width: 100%;
        opacity: 0;
        pointer-events: none;
        transition: opacity 0.3s ease, transform 0.3s ease;
      }

      .btn {
        border: none;
        border-radius: 999px;
        padding: 14px 34px;
        font-size: 1.1rem;
        font-weight: 600;
        cursor: pointer;
        box-shadow: 0 8px 18px rgba(0, 0, 0, 0.12);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
      }

      .btn:hover {
        transform: translateY(-1px);
        box-shadow: 0 10px 22px rgba(0, 0, 0, 0.15);
      }

      .btn-yes {
        background: #b8efc4;
        color: #216b35;
      }

      .btn-no {
        background: #f6b6c1;
        color: #8a2b3e;
      }

      .open .flap {
        transform: rotateX(180deg);
      }

      .open .letter {
        transform: translateX(-50%) translateY(-10%);
        opacity: 1;
      }

      .open .prompt {
        opacity: 0;
      }

      .open + .cta {
        opacity: 1;
        transform: translateX(-50%) translateY(0);
        pointer-events: auto;
      }

      .open .front,
      .open .back,
      .open .flap {
        opacity: 0;
        transition: opacity 0.4s ease;
      }

      .hearts {
        position: absolute;
        inset: 0;
        pointer-events: none;
        overflow: hidden;
      }

      .heart {
        position: absolute;
        width: 18px;
        height: 18px;
        background: var(--pink);
        transform: rotate(45deg);
        opacity: 0.9;
        animation: floatUp 2.8s ease-in forwards;
      }

      .heart::before,
      .heart::after {
        content: "";
        position: absolute;
        width: 18px;
        height: 18px;
        background: inherit;
        border-radius: 50%;
      }

      .heart::before {
        left: -9px;
      }

      .heart::after {
        top: -9px;
      }

      @keyframes floatUp {
        0% {
          transform: translateY(0) rotate(45deg) scale(1);
          opacity: 0.9;
        }
        100% {
          transform: translateY(-220px) rotate(45deg) scale(1.4);
          opacity: 0;
        }
      }
    </style>
  </head>
  <body>
    <div class="scene">
      <div class="envelope" id="envelope" aria-label="Open letter">
        <div class="back"></div>
        <div class="flap"></div>
        <div class="letter">
          <div class="message">will you be my valentines</div>
        </div>
        <div class="front">
          <div class="front-details">
            <div class="address">
              <span></span>
              <span></span>
              <span style="width: 55%"></span>
            </div>
            <div class="stamp"></div>
          </div>
          <div class="seal">❤</div>
          <div class="prompt">click me</div>
        </div>
        <div class="hearts" id="hearts"></div>
      </div>
      <div class="cta">
        <button class="btn btn-yes" id="yesButton" type="button">yes</button>
        <button class="btn btn-no" id="noButton" type="button">no</button>
      </div>
    </div>
    <div class="gif-modal" id="gifModal" aria-hidden="true">
      <div class="gif-card" id="gifCard">
        <h2 id="gifTitle">yay!!</h2>
        <img
          id="gifImage"
          src="/happy.JPG"
          alt="cat gif"
          style="width: 100%; border-radius: 12px"
        />
        <img
          id="gifOverlay"
          class="gif-overlay"
          src="/dance_cat.gif"
          alt="dancing cat"
        />
      </div>
    </div>

    <script>
      const envelope = document.getElementById("envelope");
      const heartsLayer = document.getElementById("hearts");
      const yesButton = document.getElementById("yesButton");
      const noButton = document.getElementById("noButton");
      const gifModal = document.getElementById("gifModal");
      const gifTitle = document.getElementById("gifTitle");
      const gifImage = document.getElementById("gifImage");
      const gifOverlay = document.getElementById("gifOverlay");
      let opened = false;

      function spawnHearts(count) {
        for (let i = 0; i < count; i += 1) {
          const heart = document.createElement("span");
          heart.className = "heart";
          heart.style.left = `${40 + Math.random() * 20}%`;
          heart.style.bottom = `${20 + Math.random() * 10}px`;
          heart.style.background = Math.random() > 0.5 ? "#ff6b9c" : "#ff8ab5";
          heart.style.animationDelay = `${Math.random() * 0.3}s`;
          heartsLayer.appendChild(heart);
          heart.addEventListener("animationend", () => heart.remove());
        }
      }

      envelope.addEventListener("click", () => {
        if (!opened) {
          envelope.classList.add("open");
          spawnHearts(18);
          opened = true;
        }
      });

      function showGif(title, src, overlay) {
        gifTitle.textContent = title;
        gifImage.src = src;
        gifOverlay.classList.remove("show");
        gifOverlay.style.display = overlay ? "block" : "none";
        gifModal.classList.add("open");
        gifModal.setAttribute("aria-hidden", "false");
        if (overlay) {
          requestAnimationFrame(() => gifOverlay.classList.add("show"));
        }
      }

      yesButton.addEventListener("click", () => {
        showGif("yay!!", "/happy.JPG", true);
      });

      noButton.addEventListener("click", () => {
        showGif("aww...", "/sad_cat.gif", false);
      });

      gifModal.addEventListener("click", (event) => {
        if (event.target === gifModal) {
          gifModal.classList.remove("open");
          gifModal.setAttribute("aria-hidden", "true");
          gifOverlay.classList.remove("show");
        }
      });
    </script>
  </body>
</html>"""
    return Response(html, mimetype="text/html")


@app.get("/dance_cat.gif")
def dance_cat() -> Response:
    return send_from_directory(BASE_DIR, "dance_cat.gif")


@app.get("/sad_cat.gif")
def sad_cat() -> Response:
    return send_from_directory(BASE_DIR, "sad_cat.gif")


@app.get("/happy.JPG")
def happy_image() -> Response:
    return send_from_directory(BASE_DIR, "happy.JPG")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
