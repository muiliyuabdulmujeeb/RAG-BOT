import re
from transformers import AutoTokenizer

from app.core.config import settings

class ChunkingService:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained(settings.embedding_model)

    @staticmethod
    def clean_chunk_text(text: str) -> str:
        text = re.sub(r"[_\-]{5,}", " ", text)
        text = re.sub(r"\s+", " ", text)
        return text.strip()
    
    def chunk_pages(
            self,
            pages: list[dict],
            chunk_size: int = 200,
            overlap: int = 40,
            min_tokens: int = 20
    ) -> list[dict]:
        
        chunks = []
        step = chunk_size - overlap
        if step <= 0:
            raise ValueError("chunk_size must be greater than overlap")

        for page in pages:
            page_number = page["page_number"]
            text = page["text"]

            if not text or not text.strip():
                continue

            token_ids = self.tokenizer.encode(
                text,
                add_special_tokens=False,
                truncation=False,
                verbose=False,
            )
            start=0
            while start < len(token_ids):
                end = start + chunk_size
                chunk_token_ids = token_ids[start:end]

                if not chunk_token_ids:
                    break

                chunk_text = self.tokenizer.decode(
                    chunk_token_ids,
                    skip_special_tokens=True,
                ).strip()

                
                if not chunk_text:
                    break

                if not re.search(r"\w", chunk_text):
                    break

                if len(chunk_token_ids) < min_tokens and start > 0:
                    break
                
                chunk_text = self.clean_chunk_text(chunk_text)
                if not chunk_text:
                    start += step
                    continue

                chunks.append(
                    {
                        "page_number": page_number,
                        "content": chunk_text,
                        "token_count": len(chunk_token_ids),
                    }
                )

                if end >= len(token_ids):
                    break

                start += step
                
        return chunks