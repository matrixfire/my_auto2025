import random
import pyinputplus as pyip 

def simulate_monty_hall(n_simulations):
    switch_wins = 0
    stay_wins = 0

    for _ in range(n_simulations):
        prize_door = random.randint(0, 2)
        initial_choice = random.randint(0, 2)

        remaining_doors = [d for d in range(3) if d != initial_choice and d != prize_door]
        door_opened_by_host = random.choice(remaining_doors)

        switch_choice = next(d for d in range(3) if d != initial_choice and d != door_opened_by_host)

        if initial_choice == prize_door:
            stay_wins += 1
        if switch_choice == prize_door:
            switch_wins += 1
    
    print(f"Simulating {n_simulations} times:")
    print(f"If you stay, you will win {stay_wins} times({(stay_wins / n_simulations) *100:.2f}%)")
    print(f"If you change, you will win {switch_wins} times({(switch_wins / n_simulations) *100:.2f}%)")
    return switch_wins, stay_wins

# simulate_monty_hall(10000)

def simulate_keep_baby_boy(famalies):
    girls = 0
    boys = 0
    for _ in range(famalies):
        if random.random() > 0.5:
            boys += 1
            print(f"Having a boy: {boys}")
        else:
            girls += 1
            print(f"Having a girl: {girls}")
            while True:
                if random.random() > 0.5:
                    boys += 1
                    print(f"Having a boy: {boys}")
                    break
                else:
                    girls += 1
                    print(f"Having a girl: {girls}")
    
    print(f"Simulating {famalies} famalies:")
    print(f"Girls: {girls} Boys: {boys}")
    print(f"Boys rate: {(boys / (girls + boys)) * 100:.2f}%")
    return girls, boys
                    

# simulate_keep_baby_boy(100)
    