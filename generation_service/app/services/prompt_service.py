class PromptService:
    @staticmethod
    def build_document_qa_prompt(question: str, context_chunks: list[str]) -> str:
        context = "\n\n".join(
            f"Excerpt {idx + 1}: \n{chunk}" for idx, chunk in enumerate(context_chunks)
        )

        return f"""
                    You are a careful document question-answering asssistant.
                    Answer the question using only the provided document excerpts.
                    Rules:
                    - Remove any form of the words "chunks", "sources", or "excerpts" in the answer unless the user asks for citations.
                    - Do not use outside knowledge.
                    - If the answer is not clearly supported by the excerpts, say: "I could not find the answer in the selected document."
                    - Give a direct, concise answer.
                    - If the excerpts contain unrelated material, ignore it.

                    Document excerpts:
                    {context}

                    Question:
                    {question}

                    Answer:
                            """.strip()