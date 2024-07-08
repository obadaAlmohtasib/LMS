//
// Elements/Selectors
//
const courseList = document.querySelector(`select[name="course"]`);
const groupList = document.querySelector(`select[name="course_group"]`);
const topicList = document.querySelector(`select[name="topic"]`);
const userList = document.querySelector(`select[name="users"]`);

const userSourcesList = document.querySelector(`select[name="user_sources"]`);
const filteredUsersList = document.querySelector(
  `select[name="users_filtered"]`
);

const timingList = document.querySelector(`select[name="timing"]`);
const classScheduleList = document.querySelector(
  `select[name="class_schedule"]`
);
const entryDateField = document.querySelector("input[name=entry_date]");
const repeatTimesField = document.getElementById("id_repeat_times");

//
// Listeners
//
document.addEventListener("DOMContentLoaded", (_) => {
  if (!userList || !userSourcesList) return;

  userList.innerHTML = "";
  let markup = `<option value selected>---------</option>`;
  userSourcesList.insertAdjacentHTML("afterbegin", markup);
});

//
// Functions
// Dependent Dropdown Lists
//
courseList.addEventListener("change", function (e) {
  const id = this.value;
  if (!id) return;
  fetchRelatedData(id);
});
export function fetchRelatedData(id) {
  return new Promise(async (resolve, reject) => {
    const res = await fetch(`${location.origin}/${id}/get_related_models`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
    });
    const data = await res.json();
    if (data["status_code"] === 200) {
      manipulateLists(data.data);
      resolve();
    } else {
      reject();
    }
  });
}
function manipulateLists(data) {
  let { groups, topics, users, timings, schedules } = data;
  fillGroupList(groups);
  fillTopicList(topics);
  fillFilteredUsersList(users);
  fillTimingList(timings);
  fillClassScheduleList(schedules);
}
function fillGroupList(groups) {
  groupList.innerHTML = "";
  let markup = `<option value selected>---------</option>`;
  groups.forEach((group) => {
    markup += `<option value=${group[0]}>${group[1]}</option>`;
  });
  groupList.insertAdjacentHTML("beforeend", markup);
}
function fillTopicList(topics) {
  topicList.innerHTML = "";
  let markup = `<option value selected>---------</option>`;
  topics.forEach((topic) => {
    markup += `
      <option value=${topic[0]} data-topic-type=${topic[1]}>${topic[2]}</option>
    `;
  });
  topicList.insertAdjacentHTML("beforeend", markup);
}
function fillTimingList(timings) {
  timingList.innerHTML = "";
  let markup = `<option value selected>---------</option>`;
  timings.forEach((timing) => {
    markup += `<option value=${timing[0]}>${timing[1]}</option>`;
  });
  timingList.insertAdjacentHTML("beforeend", markup);
}
function fillClassScheduleList(schedules) {
  classScheduleList.innerHTML = "";
  let markup = `<option value selected>---------</option>`;
  schedules.forEach((schedule) => {
    markup += `<option value=${schedule[0]}>${schedule[1]}</option>`;
  });
  classScheduleList.insertAdjacentHTML("beforeend", markup);
}

//
// Exclude busy users
//
entryDateField.addEventListener("input", async function (e) {
  let date = String(this.value);
  let timingId = timingList.value;
  let skdId = classScheduleList.value;
  let type = userSourcesList.value;
  if (!date || !timingId || !skdId || !type) return;

  await filterUsers(skdId, date, type);
});

//
// Dependent Dropdown Lists
//
topicList.addEventListener("change", async function (e) {
  let topicId = this.value;
  let groupId = groupList.value;
  if (!groupId || !topicId) return (this.value = "");
  await getRemainingClasses(groupId, topicId);
});
function getRemainingClasses(groupId, topicId) {
  return new Promise(async (resolve, reject) => {
    const res = await fetch(
      `${location.origin}/${groupId}/${topicId}/get_remaining_classes`,
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
      let { remainingClasses } = data.data;

      repeatTimesField.min = 1;
      repeatTimesField.max = remainingClasses;

      if (!remainingClasses) {
        // In case remains = ZERO
        classScheduleList.disabled = true;

        repeatTimesField.disabled = true;
        repeatTimesField.required = true;
        alert("You have reached the target number of classes");
      } else {
        classScheduleList.disabled = false;

        repeatTimesField.disabled = false;
        repeatTimesField.required = true;
      }

      resolve();
    } else {
      alert(data["message"]);
    }
  });
}

//
// Remaining classes
//
groupList.addEventListener("change", async function (e) {
  let groupId = this.value;
  let topicId = topicList.value;
  if (!groupId || !topicId) return;
  await getRemainingClasses(groupId, topicId);
});

//
// Timing
//
timingList.addEventListener("change", async function (e) {
  let id = this.value;
  if (!id) return;
  await getSchedules(id);
});
function getSchedules(seasonId) {
  return new Promise(async (resolve, reject) => {
    const res = await fetch(`${location.origin}/${seasonId}/get_schedules`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
    });
    const data = await res.json();
    if (data["status_code"] === 200) {
      const { start_date, schedules } = data.data;
      entryDateField.value = start_date;
      fillClassScheduleList(schedules);
      resolve();
    } else {
      reject("No data fetched");
    }
  });
}

//
// Active user
//
classScheduleList.addEventListener("change", async function (e) {
  let skdId = this.value;
  let timingId = timingList.value;
  let date = String(entryDateField.value);
  let type = userSourcesList.value;
  if (!skdId || !timingId || !date) return;

  filterUsers(skdId, date, type);
});

userSourcesList.addEventListener("change", async function (e) {
  let value = this.value;
  let date = String(entryDateField.value);
  let timingId = timingList.value;
  let skdId = classScheduleList.value;
  if (!date || !timingId || !skdId || !value) return;

  await filterUsers(skdId, date, value);
});
function filterUsers(skdId, date, type) {
  return new Promise(async (resolve, reject) => {
    const res = await fetch(
      `${location.origin}/${skdId}/filter_active_users?date=${date}&type=${type}`,
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
      const { users } = data.data;
      fillFilteredUsersList(users);
      resolve();
    } else {
      reject("No data fetched");
    }
  });
}
function fillFilteredUsersList(users) {
  filteredUsersList.innerHTML = "";
  let markup = "<option value selected>---------</option>";
  users.forEach((user) => {
    markup += `<option value=${user[0]}>${user[1]}</option>`;
  });
  filteredUsersList.insertAdjacentHTML("beforeend", markup);
}
filteredUsersList.addEventListener("change", function (e) {
  const id = this.value;
  if (!id) return; //No value
  const text = this.options[this.selectedIndex].text;
  const markup = `<option value=${id}>${text}</option>`;
  const options = Array.from(userList.options);
  const res = options.filter((opt) => opt.value === id);
  if (res.length > 0) return; //Already exist
  userList.insertAdjacentHTML("beforeend", markup);
});
