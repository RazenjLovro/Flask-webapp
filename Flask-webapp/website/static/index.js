function deleteNote(noteId) {
    fetch("/delete-note", {
      method: "POST",
      body: JSON.stringify({ noteId: noteId }),
    }).then((_res) => {
      window.location.href = "/";
    });
  }


function deleteProject(projectId) {
  fetch("/delete-project", {
    method: "POST",
    body: JSON.stringify({ projectId: projectId }),
  }).then((_res) => {
    window.location.href = "/projects";
  });
}
function deleteHole(holeId) {
  debugger
  fetch("/delete-hole", {
    method: "POST",
    body: JSON.stringify({ holeId: holeId }),
  }).then((_res) => {
    window.location.href = "/projects";
  });
}

function deleteLayer(layerId) {
  debugger
  fetch("/delete-layer", {
    method: "POST",
    body: JSON.stringify({ layerId: layerId }),
  }).then((_res) => {
    window.location.href = "/projects";
  });
}