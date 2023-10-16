import pygame
import random

def calculate_score(care_score, work_score, money_score, social_score, family_score, exp_health, babies):
    total_score = 0
    total_score += 100/((40 - (care_score - 0.01))**2)
    total_score += 100/(babies - (60/(work_score + money_score-0.01)))
    total_score += 100/((80 - (work_score + money_score - 0.01))**2)
    total_score += 100/((40 - (social_score - 0.01))**2)
    total_score += 100/((40 - (family_score - 0.01))**2)
    return total_score*exp_health

class Item:
    def __init__(self,xpos,item):
        self.xpos = xpos
        self.ypos = 0
        self.ydir = random.uniform(10,20)
        self.item = item

    def update(self):
        self.ypos += self.ydir


