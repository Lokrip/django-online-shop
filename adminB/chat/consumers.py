import json

from channels.generic.websocket import WebsocketConsumer

from asgiref.sync import async_to_sync

class ChatConsumer(WebsocketConsumer):
    #когда мы делаем коннект к текущему url адрессу будет вызываться эта функция
    def connect(self):
        #тоесть мы с url ws/chat/<room_name> достали ключь room_name
        room_name = self.scope['url_route']['kwargs']['room_name'] #scope это пу сути request только scope
        self.rome_name = room_name
        #создание группы тоесть будет chat_1 chat_2 chat_3 такие группы
        self.room_group_name = 'chat_%s' % self.rome_name
        
        #room_group_name Это имя группы, к которой вы хотите добавить канал. Например, chat_room_1. Эта группа управляется в channel layer (например, Redis) и используется для маршрутизации сообщений.
        #channel_name Это уникальный идентификатор текущего WebSocket-соединения. Django Channels автоматически присваивает этот идентификатор каждому активному каналу.
        #self.channel_layer.group_add Добавляет текущий канал (его имя хранится в self.channel_name) в указанную группу (self.room_group_name).
        #После выполнения этой операции связь между каналом и группой сохраняется в Redis (или другом бэкэнде channel layer).
        
        #async_to_sync Django Channels использует асинхронную архитектуру, но если вы работаете в синхронной среде (например, обычный Django view), вы можете обернуть асинхронные функции в синхронные с помощью async_to_sync
        
        #тоесть мы добовляем канал channel_name в группу room_group_name через self.channel_layer.group_add тоесть сделали создание группы
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name #имя канала
        )
    
        self.accept() 
    
    #когда мы делаем дисконект тогда вызываеться эта функция
    def disconnect(self, code):
        #self.channel_layer.group_discard: Эта функция используется для удаления канала из группы
        
        #тоесть в какой группы убираем канал self.channel_name
        async_to_sync(self.channel_layer.group_discard)( #async_to_sync тоесть преврощаем асинхронный код в сихронный
            self.room_group_name,
            self.channel_name
        )
        
    def receive(self, text_data): #receive он нужен чтобы получить сообщение от клиента
        text_data_json = json.load(text_data)
        message = text_data_json['message']
        
        async_to_sync(self.channel_layer.group_send)( #group_send она нужна чтобы послать сообщение определенной группы
            self.room_group_name, #тоесть этой группы мы будем посылать сообщение
            {
                'type': 'chat_message', #chat_message это тип функций каторая будет отпровлять сообщение, сообщение будет хрониться в event
                'message': message
            }
        )
        
    def chat_message(self, event):
        message = event['message']
        
        self.send(text_data=json.dumps({
            'event': 'Send',
            'message': message
        }))