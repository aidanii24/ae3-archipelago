from test.bases import WorldTestBase

from .. import AE3World
from ..data.Strings import Meta


class AE3TestBase(WorldTestBase):
    game = Meta.game
    world: AE3World
