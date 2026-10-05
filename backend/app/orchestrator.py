from .domain import AgentDecision
from .intent import classify_intent
from .providers import ChatRequest

class Orchestrator:
    def __init__(self, llm=None) -> None:
        self.llm = llm

    def decide(self, message: str, language: str = "hi") -> AgentDecision:
        intent = classify_intent(message)
        if self.llm is not None:
            result = self.llm.chat(ChatRequest(message=message, language=language))
            if result.tool_calls:
                call = result.tool_calls[0]
                return AgentDecision(intent=intent, reply=result.text, tool_name=call.get("name"), tool_args=call.get("arguments", {}), confidence=0.8)
            return AgentDecision(intent=intent, reply=result.text, confidence=0.7)
        replies = {
            "scheme": "Main verified scheme information aur required documents ke flow mein madad karunga.",
            "farming": "Main weather ya mandi ke liye verified source se data laane ka flow taiyar karunga.",
            "document": "Document ko safely process karke important points aur next action nikaal sakte hain.",
            "task": "Main task ko follow-up ke liye taiyar kar sakta hoon; memory save karne se pehle consent zaroori hai.",
            "human": "Aap chahein to request ko volunteer support ke liye escalate kiya ja sakta hai.",
            "general": "Namaste! Main Saathi hoon. Aap Hindi mein apni zaroorat bata sakte hain.",
        }
        return AgentDecision(intent=intent, reply=replies[intent], confidence=0.55)
