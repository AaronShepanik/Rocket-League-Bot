# This file is for strategy

from util.objects import *
from util.routines import *
from util.tools import find_hits

# adding comment to test out branching with GIT
# TODO # potential problem with goto_boost and passing location
# the car just goes in circles and can't actually get the boost?
# possibly add an "upfield" target for shots
# bot is prioritzing boost too much, need to keep track of where ball is on field and decide from there


class Bot(GoslingAgent):
    # This function runs every in-game tick (every time the game updates anything)

    def run(self):
        self.print_debug()

        if self.get_intent() is not None:
            self.debug_intent()
            return

        if self.kickoff_flag:
            self.clear_debug_lines()
            self.set_intent(kickoff())
            self.add_debug_line('kickoff',
                                self.me.location, self.ball.location)
            return
        self.clear_debug_lines()

        if self.is_in_front_of_ball():
            self.set_intent(goto(self.friend_goal.location))
            self.debug_text = 'retreating'
            self.add_debug_line('retreat', self.me.location,
                                self.friend_goal.location, [250, 0, 0])
            return

        # targets = {
        #     'at_opponent_goal': (self.foe_goal.left_post, self.foe_goal.right_post),
        #     'away_from_our_net': (self.friend_goal.right_post, self.friend_goal.left_post)
        # }

        if self.me.boost > 50:
            targets = {'at_opponent_goal': (
                self.foe_goal.left_post, self.foe_goal.right_post)}
            hits = find_hits(self, targets)
            if len(hits['at_opponent_goal']) > 0:
                self.set_intent(hits['at_opponent_goal'][0])
                self.debug_text = 'hitting at opponent goal'
                self.add_debug_line('shot', self.me.location,
                                    self.ball.location, [0, 0, 255])
                return

        target_large_boost = self.get_closest_large_boost()
        active_boost = self.get_closest_boost()

        if target_large_boost is not None and self.me.boost < 20:
            self.set_intent(goto(target_large_boost.location))
            self.debug_text = 'getting large boost'
            self.add_debug_line('boost', self.me.location,
                                target_large_boost.location, [0, 255, 0])
            return

        elif active_boost is not None and self.me.boost < 50:
            self.set_intent(goto_boost(active_boost))
            self.debug_text = 'getting active boost'
            self.add_debug_line('boost', self.me.location,
                                active_boost.location, [0, 255, 0])
            return

        # if len(hits['at_opponent_goal']) > 0:
        #     self.set_intent(hits['at_opponent_goal'][0])
        #     print('at their goal')
        #     return
        # if len(hits['away_from_our_net']) > 0:
        #     self.set_intent(hits['away_from_our_net'][0])
        #     print('away from our goal')
        #     return

        else:
            self.set_intent(short_shot(self.foe_goal.location))
            self.debug_text = 'default routine'
