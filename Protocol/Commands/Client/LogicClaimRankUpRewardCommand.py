from ByteStream.Reader import Reader
from Protocol.Messages.Server.AvailableServerCommandMessage import AvailableServerCommandMessage
from Protocol.Commands.Server.LogicGiveDeliveryItemsCommand import LogicGiveDeliveryItemsCommand

class LogicClaimRankUpRewardCommand(Reader):
    def __init__(self, client, player, initial_bytes):
        super().__init__(initial_bytes)
        self.player = player
        self.client = client

    def decode(self):
        self.readVInt()
        self.readVInt()
        self.readLogicLong()
        self.reward_id = self.readVInt() # Індекс нагороди на дорозі кубків

    def process(self, db):
        # Поки що видаємо звичайний ящик за будь-яку нагороду
        self.player.delivery_items = {
            "DeliveryTypes": [10], # 10 = Brawl Box
            'Items': []
        }
        
        # Збільшуємо індекс наступної нагороди
        self.player.trophy_reward += 1
        db.update_player_account(self.player.token, 'TrophyRoadReward', self.player.trophy_reward)
        
        # Відправляємо команду на відкриття ящика
        self.player.db = db
        AvailableServerCommandMessage(self.client, self.player, LogicGiveDeliveryItemsCommand).send()
