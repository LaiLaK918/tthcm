console.log("Trung nguyên xin chào!");

document.addEventListener("DOMContentLoaded", function () {
  const imgElements = document.querySelectorAll("img");

  imgElements.forEach(function (img) {
    const srcValue = img.getAttribute("src");

    if (srcValue && srcValue.includes("/logo?theme=")) {
      const spanElement = document.createElement("span");
      spanElement.className = "chat-bot-text";
      spanElement.style.fontWeight = "bold";
      spanElement.style.fontSize = "15px";
      spanElement.style.paddingLeft = "20px";
      spanElement.textContent = "TrungNguyenGPT";

      img.parentNode.appendChild(spanElement);
    }
  });
});