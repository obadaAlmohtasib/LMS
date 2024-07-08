//
// Elements
const institutionList = document.querySelector("select[name=institution]");
const courseList = document.querySelector("select[name=course]");
const groupList = document.querySelector("select[name=group]");

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
  fetchRelatedGroups(id);
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
      fillGroupList([]);
      resolve();
    } else {
      reject();
    }
  });
}
function fetchRelatedGroups(courseId) {
  return new Promise(async (resolve, reject) => {
    const res = await fetch(
      `${location.origin}/${courseId}/get_related_groups`,
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
      let { groups } = data.data;
      fillGroupList(groups);
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
function fillGroupList(groups) {
  groupList.innerHTML = "";
  let markup = `
    <option value="" disabled="disabled" selected="selected">
        إختر المجموعة
    </option>
  `;
  groups.forEach((group) => {
    markup += `<option value=${group[0]}>${group[1]}</option>`;
  });
  groupList.insertAdjacentHTML("beforeend", markup);
}
