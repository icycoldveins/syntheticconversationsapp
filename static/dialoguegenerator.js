document
  .querySelector(".text-container")
  .addEventListener("click", function (event) {
    const clickedElement = event.target.closest("div");
    console.log("Clicked element:", clickedElement); // Debug statement
    if (!clickedElement) return; // Exit if clicked outside of any div

    generateDialogue(clickedElement);
  });

function generateDialogue(element) {
  const text = element.textContent.trim();
  const title = document.querySelector("h1").textContent;
  console.log("Text:", text); // Debug statement
  console.log("Title:", title); // Debug statement

  // Modularized fetch request
  postDialogueData({ content: text, title })
    .then((data) => {
      console.log("Dialogue data:", data); // Debug statement
      data.dialogue
        .split("\n")
        .filter((line) => line.trim() !== "")
        .forEach((line) => {
          const [role, dialogueText] = line
            .split(":")
            .map((part) => part.trim());
          if (role && dialogueText) {
            createAndAppendDialogueSection(
              role.toLowerCase() + "-section",
              role,
              dialogueText
            );
          }
        });
    })
    .catch((error) => {
      console.error("Error generating dialogue:", error);
    });
}

// Modularized fetch request logic
function postDialogueData(body) {
  return fetch("/generate-dialogue", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  }).then((response) => {
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.json();
  });
}

function createAndAppendDialogueSection(sectionId, role, dialogueText) {
  const container = document.querySelector(".space-y-4");
  const bgColorClass = role === "Teacher" ? "bg-blue-100" : "bg-yellow-100";
  const colorIndicatorClass =
    role === "Teacher" ? "bg-blue-500" : "bg-yellow-500";
  const textColorClass =
    role === "Teacher" ? "text-blue-800" : "text-yellow-800";

  const section = document.createElement("div");
  section.className = `p-4 rounded-lg ${bgColorClass}`;

  const header = document.createElement("div");
  header.className = "flex items-center";

  const colorIndicator = document.createElement("div");
  colorIndicator.className = `rounded-full w-3 h-3 mr-2 ${colorIndicatorClass}`;

  const roleText = document.createElement("p");
  roleText.className = `font-semibold ${textColorClass}`;
  roleText.textContent = role;

  const dialogueContent = document.createElement("div");
  dialogueContent.className = "mt-2 ml-5 text-gray-700";
  dialogueContent.textContent = dialogueText;

  header.appendChild(colorIndicator);
  header.appendChild(roleText);
  section.appendChild(header);
  section.appendChild(dialogueContent);
  container.appendChild(section);
}
