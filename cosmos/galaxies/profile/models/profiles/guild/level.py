from .base import GuildMemberProfileBase
from abc import ABC, abstractmethod


class UserLevel(GuildMemberProfileBase, ABC):

    K = 5777
    LEVELS_XP = [5 * (i ** 2) + 50 * i + 100 for i in range(200)]

    def get_level(self, xp):
        level = 0
        while xp >= self.LEVELS_XP[level]:
            xp -= self.LEVELS_XP[level]
            level += 1
        return level

    @property
    @abstractmethod
    def xp(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def voice_xp(self):
        raise NotImplementedError

    @property
    def delta_xp(self):
        return sum(self.LEVELS_XP[: self.level + 1]) - self.xp

    @property
    def delta_voice_xp(self):
        return sum(self.LEVELS_XP[: self.voice_level + 1]) - self.voice_xp

    # @property
    # def xp_level(self):
    #     return self._xp_level + math.log(self._level + math.e)*self.K

    # @property
    # def delta_xp(self):
    #     return int(self.xp_level - self.xp)
    #
    # def from_delta_xp(self):
    #     while self.xp >= self.xp_level:    # TODO: Remove loop.
    #         self._xp_level += self.xp_level
    #         self._level += 1    # Don't really need self._level -= 1 'cause user will never loose xp.
    #     return self._level

    @property
    def level(self):
        return self.get_level(self.xp)

    @property
    def voice_level(self):
        return self.get_level(self.voice_xp)

    async def level_up_callback(self):
        guild_profile = await self.fetch_guild_profile()
        await guild_profile.levels.give_rewards(self, channel="text")

        # TODO: Level up announcements, notifications.

    async def voice_level_up_callback(self):
        guild_profile = await self.fetch_guild_profile()
        await guild_profile.levels.give_rewards(self, channel="voice")

        # TODO: Level up announcements, notifications.
