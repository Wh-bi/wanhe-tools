"""
AI Toolbox Backend v1.0 - Unified API for Summarizer + RAG
"""
import json, os, requests, time
from datetime import date
from http.server import HTTPServer, BaseHTTPRequestHandler
import chromadb

OLLAMA_URL = "http://localhost:11434"
MODEL = "qwen3:0.6b"
EMBED_MODEL = "nomic-embed-text"
PORT = 8888
RAG_DB = r"D:\Lobster_Workspace\projects\rag_from_scratch\chroma_db"
RAG_DOCS = r"D:\Lobster_Workspace\projects\rag_from_scratch\docs"
USAGE_LOG = r"D:\Lobster_Workspace\sandbox\usage.log"
START_TIME = time.time()

def log_usage(action, **kwargs):
    ts = time.strftime("%Y-%m-%d %H:%M:%S")
    parts = [f"{ts} | {action}"]
    for k, v in kwargs.items():
        parts.append(f"{k}={v}")
    with open(USAGE_LOG, "a", encoding="utf-8") as f:
        f.write(" | ".join(parts) + "\n")

def get_stats():
    today = str(date.today())
    stats = {"today": {}, "total": {}}
    try:
        with open(USAGE_LOG, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except:
        return stats
    for line in lines:
        parts = line.strip().split(" | ")
        if len(parts) < 2:
            continue
        line_date = parts[0][:10]
        action = parts[1]
        for p in parts[2:]:
            if "=" in p:
                k, v = p.split("=", 1)
                if k in ("chars_in", "chars_out"):
                    v = int(v)
        if action not in stats["total"]:
            stats["total"][action] = 0
        stats["total"][action] += 1
        if line_date == today:
            if action not in stats["today"]:
                stats["today"][action] = 0
            stats["today"][action] += 1
    return stats

chroma_client = chromadb.PersistentClient(path=RAG_DB)
try:
    collection = chroma_client.get_collection(name="rag_test")
except:
    collection = chroma_client.create_collection(name="rag_test")

def chunk_text(text, size=300, overlap=50):
    chunks = []
    start = 0
    while start < len(text):
        chunks.append(text[start:start + size])
        start += size - overlap
    return chunks

def get_uptime():
    mins = int((time.time() - START_TIME) / 60)
    if mins < 60:
        return f"{mins}m"
    return f"{mins//60}h{mins%60}m"

def get_ollama_models():
    try:
        r = requests.get(f"{OLLAMA_URL}/api/tags", timeout=5)
        if r.status_code == 200:
            return [m["name"] for m in r.json().get("models", [])]
    except:
        pass
    return []

class ToolboxHandler(BaseHTTPRequestHandler):
    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def do_OPTIONS(self):
        self.send_response(200)
        self._cors()
        self.end_headers()

    def do_GET(self):
        if self.path == "/":
            self._handle_root()
        elif self.path == "/health":
            self._handle_health()
        elif self.path == "/stats":
            self._handle_stats()
        else:
            self.send_error(404)

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(length)) if length > 0 else {}
        if self.path == "/summarize":
            self._handle_summarize(body)
        elif self.path == "/rag/query":
            self._handle_rag_query(body)
        elif self.path == "/rag/upload":
            self._handle_rag_upload(body)
        elif self.path == "/translate":
            self._handle_translate(body)
        elif self.path == "/review":
            self._handle_review(body)
        elif self.path == "/classify":
            self._handle_classify(body)
        else:
            self.send_error(404)

    def _handle_root(self):
        models = get_ollama_models()
        doc_count = collection.count()
        model_list = "".join(f"<li>{m}</li>" for m in models)
        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head><meta charset="UTF-8"><title>AI Toolbox Status</title>
