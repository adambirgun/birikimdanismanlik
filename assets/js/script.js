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

  var lang = (document.documentElement.lang || "tr").toLowerCase().slice(0, 2);

  var copy = {
    tr: {
      menuOpen: "Menüyü aç",
      menuClose: "Menüyü kapat",
      errName: "Lütfen adınızı soyadınızı yazın.",
      errEmail: "Geçerli bir e-posta adresi girin.",
      errService: "İlgilendiğiniz programı seçin.",
      errMsg: "Mesajınız en az birkaç cümle olsun — hedef ülke ve program yazmanız yeterli.",
      ok: "E-posta uygulamanız açılıyor. Göndermeyi oradan tamamlayın.",
      subject: "Birikim Danışmanlık — Ön değerlendirme",
      bodyName: "Ad Soyad",
      bodyEmail: "E-posta",
      bodyProgram: "Program",
      bodyMsg: "Mesaj",
      services: {
        universite: "Üniversite (lisans / yüksek lisans)",
        "dil-okulu": "Dil okulu yerleştirme",
        vize: "Vize & belge desteği",
        diger: "Diğer"
      }
    },
    en: {
      menuOpen: "Open menu",
      menuClose: "Close menu",
      errName: "Please enter your full name.",
      errEmail: "Please enter a valid email address.",
      errService: "Please select a programme.",
      errMsg: "Add a few sentences — target country and programme are enough.",
      ok: "Opening your email app. Complete the send there.",
      subject: "Birikim Danışmanlık — Preliminary review",
      bodyName: "Full name",
      bodyEmail: "Email",
      bodyProgram: "Programme",
      bodyMsg: "Message",
      services: {
        universite: "University (bachelor’s / master’s)",
        "dil-okulu": "Language school placement",
        vize: "Visa & document support",
        diger: "Other"
      }
    },
    es: {
      menuOpen: "Abrir menú",
      menuClose: "Cerrar menú",
      errName: "Escriba su nombre y apellidos.",
      errEmail: "Introduzca un correo válido.",
      errService: "Seleccione un programa.",
      errMsg: "Añada unas frases — país y programa bastan.",
      ok: "Se abre su aplicación de correo. Complete el envío allí.",
      subject: "Birikim Danışmanlık — Evaluación preliminar",
      bodyName: "Nombre y apellidos",
      bodyEmail: "Correo",
      bodyProgram: "Programa",
      bodyMsg: "Mensaje",
      services: {
        universite: "Universidad (grado / máster)",
        "dil-okulu": "Colocación en escuela de idiomas",
        vize: "Visado y documentos",
        diger: "Otro"
      }
    },
    de: {
      menuOpen: "Menü öffnen",
      menuClose: "Menü schließen",
      errName: "Bitte Vor- und Nachnamen eingeben.",
      errEmail: "Bitte eine gültige E-Mail-Adresse eingeben.",
      errService: "Bitte ein Programm wählen.",
      errMsg: "Schreiben Sie ein paar Sätze — Zielland und Programm reichen.",
      ok: "E-Mail-App wird geöffnet. Senden Sie dort weiter.",
      subject: "Birikim Danışmanlık — Vorprüfung",
      bodyName: "Vor- und Nachname",
      bodyEmail: "E-Mail",
      bodyProgram: "Programm",
      bodyMsg: "Nachricht",
      services: {
        universite: "Universität (Bachelor / Master)",
        "dil-okulu": "Sprachschulplatzierung",
        vize: "Visum & Dokumente",
        diger: "Sonstiges"
      }
    },
    fr: {
      menuOpen: "Ouvrir le menu",
      menuClose: "Fermer le menu",
      errName: "Veuillez indiquer votre nom complet.",
      errEmail: "Veuillez indiquer une adresse e-mail valide.",
      errService: "Veuillez sélectionner un programme.",
      errMsg: "Ajoutez quelques phrases — pays et programme suffisent.",
      ok: "Ouverture de votre application e-mail. Finalisez l’envoi là-bas.",
      subject: "Birikim Danışmanlık — Évaluation préliminaire",
      bodyName: "Nom complet",
      bodyEmail: "E-mail",
      bodyProgram: "Programme",
      bodyMsg: "Message",
      services: {
        universite: "Université (licence / master)",
        "dil-okulu": "Placement en école de langues",
        vize: "Visa et documents",
        diger: "Autre"
      }
    },
    ru: {
      menuOpen: "Открыть меню",
      menuClose: "Закрыть меню",
      errName: "Укажите имя и фамилию.",
      errEmail: "Укажите действительный e-mail.",
      errService: "Выберите программу.",
      errMsg: "Добавьте несколько предложений — страны и программы достаточно.",
      ok: "Открывается почтовое приложение. Завершите отправку там.",
      subject: "Birikim Danışmanlık — Предварительная оценка",
      bodyName: "Имя и фамилия",
      bodyEmail: "E-mail",
      bodyProgram: "Программа",
      bodyMsg: "Сообщение",
      services: {
        universite: "Университет (бакалавриат / магистратура)",
        "dil-okulu": "Размещение в языковой школе",
        vize: "Виза и документы",
        diger: "Другое"
      }
    }
  };

  var t = copy[lang] || copy.tr;

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
    toggle.setAttribute("aria-label", open ? t.menuClose : t.menuOpen);
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

  var langSelect = document.querySelector(".lang-switch");
  if (langSelect) {
    try {
      localStorage.setItem("birikimedu_lang", lang);
    } catch (err) {
      /* ignore */
    }
    langSelect.querySelectorAll("a[data-lang]").forEach(function (link) {
      link.addEventListener("click", function () {
        try {
          localStorage.setItem("birikimedu_lang", link.getAttribute("data-lang") || lang);
        } catch (err2) {
          /* ignore */
        }
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
    form.addEventListener("submit", function (event) {
      event.preventDefault();

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
        showStatus(t.errName, false);
        return;
      }
      if (!isValidEmail(email)) {
        showStatus(t.errEmail, false);
        return;
      }
      if (!service) {
        showStatus(t.errService, false);
        return;
      }
      if (message.length < 10) {
        showStatus(t.errMsg, false);
        return;
      }

      var serviceLabel = (t.services && t.services[service]) || service;
      var subject = t.subject + " (" + name + ")";
      var body = [
        t.bodyName + ": " + name,
        t.bodyEmail + ": " + email,
        t.bodyProgram + ": " + serviceLabel,
        "",
        t.bodyMsg + ":",
        message
      ].join("\n");

      var mailto =
        "mailto:info@birikimedu.com" +
        "?subject=" +
        encodeURIComponent(subject) +
        "&body=" +
        encodeURIComponent(body);

      showStatus(t.ok, true);
      window.location.href = mailto;
    });
  }
})();
