import cv2
import pygame
import numpy as np
import mediapipe as mp
import time
import math
from itemsclasses import Item
import random
from itemsclasses import calculate_score

def distance(p1x,p2x,p1y,p2y):
    return math.sqrt((p1x - p2x) ** 2 + (p1y - p2y) ** 2)

# Initialize Pygame
pygame.init()
mp_hands = mp.solutions.hands

# SETTING THE WINDOW STUFF
width, height = 1280, 720

# PYGAME SETUP
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("RGB Camera in Pygame")

# CV2 STUFF
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# Palm Variables
palm_center_x = None
palm_center_y = None

# Font Creation
font = pygame.font.Font("Die in a fire PG.otf", 50)  # You can choose a font and size

# Current Time
start_time = time.time()

# Spawned Item List
spawned_items = []

# Elapsed tick
elapsed_tick = 0
previous_time = time.time()

# INTRO VARIABLES
intro_font = pygame.font.Font("Die in a fire PG.otf", 100)
needs_font = pygame.font.Font("Die in a fire PG.otf", 40)
intro_text = font.render("OBJECTIVE: LIVE A PERFECTLY NORMAL LIFE", True, (255, 255, 255))
intro_text_rect = intro_text.get_rect()
intro_text_rect.center = (1280 // 2, 720 // 2)
# Different Scores to Maintain
"""
Golden Scores are: Spoil_score = 20, Care_score = 10, Work_score = 30, Social_score = 20, Family_score = 50   
"""
care_score = 0
work_score = 0
money_score = 0
social_score = 0
babies = 0
family_score = 0
total_score = 0
health = 100
needs = ["More Loving","More Money and Work","More Fun","More Familial Time"]
needs_text = "YOU NEED: " + str(needs[random.randint(0,len(needs) - 1)])

end_font = pygame.font.Font("Die in a fire PG.otf", 30)

while(time.time() - previous_time < 5):
    # Fill the screen with the background color (black)
    screen.fill((0,0,0))

    # Draw the text on the screen
    screen.blit(intro_text, intro_text_rect)

    # Update the display
    pygame.display.flip()

previous_time = time.time()
time_starter = time.time()
start_time = time.time()

while True:
    """OBTAIN THE PALM CENTERS TO USE LATER ON"""
    ret, frame = cap.read()

    if not ret:
        continue

    with mp_hands.Hands(min_detection_confidence=0.2, min_tracking_confidence=0.2) as hands:
        # Convert the BGR image to RGB
        rgb_frame = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB)

        # Process the frame to detect hands
        results_hands = hands.process(rgb_frame)

        # Extract and draw the central points of the palms
        if results_hands.multi_hand_landmarks:
            for landmarks in results_hands.multi_hand_landmarks:
                palm_center_x = int(landmarks.landmark[mp_hands.HandLandmark.WRIST].x * frame.shape[1])
                palm_center_y = int(landmarks.landmark[mp_hands.HandLandmark.WRIST].y * frame.shape[0]) - 150
        else:
            palm_center_x = None
            palm_center_y = None

    """DO ALL THE PYGAME STUFF"""
    # Rotate the frame 90 degrees counterclockwise
    rotated_frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)

    # Convert the BGR frame to RGB
    frame_rgb = cv2.cvtColor(rotated_frame, cv2.COLOR_BGR2RGB)

    # Convert the frame to a Pygame surface
    pygame_frame = pygame.surfarray.make_surface(frame_rgb)

    # Blit the frame onto the Pygame screen
    screen.blit(pygame_frame, (0, 0))

    """DISPLAY ALL THE TEXT"""
    # Figure out the current time
    current_year = math.floor(time.time() - start_time)
    if (current_year > health):
        break

    # Create UI for year
    text = str(current_year) + " years old"  # Your desired text here
    text_surface = font.render(text, True, (0, 0, 0))  # Text color: white

    expected_lifespan = "EXPECTED LIFESPAN: " + str(health)
    expected_lifespan_surface = font.render(expected_lifespan, True, (0, 0, 0))
    screen.blit(expected_lifespan_surface,(700,20))

    if(care_score > 20):
        try:
            needs.remove("More Loving")
        except:
            print("Already Removed")
    if(work_score + money_score > (babies*60) + 80):
        try:
            needs.remove("More Money and Work")
        except:
            print("Already Removed")
    if(social_score > 40):
        try:
            needs.remove("More Fun")
        except:
            print("Already Removed")
    if(family_score > 40):
        try:
            needs.remove("More Familial Time")
        except:
            print("Already Removed")
    if(len(needs) == 0):
        needs_text = "YOU NEED: TO LIVE AS LONG AS YOU CAN"
    else:
        if(time.time() - time_starter > 2):
            time_starter = time.time()
            needs_text = "YOU NEED: " + str(needs[random.randint(0,len(needs) - 1)])
    needs_text_surface = needs_font.render(needs_text, True, (0, 0, 0))
    screen.blit(needs_text_surface, (10, 650))
    # Blit the text onto the Pygame screen
    screen.blit(text_surface, (20, 20))  # Adjust position as needed

    # CREATE UI FOR SCORE
    total_score = math.floor(calculate_score(care_score,work_score,money_score,social_score,family_score,current_year,babies))
    score = "SCORE: " + str(total_score)
    score_surface = font.render(score,True, (0,0,0))
    screen.blit(score_surface,(350,20))

    """GAME LOGIC"""
    elapsed_tick = (time.time() - previous_time)
    # Create a new item for baby stage
    if(current_year < 5 and elapsed_tick > 0.6):
        previous_time = time.time()
        new_item = None
        random_number = random.randint(0, 3)
        if(random_number == 0):
            new_item = Item(random.randint(0,1280),"ItemPhotos/binky.png")
        elif(random_number == 1):
            new_item = Item(random.randint(0, 1280), "ItemPhotos/heart.png")
        elif (random_number == 2):
            new_item = Item(random.randint(0, 1280), "ItemPhotos/virus.png")
        else:
            new_item = Item(random.randint(0,1280),"ItemPhotos/stuffedanimal.png")
        spawned_items.append(new_item)
    print(money_score)
    # Elementary Stage
    if(current_year > 5 and current_year < 12 and elapsed_tick > 0.5):
        previous_time = time.time()
        new_item = None
        random_number = random.randint(0,3)
        if (random_number == 0):
            new_item = Item(random.randint(0, 1280), "ItemPhotos/lego.png")
        elif(random_number == 1):
            new_item = Item(random.randint(0, 1280), "ItemPhotos/soccer.png")
        elif(random_number == 2):
            new_item = Item(random.randint(0, 1280), "ItemPhotos/videogame.png")
        else:
            new_item = Item(random.randint(0, 1280), "ItemPhotos/book.png")
        spawned_items.append(new_item)

    # Middle to High School
    if (current_year > 12 and current_year < 19 and elapsed_tick > 0.4):
        previous_time = time.time()
        new_item = None
        random_number = random.randint(0, 5)
        if (random_number == 0):
            new_item = Item(random.randint(0, 1280), "ItemPhotos/phone.png")
        elif (random_number == 1):
            new_item = Item(random.randint(0, 1280), "ItemPhotos/run.png")
        elif (random_number == 3):
            new_item = Item(random.randint(0, 1280), "ItemPhotos/virus.png")
        elif (random_number == 2):
            new_item = Item(random.randint(0, 1280), "ItemPhotos/relationship.png")
        else:
            new_item = Item(random.randint(0, 1280), "ItemPhotos/book.png")
        spawned_items.append(new_item)

    # College to Marriage
    if (current_year > 19 and current_year < 30 and elapsed_tick > 0.2):
        previous_time = time.time()
        new_item = None
        random_number = random.randint(0, 4)
        if (random_number == 0):
            new_item = Item(random.randint(0, 1280), "ItemPhotos/work.png")
        elif (random_number == 1):
            new_item = Item(random.randint(0, 1280), "ItemPhotos/baby.png")
        elif (random_number == 2):
            new_item = Item(random.randint(0, 1280), "ItemPhotos/car.png")
        elif (random_number == 3):
            new_item = Item(random.randint(0, 1280), "ItemPhotos/pills.png")
        else:
            new_item = Item(random.randint(0, 1280), "ItemPhotos/book.png")
        spawned_items.append(new_item)

    # End Of Life
    if (current_year > 30 and elapsed_tick > 0.2):
        previous_time = time.time()
        new_item = None
        random_number = random.randint(0, 6)
        if (random_number == 5):
            new_item = Item(random.randint(0, 1280), "ItemPhotos/work.png")
        elif (random_number == 0):
            new_item = Item(random.randint(0, 1280), "ItemPhotos/virus.png")
        elif (random_number == 1):
            new_item = Item(random.randint(0, 1280), "ItemPhotos/baby.png")
        elif (random_number == 2):
            new_item = Item(random.randint(0, 1280), "ItemPhotos/house.png")
        elif (random_number == 3):
            new_item = Item(random.randint(0, 1280), "ItemPhotos/pills.png")
        else:
            new_item = Item(random.randint(0, 1280), "ItemPhotos/book.png")
        spawned_items.append(new_item)

    # Check over our current spawned_items list
    #print(spawned_items)
    for item in spawned_items:
        #Checks if our item is touching anything
        if(palm_center_x != None):
            if(item.ypos > 720 or distance(palm_center_x,item.xpos,palm_center_y,item.ypos) < 40):
                spawned_items.remove(item)
                """UPDATING SCORE"""
                if(distance(palm_center_x,item.xpos,palm_center_y,item.ypos) < 40):
                    if(item.item == "ItemPhotos/baby.png"):
                        babies += 5
                    elif(item.item == "ItemPhotos/binky.png"):
                        care_score += 5
                    elif (item.item == "ItemPhotos/book.png"):
                        work_score += 5
                        money_score += 5
                    elif (item.item == "ItemPhotos/car.png"):
                        money_score -= 5
                        social_score += 5
                    elif (item.item == "ItemPhotos/house.png"):
                        money_score -= 5
                    elif (item.item == "ItemPhotos/heart.png"):
                        care_score += 5
                        family_score += 6
                    elif (item.item == "ItemPhotos/lego.png"):
                        care_score += 5
                        money_score -= 5
                        social_score += 10
                    elif (item.item == "ItemPhotos/phone.png"):
                        social_score += 5
                    elif (item.item == "ItemPhotos/pills.png"):
                        health -= random.randint(-10, 10)
                    elif (item.item == "ItemPhotos/relationship.png"):
                        family_score += 5
                        social_score += 5
                        care_score += 5
                    elif (item.item == "ItemPhotos/run.png" or item.item == "ItemPhotos/soccer.png"):
                        health += 5
                        social_score += 5
                    elif (item.item == "ItemPhotos/stuffedanimal.png"):
                        care_score += 5
                    elif (item.item == "ItemPhotos/videogame.png"):
                        work_score -= 5
                        money_score -= 5
                        social_score += 10
                    elif (item.item == "ItemPhotos/virus.png"):
                        health -= random.randint(1, 20)
                    elif (item.item == "ItemPhotos/work.png"):
                        work_score += 5
                        money_score += 5
            else:
                # Update item position
                item.update()
                # Renders the item
                screen.blit(pygame.image.load(item.item).convert_alpha(), (item.xpos, item.ypos))
        else:
            #Update item position
            item.update()
            #Renders the item
            screen.blit(pygame.image.load(item.item).convert_alpha(),(item.xpos,item.ypos))

    """PRINT THE PALM CENTER VARIABLES"""
    if (palm_center_x != None):
        screen.blit(pygame.image.load("ItemPhotos/hand.png").convert_alpha(), (palm_center_x, palm_center_y))

    """ENDING MANAGEMENT PYGAME STUFF"""
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            cap.release()
            cv2.destroyAllWindows()
            exit()

while True:
    # Fill the screen with the background color (black)
    screen.fill((0,0,0))
    end_text = f"FINAL SCORE: {total_score}\nLIFE LIVED: {current_year} years"
    end_text_surface = font.render(end_text, True, (255,255,255))
    end_text_rect = end_text_surface.get_rect()
    end_text_rect.center = (1280 // 2, 720 // 2)
    screen.blit(end_text_surface, end_text_rect)

    # Update the display
    pygame.display.flip()

# Clean up
pygame.quit()
cap.release()
cv2.destroyAllWindows()
