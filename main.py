# This file is for strategy

from util.objects import *
from util.routines import *
from util.tools import find_hits


# TODO #
# the car just goes in circles and can't actually get the boost sometimes?


class Bot(GoslingAgent):
    # This function runs every in-game tick (every time the game updates anything)

    def run(self):
        self.print_debug()

        large_boost = self.get_closest_large_boost()
        home = self.friend_goal.location - \
            Vector3(0, side(self.team)*1000, 100)
        leftfield = Vector3(-side(self.team)*4200,
                            self.ball.location.y + (-side(self.team)*2000), 200)
        rightfield = Vector3(side(self.team)*4200,
                             self.ball.location.y + (-side(self.team)*2000), 200)
        targets = {'at_opponent_goal': (self.foe_goal.left_post, self.foe_goal.right_post), 'away_from_our_net': (
            self.friend_goal.right_post, self.friend_goal.left_post), 'upfield': (leftfield, rightfield)}
        hits = find_hits(self, targets)
        ball_to_goal = (self.ball.location -
                        self.friend_goal.location).magnitude()

        if self.get_intent() is not None:
            self.debug_intent()
            return

        if self.kickoff_flag:
            self.clear_debug_lines()
            self.set_intent(kickoff())
            self.debug_text = 'Kickoff'
            return
        self.clear_debug_lines()

        # retreat if in front of ball and enemy can shoot or ball is close to own goal
        if self.is_in_front_of_ball() and (self.foe_close() or ball_to_goal < 4000):

            self.set_intent(goto(self.friend_goal.location))
            self.debug_text = 'retreating'
            return

        # look for a way to hit the ball in the right direction if no threat of enemy shot
        if self.is_in_front_of_ball() and not self.foe_close():

            if len(hits['upfield']) > 0 and abs(self.friend_goal.location.y - self.ball.location.y) < 6000:
                # only hit the ball "upfield" if we're kind of close to our net, 6000 units is about half the field including goal depth
                self.set_intent(hits['upfield'][0])
                self.debug_text = 'foe not close hitting upfield'
                return
            elif len(hits['at_opponent_goal']) > 0:
                self.set_intent(hits['at_opponent_goal'][0])
                self.debug_text = 'foe not close hit at opponent goal'
                return

            # only hit the ball away from our net if it's close to our goal
            elif len(hits['away_from_our_net']) > 0 and abs(self.friend_goal.location.y - self.ball.location.y) < 1200:
                self.set_intent(hits['away_from_our_net'][0])
                self.debug_text = 'foe not close hitaway from our net'
                return

            else:
                self.set_intent(goto(home))
                self.debug_text = 'No shots,going home'
                return

        if not self.is_in_front_of_ball() and self.me.boost > 25:
            # attack!
            # look for a way to hit the ball in the right direction

            if len(hits['at_opponent_goal']) > 0:
                self.set_intent(hits['at_opponent_goal'][0])
                self.debug_text = 'hitting at opponent goal'
                return
            # only hit the ball "upfield" if we're kind of close to our net, 6000 units is about half the field including goal depth
            elif len(hits['upfield']) > 0 and abs(self.friend_goal.location.y - self.ball.location.y) < 6000:
                self.set_intent(hits['upfield'][0])
                self.debug_text = 'hitting upfield'
                return

            else:
                # reset position by moving towards own goal

                self.set_intent(goto(home))
                self.debug_text = 'no-shots going towards home'
                return

        if large_boost is not None and self.me.boost < 15:
            boost_location = large_boost.location
            self.set_intent(goto(boost_location))
            self.debug_text = 'getting large boost'
            return

        # default routine for when we run out of logic
        if not (large_boost is not None and self.me.boost < 15):
            self.set_intent(short_shot(self.foe_goal.location))
            self.debug_text = 'default routine'
            return
