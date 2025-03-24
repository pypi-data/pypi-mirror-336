# Импорт модулей
import copy
import discord
from discord.ext import commands
import os
# Права бота
intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.guilds = True
# Создание обьекта Bot
bot = commands.Bot(command_prefix="!", intents=intents)
# Класс для передачи данных через дискорд
class SendData():
    def __init__(self):
        # Иницилизация переменных класса
        self.messagesList = []
    async def sendData(self, chanell, message):
        # Метод для отправки сообщений в дискорд
        chanell = bot.get_channel(chanell)
        if chanell == None:
            raise ValueError("Invalid channel ID")
        await chanell.send(message)
# Класс для получения данных из дискорд
class GetData():
    def __init__(self):
        # Иницилизация переменных
        self.messagesList = []
    async def getData(self, chanell,  messagesLength=None, messagesNum=None):
        # Метод пакующий определенное количество сообщений и возращающий их
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
            i = 0
            async for mes in chanell.history(limit=messagesNum):
                if i == messagesNum-1:
                    self.messagesList.append(mes.content)
                result = copy.deepcopy(self.messagesList)
                self.messagesList = []
                return result
# Класс управления сообщениями
class MessagesManager():
    def __init__(self):
        pass
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
        # Метод корректирующий сообщения
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
# Класс создания и управления базами данных
class DBase():
    def __init__(self, chanell):
        self.chanell = chanell
        self.dataList = []
        self.message = ''
        self.valuePack = {}
    async def addData(self, **kwargs):
        # Метод добавления информации в базу данных
        for key, value in kwargs.items():
            formData = f"{key}:{value}"
            self.dataList.append(formData)
        for data in self.dataList:
            self.message += str(data) + '\n'
        await sendData.sendData(self.chanell, self.message)
        self.message, self.dataList = '', []
    async def finedInDBase(self, need):
        # Метод нахождения информации
        self.valuePack = {}
        async for data in bot.get_channel(self.chanell).history():
            data = data.content.splitlines()
            for i in data:
                k, v = i.split(":", 1)
                self.valuePack[k] = v
            for line in data:
                key = ''
                for index, char in enumerate(line):
                    key, value = line.split(":", 1)
                    for k, v in need.items():
                        if k == key and str(v) == value:
                            return True, self.valuePack
        return False, None
    async def editDBasaData(self, oldData, newData):
        # Метод корректирующий данные в базе
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

sendData = SendData()
getData = GetData()
messagesManager = MessagesManager()
