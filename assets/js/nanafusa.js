const modal = document.getElementById("modal");
const modalBox = modal.querySelector("div.bg-white");
const modalContent = document.getElementById("modalContent");
const closeModal = document.getElementById("closeModal");

document.querySelectorAll(".card").forEach(card => {
  card.addEventListener("click", () => {
    const title = card.dataset.title;
    const video = card.dataset.video;
    const intro = card.dataset.intro;
    const comment = card.dataset.comment;

    modalContent.innerHTML = `
      <iframe class="w-full aspect-video rounded-md" src="${video}" allowfullscreen></iframe>
      <h3 class="text-xl font-bold">${title}</h3>
      <p><strong>イントロダクション：</strong><br>${intro}</p>
      <p><strong>スタッフコメント：</strong><br>${comment}</p>
    `;

    modal.classList.remove("hidden");
    setTimeout(() => {
      modal.classList.add("flex");
      modalBox.classList.remove("scale-95", "opacity-0");
      modalBox.classList.add("scale-100", "opacity-100");
    }, 10);
  });
});

closeModal.addEventListener("click", () => {
  modalBox.classList.add("scale-95", "opacity-0");
  modalBox.classList.remove("scale-100", "opacity-100");
  setTimeout(() => {
    modal.classList.remove("flex");
    modal.classList.add("hidden");
  }, 200);
});
