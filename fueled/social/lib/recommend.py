from social.models import RestaurantVisits, Team
from restaurants.models import Restaurant
from accounts.models import TeamUser
import random

class BaseRecommendationEngine(object):
    def __init__(self, request, team, jitter_level=2):
        self.team_users = TeamUser.objects.filter(team=team)
        self.team_most_visited = []
        
        for member in self.team_users:
            try:
                most_visited = RestaurantVisits.objects.filter(user=member.user).order_by('-visit_count')[:1][0]
                self.team_most_visited.append(most_visited)
            except IndexError:
                pass
            
        
        self.restaurants = Restaurant.objects.all()
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
    4 - Random selection from Team Top Choices, Weighted on First Two Top Choices, with a Random Restaurant
    
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
        if self.jitter_level == 3:
            index = random.randint(1, len(self.restaurants))
            random_restaurant = self.restaurants[index-1:index][0]
            top_choices.append(random_restaurant)
            return top_choices[random.randint(0, len(top_choices)-1)]
        
            
            

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