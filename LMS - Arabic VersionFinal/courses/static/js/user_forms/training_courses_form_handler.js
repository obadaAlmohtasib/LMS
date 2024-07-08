const trainingCourseContainer = document.querySelector(
  ".training-courses-container"
);
const addTrainingCourseBtn = document.querySelector(".add-training-course-btn");
const removeTrainingCourseBtn = document.querySelector(
  ".remove-training-course-btn"
);

addTrainingCourseBtn.addEventListener("click", (_) => {
  removeTrainingCourseBtn.parentElement.style.display = "block";
  insertNewTrainingCourse();
});
removeTrainingCourseBtn.addEventListener("click", (_) => {
  removeTrainingCourse();
  if (!trainingCourseContainer.childElementCount) {
    removeTrainingCourseBtn.parentElement.style.display = "none";
  }
});

function insertNewTrainingCourse() {
  const x = trainingCourseContainer.childElementCount + 1;

  // 'crs-' Prefix
  // Do not forgot to add a prefix to name's value, since some fields got conflict with other models' fields
  const markup = `
    <div class="training-course-${x}">
        <p>
          <label for="id_crs_name_${x}">اسم الدورة: </label>
          <input type="text" name="crs-name-${x}" maxlength="128" required id="id_crs_name_${x}">
        </p>
        
        <p>
          <label for="id_crs_party_${x}">الجهة: </label>
          <input type="text" name="crs-party-${x}" maxlength="128" required id="id_crs_party_${x}">
        </p>
          
        <p>
          <label for="id_crs_start_date_${x}">تاريخ البداية: </label>
          <input type="date" name="crs-start-date-${x}" required id="id_crs_start_date_${x}">
        </p>
        
        <p>
          <label for="id_crs_end_date_${x}">تاريخ النهاية: </label>
          <input type="date" name="crs-end-date-${x}" required id="id_crs_end_date_${x}">
        </p>
        
        <p>
          <label for="id_crs_description_${x}">الوصف: </label>
          <input type="text" name="crs-description-${x}" required id="id_crs_description_${x}">
        </p>
        <hr>
    </div>
  `;

  trainingCourseContainer.insertAdjacentHTML("beforeend", markup);
}

function removeTrainingCourse() {
  trainingCourseContainer.removeChild(trainingCourseContainer.lastElementChild);
}
