import openai
import os
import base64
import time
from dataclasses import dataclass
from typing import Any
import pathlib

# relative imports
from .data import *


@dataclass(frozen=True)
class TextNode:
    """
    # TextNode
    
    ## Description
    Represents an immutable text node with metadata attributes. A TextNode object represents a single message in a conversation.

    ## Attributes 
    ```
    role: str      # The role of the TextNode ('assistant' or 'user').
    content: str   # The content of the TextNode.
    owner: str     # The owner name of the TextNode.
    tokens: int    # The number of tokens associated with the TextNode.
    date: str      # The creation date of the TextNode.
    ```

    ## Methods
    ```
    __str__() -> str   # Returns the string representation of the object in JSON-like format.
    __iter__() -> dict # Returns an iterator for the object's attributes as key-value pairs. Useful for unpacking the object with the dict() constructor.
    ```
    """
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
    """
    # Model
    
    ## Description
    Represents a wrapper class for managing AI models and their API keys. This class handles model definition, validation, and API client initialization.

    ## Attributes 
    ```
    model: str           # The name of the model (default is "gpt-4o").
    __model: str         # Private attribute representing the model name.
    __api_key: str       # Private attribute storing the API key.
    __client: openai.OpenAI  # Private attribute for the API client.
    ```

    ## Methods
    ```
    __str__() -> str         # Returns the string representation of the object.
    __repr__() -> str        # Returns a formal string representation of the object.
    model_model -> str       # Property to get the model name.
    model_api_key -> str     # Property to get the API key.
    model_client -> openai.OpenAI  # Property to get the API client instance.
    model_model.setter(new_model: str) -> None  # Sets the model name.
    model_api_key.setter(new_api_key: str) -> None  # Sets the API key and initializes the client.
    define_model(model: str, api_key: str | None) -> None  # Defines the model and API key.
    check_model_name(model: str) -> bool  # Validates the model name.
    __check_api_key() -> None  # Validates the API key format and connectivity.
    ```
    """
    
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
    @property
    def model_model(self) -> str:
        return self.__model
    
    @property
    def model_api_key(self) -> str:
        return self.__api_key
    
    @property
    def model_client(self) -> openai.OpenAI:
        return self.__client
    
    
    # -------- SET --------
    @model_model.setter
    def model_model(self, new_model: str) -> None:
        """This method sets the model name of the AI.

        Args:
            new_model (str): The new model name to set.
        """
        self.__model: str = new_model if self.check_model_name(new_model) else self.__model
    
    @model_api_key.setter
    def model_api_key(self, new_api_key: str) -> None:
        self.__api_key: str = os.getenv("OPENAI_API_KEY", str(new_api_key))
        self.__check_api_key()
        self.__client = openai.OpenAI(api_key=self.__api_key)
    
    
    # -------- DEFINE --------
    def define_model(self, model: str, api_key: str | None) -> None:
        self.__api_key: str | None = os.getenv("OPENAI_API_KEY", str(api_key))
        self.__client = openai.OpenAI(api_key=self.__api_key)
        self.__check_api_key()
        
        self.check_model_name(model)
        self.__model: str = model
    
    
    # -------- CHECK --------
    def check_model_name(self, model) -> bool:
        if model in chat_weaver_models:
            return True
        else:
            raise Exception(f"{model} is not acceptable.")
    
    def __check_api_key(self):
        try:
            if not self.__api_key.startswith("sk-") or len(self.__api_key) < 20:
                raise ValueError("Invalid API key format.")
            
            self.__client.chat.completions.list()
        except Exception as e:
            raise Exception(f"Invalid API key: {e}")
    



