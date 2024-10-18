/* Listener on file uploader for styling purposes */
document.querySelector("#file").addEventListener("change", function () {
  const fileName = this.files[0].name;
  const fileSelectedLabel = document.getElementById("file-selected");
  fileSelectedLabel.innerHTML = fileName;
  fileSelectedLabel.style.color = "#fbfbfb";
});

document.querySelector("#run-button").addEventListener("click", function () {
  const file = document.getElementById("file").files[0];
  if (file !== undefined) doRun(file);
  else document.querySelector("#file-selected").style.color = "red";
});

function doRun(file) {
  const apiCallArgs = {
    model: document.querySelector("#model").innerHTML.trim(),
    analysisMode: document.querySelector("#analysis-mode").innerHTML.trim(),
    prompt: document.querySelector("#prompt-field").value,
  };
  const formData = new FormData();
  formData.append("file", file);
  formData.append("apiCallArgs", JSON.stringify(apiCallArgs));
  fetch("/upload", {
    method: "POST",
    body: formData,
  })
    .then((response) => response.text())
    .then((data) => (document.querySelector("#output-body").innerHTML = data))
    .catch((error) => console.error(error));
}
