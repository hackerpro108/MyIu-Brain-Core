export async function sendCommand(cmd) {
  const r = await fetch("http://103.78.2.25:12440/send_command", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ command: cmd })
  });
  return await r.json();
}
export async function getLog() {
  const r = await fetch("http://103.78.2.25:12440/log");
  return await r.json();
}
