import openai
import os
import base64
import time
from dataclasses import dataclass

# relative imports
from .data import *


@dataclass(frozen=True)
class TextNode:
    role: str
    content: str
    owner: str
    tokens: int
    date: str
    
    def __str__(self) -> str:
        return str({"role":self.role, 
                    "content":self.content, 
                    "owner":self.owner, 
                    "tokens":self.tokens, 
                    "date":self.date})
        
    def __iter__(self) -> dict:
        return iter(eval(self.__str__()).items())
    


class Model(object):
    model = "gpt-4o" 
    def __init__(self, 
                 model: str = "gpt-4o", 
                 api_key: str | None = None) -> None:
        self.define_model(model=model, api_key=api_key)
        
    
    def __str__(self) -> str:
        return f"<Model | {self.__model:=}, {self.__api_key:=}>"
    def __repr__(self) -> str:
        return f"Model(model={repr(self.__model)}, api_key={repr(self.__api_key)})"
    
    # -------- GET --------
    def get_model(self) -> str:
        return self.__model
    def get_api_key(self) -> str:
        return self.__api_key
    def get_client(self) -> openai.OpenAI:
        return self.__client
    
    # -------- SET --------
    def set_model(self, new_model: str) -> None:
        """This method sets the model name of the AI.

        Args:
            new_model (str): The new model name to set.
        """
        self.__model: str = new_model if self.check_model_name(new_model) else self.__model
    def set_api_key(self, new_api_key: str) -> None:
        self.__api_key: str = os.getenv("OPENAI_API_KEY", str(new_api_key))
    
    # -------- DEFINE --------
    def define_model(self, model: str, api_key: str | None) -> None:
        self.__api_key: str | None = os.getenv("OPENAI_API_KEY", str(api_key))
        self.__client = openai.OpenAI(api_key=self.__api_key)
        self.check_api_key()
        
        self.check_model_name(model)
        self.__model: str = model
    
    # -------- CHECK --------
    def check_model_name(self, model) -> bool:
        if model in chat_weaver_models:
            return True
        else:
            raise Exception(f"{model} is not acceptable.")
    
    def check_api_key(self):
        try:
            if not self.__api_key.startswith("sk-") or len(self.__api_key) < 20:
                raise ValueError("Invalid API key format.")
            
            self.__client.chat.completions.list()
        except Exception as e:
            raise Exception(f"Invalid API key: {e}")
    



class Bot(Model):
    def __init__(self, 
                 *args, 
                 rules: str | None = None, 
                 name: str = "AI Bot", 
                 cw_model: Model | None = None, 
                 **kwargs) -> None:
        self.define_bot(*args, rules=rules, name=name, cw_model=cw_model, **kwargs)
    
    # -------- DEFINE --------
    def define_bot(self, *args, rules: str | None, name: str, cw_model: Model, **kwargs) -> None:
        # name
        self.__name: str = str(name)
        
        # rules
        self.__input_rules: str | None = str(rules) if rules != None else "You are a usefull assistant."
        self.__rules: str = self.__input_rules + f" Your name is: {self.__name}."
        
        # model
        if not isinstance(cw_model, Model) and cw_model != None:
            raise TypeError(f"<Invalid 'cw_model' type: Expected 'Model' instance, got {type(cw_model)}>")
        if cw_model == None:
            super().__init__(*args, **kwargs)
            self.__model: Model = Model(*args, **kwargs)
        else:
            self.__model: Model = cw_model
            super().__init__(model=self.__model.get_model(), api_key=self.__model.get_api_key())
    
    # -------- MAGIC METHODS --------
    def __str__(self) -> str:
        return f"<Bot | {self.__name}>"
    def __repr__(self) -> str:
        return f"Bot(rules={repr(self.__rules)}, name={repr(self.__name)}, cw_model={super().__repr__()})"
    
    # -------- GET --------
    def get_rules(self) -> str:
        return self.__rules
    def get_name(self) -> str:
        return self.__name
    
    # -------- SET --------
    def set_rules(self, new_rules: str | None) -> None:
        self.__input_rules: str | None = str(new_rules) if new_rules != None else "You are a usefull assistant."
        self.__rules: str = self.__input_rules + f" Your name is {self.__name}"
    def set_name(self, new_name: str) -> None:
        self.__name: str = new_name
        self.set_rules(self.__input_rules)
    
    # --------  --------
    def response(self, prompt: str, 
                 user: str = "User", 
                 history: list | None = None, 
                 image_path: str | None = None, 
                 file_path: str | None = None) -> str:
        self.__start_date = time.strftime("%d/%m/%Y %H:%M", time.localtime(time.time())) # user prompt date
        
        self.__prompt = prompt
        
        messages = [
            {"role": "developer", "content": self.__rules + f"User name is: {user}"}, 
            {"role": "user", "content": [{"type": "text", "text": self.__prompt}]}
        ]
        
        if image_path != None:
            with open(image_path, "rb") as f:
                base64_image = base64.b64encode(f.read()).decode("utf-8")
            image = f"data:image/png;base64,{base64_image}"
            
            image_message ={
                "type": "image_url",
                "image_url": {"url": image}
                }
            
            messages[1]["content"].append(image_message)
            
        if file_path != None:
            file = self.get_client().files.create(
                file=open(file_path, "rb"), 
                purpose="user_data"
            )
            
            file_message = {
                "type": "file", 
                "file": {"file_id": file.id}
            }
            
            messages[1]["content"].append(file_message)
        
        messages = [dict(message) for message in history] + messages if history != None else messages
        
        start = time.perf_counter()
        response = self.get_client().chat.completions.create(
            model=self.get_model(),
            messages=messages
        )
        end = time.perf_counter()
        self.__final_date = time.strftime("%d/%m/%Y %H:%M", time.localtime(time.time())) # assistant resposne date
        
        response.usage.completion_tokens
        response.usage.prompt_tokens
        response.usage.total_tokens
        
        content = response.choices[0].message.content if response.choices[0].message.content != None else response.choices[0].message.refusal
        
        return {"content": content, 
                "prompt_tokens": response.usage.prompt_tokens, 
                "completion_tokens": response.usage.completion_tokens, 
                "total_tokens": response.usage.total_tokens,
                "start_date": self.__start_date,
                "delta_time": end-start, 
                "final_date": self.__final_date}



