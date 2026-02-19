from flask import Flask, request, jsonify, render_template_string
from send_mail_update2 import send_bulk_emails
from dotenv import load_dotenv
load_dotenv()
app = Flask(__name__)

HTML = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>SMTP Bulk Sender</title>
  <style>
    body{font-family:Arial;max-width:900px;margin:40px auto;padding:0 16px}
    .card{border:1px solid #ddd;border-radius:12px;padding:16px}
    textarea{width:100%;min-height:220px;padding:10px;border:1px solid #ccc;border-radius:10px}
    button{margin-top:12px;padding:10px 16px;border:0;border-radius:10px;cursor:pointer}
    .note{color:#555;font-size:14px;margin-top:8px}
    pre{background:#111;color:#eee;padding:12px;border-radius:10px;overflow:auto}
  </style>
</head>
<body>
  <h2>Bulk Email Sender (10s delay)</h2>
  <div class="card">
    <div class="note">
      Paste emails (comma or newline separated). Message is fixed: <b>hi this is vaibhav from docker container</b>
    </div>
    <textarea id="emails" placeholder="a@example.com&#10;b@example.com"></textarea>
    <button onclick="startSend()">Start</button>
    <div class="note" id="status"></div>
    <pre id="out" style="display:none;"></pre>
  </div>

<script>
async function startSend(){
  const raw = document.getElementById("emails").value;
  document.getElementById("status").textContent = "Sending...";
  document.getElementById("out").style.display = "none";

  const res = await fetch("/send", {
    method: "POST",
    headers: {"Content-Type":"application/json"},
    body: JSON.stringify({ emails: raw })
  });

  const data = await res.json();
  document.getElementById("status").textContent = data.ok ? "Done." : ("Failed: " + data.error);
  document.getElementById("out").style.display = "block";
  document.getElementById("out").textContent = JSON.stringify(data, null, 2);
}
</script>
</body>
</html>
"""

@app.get("/")
def home():
    return render_template_string(HTML)

@app.post("/send")
def send():
    data = request.get_json(force=True) or {}
    raw = (data.get("emails") or "").strip()

    # split by newline and commas
    parts = raw.replace("\n", ",").split(",")
    recipients = [p.strip() for p in parts if p.strip()]

    try:
        results = send_bulk_emails(recipients, delay_seconds=10)
        return jsonify({"ok": True, **results})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
