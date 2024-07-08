//
// Elements/Selectors
//
const tableWrapper = document.querySelector(".table-wrapper");

//
// Listeners
//
document.addEventListener("DOMContentLoaded", (_) => {});

tableWrapper.addEventListener("click", async (e) => {
  const el = e.target;
  if (!e.target.matches("a")) return;

  let { modelId } = el.closest("tr").dataset;

  if (
    el.matches("#delete_link") &&
    confirm(`Are you sure that you want to delete? entry=${modelId}`)
  ) {
    let deleted = deleteEntry(modelId);
    if (!deleted) return;
    el.closest("tr").remove(); //  el.parentElement.parentElement.remove();
  }
});

//
// Functions
//
// DELETE Entry
//
async function deleteEntry(id) {
  const CSRF_TOKEN = document.querySelector(
    "input[name=csrfmiddlewaretoken]"
  ).value;
  let res = await fetch(`${location.origin}/${id}/delete_daily_entry`, {
    method: "DELETE",
    headers: {
      "X-CSRFTOKEN": CSRF_TOKEN,
      "Content-Type": "application/json",
      Accept: "application/json",
    },
  });
  let data = await res.json();
  if (data["status_code"] === 204) {
    alert("Entry Deleted Successfully !");
    return true;
  } else if (data["status_code"] === 400) {
    alert("Something Went Wrong !");
    return false;
  }
}
