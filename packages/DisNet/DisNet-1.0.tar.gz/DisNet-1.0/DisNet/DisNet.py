# Import modules
import copy
import discord
from discord.ext import commands
print("Github wiki: (https://github.com/DisNetOfficial/DisNet/wiki/DisNet-Official-wiki)")
print("Discord community: (https://discord.gg/ePqKqBKNTj)")
# Bot permissions
intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.guilds = True
# Creating the Bot object
bot = commands.Bot(command_prefix="!", intents=intents)
# Messages management class
class MessagesManager():
    def __init__(self):
        self.messagesList = []
        self.message = ''
    async def getData(self, chanell,  messagesLength=None, messagesNum=None):
        # Method that packs a certain number of messages and returns them
        chanell = bot.get_channel(chanell)
        if chanell == None:
            raise ValueError("Invalid channel ID")
        if messagesLength != None:
            async for mes in chanell.history(limit=messagesLength):
                self.messagesList.append(mes.content)
            result = copy.deepcopy(self.messagesList)
            self.messagesList = []
            return result
        elif messagesNum != None:
            i, self.message = 0, ''
            async for mes in chanell.history(limit=messagesNum):
                if i == messagesNum-1:
                    self.message = mes.content
                    return self.message
                i += 1
    async def sendData(self, chanell, message):
        # Method for sending messages to Discord
        chanell = bot.get_channel(chanell)
        if chanell == None:
            raise ValueError("Invalid channel ID")
        await chanell.send(message)

    async def clearMessages(self, chanell, messagesLength=None, messagesNum=None):
        # метод очищающий сообщения
        chanell = bot.get_channel(chanell)
        if chanell == None:
            raise ValueError("Invalid channel ID")
        if messagesLength != None:
            async for mes in chanell.history(limit=messagesLength):
                await mes.delete()
        elif messagesNum != None:
            i = 0
            async for mes in chanell.history(limit=messagesNum):
                if i == messagesNum-1:
                    await mes.delete()
                i += 1
    async def editMessages(self, chanell, messagesLength=None, messagesNum=None, newMessage=None):
        # Method for editing messages
        chanell = bot.get_channel(chanell)
        if chanell == None:
            raise ValueError("Invalid channel ID")
        if messagesLength != None:
            async for mes in chanell.history(limit=messagesLength):
                await mes.edit(content=newMessage)
        elif messagesNum != None:
            i = 0
            async for mes in chanell.history(limit=messagesNum):
                if i == messagesNum-1:
                    await mes.edit(content=newMessage)
                else:
                    i += 1
# Class for creating and managing databases
class DBase():
    def __init__(self, chanell):
        self.chanell = chanell
        self.dataList = []
        self.message = ''
        self.valuePack = {}
    async def addData(self, **kwargs):
        # Method for adding information to the database
        for key, value in kwargs.items():
            formData = f"{key}:{value}"
            self.dataList.append(formData)
        for data in self.dataList:
            self.message += str(data) + '\n'
        await messagesManager.sendData(self.chanell, self.message)
        self.message, self.dataList = '', []
    async def findInDBase(self, need):
        # Method for finding information
        self.valuePack = {}
        async for data in bot.get_channel(self.chanell).history():
            data = data.content.splitlines()
            for i in data:
                try:
                    k, v = i.split(":", 1)
                except:
                    return False, None
                self.valuePack[k] = v
            for line in data:
                for index, char in enumerate(line):
                    key, value = line.split(":", 1)
                    for k, v in need.items():
                        if k == key and str(v) == value:
                            return True, self.valuePack
        return False, None
    async def editDBasaData(self, oldData, newData):
        # Method for editing data in the database
        integration = 0
        async for data in bot.get_channel(self.chanell).history():
            integration += 1
            data = data.content.splitlines()
            for i in range(len(data)):
                key, value = data[i].split(':', 1)
                for k, v in oldData.items():
                    if key == k and value == str(v):
                        for newKey, newValue in newData.items():
                            data[i] = f'{newKey}:{newValue}'
                        editData = ''
                        for readyData in data:
                            editData += str(readyData) + '\n'
                        await messagesManager.editMessages(self.chanell, messagesNum=integration, newMessage=editData)
                        return

messagesManager = MessagesManager()

