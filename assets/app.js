(function () {
  "use strict";

  var STORAGE_PREFIX = "fnspl-v1:";

  function storageKeyFor(cb) {
    if (cb.dataset.key) return STORAGE_PREFIX + cb.dataset.key;
    var path = window.location.pathname;
    var all = document.querySelectorAll('input[type="checkbox"]');
    var idx = Array.prototype.indexOf.call(all, cb);
    return STORAGE_PREFIX + path + ":cb" + idx;
  }

  function restore() {
    var boxes = document.querySelectorAll('input[type="checkbox"]');
    boxes.forEach(function (cb) {
      var key = storageKeyFor(cb);
      try {
        if (window.localStorage.getItem(key) === "1") cb.checked = true;
      } catch (e) {
        return;
      }
    });
  }

  function persistChange(e) {
    var cb = e.target;
    if (!cb || cb.type !== "checkbox") return;
    var key = storageKeyFor(cb);
    try {
      if (cb.checked) {
        window.localStorage.setItem(key, "1");
      } else {
        window.localStorage.removeItem(key);
      }
    } catch (err) {
      return;
    }
  }

  function clearAll() {
    var boxes = document.querySelectorAll('input[type="checkbox"]');
    boxes.forEach(function (cb) {
      cb.checked = false;
      var key = storageKeyFor(cb);
      try {
        window.localStorage.removeItem(key);
      } catch (e) {
        return;
      }
    });
  }

  document.addEventListener("change", persistChange);

  var clearBtn = document.querySelector("[data-clear-checks]");
  if (clearBtn) {
    clearBtn.addEventListener("click", clearAll);
  }

  var printBtn = document.querySelector("[data-print]");
  if (printBtn) {
    printBtn.addEventListener("click", function () {
      window.print();
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", restore);
  } else {
    restore();
  }
})();
