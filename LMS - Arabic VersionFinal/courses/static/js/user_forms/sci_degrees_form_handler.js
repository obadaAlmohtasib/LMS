const sciDegreesContainer = document.querySelector(".sci-degrees-container");
const addSciDegreeBtn = document.querySelector(".add-sci-degree-btn");
const removeSciDegreeBtn = document.querySelector(".remove-sci-degree-btn");

addSciDegreeBtn.addEventListener("click", (_) => {
  removeSciDegreeBtn.parentElement.style.display = "block";
  insertNewSciDegree();
});
removeSciDegreeBtn.addEventListener("click", (_) => {
  removeSciDegree();
  if (!sciDegreesContainer.childElementCount) {
    removeSciDegreeBtn.parentElement.style.display = "none";
  }
});

function insertNewSciDegree() {
  const x = sciDegreesContainer.childElementCount + 1;
  const markup = `
    <div class="sci-degree-${x}">
        <p>
            <label for="id_sci_degree_${x}">الدرجة العلمية: </label>
            <select name="sci-degree-${x}" required id="id_sci_degree_${x}">
                <option value="" selected>---------</option>
                <option value="HIGH_SCHOOL">الدراسة الثانوية</option>
                <option value="DIPLOMA">دبلوم</option>
                <option value="BACHELOR">بكالوريوس</option>
                <option value="MASTER">الماجستير</option>
                <option value="DOCTORAL">دكتوراه</option>
            </select>
        </p>

        <p>
            <label for="id_educational_institution_${x}">الجهة التعليمية:</label>
            <input type="text" name="educational-institution-${x}" maxlength="128" required id="id_educational_institution_${x}">
        </p>
        
        <p>
            <label for="id_major_${x}">التخصص: </label>
            <input type="text" name="major-${x}" maxlength="128" required id="id_major_${x}">
        </p>

        <p>
            <label for="id_year_obtained_${x}">السنة المكتسة: </label>
            <input type="number" name="year-obtained-${x}" required id="id_year_obtained_${x}">
        </p>

        <p>
            <label for="id_grade_${x}">التقدير: </label>
            <input type="number" name="grade-${x}" step="any" required id="id_grade_${x}">
        </p>
        <hr>
    </div>
  `;

  sciDegreesContainer.insertAdjacentHTML("beforeend", markup);
}

function removeSciDegree() {
  sciDegreesContainer.removeChild(sciDegreesContainer.lastElementChild);
}
