# This file is for strategy

from util.objects import *
from util.routines import *
from util.tools import find_hits


# TODO # potential problem with goto_boost and passing location
# the car just goes in circles and can't actually get the boost?


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

        if self.me_offside() and self.foe_close():

            if self.me.boost < 50:
                # Before retreating--see if there's boosts on the way home
                if self.get_boost_while_going_home() is not None:
                    boost_target = self.get_boost_while_going_home
                    self.set_intent(goto_boost(
                        boost_target.location, self.friend_goal.location))
                    self.debug_text = 'foe close get boost and going home'
                    return
                else:
                    self.set_intent(goto(self.friend_goal.location))
                    self.debug_text = 'foe close going home'
                    self.add_debug_line('retreat', self.me.location,
                                        self.friend_goal.location, [250, 0, 0])
                    return

            else:
                # just go home if we have lots of boost
                self.set_intent(goto(self.friend_goal.location))
                self.debug_text = 'retreating'
                self.add_debug_line('retreat', self.me.location,
                                    self.friend_goal.location, [250, 0, 0])
                return

        elif self.me_offside() and not self.foe_close():
            # look for a way to hit the ball in the right direction
            leftfield = Vector3(-side(self.team)*4200,
                                self.ball.location.y + (-side(self.team)*2000), 200)
            rightfield = Vector3(side(self.team)*4200,
                                 self.ball.location.y + (-side(self.team)*2000), 200)
            targets = {'at_opponent_goal': (self.foe_goal.left_post, self.foe_goal.right_post), 'away_from_our_net': (
                self.friend_goal.right_post, self.friend_goal.left_post), 'upfield': (leftfield, rightfield)}
            hits = find_hits(self, targets)
            if len(hits['at_opponent_goal']) > 0:
                self.set_intent(hits['at_opponent_goal'][0])
                self.debug_text = 'foe not close hit at opponent goal'
                return
            elif len(hits['upfield']) > 0 and abs(self.friend_goal.location.y - self.ball.location.y) < 6000:
                # only hit the ball "upfield" if we're kind of close to our net, 6000 units is about half the field including goal depth
                self.set_intent(hits['upfield'][0])
                self.debug_text = 'foe not close hitting upfield'
                return
            # only hit the ball away from our net if it's close to our goal
            elif len(hits['away_from_our_net']) > 0 and abs(self.friend_goal.location.y - self.ball.location.y) < 1200:
                self.set_intent(hits['away_from_our_net'][0])
                self.debug_text = 'foe not close hitaway from our net'
                return
            # if we don't have any shots to take from above, let's retreat home and get boost on the way
            elif self.get_boost_while_going_home() is not None:
                boost_target = self.get_boost_while_going_home
                self.set_intent(goto_boost(
                    boost_target.location, self.friend_goal.location))
                self.debug_text = 'No shots-get boost and go home'
                return
            else:
                self.set_intent(goto(self.friend_goal.location))
                self.debug_text = 'No shots,going home'
                self.add_debug_line('retreat', self.me.location,
                                    self.friend_goal.location, [250, 0, 0])
                return

        elif not self.me_offside():
            # attack!
            # look for a way to hit the ball in the right direction
            leftfield = Vector3(-side(self.team)*4200,
                                self.ball.location.y + (-side(self.team)*2000), 200)
            rightfield = Vector3(side(self.team)*4200,
                                 self.ball.location.y + (-side(self.team)*2000), 200)
            targets = {'at_opponent_goal': (self.foe_goal.left_post, self.foe_goal.right_post), 'away_from_our_net': (
                self.friend_goal.right_post, self.friend_goal.left_post), 'upfield': (leftfield, rightfield)}
            hits = find_hits(self, targets)
            if len(hits['at_opponent_goal']) > 0:
                self.set_intent(hits['at_opponent_goal'][0])
                self.debug_text = 'hitting at opponent goal'
                return
            # only hit the ball "upfield" if we're kind of close to our net, 6000 units is about half the field including goal depth
            elif len(hits['upfield']) > 0 and abs(self.friend_goal.location.y - self.ball.location.y) < 6000:
                self.set_intent(hits['upfield'][0])
                self.debug_text = 'hitting upfield'
                return
            # go home to reposition and get boost
            elif self.get_boost_while_going_home() is not None:
                boost_target = self.get_boost_while_going_home
                self.set_intent(goto_boost(
                    boost_target.location, self.friend_goal.location))
                self.debug_text = 'No shots-get boost and go home'
                return

            else:
             # reset position by moving towards own goal
                self.set_intent(goto(
                    self.friend_goal.location - Vector3(0, side(self.team)*400, 0)))
                self.debug_text = 'no-shots going towards home'
                self.add_debug_line('atball', self.me.location,
                                    self.friend_goal.location - Vector3(0, side(self.team)*400, 0), [0, 255, 0])
                return

        # default routine for when we run out of logic
        else:
            self.set_intent(short_shot(self.foe_goal.location))
            self.debug_text = 'default routine'
            return


"""
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

"""
