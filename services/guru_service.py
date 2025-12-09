# services/guru_service.py
import PyPDF2
from database.db import init_db, SessionLocal
from database.models import GuruDoc
import streamlit as st
import re

init_db()

class GuruService:
    def __init__(self):
        pass

    def ingest_file(self, file_obj, filename: str):
        """
        Read PDF/TXT and store content into database table guru_docs.
        """
        content = ""
        fn = filename.lower()
        try:
            if fn.endswith(".pdf"):
                reader = PyPDF2.PdfReader(file_obj)
                for p in reader.pages:
                    content += (p.extract_text() or "") + "\n"
            else:
                raw = file_obj.read()
                if isinstance(raw, bytes):
                    content = raw.decode(errors='ignore')
                else:
                    content = str(raw)
        except Exception as e:
            content = ""
            print("Guru ingest error:", e)

        s = SessionLocal()
        try:
            doc = GuruDoc(filename=filename, content=content)
            s.add(doc)
            s.commit()
            s.refresh(doc)
            return {"id": doc.id, "filename": doc.filename}
        finally:
            s.close()

    def list_docs(self):
        s = SessionLocal()
        try:
            rows = s.query(GuruDoc).order_by(GuruDoc.ingested_at.desc()).all()
            return [{"id": r.id, "filename": r.filename, "content": r.content[:1000]} for r in rows]
        finally:
            s.close()

    def retrieve_relevant(self, query: str, top_k: int = 3):
        """
        Simple keyword overlap retrieval from DB.
        """
        s = SessionLocal()
        try:
            rows = s.query(GuruDoc).all()
            if not rows:
                return []
            qwords = [w for w in re.findall(r"\w+", query.lower()) if len(w) > 2]
            scored = []
            for r in rows:
                text = (r.content or "").lower()
                score = sum(text.count(w) for w in qwords)
                scored.append((score, r))
            scored.sort(key=lambda x: x[0], reverse=True)
            out = []
            for score, r in scored[:top_k]:
                snippet = (r.content or "")[:1200].replace("\n", " ").strip()
                out.append({"id": r.id, "filename": r.filename, "snippet": snippet, "score": score})
            return out
        finally:
            s.close()
