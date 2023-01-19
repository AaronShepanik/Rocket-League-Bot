# This file is for strategy

from util.objects import *
from util.routines import *
from util.tools import find_hits

# adding comment to test out branching with GIT


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

        targets = {
            'at_opponent_goal': (self.foe_goal.left_post, self.foe_goal.right_post),
            'away_from_our_net': (self.friend_goal.right_post, self.friend_goal.left_post)
        }
        hits = find_hits(self, targets)
        if self.me.boost > 80:
            if len(hits['at_opponent_goal']) > 0:
                self.set_intent(hits['at_opponent_goal'][0])
                self.debug_text = 'hitting at opponent goal'
                self.add_debug_line('shot', self.me.location,
                                    self.ball.location, [0, 0, 255])
                return
            # if len(hits['away_from_our_net']) > 0:
            #     self.set_intent(hits['away_from_our_net'][0])
            #     print('away from our goal')
            #     self.debug_text = 'hitting away from own goal'
            #     self.add_debug_line('shot', self.me.location,
            #                         self.ball.location, [0, 0, 255])
            #     return

            # self.set_intent(short_shot(self.foe_goal.location))
            # self.debug_text = 'shooting'
            # self.add_debug_line('shot', self.me.location,
            #                    self.ball.location, [0, 0, 255])
            # return

        target_boost = self.get_closest_large_boost()
        if target_boost is not None:
            self.set_intent(goto(target_boost.location))
            self.debug_text = 'getting boost'
            self.add_debug_line('boost', self.me.location,
                                target_boost.location, [0, 255, 0])
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
            self.set_intent(atba())
