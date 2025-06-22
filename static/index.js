const ws = new WebSocket(`ws://${location.host}/ws`);
const container = document.getElementById("orders");

ws.onmessage = (e) => {
  const { event, document_id, before, after } = JSON.parse(e.data);

  const div = document.createElement("div");
  div.classList.add("order", event);

  let beforeContent = before && Object.keys(before).length ? JSON.stringify(before, null, 2) : "N/A";
  let afterContent = after && Object.keys(after).length ? JSON.stringify(after, null, 2) : (event === "delete" ? "Document deleted." : "N/A");

  div.innerHTML = `
    <strong>${event.toUpperCase()}</strong><br/>
    <strong>ID:</strong> ${document_id}<br/>
    <strong>Before:</strong><pre>${beforeContent}</pre>
    <strong>After:</strong><pre>${afterContent}</pre>
  `;

  container.prepend(div);
};