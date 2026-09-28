(function () {
  "use strict";

  function sanitize(value) {
    return String(value || "")
      .replace(/[<>]/g, "")
      .replace(/javascript:/gi, "")
      .replace(/on\w+=/gi, "")
      .trim();
  }

  function isValidEmail(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email);
  }

  var toggle = document.querySelector(".nav-toggle");
  var nav = document.getElementById("main-nav");
  var backdrop = document.getElementById("nav-backdrop");
  var header = document.querySelector(".site-header");

  function setNav(open) {
    if (!nav || !toggle) return;
    nav.classList.toggle("is-open", open);
    toggle.classList.toggle("is-open", open);
    if (header) header.classList.toggle("is-open", open);
    if (backdrop) backdrop.classList.toggle("is-open", open);
    toggle.setAttribute("aria-expanded", open ? "true" : "false");
    toggle.setAttribute("aria-label", open ? "Menüyü kapat" : "Menüyü aç");
    document.body.style.overflow = open ? "hidden" : "";
  }

  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      setNav(!nav.classList.contains("is-open"));
    });
  }
  if (backdrop) {
    backdrop.addEventListener("click", function () {
      setNav(false);
    });
  }
  if (nav) {
    nav.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", function () {
        setNav(false);
      });
    });
  }

  var cookieBar = document.getElementById("cookie-bar");
  var cookieKey = "birikimedu_cookie_ok";
  function hideCookie() {
    if (cookieBar) cookieBar.classList.remove("is-visible");
    try {
      localStorage.setItem(cookieKey, "1");
    } catch (e) {
      /* ignore */
    }
  }
  if (cookieBar) {
    var seen = false;
    try {
      seen = localStorage.getItem(cookieKey) === "1";
    } catch (e) {
      seen = false;
    }
    if (!seen) cookieBar.classList.add("is-visible");
    var essential = document.getElementById("cookie-essential");
    var accept = document.getElementById("cookie-accept");
    if (essential) essential.addEventListener("click", hideCookie);
    if (accept) accept.addEventListener("click", hideCookie);
  }

  var form = document.getElementById("contact-form");
  var statusEl = document.getElementById("form-status");

  function showStatus(message, ok) {
    if (!statusEl) return;
    statusEl.textContent = message;
    statusEl.classList.add("is-visible");
    statusEl.classList.toggle("is-ok", !!ok);
    statusEl.classList.toggle("is-error", !ok);
  }

  if (form) {
    var params = new URLSearchParams(window.location.search);
    if (params.get("sent") === "1") {
      showStatus("Mesajınız alındı. En kısa sürede info@birikimedu.com üzerinden dönüş yapacağız.", true);
    }

    form.addEventListener("submit", function (event) {
      var nameInput = form.querySelector("#name");
      var emailInput = form.querySelector("#email");
      var serviceInput = form.querySelector("#service");
      var messageInput = form.querySelector("#message");

      var name = sanitize(nameInput && nameInput.value);
      var email = sanitize(emailInput && emailInput.value);
      var service = sanitize(serviceInput && serviceInput.value);
      var message = sanitize(messageInput && messageInput.value);

      if (nameInput) nameInput.value = name;
      if (emailInput) emailInput.value = email;
      if (serviceInput) serviceInput.value = service;
      if (messageInput) messageInput.value = message;

      if (name.length < 2) {
        event.preventDefault();
        showStatus("Lütfen adınızı soyadınızı yazın.", false);
        return;
      }
      if (!isValidEmail(email)) {
        event.preventDefault();
        showStatus("Geçerli bir e-posta adresi girin.", false);
        return;
      }
      if (!service) {
        event.preventDefault();
        showStatus("İlgilendiğiniz programı seçin.", false);
        return;
      }
      if (message.length < 10) {
        event.preventDefault();
        showStatus("Mesajınız en az birkaç cümle olsun — hedef ülke ve program yazmanız yeterli.", false);
      }
    });
  }
})();