<style>body{{font-family:-apple-system,BlinkMacSystemFont,sans-serif;background:#0f172a;color:#e2e8f0;padding:40px}}h1{{color:#60a5fa}}table{{border-collapse:collapse;margin:16px 0}}td{{padding:8px 16px;border-bottom:1px solid #334155}}.ok{{color:#4ade80}}.val{{color:#a78bfa}}</style></head>
<body>
<h1>AI Toolbox v1.0</h1>
<h2>Status</h2>
<table>
<tr><td>Ollama</td><td class="ok">Connected ({len(models)} models)</td></tr>
<tr><td>RAG Database</td><td class="ok">{doc_count} docs indexed</td></tr>
<tr><td>Uptime</td><td class="val">{get_uptime()}</td></tr>
</table>
<h3>Models</h3><ul>{model_list}</ul>
<h3>Endpoints</h3>
<table>
<tr><td>GET /</td><td>This page</td></tr>
<tr><td>GET /health</td><td>Health check JSON</td></tr>
<tr><td>POST /summarize</td><td>Text summarization</td></tr>
<tr><td>POST /rag/query</td><td>RAG question answering</td></tr>
<tr><td>POST /rag/upload</td><td>Upload document to RAG</td></tr>
</table>
</body></html>"""
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self._cors()
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))

    def _handle_health(self):
        ollama_ok = len(get_ollama_models()) > 0
        self._json_response({
            "status": "ok" if ollama_ok else "degraded",
            "ollama": ollama_ok,
            "rag": collection.count() > 0,
            "uptime": get_uptime(),
            "models": get_ollama_models(),
            "doc_count": collection.count(),
            "default_model": MODEL
        })

    def _handle_stats(self):
        self._json_response(get_stats())

    def _handle_translate(self, body):
        text = body.get("text", "")
        target_lang = body.get("target_lang", "Chinese")
        if not text:
            self._json_response({"error": "No text"}, 400)
            return
        prompt = f"Translate the following text to {target_lang}. Only output the translation, no explanations:\n\n{text}\n\nTranslation:"
        resp = requests.post(f"{OLLAMA_URL}/api/generate", json={
            "model": MODEL, "prompt": prompt, "stream": False,
            "options": {"temperature": 0.1}
        }, timeout=60)
        result = resp.json()["response"] if resp.status_code == 200 else "Translation failed"
        log_usage("translate", chars_in=len(text), target=target_lang)
        self._json_response({"translation": result})

    def _handle_review(self, body):
        code = body.get("code", "")
        language = body.get("language", "auto")
        if not code:
            self._json_response({"error": "No code"}, 400)
            return
        prompt = f"""Review the following code. List:
1. Potential bugs and logic errors
2. Performance optimizations
3. Security vulnerabilities
4. Code style improvements

Format the response with bullet points. Be concise.

Language: {language}
Code:
{code[:5000]}

Review:"""
        resp = requests.post(f"{OLLAMA_URL}/api/generate", json={
            "model": MODEL, "prompt": prompt, "stream": False,
            "options": {"temperature": 0.2}
        }, timeout=120)
        result = resp.json()["response"] if resp.status_code == 200 else "Review failed"
        log_usage("review", chars_in=len(code))
        self._json_response({"review": result})

    def _handle_classify(self, body):
        bookmarks = body.get("bookmarks", [])
        if not bookmarks:
            self._json_response({"error": "No bookmarks"}, 400)
            return
        titles = [f"{i}: {b['title']} - {b['url']}" for i, b in enumerate(bookmarks[:50])]
        prompt = f"""Classify these bookmarks into exactly these categories: Work, Study, Entertainment, Tools, Social, News, Uncategorized.

For each bookmark, output ONLY its index and category in this format:
index:category

Bookmarks:
{chr(10).join(titles)}

Output:"""
        resp = requests.post(f"{OLLAMA_URL}/api/generate", json={
            "model": MODEL, "prompt": prompt, "stream": False,
            "options": {"temperature": 0.1}
        }, timeout=60)
        text = resp.json()["response"] if resp.status_code == 200 else ""
        # Parse response: "0:Work\n1:Tools\n..."
        categories = {}
        import re
        for line in text.split("\n"):
            m = re.match(r"(\d+)\s*[:：]\s*(\w+)", line.strip())
            if m:
                idx = int(m.group(1))
                cat = m.group(2).strip()
                if cat not in categories:
                    categories[cat] = []
                categories[cat].append(idx)
        log_usage("classify", count=len(bookmarks))
        self._json_response({"categories": categories})

    def _handle_summarize(self, body):
        text = body.get("text", "")
        detail = body.get("detail", "moderate")
        model = body.get("model", MODEL)
        limits = {"brief": 100, "moderate": 300, "detailed": 600}
        limit = limits.get(detail, 300)
        prompt = f"Please summarize the following text in Chinese (within {limit} characters):\n\n{text}\n\nSummary:"
        resp = requests.post(f"{OLLAMA_URL}/api/generate", json={
            "model": model, "prompt": prompt, "stream": False,
            "options": {"temperature": 0.3}
        }, timeout=120)
        result = resp.json()["response"] if resp.status_code == 200 else "Failed"
        log_usage("summarize", chars_in=len(text), chars_out=len(result))
        self._json_response({"result": result})

    def _handle_rag_query(self, body):
        query = body.get("query", "")
        model = body.get("model", MODEL)
        if not query:
            self._json_response({"error": "No query"}, 400)
            return
        r = requests.post(f"{OLLAMA_URL}/api/embeddings", json={"model": EMBED_MODEL, "prompt": query})
        if r.status_code != 200:
            self._json_response({"error": "Embedding failed"}, 500)
            return
        qv = r.json()["embedding"]
        results = collection.query(query_embeddings=[qv], n_results=3)
        chunks = []
        if results["documents"] and results["documents"][0]:
            dists = results.get("distances", [[0]*3])[0]
            for i, (doc, meta) in enumerate(zip(results["documents"][0], results["metadatas"][0])):
                chunks.append({
                    "content": doc,
                    "source": meta.get("source", "unknown"),
                    "distance": round(dists[i], 4) if i < len(dists) else 0
                })
        if not chunks:
            self._json_response({"answer": "No relevant documents found.", "chunks": []})
            return
        ctx = "\n\n---\n\n".join([c["content"] for c in chunks])
        prompt = f"Answer based on references. If not found, say so.\n\nReferences:\n{ctx}\n\nQuestion: {query}\n\nAnswer (in Chinese):"
        r2 = requests.post(f"{OLLAMA_URL}/api/generate", json={
            "model": model, "prompt": prompt, "stream": False,
            "options": {"temperature": 0.3}
        }, timeout=120)
        answer = r2.json()["response"] if r2.status_code == 200 else "Generation failed"
        log_usage("rag_query", question=query[:30], chunks=len(chunks), model=model)
        self._json_response({"answer": answer, "chunks": chunks})

    def _handle_rag_upload(self, body):
        filename = body.get("filename", "upload.txt")
        content = body.get("content", "")
        if not content:
            self._json_response({"error": "No content"}, 400)
            return
        os.makedirs(RAG_DOCS, exist_ok=True)
        filepath = os.path.join(RAG_DOCS, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        chunks = chunk_text(content)
        for i in range(0, len(chunks), 5):
            batch = chunks[i:i+5]
            vectors = []
            for chunk in batch:
                r = requests.post(f"{OLLAMA_URL}/api/embeddings", json={"model": EMBED_MODEL, "prompt": chunk})
                vectors.append(r.json()["embedding"] if r.status_code == 200 else [0.0]*768)
            max_id = len(collection.get()["ids"]) if collection.count() > 0 else 0
            collection.add(
                embeddings=vectors, documents=batch,
                metadatas=[{"source": f"{filename}#{j}"} for j in range(len(batch))],
                ids=[f"up_{max_id+j}" for j in range(len(batch))]
            )
        self._json_response({"status": "ok", "chunks": len(chunks), "filename": filename})

    def _json_response(self, data, code=200):
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self._cors()
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))

    def log_message(self, format, *args):
        print(f"[Toolbox] {args[0]}")

if __name__ == "__main__":
    print(f"AI Toolbox v1.0: http://localhost:{PORT}")
    print(f"  GET  /          - Status dashboard")
    print(f"  GET  /health    - Health check")
    print(f"  POST /summarize - Text summarization")
    print(f"  POST /rag/query - RAG question answering")
    print(f"  POST /rag/upload - Upload document to RAG")
    HTTPServer(("localhost", PORT), ToolboxHandler).serve_forever()
