from src.main import Main
from cfg.config import config
from cfg.queries import queries

print("Playlist Creator v2")


main = Main(config, queries)
main.run()
