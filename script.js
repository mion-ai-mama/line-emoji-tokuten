/**
 * script.js — ページの動き（コピー機能・アコーディオン・スクロール演出）
 * 文章は index.html を直接編集してください（content.js方式は使いません）。
 */

(function () {
  "use strict";

  /* ------------------------------------------------------------
     コピー機能（クリップボードAPI／古いブラウザ向けの代替あり）
  ------------------------------------------------------------ */
  function legacyCopy(text) {
    try {
      const textarea = document.createElement("textarea");
      textarea.value = text;
      textarea.style.position = "fixed";
      textarea.style.opacity = "0";
      document.body.appendChild(textarea);
      textarea.focus();
      textarea.select();
      const successful = document.execCommand("copy");
      document.body.removeChild(textarea);
      return successful;
    } catch (e) {
      return false;
    }
  }

  function copyText(text) {
    if (navigator.clipboard && window.isSecureContext) {
      return navigator.clipboard.writeText(text).then(
        () => true,
        () => legacyCopy(text)
      );
    }
    return Promise.resolve(legacyCopy(text));
  }

  function bindCopyDelegation() {
    document.addEventListener("click", function (e) {
      const btn = e.target.closest(".copy-btn[data-copy-target]");
      if (!btn) return;
      const target = document.getElementById(btn.getAttribute("data-copy-target"));
      if (!target) return;
      copyText(target.textContent).then((ok) => {
        if (!ok) return;
        btn.classList.add("is-copied");
        window.clearTimeout(btn._copyTimeout);
        btn._copyTimeout = window.setTimeout(() => btn.classList.remove("is-copied"), 2200);
      });
    });
  }

  /* ------------------------------------------------------------
     モチーフ選択 → Codex/ChatGPTプロンプトへの自動合成
     選んだモチーフの指示文（テンプレート）を、各ルートの本文テンプレートの
     先頭に足して、コピー用の1本のプロンプトを組み立てる。
  ------------------------------------------------------------ */
  function getTemplateText(id) {
    const tpl = document.getElementById(id);
    return tpl ? tpl.content.textContent.trim() : "";
  }

  function getSelectedMotif() {
    const checked = document.querySelector('input[name="motif"]:checked');
    return checked ? checked.value : "animal";
  }

  function composePrompt(taskTemplateId, outputId) {
    const output = document.getElementById(outputId);
    if (!output) return;
    const motifText = getTemplateText("motif-text-" + getSelectedMotif());
    const bodyText = getTemplateText(taskTemplateId);
    output.textContent = motifText + "\n\n" + bodyText;
  }

  function updatePrompts() {
    composePrompt("codex-task-body", "codex-prompt-text");
    composePrompt("chatgpt-task-body", "chatgpt-prompt-text");
  }

  function updateMotifSelectionStyle() {
    document.querySelectorAll(".motif-option").forEach((label) => {
      const input = label.querySelector('input[name="motif"]');
      label.classList.toggle("is-selected", !!input && input.checked);
    });
  }

  function bindMotifSelector() {
    const selector = document.getElementById("motif-selector");
    if (!selector) return;
    selector.addEventListener("change", () => {
      updateMotifSelectionStyle();
      updatePrompts();
    });
    updateMotifSelectionStyle();
    updatePrompts();
  }

  /* ------------------------------------------------------------
     アコーディオン（うまくいかないとき）
  ------------------------------------------------------------ */
  function bindAccordion() {
    document.addEventListener("click", function (e) {
      const question = e.target.closest(".accordion-item__question");
      if (!question) return;
      const expanded = question.getAttribute("aria-expanded") === "true";
      question.setAttribute("aria-expanded", String(!expanded));
    });
  }

  /* ------------------------------------------------------------
     スクロールで軽くフェードインする演出
  ------------------------------------------------------------ */
  function setupRevealAnimation() {
    const revealEls = document.querySelectorAll(".reveal");
    if (!("IntersectionObserver" in window)) {
      revealEls.forEach((el) => el.classList.add("is-visible"));
      return;
    }
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.15, rootMargin: "0px 0px -40px 0px" }
    );
    revealEls.forEach((el) => observer.observe(el));
  }

  function init() {
    bindCopyDelegation();
    bindMotifSelector();
    bindAccordion();
    setupRevealAnimation();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
