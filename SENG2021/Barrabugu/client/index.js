const fetchStudentOrganizationPromise = fetch(
  "/api/students-organization"
  ).then((response) => response.json())

document.addEventListener("DOMContentLoaded", () => {

    window.Svgs = {
        dragHandle: document.querySelector("#svg-drag-handle")
    }

    EM.init()

    Sync.init()
    MainContainer.init() // Teams and teamless
    StudentDetailsPopup.init()
    Filter.init()

    fetchStudentOrganizationPromise.catch(err => {
        alert(`Error occured whilst fetching the student organization data. Please reload the page.\n\n\t${err}`);
    }).then((data) => {
        EM.emit("students-organization-recieved", data)
    })
});
