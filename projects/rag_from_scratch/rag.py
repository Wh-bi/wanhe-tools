"""
RAG 从零实现 —— 理解检索增强生成的每一步
"""
import os
import requests
import chromadb
import subprocess

# ===== 配置 =====
OLLAMA_URL = "http://localhost:11434"
MODEL_NAME = "qwen3:8b"
EMBED_MODEL = "nomic-embed-text"
DOCS_PATH = "docs"
CHUNK_SIZE = 300
CHUNK_OVERLAP = 50

print("=" * 50)
print("RAG 系统启动")
print(f"生成模型: {MODEL_NAME}  |  嵌入模型: {EMBED_MODEL}")
print("=" * 50)

# ===== 步骤1：加载文档 =====
def load_documents(docs_path):
    documents = []
    for filename in os.listdir(docs_path):
        if filename.endswith(".txt"):
            filepath = os.path.join(docs_path, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
                documents.append({"source": filename, "content": content})
            print(f"  已加载: {filename} ({len(content)} 字)")
    return documents

def chunk_text(text, size=300, overlap=50):
    chunks = []
    start = 0
    while start < len(text):
        chunks.append(text[start:start + size])
        start += size - overlap
    return chunks

print("\n[1/4] 加载并切分文档...")
docs = load_documents(DOCS_PATH)
all_chunks = []
chunk_sources = []
for doc in docs:
    chunks = chunk_text(doc["content"], CHUNK_SIZE, CHUNK_OVERLAP)
    for i, c in enumerate(chunks):
        all_chunks.append(c)
        chunk_sources.append(f"{doc['source']}#{i}")
    print(f"  {doc['source']} -> {len(chunks)} 块")
print(f"[OK] 共 {len(all_chunks)} 个文本块")

# ===== 步骤2：向量化存入 ChromaDB =====
print("\n[2/4] 向量化并存入数据库...")
chroma_client = chromadb.PersistentClient(path="./chroma_db")
try:
    collection = chroma_client.get_collection(name="rag_demo")
    collection.delete(ids=collection.get()["ids"])  # 清空旧数据
except:
    collection = chroma_client.create_collection(name="rag_demo")

for i in range(0, len(all_chunks), 5):
    batch = all_chunks[i:i+5]
    sources_batch = chunk_sources[i:i+5]
    vectors = []
    for chunk in batch:
        resp = requests.post(f"{OLLAMA_URL}/api/embeddings",
            json={"model": EMBED_MODEL, "prompt": chunk})
        vectors.append(resp.json()["embedding"] if resp.status_code == 200 else [0.0]*768)
    collection.add(
        embeddings=vectors,
        documents=batch,
        metadatas=[{"source": s} for s in sources_batch],
        ids=[f"chunk_{j}" for j in range(i, i+len(batch))]
    )
    print(f"  已存入 {min(i+5, len(all_chunks))}/{len(all_chunks)} 块")
print(f"[OK] 数据库就绪，共 {collection.count()} 条")

# ===== 步骤3：检索 =====
def retrieve(query, top_k=3):
    resp = requests.post(f"{OLLAMA_URL}/api/embeddings",
        json={"model": EMBED_MODEL, "prompt": query})
    if resp.status_code != 200:
        return []
    qv = resp.json()["embedding"]
    results = collection.query(query_embeddings=[qv], n_results=top_k)
    return [{"content": d, "source": m["source"]}
            for d, m in zip(results["documents"][0] or [], results["metadatas"][0] or [])]

# ===== 步骤4：生成回答 =====
def generate(query, chunks):
    ctx = "\n\n---\n\n".join([c["content"] for c in chunks])
    prompt = f"""基于以下参考资料回答问题。资料中没有的就说「资料中未提及」。
## 参考资料：
{ctx}
## 问题：{query}
## 回答："""
    resp = requests.post(f"{OLLAMA_URL}/api/generate",
        json={"model": MODEL_NAME, "prompt": prompt, "stream": False,
              "options": {"temperature": 0.3}})
    return resp.json()["response"] if resp.status_code == 200 else f"错误: {resp.text}"

# ===== 交互循环 =====
print("\n" + "=" * 50)
print("RAG 就绪！输入 quit 退出")
print("=" * 50)
while True:
    q = input("\n[?] 你的问题: ").strip()
    if q.lower() == "quit":
        break
    if not q:
        continue
    chunks = retrieve(q, top_k=3)
    if not chunks:
        print("  [!] 未检索到相关内容")
        continue
    print(f"  找到 {len(chunks)} 个相关块:")
    for i, c in enumerate(chunks):
        print(f"    [{i+1}] {c['source']}")
    answer = generate(q, chunks)
    print(f"\n[AI] {answer}")
