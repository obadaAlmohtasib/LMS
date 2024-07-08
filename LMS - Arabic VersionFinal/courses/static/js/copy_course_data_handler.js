//
// Elements
const institutionList = document.querySelector("select[name=institution]");
const courseList = document.querySelector("select[name=course]");
const copyToInstitutionList = document.querySelector(
  "select[name=copy-to-institution]"
);
const copyCourseDataLink = document.querySelector("#copy_course_data_link");
const form = document.querySelector("form.container");

//
// Handlers
institutionList.addEventListener("change", function () {
  id = this.value;
  if (!id) return;
  fetchRelatedCourses(id);
});
courseList.addEventListener("change", function () {
  id = this.value;
  if (!id) return;
});
function fetchRelatedCourses(instId) {
  return new Promise(async (resolve, reject) => {
    const res = await fetch(
      `${location.origin}/${instId}/get_related_courses`,
      {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json",
        },
      }
    );
    const data = await res.json();
    if (data["status_code"] === 200) {
      let { courses } = data.data;
      fillCourseList(courses);
      resolve();
    } else {
      reject();
    }
  });
}

function fillCourseList(courses) {
  courseList.innerHTML = "";
  let markup = `
    <option value="" disabled="disabled" selected="selected">
        إختر الدورة
    </option>
  `;
  courses.forEach((course) => {
    markup += `
          <option value=${course[0]}>${course[1]}</option>
        `;
  });
  courseList.insertAdjacentHTML("beforeend", markup);
}

copyCourseDataLink.addEventListener("click", async function (e) {
  e.preventDefault();
  console.log("inside event");
  const courseId = courseList.value;
  const copyToInstitutionId = copyToInstitutionList.value;

  form.reset();

  if (!courseId || !copyToInstitutionId) return;

  const params = `course=${courseId}&&copy-to-institution=${copyToInstitutionId}`;
  const res = await fetch(`${location.origin}/copy-course-data?${params}`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json",
    },
  });
  const data = await res.json();
  console.log(data);
  if (data["status_code"] === 200) {
    let { message } = data;
    alert(message);
  } else {
    let { message } = data;
    alert(message);
  }
});