class Chat(Bot):
    def __init__(self, 
                 *args, 
                 replies_limit: int | None = 10, 
                 user: str = "User", 
                 cw_bot: Bot | None = None,
                 **kwargs) -> None:
        self.define_chat(*args, replies_limit=replies_limit, user=user, cw_bot=cw_bot, **kwargs)
        
    
    # -------- DEFINE --------
    def define_chat(self, *args, replies_limit: int | None, user: str, cw_bot: Bot | None, **kwargs) -> None:
        # creation_date
        self.__creation_date = time.strftime("%d/%m/%Y %H:%M", time.localtime(time.time()))
        
        # replies_limit
        self.__replies_limit: int = float("inf") if replies_limit == None else int(replies_limit)
        
        self.__replies: int = 0
        self.__history: list[TextNode] = [] # [{"role":"user", "text","message"}, {"role":"AiBot", "text":"response"}]
        
        # user
        self.__user: str = str(user)
        
        # bot
        if not isinstance(cw_bot, Bot) and cw_bot != None:
            raise TypeError(f"<Invalid 'cw_bot' type: Expected 'Bot' instance, got {type(cw_bot)}>")
        if cw_bot == None:
            super().__init__(*args, **kwargs)
            self.__bot: Bot = Bot(*args, **kwargs)
        else:
            self.__bot: Bot = cw_bot
            super().__init__(rules=self.__bot.get_rules(), name=self.__bot.get_name(), model=self.__bot.get_model(), api_key=self.__bot.get_api_key())
            
        # cost 
        self.__cost: int = 0
    
    # -------- MAGIC METHODS --------
    def __str__(self):
        return f"<Chat | {self.__replies_limit:=}, {self.__replies:=}>"
    def __repr__(self):
        return f"Chat(reply_limit={self.__replies_limit}, user={repr(self.__user)}, cw_bot={super().__repr__()}).set_history({self.__history}, return_self=True)"
    
    # -------- GET --------
    def get_chat_limit(self) -> int:
        return self.__replies_limit
    def get_replies(self) -> int:
        return self.__replies
    def get_history(self) -> list[dict[str, str]]:
        return self.__history
    def get_user(self) -> str:
        return self.__user
    def get_cost(self) -> int:
        return self.__cost
    
    # -------- SET --------
    def set_replies_limit(self, new_replies_limit: int | None) -> None:
        self.__replies_limit = float("inf") if new_replies_limit == None else int(new_replies_limit)
    def set_replies(self, new_replies: int) -> None:
        self.__replies = int(new_replies)
    def set_history(self, new_history: list[TextNode] | list[dict[str, str]] | None, return_self: bool = False) -> None:
        if new_history:
            if isinstance(new_history[0], TextNode):
                for node in new_history:
                    if not isinstance(node, TextNode):
                        raise TypeError("<Invalid 'new_history' format>")
                self.__history = new_history
            elif isinstance(new_history[0], dict):
                try: 
                    self.__history = [TextNode(**node) for node in new_history]
                except:
                    raise TypeError("<Invalid 'new_history' format>")
            else:
                raise TypeError(f"<Invalid 'new_history' format>")
        else:
            self.__history = []
        
        self.__calc_cost()
        
        return self if return_self else None
    def set_cost(self, new_cost: int) -> None:
        try: 
            self.__cost = int(new_cost)
        except:
            raise TypeError(f"<Invalid 'new_cost' format: Expected 'int', got {type(new_cost)}>")
    
    # --------  --------
    def get_response(self, 
                     prompt: str, 
                     user: str | None = None, 
                     image_path: str | None = None,
                     file_path: str | None = None) -> str:
        response = self.response(prompt=prompt, 
                                 user=self.__user if user == None else str(user), 
                                 history=self.__history if self.__history else None, 
                                 image_path=image_path,
                                 file_path=file_path)
        
        self.__update_history(prompt=prompt, response=response, owner_user=user)
        self.__update_cost(response=response)
        return response["content"]
    
    def __update_history(self, prompt: str, response: str, owner_user: str | None = None) -> None:
        owner_user: str = self.__user if owner_user == None else str(owner_user)
        
        user_node: TextNode = TextNode(role="user", content=prompt, owner=owner_user, tokens=response["prompt_tokens"], date=response["start_date"])
        
        assistant_node: TextNode = TextNode(role="assistant", content=response["content"], owner=self.get_name(), tokens=response["completion_tokens"], date=response["final_date"])
        
        if self.__replies + 1 <= self.__replies_limit:
            self.__replies: int = self.__replies + 1
            
            self.__history.append(user_node)
            self.__history.append(assistant_node)
        else:
            self.__history.pop(0)
            self.__history.pop(0)
            
            self.__history.append(user_node)
            self.__history.append(assistant_node)
            
    def __update_cost(self, response: str) -> None:
        self.__cost += response["total_tokens"]
    
    def __calc_cost(self) -> None:
        self.__cost = 0
        for node in self.__history:
            self.__cost += node.tokens




