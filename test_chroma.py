import psutil, os
from chromadb import PersistentClient

proc = psutil.Process(os.getpid())
print("Total Python memory RSS:", proc.memory_info().rss/1024**2, "MB")

client = PersistentClient(path="/app/backend/data/vector_db")

for col in client.list_collections():
    c = client.get_collection(col.name)
    n = c.count()
    print(f"Collection {col.name}: {n} embeddings")
    try:
        meta = c.get(include=["embeddings"], limit=1)
        if "embeddings" in meta and meta["embeddings"]:
            dim = len(meta["embeddings"][0])
            est = n * dim * 4 / 1024**2
            print(f"  -> estimated RAM for embeddings: {est:.2f} MB")
    except Exception as e:
        print("  (couldn’t estimate vector size)", e)