class Bot(Model):
    """
    # Bot
    
    ## Description
    Represents a conversational AI bot based on a specific model. This class allows customization of rules, bot name, and associated model behavior. It supports managing user prompts, handling responses, and integrating optional images or files.

    ## Attributes 
    ```
    bot_rules: str         # The rules that define the bot's behavior and responses.
    bot_name: str          # The name of the bot (default is "AI Bot").
    bot_time_format: str   # The format used for time-related attributes (default is "%d/%m/%Y %H:%M:%S").
    __rules: str           # Internal representation of bot rules.
    __name: str            # Internal representation of the bot's name.
    __time_format: str     # Internal time format used for operations.
    __model: Model         # The model instance associated with the bot.
    ```

    ## Methods
    ```
    __str__() -> str                # Returns the string representation of the bot.
    __repr__() -> str               # Returns a formal string representation of the bot.
    define_bot(*args, rules, name, cw_model, **kwargs) -> None  
                                    # Initializes the bot's attributes and model.
    bot_rules -> str                # Gets the current bot rules.
    bot_name -> str                 # Gets the bot name.
    bot_time_format -> str          # Gets the bot's time format.
    bot_rules.setter(new_rules) -> None   
                                    # Sets new rules for the bot and updates its behavior.
    bot_name.setter(new_name) -> None   
                                    # Sets a new name for the bot and updates its rules.
    bot_time_format.setter(new_time_format) -> None
                                    # Sets a new time format for the bot and validates it.
    response(prompt, user, history, image_path, file_path) -> str
                                    # Generates a response to a user's prompt with optional history, images, or files.
    ```
    """
    
    def __init__(self, 
                 *args, 
                 rules: str | None = None, 
                 name: str = "AI Bot", 
                 cw_model: Model | None = None, 
                 **kwargs) -> None:
        self.define_bot(*args, rules=rules, name=name, cw_model=cw_model, **kwargs)
    
    
    # -------- MAGIC METHODS --------
    def __str__(self) -> str:
        return f"<Bot | {self.__name}>"
    def __repr__(self) -> str:
        return f"Bot(rules={repr(self.__rules)}, name={repr(self.__name)}, cw_model={super().__repr__()})"
    
    
    # -------- DEFINE --------
    def define_bot(self, *args, rules: str | None, name: str, cw_model: Model, **kwargs) -> None:
        # time format
        self.__time_format = "%d/%m/%Y %H:%M:%S" 
        
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
            super().__init__(model=self.__model.model_model, api_key=self.__model.model_api_key)
    
    
    # -------- GET --------
    @property
    def bot_rules(self) -> str:
        return self.__rules
    
    @property
    def bot_name(self) -> str:
        return self.__name
    
    @property
    def bot_time_format(self) -> str:
        return self.__time_format
    
    
    # -------- SET --------
    @bot_rules.setter
    def bot_rules(self, new_rules: str | None) -> None:
        self.__input_rules: str | None = str(new_rules) if new_rules != None else "You are a usefull assistant."
        self.__rules: str = self.__input_rules + f" Your name is {self.__name}"
    
    @bot_name.setter
    def bot_name(self, new_name: str) -> None:
        self.__name: str = new_name
        self.bot_rules = self.__input_rules
    
    @bot_time_format.setter
    def bot_time_format(self, new_time_format: str) -> None:
        try:
            time.strftime(new_time_format, time.localtime(time.time()))
            self.__time_format = new_time_format
        except:
            raise ValueError(f"<Invalid 'new_time_format' format: Expected valid time format>")
    
    # -------- ACTIONS --------
    def response(self, prompt: str, 
                 user: str = "User", 
                 history: list | None = None, 
                 image_path: str | None = None, 
                 file_path: str | None = None) -> str:
        self.__start_date = time.strftime(self.bot_time_format, time.localtime(time.time())) # user prompt date
        
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
            file = self.model_client.files.create(
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
        response = self.model_client.chat.completions.create(
            model=self.model_model,
            messages=messages
        )
        end = time.perf_counter()
        self.__final_date = time.strftime(self.bot_time_format, time.localtime(time.time())) # assistant resposne date
        
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
    """
    # Chat

    ## Description
    Represents a chat session built upon the Bot class. This class manages conversation history, response generation, and chat metadata such as reply limits, creation date, and cost calculation. It facilitates interactions by maintaining a log of messages and integrating model responses.

    ## Attributes 
    ```
    chat_time_format: str              # The time format used for chat timestamps (default: "%d/%m/%Y %H:%M:%S").
    chat_replies_limit: int            # The maximum number of replies allowed in the chat (or infinity if None).
    chat_history: list[TextNode]       # The conversation history as a list of TextNode objects.
    chat_user: str                     # The user participating in the chat session.
    chat_creation_date: str            # The timestamp when the chat was created.
    chat_replies: int                  # The current number of replies in the chat.
    chat_cost: int                     # The total cost calculated based on the tokens used in all messages.
    chat_title: str                    # The title of the chat session.
    ```

    ## Methods
    ```
    __str__() -> str  
        # Returns a string representation of the chat, including the chat title, replies limit, current number of replies, and creation date.
    __repr__() -> str  
        # Returns a formal string representation of the chat with its internal state.
    __lt__(other: Chat) -> bool  
        # Compares two chat sessions based on their creation dates.
    define_chat(*args, replies_limit: int | None, user: str, cw_bot: Bot | None, **kwargs) -> None  
        # Initializes the chat session with reply limits, the participating user, associated bot, and sets the creation date.
    get_response(prompt: str, user: str | None = None, image_path: str | None = None, file_path: str | None = None) -> str  
        # Generates a response based on a given prompt (with optional image or file attachments) and updates the conversation history.
    set_all(return_self: bool = True, **kwargs: Any) -> None  
        # Updates multiple chat and inherited attributes using provided keyword arguments.
    save() -> None  
        # Returns a string representation of the chat session state for saving purposes.
    ```
    """
    
    def __init__(self, 
                 *args, 
                 replies_limit: int | None = 10, 
                 user: str = "User", 
                 cw_bot: Bot | None = None,
                 **kwargs) -> None:
        self.define_chat(*args, replies_limit=replies_limit, user=user, cw_bot=cw_bot, **kwargs)
    
    
    # -------- MAGIC METHODS --------
    def __str__(self):
        return f"<Chat | title={repr(self.chat_title)}, replies_limit={self.chat_replies_limit}, replies={self.chat_replies}, creation_date={repr(self.chat_creation_date)}>"
    def __repr__(self):
        return f"Chat(reply_limit={self.__replies_limit}, user={repr(self.__user)}, cw_bot={super().__repr__()}).set_all(_Chat__history={self.__history}, _Chat__creation_date={repr(self.__creation_date)})"
    def __lt__(self, other) -> bool:
        # Convert the string to a time object and compare
        self_time = time.strptime(self.chat_creation_date, self.chat_time_format)
        other_time = time.strptime(other.chat_creation_date, self.chat_time_format)
        return self_time < other_time
    
    # -------- DEFINE --------
    def define_chat(self, *args, replies_limit: int | None, user: str, cw_bot: Bot | None, **kwargs) -> None:
        # time format
        self.__time_format = "%d/%m/%Y %H:%M:%S"
        
        # creation_date
        self.__creation_date = time.strftime(self.chat_time_format, time.localtime(time.time()))
        
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
            super().__init__(rules=self.__bot.bot_rules, name=self.__bot.bot_name, model=self.__bot.model_model, api_key=self.__bot.model_api_key)
        # cost 
        self.__cost: int = 0
        
        # title
        self.__title: str = "New Chat"
    
    
    # -------- GET --------
    @property
    def chat_time_format(self) -> str:
        return self.__time_format
    
    @property
    def chat_replies_limit(self) -> int:
        return self.__replies_limit
    
    @property
    def chat_history(self) -> list[TextNode]:
        return self.__history
    
    @property
    def chat_user(self) -> str:
        return self.__user
    
    @property
    def chat_creation_date(self) -> str:
        return self.__creation_date
    
    @property
    def chat_replies(self) -> int:
        self.__replies = len(self.__history) // 2
        return self.__replies
    
    @property
    def chat_cost(self) -> int:
        self.__cost = 0
        for node in self.__history:
            self.__cost += node.tokens
        return self.__cost
    
    @property
    def chat_title(self) -> str:
        return self.__title
    
    # -------- SET --------
    def set_all(self, return_self: bool = True, **kwargs: Any) -> None:
        """
        
        """
        
        for key, value in kwargs.items():
            match key:
                # Chat
                case "_Chat__replies_limit":
                    self.chat_replies_limit = value
                case "_Chat__history":
                    self.chat_history = value
                case "_Chat__creation_date":
                    self.chat_creation_date = value
                case "_Chat__user":
                    self.chat_user = value
                # Bot
                case "_Bot__rules":
                    self.bot_rules = value
                case "_Bot__name":
                    self.bot_name = value
                # Model
                case "_Model__model":
                    self.model_model = value
                case "_Model__api_key":
                    self.model_api_key = value
        
        return self if return_self else None
    
    @chat_replies_limit.setter
    def chat_replies_limit(self, new_replies_limit: int | None) -> None:
        try:
            self.__replies_limit = float("inf") if new_replies_limit == None else int(new_replies_limit)
        except:
            raise TypeError(f"<Invalid 'new_replies_limit' format: Expected 'int', got {type(new_replies_limit)}>")
    
    @chat_history.setter
    def chat_history(self, new_history: list[TextNode] | list[dict[str, str]] | None) -> None:
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
    
    @chat_creation_date.setter
    def chat_creation_date(self, new_creation_date: str) -> None:
        # check if new_creation_date is a valid date format
        try:
            # try to convert the string to a datetime object
            time.strptime(new_creation_date, self.chat_time_format)
            self.__creation_date = new_creation_date
        except:
            raise ValueError(f"<Invalid 'new_creation_date' format: Expected {repr(self.chat_time_format)}>")
    
    @chat_user.setter
    def chat_user(self, new_user: str) -> None:
        self.__user = str(new_user)
    
    @chat_time_format.setter
    def chat_time_format(self, new_time_format: str) -> None:
        try:
            time.strftime(new_time_format, time.localtime(time.time()))
            self.__time_format = new_time_format
        except:
            raise ValueError(f"<Invalid 'new_time_format' format: Expected valid time format>")
    
    # -------- ACTIONS --------
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
        return response["content"]
    
    def __update_history(self, prompt: str, response: str, owner_user: str | None = None) -> None:
        owner_user: str = self.__user if owner_user == None else str(owner_user)
        
        user_node: TextNode = TextNode(role="user", content=prompt, owner=owner_user, tokens=response["prompt_tokens"], date=response["start_date"])
        
        assistant_node: TextNode = TextNode(role="assistant", content=response["content"], owner=self.bot_name, tokens=response["completion_tokens"], date=response["final_date"])
        
        if self.__replies + 1 <= self.__replies_limit:
            self.__replies: int = self.__replies + 1
            
            self.__history.append(user_node)
            self.__history.append(assistant_node)
        else:
            self.__history.pop(0)
            self.__history.pop(0)
            
            self.__history.append(user_node)
            self.__history.append(assistant_node)
    
    def save(self) -> None:
        return f"Chat(reply_limit={self.__replies_limit}, user={repr(self.__user)}, cw_bot={super().__repr__()}).set_all(_Chat__history={self.__history}, _Chat__creation_date={repr(self.__creation_date)})"




class CWArchive(object):
    def __init__(self, path: str) -> None:
        self.define()
    
    
    # -------- MAGIC METHODS --------
    def __str__(self) -> str:
        return f"<Archive | path={self.__path}>"
    def __repr__(self) -> str:
        return f"Archive(path={repr(self.__path)})"
    
    
    # -------- GET --------
    @property
    def archive_path(self) -> str:
        return self.__path
    
    @property
    def archive_data(self) -> dict:
        return self.__data
    
    @property
    def archive_id(self) -> int:
        return 0
    
    # -------- SET --------
    @archive_path.setter
    def archive_path(self, new_path: str) -> None:
        # move the archive to the new path
        self.__path = new_path
        
        self.__data = dict()
    
    @archive_data.setter
    def archive_data(self, new_archive_data: dict) -> None:
        self.__data = new_archive_data
    
    
    # -------- DEFINE --------
    def define(self, path: str) -> None:
        self.__path = path 
    
    def add(self, chat: Chat) -> None:
        pass
    
    def save(self) -> None:
        pass
    
    def remove(self, id) -> None:
        pass
    
    def load(self) -> None:
        pass




class Loom(object):
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




def load(cw_string_object) -> Any:
    try:
        # Run the code, which defines the variable 'obj'
        exec(f'obj = {cw_string_object}', globals())
        # retrieve and return the variable 'obj'
        return globals()['obj']
    except:
        raise Exception("<The object entered cannot be converted to a chatweaver object. Invalid format.>")