const certifContainer = document.querySelector(".certificates-container");
const addCertifBtn = document.querySelector(".add-certificate-btn");
const removeCertifBtn = document.querySelector(".remove-certificate-btn");

addCertifBtn.addEventListener("click", (_) => {
  removeCertifBtn.parentElement.style.display = "block";
  insertNewCertif();
});
removeCertifBtn.addEventListener("click", (_) => {
  removeCertif();
  if (!certifContainer.childElementCount) {
    removeCertifBtn.parentElement.style.display = "none";
  }
});

function insertNewCertif() {
  const x = certifContainer.childElementCount + 1;

  // 'c-' Prefix
  // Do not forgot to add a prefix to name's value, since some fields got conflict with other models' fields
  const markup = `
    <div class="certificate-${x}">   
        <p>
          <label for="id_certificate_${x}">الشهادة: </label>
          <input type="text" name="c-certificate-${x}" maxlength="128" required id="id_certificate_${x}">
        </p>
    
        <p>
          <label for="id_certif_provider_${x}">الشركة المزوّدة: </label>
          <input type="text" name="c-certif-provider-${x}" maxlength="128" required id="id_certif_provider_${x}">
        </p>
    
        <p>
          <label for="id_year_obtained_${x}">السنة المكتسبة: </label>
          <input type="number" name="c-year-obtained-${x}" required id="id_year_obtained_${x}">
        </p>
    
        <p>
          <label for="id_validity_${x}">الصلاحية: </label>
          <select name="c-validity-${x}" required id="id_validity_${x}">
            <option value="" selected>---------</option>
            <option value="-1">مدى الحياة</option>
            <option value="1">سنة واحدة</option>
            <option value="5">خمس سنوات</option>
          </select>
        </p>
        <hr>
    </div>
  `;

  certifContainer.insertAdjacentHTML("beforeend", markup);
}

function removeCertif() {
  certifContainer.removeChild(certifContainer.lastElementChild);
}
