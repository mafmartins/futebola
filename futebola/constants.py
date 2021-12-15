class BonusType:
    @classmethod
    def choices(cls):
        return (("most_assists_in_game", "Mais assistências num jogo pela sua equipa"),)

    @classmethod
    def types(cls):
        return [key for key, item in cls.choices()]