class Loom():
    def __init__(self, *args, strands: list | None = None, name: str = "Loom AI", **kwargs) -> None:
        self.__name: str = name
        self.__strands: list = strands if strands else []
        self.__initialized: bool = False
        self.__setup_strands(*args, **kwargs)

    # -------- SETUP --------
    def __setup_strands(self, *args, **kwargs):
        # Logica per inizializzare gli agenti o strands
        self.__initialized = True
        print(f"Loom '{self.__name}' è stato inizializzato con {len(self.__strands)} strand.")

    # -------- MAGIC METHODS --------
    def __str__(self):
        return f"<Loom | {self.__name:=}, {len(self.__strands):=} strands>"
    def __repr__(self):
        return f"Loom(name={self.__name}, strands={len(self.__strands)})"

    # -------- GET --------
    def get_strands(self) -> list:
        return self.__strands
    def get_name(self) -> str:
        return self.__name
    def get_status(self) -> bool:
        return self.__initialized

    # -------- SET --------
    def set_threads(self, new_strands: list) -> None:
        self.__strands = new_strands
    def add_thread(self, strand) -> None:
        self.__strands.append(strand)
        print(f"Aggiunto nuovo thread: {strand}")

    # -------- EXECUTE --------
    def weave(self, task: str, *args, **kwargs) -> None:
        if not self.__initialized:
            raise Exception(f"Loom '{self.__name}' non è inizializzato.")
        print(f"Eseguo il compito: '{task}' con {len(self.__strands)} strand.")
        # Logica per orchestrare il weaving dei threads
        for strand in self.__strands:
            print(f"Esecuzione strand: {strand}")
        print(f"Compito '{task}' completato.")




def load(cw_string_object):
    # Run the code, which defines the variable 'obj'
    exec(f'obj = {cw_string_object}', globals())
    # retrieve and return the variable 'obj'
    return globals()['obj']