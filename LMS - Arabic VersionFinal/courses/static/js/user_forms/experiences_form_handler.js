const expContainer = document.querySelector(".experiences-container");
const addExpBtn = document.querySelector(".add-experience-btn");
const removeExpBtn = document.querySelector(".remove-experience-btn");

addExpBtn.addEventListener("click", (_) => {
  removeExpBtn.parentElement.style.display = "block";
  insertNewExp();
});
removeExpBtn.addEventListener("click", (_) => {
  removeExp();
  if (!expContainer.childElementCount) {
    removeExpBtn.parentElement.style.display = "none";
  }
});

function insertNewExp() {
  const x = expContainer.childElementCount + 1;
  const markup = `
    <div class="experience-${x}">
        <p>
            <label for="company_name_id_${x}">اسم الشركة: </label>
            <input type="text" id="company_name_id_${x}" name="company-name-${x}" required />
        </p>

        <p>
            <label for="role_id_${x}">الوظيفة: </label>
            <input type="text" id="role_id_${x}" name="role-${x}" required />
        </p>

        <p>
            <label for="start_date_id_${x}">تاريخ البداية: </label>
            <input type="date" id="start_date_id_${x}" name="start-date-${x}" required />
        </p>

        <p>
            <label for="end_date_id_${x}">تاريخ النهاية: </label>
            <input type="date" id="end_date_id_${x}" name="end-date-${x}" required />
        </p>

        <p>
            <label for="description_id_${x}">الوصف: </label>
            <input type="text" id="description_id_${x}" name="description-${x}" required />
        </p>
        <hr>
    </div>
  `;

  expContainer.insertAdjacentHTML("beforeend", markup);
}

function removeExp() {
  expContainer.removeChild(expContainer.lastElementChild);
}
