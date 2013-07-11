from social.models import RestaurantVisits, Team
from restaurants.models import Restaurant
from accounts.models import TeamUser
import random

class BaseRecommendationEngine(object):
    def __init__(self, request, team, jitter_level=2):
        self.team_users = TeamUser.objects.filter(team=team)
        # Lets use list comprehension to get all the ids
        self.team_user_ids = [member.user.pk for member in self.team_users]
        self.team_most_visited = []
        
        for member in self.team_users:
            try:
                most_visited = RestaurantVisits.objects.exclude(restaurant__restaurantthumbsdown__user=request.user).filter(user=member.user).order_by('-visit_count')[:1][0]
                self.team_most_visited.append(most_visited)
            except IndexError:
                pass
            
        self.team_most_visited_restaurant_ids = [visitcount.restaurant.pk for visitcount in self.team_most_visited]
        self.restaurants = Restaurant.objects.exclude(restaurantthumbsdown__user__in=self.team_user_ids).exclude(pk__in=self.team_most_visited_restaurant_ids).all()
        self.jitter_level = jitter_level


    """
    We need a way to add some jitter to our recommendation engine.
    We cant always recommend the save restaurant. Sometimes we want to recommend something new, 
    or recommend the second best choice.
    Level Definitions:
    0 - No Jitter
    1 - Random selection between First choice and Second choice if First choice is Definitive.
    2 - Random selection from Team Top Choices.
    3 - Random selection from Team Top Choices with a Random Restaurant.
    4 - Random selection from Team Top Choices with a small possibility of a Random Restaurant
        however, if the top choices amount to less than 1 top choice, the recommendation must be random
        final chance of random restaurant is (1 in 3) chance that you will have a (1 in len(top_choices+1) chance to select a random restaurant. This is a good jitter level for small teams, but may not be optimal for larger teams that want to explore a little.

    5 - Random selection from Team Top Choices, Weighted on First Two Top Choices, with a Random Restaurant
    
    ** In Respect to number 3, the restaurants table is currently denormalized, 
    but in an actual system we would use Location to limit the select first, and then use cuisine types 
    to limit further, and then select randomly from that final pool.
    """
    def set_jitter(self, jitter_level):
        self.jitter_level = jitter_level

    """
    Refer to _get_top_choices for definition of heuristic
    """
    def recommend(self, heuristic):
        top_choices = self._get_top_choices(heuristic)
        if self.jitter_level == 2:
            return top_choices[random.randint(0, len(top_choices)-1)]
            
        if self.jitter_level == 3:
            try:
                index = random.randint(1, len(self.restaurants))
                random_restaurant = self.restaurants[index-1:index][0]
                top_choices.append(random_restaurant)
            except ValueError as e:
                # if there are no random restaurants due to thumbsdowns we just pass
                pass
            
            
        
        if self.jitter_level == 4:
            if random.randint(0,2) == 1 or len(top_choices) < 1:
                
                try:
                    index = random.randint(1, len(self.restaurants))
                    random_restaurant = self.restaurants[index-1:index][0]
                    top_choices.append(random_restaurant)
                except ValueError as e:
                    # if there are no random restaurants due to thumbs downs, we just pass
                    pass

        try:
            return top_choices[random.randint(0, len(top_choices)-1)]
        except:
            return []

    """
    Heuristic is how we define top 3 choices.
    1. Most visited per member.
    2. Most visited overall
    3. Most liked
    """
    def _get_top_choices(self, heuristic):
        if heuristic == 1:
            self.team_most_visited.sort(key=lambda restaurantvisits: restaurantvisits.visit_count, 
                                        reverse=True)
        
        restaurants = []
        for record in self.team_most_visited:
            restaurants.append(record.restaurant)
            print record.restaurant.name + ' | ' + unicode(record.visit_count)

        return restaurants
