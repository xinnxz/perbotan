from pydantic_settings import BaseSettings

class Settings(BaseSettings):


    # True - вкл
    # False - выкл

    TAPS_ENABLED: bool = True # Вкл/выкл тапы
    TAPS_PER_SECOND: list[int] = [20, 30]  
    INVEST_ENABLED: bool = False  # НЕ ВОРК
    PVP_ENABLED: bool = False # ПОКА ЧТО НЕ ВОРК ####будет работать после прокачки навыка "переговоры"####
    PVP_LEAGUE: str = 'auto'
    PVP_UPGRADE_LEAGUE: bool = True # Вкл/выкл прокачку лиги в пвп
    PVP_COUNT: int = 10 # Количество боев
    PVP_STRATEGY: str = 'random'
    SKILLS_COUNT: int = 10 # Максимальный лвл прокачки скилов дохода
    SKILLS_MODE: str = 'aggressive'
    IGNORED_SKILLS: list[str] = [] # Скилы для игнорирования
    MINING_SKILLS_LEVEL: int = 10 # Максимальный лвл прокачки скилов майнинга
    PROTECTED_BALANCE: int = 0 # Сумма на баллансе для сохранения, не будет тратить, если баланс может опустится ниже этой суммы
    SLEEP_MULT: int = 120 # Сон между аккаунтами 2 мин
    SLEEP_ALL: int = 3600 # Сон между кругами 1 час, указывать в секундах




try:
    config = Settings()
except Exception as error:
    print(f"{error}")
    config = False
