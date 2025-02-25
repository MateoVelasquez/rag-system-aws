"""LLM Langchain service module."""
from langchain.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM


class LLM:
    """LLM manager."""
    def __init__(
            self,
            model: str | OllamaLLM = "llama3",
            prompt_template: str | None = None
        ) -> None:
        """LLM Class init."""
        if isinstance(model, str):
            self.model = OllamaLLM(model=model)
        elif isinstance(model, OllamaLLM):
            self.model = model
        else:
            msg = "Invalid Object for model argument."
            raise TypeError(msg)
        if prompt_template:
            self.prompt = ChatPromptTemplate.from_template(prompt_template)
            self.chain = self.prompt | self.model
        else:
            self.chain = model

    def generate_response(self, query: str, chunks: str | None = None) -> str:
        """Generate response using model."""
        context = "\n\n".join(chunks) if chunks else "No relevant information found."
        return self.chain.invoke({"context": context, "question": query})

