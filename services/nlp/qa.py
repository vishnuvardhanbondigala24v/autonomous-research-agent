from transformers import pipeline
from typing import List, Dict

# Use a generative model instead of span-extraction
qa_pipeline = pipeline("text2text-generation", model="google/flan-t5-small")

def answer_question(question: str, context_chunks: List[str]) -> Dict:
    """
    Answers a question using relevant context chunks.
    Uses a generative model (Flan-T5) to produce natural answers.
    """
    if not context_chunks:
        return {
            "answer": "No content available to answer from.",
            "confidence": 0.0,
            "source": ""
        }

    # Combine chunks into one context
    combined_context = " ".join(context_chunks)

    # Create a prompt for the model
    prompt = f"Answer the question based on the text:\n\n{combined_context}\n\nQuestion: {question}\nAnswer:"

    try:
        result = qa_pipeline(prompt, max_length=200, do_sample=False)
        return {
            "answer": result[0]["generated_text"],
            "confidence": 1.0,  # generative models don’t return a score, so we set it high
            "source": combined_context[:500]  # include a snippet of the source
        }
    except Exception as e:
        return {
            "answer": f"Error generating answer: {str(e)}",
            "confidence": 0.0,
            "source": ""
        }
