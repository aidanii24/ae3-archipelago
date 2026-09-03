from ..data.Strings import APHelper, Itm, Loc
from .bases import AE3TestBase


class TestShopPGCItem(AE3TestBase):
    options = {
        "goal_target": 0,
        "logic_preference": 0,
        "post_game_condition_monkeys": -2,
        "post_game_condition_bosses": 0,
        "post_game_condition_cameras": 0,
        "post_game_condition_cellphones": 0,
        "post_game_condition_shop": 0,
        "post_game_condition_keys": 0,
        "monkeysanity_break_rooms": 1,
        "shoppingsanity": 1,
    }

    def test_shop_pgc_item_access(self):
        """Test Access to PGC Items"""

        loc_shop_ultimape_fighter = self.world.get_location(Loc.shop_ultim_ape_fighter.value)
        loc_specter = self.world.get_location(Loc.boss_specter.value)

        # Ultim-ape Fighter and Specter (the Goal Boss) should not be accessible
        # due to their areas being locked behind having can_reach return true for 440 Monkey Locations
        self.assertFalse(loc_shop_ultimape_fighter.can_reach(self.multiworld.state))
        self.assertFalse(loc_specter.can_reach(self.multiworld.state))

        # Getting all Channel Keys should not change accessibility of the locations
        # As Channel Keys only unlock more levels
        self.collect_by_name(APHelper.channel_key.value)
        self.assertFalse(loc_shop_ultimape_fighter.can_reach(self.multiworld.state))
        self.assertFalse(loc_specter.can_reach(self.multiworld.state))

        # With PGC Monkeys set to Vanilla, getting most items should not be enough either
        self.collect_by_name(Itm.get_gadgets_ordered())
        self.collect_by_name(Itm.morph_ninja.value)
        self.collect_by_name(Itm.morph_magician.value)
        self.collect_by_name(Itm.morph_kungfu.value)

        self.assertFalse(loc_shop_ultimape_fighter.can_reach(self.multiworld.state))
        self.assertFalse(loc_specter.can_reach(self.multiworld.state))

        # Remaining Possible Progressive Items except for Super Monkey
        # which should allow into logic the Break Room Monkeys
        self.collect_by_name(Itm.morph_knight.value)
        self.collect_by_name(Itm.morph_cowboy.value)
        self.collect_by_name(Itm.morph_hero.value)

        self.assertFalse(loc_shop_ultimape_fighter.can_reach(self.multiworld.state))
        self.assertFalse(loc_specter.can_reach(self.multiworld.state))

        # Collecting Super Monkey should make the game beatable
        self.collect_by_name(Itm.morph_monkey.value)

        # Getting Super Monkey should make the world beatable
        self.assertBeatable(beatable=True)
