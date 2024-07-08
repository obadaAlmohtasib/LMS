//
// Elements / Selectors
//
formsTogglers = document.querySelectorAll(".card #form_toggler");
saveButtons = document.querySelectorAll(".save_btn");
cancelButtons = document.querySelectorAll(".cancel_btn");
topicsTable = document.querySelector(".fl-table");
publicHolidaysContainer = document.querySelector(
  ".card-public-holidays .card-body"
);
timingsContainer = document.querySelector(".card-timings .card-body");
courseGroupsContainer = document.querySelector(
  ".card-course-groups .card-body"
);
courseStatusCheckbox = document.querySelector("#status_chk");
courseReleaseBtn = document.querySelector(".release_btn");
courseCancelDateBtn = document.querySelector(".cancel_date_btn");

//
// FORM handler
//
formsTogglers.forEach((el) => {
  el.addEventListener("click", function (e) {
    const form = e.target.closest(".card").querySelector("form");
    // form = e.target.closest(".card form");
    if (form) {
      form.classList.toggle("hidden");
    }
  });
});

//
// POST data ( SAVE opt )
//
saveButtons.forEach((el) => {
  el.addEventListener("click", async function (e) {
    e.preventDefault();
    const form = e.target.closest(".card form");
    const url = form.action;
    // console.log(formData); // looks like an empty object, => you've to Split/Destructure it
    const dataArr = [...new FormData(form)];
    data = Object.fromEntries(dataArr);
    // console.log(data);
    // console.log(JSON.stringify(data));
    // console.log(...formData);
    await postData(url, data);
    form.reset();
    form.classList.add("hidden");
  });
});

//
// CANCEL FORM ( RESET )
//
cancelButtons.forEach((el) => {
  el.addEventListener("click", function (e) {
    e.target.closest(".card form")?.classList.toggle("hidden");
  });
});

