import fastify from "fastify";
import * as marked from "marked";
import path from "node:path";

const app = fastify();

app.register(await import("@fastify/static"), {
  root: path.join(import.meta.dirname, "public"),
  prefix: "/",
});

const sanitize = (unsafe) => unsafe.replaceAll("<", "＜").replaceAll(">", "＞");

const escapeHtml = (str) =>
  str
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");

const unescapeHtml = (str) =>
  str
    .replaceAll("&amp;", "&")
    .replaceAll("&lt;", "<")
    .replaceAll("&gt;", ">")
    .replaceAll("&quot;", '"')
    .replaceAll("&#039;", "'");

app.get("/render", async (req, reply) => {
  const markdown = sanitize(String(req.query.markdown));
  if (markdown.length > 1024) {
    return reply.status(400).send("Too long");
  }

  const escaped = escapeHtml(marked.parse(markdown));
  const unescaped = unescapeHtml(escaped);

  return { escaped, unescaped };
});

// Rate limiting for report endpoint
const reportRateLimit = new Map();

// Serve the report page
app.get("/report", async (req, reply) => {
  return reply.sendFile("report.html");
});

app.post("/api/report", async (req, reply) => {
  // Simple rate limiting - 4 requests per minute per IP
  const clientIp = req.ip;
  const now = Date.now();
  const windowMs = 60 * 1000; // 1 minute
  
  if (!reportRateLimit.has(clientIp)) {
    reportRateLimit.set(clientIp, []);
  }
  
  const requests = reportRateLimit.get(clientIp);
  // Clean old requests
  const recentRequests = requests.filter(time => now - time < windowMs);
  
  if (recentRequests.length >= 4) {
    return reply.status(429).send("Too Many Requests");
  }
  
  recentRequests.push(now);
  reportRateLimit.set(clientIp, recentRequests);

  const { url } = req.body;
  if (
    typeof url !== "string" ||
    (!url.startsWith("http://") && !url.startsWith("https://"))
  ) {
    return reply.status(400).send("Invalid url");
  }

  try {
    // Make internal request to bot service
    const response = await fetch("http://bot:1337/api/report", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ url }),
    });

    if (response.ok) {
      return reply.status(200).send("Completed!");
    } else {
      const errorText = await response.text();
      return reply.status(500).send(errorText || "Something wrong");
    }
  } catch (e) {
    console.error(e);
    return reply.status(500).send("Something wrong");
  }
});

app.listen({ port: 3000, host: "0.0.0.0" });