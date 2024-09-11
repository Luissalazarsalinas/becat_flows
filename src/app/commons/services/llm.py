from langchain_openai.chat_models import ChatOpenAI

class LLM:

    def chat_openai(self, model_name: str | None = "gpt-4o", model_api_key: str | None = None):

        llm = ChatOpenAI(
            model= model_name,
            api_key= model_api_key,
            temperature= 0.001
        )

        return llm
    
    def get_llm(self, provider: str | None = "onpenai", model_name: str | None = None, model_api_key: str | None = None):

        if provider == "onpenai":
            
            if model_name != None:
                
                return self.chat_openai(model_name=model_name, model_api_key=model_api_key)