async function postData(url, payload) {
  const csrfToken = payload["csrfmiddlewaretoken"];

  const response = await fetch(url, {
    method: "POST",
    headers: {
      "X-CSRFTOKEN": csrfToken,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  const data = await response.json();
  if (data?.["status_code"] == 201) {
    alert("Data inserted successfully :)");
    appendData(data);
  } else {
    alert("Something went wrong :(");
  }
}

//
// APPEND NEW ADDED DATA [  PUBLIC_HOLIDAY  |  COURSE_GROUP ]
//
function appendData(data) {
  let markup = "";
  const { type, object } = data["data"]; // Destructure

  if (type === "Public Holiday") {
    markup += `
        <div class="public-holiday-info-wrapper">
          <div class="public-holiday-event">
            <p>${object.event_name}</p>
          </div>
          <div class="public-holiday-date-range">
            <p class="public-holiday-date"><b>${object.start_date}</b></p>
            <p class="public-holiday-date"><b>TO</b></p>
            <p class="public-holiday-date"><b>${object.end_date}</b></p>
          </div>
          <div>
            <a
              id="delete_public_holiday_link"
              data-model-id="${object.id}"
              data-model-name="${object.event_name}"
              href="#">حذف
            </a>
          </div>
        </div>
      `;
    document
      .querySelector(".card-public-holidays .card-body")
      .insertAdjacentHTML("beforeend", markup);
  }

  if (type === "Course Group") {
    markup += `
        <div class="course-groups-info-wrapper">
          <div class="course-group-name">
            <p>${object.name}</p>
          </div>
          <div class="course-groups-actions">
            <a
              id="view_course_group_link"
              href="/${object.id}/view_course_group"
              >عرض</a
            >
            <a
              id="edit_course_group_link"
              href="/${object.id}/edit_course_group"
              >تعديل</a
            >
            <a
              id="delete_course_group_link"
              data-model-id="${object.id}"
              data-model-name="${object.name}"
              href="#"
              >حذف</a
            >
          </div>
        </div>
      `;
    document
      .querySelector(".card-course-groups .card-body")
      .insertAdjacentHTML("beforeend", markup);
  }
}

//
// DELETE Topic
//
topicsTable?.addEventListener("click", async (e) => {
  let el = e.target.closest("#delete_topic_link");
  if (!el) return;
  let { modelId, modelName } = el?.closest("td").dataset;
  if (el && confirm(`Are you sure that you want to delete? ${modelName}`)) {
    e.preventDefault();
    const csrfToken = document.querySelector(
      "input[name='csrfmiddlewaretoken']"
    ).value;
    let res = await fetch(`${location.origin}/${modelId}/delete_topic`, {
      method: "delete",
      headers: {
        "X-CSRFTOKEN": csrfToken,
        "Content-Type": "application/json",
      },
    });
    let data = await res.json();
    if (data.status_code === 204) {
      el.closest("tr").remove();
    }
  }
});

//
// DELETE Public Holiday
//
publicHolidaysContainer.addEventListener("click", async (e) => {
  let el = e.target.closest("#delete_public_holiday_link");
  if (!el) return;
  let { modelId, modelName } = el.dataset;
  if (el && confirm(`Are you sure that you want to delete? ${modelName}`)) {
    e.preventDefault();
    const CSRF_TOKEN = document.querySelector(
      `.public-holidays-form input[name="csrfmiddlewaretoken"]`
    ).value;
    let res = await fetch(
      `${location.origin}/${modelId}/delete_public_holiday`,
      {
        method: "delete",
        headers: {
          "X-CSRFTOKEN": CSRF_TOKEN,
          "Content-Type": "application/json",
        },
      }
    );
    let data = await res.json();
    if (data.status_code === 204) {
      el.closest(".public-holiday-info-wrapper").remove();
    } else {
      alert("Deletion Failed  :(  Try Again !");
    }
  }
});

//
// DELETE Timing
//
timingsContainer.addEventListener("click", async (e) => {
  let el = e.target.closest("#delete_timing_link");
  if (!el) return;
  let { modelId, modelName } = el.dataset;
  if (el && confirm(`Are you sure that you want to delete? ${modelName}`)) {
    e.preventDefault();
    const CSRF_TOKEN = el
      .closest(".card")
      .querySelector("input[name='csrfmiddlewaretoken']").value;

    let res = await fetch(`${location.origin}/${modelId}/delete_timing`, {
      method: "delete",
      headers: {
        "X-CSRFTOKEN": CSRF_TOKEN,
        "Content-Type": "application/json",
      },
    });
    let data = await res.json();
    if (data.status_code === 204) {
      el.closest(".timings-info-wrapper").remove();
    } else {
      alert("Deletion Failed  :(  Try Again !");
    }
  }
});

//
// DELETE Course Group
//
courseGroupsContainer.addEventListener("click", async (e) => {
  let el = e.target.closest("#delete_course_group_link");
  if (!el) return;
  let { modelId, modelName } = el.dataset;
  if (el && confirm(`Are you sure that you want to delete? ${modelName}`)) {
    e.preventDefault();
    const CSRF_TOKEN = el
      .closest(".card")
      .querySelector("input[name='csrfmiddlewaretoken']").value;
    let res = await fetch(`${location.origin}/${modelId}/delete_course_group`, {
      method: "delete",
      headers: {
        "X-CSRFTOKEN": CSRF_TOKEN,
        "Content-Type": "application/json",
      },
    });
    let data = await res.json();
    if (data.status_code === 204) {
      el.closest(".course-groups-info-wrapper").remove();
    } else {
      alert("Deletion Failed  :(  Try Again !");
    }
  }
});

// Checkbox
courseStatusCheckbox.addEventListener("change", async function (e) {
  const courseId = this.dataset.courseId;
  if (!courseId) return;

  if (this.checked) {
    // After Click
    // Checked
    modal.style.display = "block";
  } else {
    // un-checked
    let ans = confirm("Are you sure, you want to suspend the course?");
    if (!ans) {
      this.checked = !this.checked;
      return;
    }

    let res = await fetch(`${location.origin}/${courseId}/suspend_course`, {
      headers: {
        "Content-Type": "application/json",
      },
    });
    let data = await res.json();
    const course_status = data.course_status;

    if (course_status === "SUSPENDED") {
      alert("The course is suspended");
      document.getElementById("status_chk").removeAttribute("checked");
    } else {
      alert("Failed  :(  Try Again !");
    }
  }
});

courseReleaseBtn.addEventListener("click", async function (e) {
  e.preventDefault();
  parent = e.target.closest("form");
  const optList = document.getElementById("id_release_opt");
  const resumeDateField = document.getElementById("id_resume_date");

  if (!optList.value) return alert("Plz, Choose an option");

  if (optList.value === "custom_date" && !resumeDateField.value)
    return alert("Plz, Enter date:");

  const dataArr = [...new FormData(parent)];
  const formData = Object.fromEntries(dataArr);

  const CSRF_TOKEN = document.querySelector(
    ".suspension-date-form input[name='csrfmiddlewaretoken']"
  ).value;

  let res = await fetch(`${parent.action}`, {
    method: "POST",
    headers: {
      "X-CSRFTOKEN": CSRF_TOKEN,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(formData),
  });
  let data = await res.json();

  const course_status = data.course_status;
  progressBar = document.querySelector(".progress-bar");

  if (course_status === "RUNNING") {
    modal.style.display = "none";
    document.querySelector(".suspension-date-form").reset();
    if (progressBar) progressBar.style.display = "none";
  }
  if (course_status === "SUSPENDED") {
    alert("Course is suspended");
    modal.style.display = "none";
    document.querySelector(".suspension-date-form").reset();
    remaining_time = data.remaining_time;
    console.log(remaining_time);
    if (remaining_time) {
      if (progressBar) {
        courseStatusCheckbox.checked = false;
        progressBar.style.display = "block";
        document.querySelector(
          ".skill-count1"
        ).textContent = `after ${remaining_time} days`;
      }
    }
  }
});

courseCancelDateBtn.addEventListener("click", function (e) {
  cancelFunction();
});

//
// Modal
//
const modal = document.getElementById("modal-div");
const closeModalSpan = document.getElementById("close-modal-span");

closeModalSpan.addEventListener("click", function () {
  cancelFunction();
});

// When the user clicks anywhere outside of the modal, close it
window.onclick = function (e) {
  if (e.target == modal) {
    cancelFunction();
  }
};

function cancelFunction() {
  // In case of cancel => uncheck the box
  courseStatusCheckbox.checked = false;
  modal.style.display = "none";
}
