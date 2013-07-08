from social.models import RestaurantVisits, Team
from restaurants.models import Restaurant
from accounts.models import TeamUser


class BaseRecommendationEngine(object):
    def __init__(self, team, jitter_level=2):
        self.team_users = TeamUser.objects.filter(team=team)
        self.team_most_visited = []
        
        for member in self.team_users:
            try:
                most_visited = RestaurantVisits.objects.filter(user=member.user).exclude(user=request.user).order_by('-visit_count')[:1][0]
                self.team_most_visited.append(most_visited)
            except IndexError:
                pass
            
        
        self.restaurants = Restaurants.objects.all()
        self.jitter_level = jitter_level


    """
    We need a way to add some jitter to our recommendation engine.
    We cant always recommend the save restaurant. Sometimes we want to recommend something new, or recommend the second best choice.
    Level Definitions:
    0 - No Jitter
    1 - Random selection between First choice and Second choice if First choice is Definitive.
    2 - Random selection between Top 3 Choices.
    3 - Random selection from array of Top 3 Choices with a Random Restaurant.
    ** In Respect to number 3, the restaurants table is currently denormalized, 
    but in an actual system we would use Location to limit the select first, and then use cuisine types 
    to limit further, and then select randomly from that final pool.
    """
    def set_jitter(jitter_level):
        self.jitter_level = jitter_level

    
        
    
