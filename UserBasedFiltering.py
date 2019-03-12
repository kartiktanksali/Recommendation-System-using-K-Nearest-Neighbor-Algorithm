# -*- coding: utf-8 -*-
"""
Assignment
"""

# you must NOT import or use any other packages or modules besides these
import math
from operator import itemgetter

#################################################
# recommender class does user-based filtering and recommends items 
class UserBasedFilteringRecommender:

        def __init__(self, usersItemRatings, k=1):
            
            # set self.usersItemRatings
            self.usersItemRatings = usersItemRatings
            
            
                # set self.k
            if k > 0:   
                self.k = k
            else:
                raise ValueError("(FYI - invalid value of k (must be > 0) - defaulting to 1)")
    #                print ("(FYI - invalid value of k (must be > 0) - defaulting to 1)")
    #                self.k = 1
        
        
    
    
            


        def pearsonFn(self, userXItemRatings, userYItemRatings):
            
     #      initialize parameters       
            a = 0
            b = 0
            common_count = 0
            sum_of_a = 0
            sum_of_b = 0
            sum_of_aXb = 0
            a_square_sum = 0
            b_square_sum = 0
            
     #      calculate basic elements in the Pearson Correlation equation       
            for k in userXItemRatings:
                if k in userYItemRatings:
                    common_count = common_count + 1
                    a = userXItemRatings[k]
                    b = userYItemRatings[k]
                    sum_of_aXb += a * b
                    sum_of_a = sum_of_a + a
                    sum_of_b = sum_of_b + b
                    a_square_sum += pow(a, 2)
                    b_square_sum += pow(b, 2)
                    
     #      Exception circumstances               
            if common_count == 0:
                return -2
     
    #       Calculate Pearson Correlation     
            numerator = (sum_of_aXb - (sum_of_a * sum_of_b) / common_count)
            denominator = (math.sqrt(a_square_sum - pow(sum_of_a, 2) / common_count) * math.sqrt(b_square_sum - pow(sum_of_b, 2) / common_count))
            if denominator == 0:
                return -2
            else:
                return numerator / denominator
    
        #################################################
        # make recommendations for userX from the k most similar nearest neigibors (NNs)
        # NOTE: the number, names, or format of the input parameters to this method must NOT be changed.
        def recommendKNN(self, userX):
            
           coefficient_values = []       
    #      Calculating the distances & Sorting it with nearest to be first
           for nn in self.usersItemRatings:
                if nn != userX:
                    d = self.pearsonFn(self.usersItemRatings[userX], self.usersItemRatings[nn])
                    coefficient_values.append([nn, d])
        
               
           nearest = {}
           keys = itemgetter(1)
           coefficient_values.sort(key=keys, reverse=True) 
           nearest = coefficient_values
          
    #      Rounding of the values for further calculations 
           for i in range(len(nearest)):
               nearest[i][1] = round(nearest[i][1],2)
               
           
    #      Obtaining the distance and rescale (pc+1)/2
           pc = 0
           for i in range(self.k):
              nearest[i][1] = (nearest[i][1]+1)/2
              nearest[i][1] = round(nearest[i][1],2)
              pc = pc+nearest[i][1]
            
           UserInfo = self.usersItemRatings[userX]
           
           final_recommendation = {} #Final Recommendation dictionary
           
    #      Measuring the weight 
           for i in range(self.k): 
              weight = round((nearest[i][1]/pc),2)
    
    #         Obtaining information user which are included in the collabration
              user = nearest[i][0]
              NNRatings = self.usersItemRatings[user]
             
    #         Final Calculation, identifying non rated albums and drawing recommendations
              for albums in NNRatings:
                 if not albums in UserInfo:
                    if albums not in final_recommendation:
                       final_recommendation[albums] = round((NNRatings[albums] * weight),2)
                    else:
                       final_recommendation[albums] = round((final_recommendation[albums] + (NNRatings[albums] * weight)),2)
    
    #      Transfer the dictionary into a list and sort it based on Person Correlation
           final_recommendation = list(final_recommendation.items())
    
           keys = itemgetter(1)
           final_recommendation.sort(key=keys, reverse=True)
           
    
           return final_recommendation



        
