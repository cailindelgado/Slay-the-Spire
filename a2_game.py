from a2_support import *

class Card(object):
    def __init__(self) -> None:
        self.damage = 0
        self.block = 0
        self.energy_cost = 1
        self.status_modifiers = dict()
        self.card_name = "Card"
        self.card_description = "A card."

    def get_damage_amount(self) -> int:
        return self.damage

    def get_block(self) -> int:
        return self.block

    def get_energy_cost(self) -> int:
        return self.energy_cost

    def get_status_modifiers(self) -> dict[str, int]:
        return self.status_modifiers

    def get_name(self) -> str:
        return type(self).__name__

    def get_description(self) -> str:
        return self.card_description

    def requires_target(self) -> bool:
        return not (self.card_name == "Survivor" or self.card_name == "Defend" or self.card_name == "Vigilance")

    def __str__(self) -> str:
        return f"{self.card_name}: {self.card_description}"

    def __repr__(self) -> str:
        return f"{type(self).__name__}()"

class Strike(Card):
    def __init__(self) -> None:
        super().__init__()
        self.card_name = "Strike"
        self.card_description = "Deal 6 damage. Costs 1 energy."
        self.damage = 6

class Defend(Card):
    def __init__(self) -> None:
        super().__init__()
        self.card_name = "Defend"
        self.card_description = "Gain 5 block. Costs 1 energy."
        self.block = 5

class Bash(Card):
    def __init__(self) -> None:
        super().__init__()
        self.card_name = "Bash"
        self.card_description = "Deal 7 damage. Gain 5 block. Costs 2 energy."
        self.damage = 7
        self.block = 5
        self.energy_cost = 2
        
class Neutralize(Card):
    def __init__(self) -> None:
        super().__init__()
        self.card_name = "Neutralize"
        self.card_description = str("Deal 3 damage. Apply 1 weak. Apply 2 vulnerable. Costs 0 energy")
        self.damage = 3
        self.energy_cost = 0
        self.status_modifiers["weak"] = 1
        self.status_modifiers["vulnerable"] = 2

class Survivor(Card):
    def __init__(self) -> None:
        super().__init__()
        self.card_name = "Survivor"
        self.card_description = "Gain 8 block and 1 strength. Costs 1 energy."
        self.block = 8
        self.status_modifiers["strength"] = 1

class Eruption(Card):
    def __init__(self) -> None:
        super().__init__()
        self.card_name = "Eruption"
        self.card_description = "Deal 9 damage. Costs 2 energy."
        self.energy_cost = 2
        self.damage = 9

class Vigilance(Card):
    def __init__(self) -> None:
        super().__init__()
        self.card_name = "Vigilance"
        self.card_description = "Gain 8 block. Gain 1 strength. Costs 0 energy."
        self.block = 8
        self.status_modifiers["strength"] = 1
        self.energy_cost = 0

class Entity(object):
    def __init__(self, max_hp: int) -> None:
        self.name = "Entity"
        self.max_hp = max_hp
        self.hp = max_hp
        self.block = 0
        self.status_modifiers = {
            "strength": 0,
            "weak": 0,
            "vulnerable": 0
        }

    def get_hp(self) -> int:
        return self.hp

    def get_max_hp(self) -> int:
        return self.max_hp

    def get_block(self) -> int:
        return self.block

    def get_strength(self) -> int:
        return self.status_modifiers.get("strength")

    def get_weak(self) -> int:
        return self.status_modifiers.get("weak")

    def get_vulnerable(self) -> int:
        return self.status_modifiers.get("vulnerable")

    def get_name(self) -> int:
        return type(self).__name__

    def reduce_hp(self, amount: int) -> None:
        if self.block <= amount:
            amount -= self.block
            self.block = 0
        elif self.block >= amount: 
            self.block -= amount
            amount = 0

        self.hp -= amount

        if self.hp <= 0:
            self.hp = 0

    def is_defeated(self) -> bool:
        if self.hp == 0:
            return True
        
        return False

    def add_block(self, amount: int) -> None:
        self.block += amount

    def add_strength(self, amount: int) -> None:
        self.status_modifiers["strength"] += amount

    def add_weak(self, amount: int) -> None:
        self.status_modifiers["weak"] += amount

    def add_vulnerable(self, amount: int) -> None:
        self.status_modifiers["vulnerable"] += amount

    def new_turn(self) -> None:
        self.block = 0
        if self.status_modifiers["weak"] > 0:
            self.status_modifiers["weak"] -= 1
        if self.status_modifiers["vulnerable"] > 0:
            self.status_modifiers["vulnerable"] -= 1

    def __str__(self) -> str:
        return f"{self.get_name()}: {self.hp}/{self.get_max_hp()} HP"
    
    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.max_hp})" 

class Player(Entity):
    def __init__(self, max_hp: int, cards: list[Card] | None = None) -> None:
        super().__init__(max_hp)
        self.player_energy = 3
        self.card_deck = cards
        self.card_hand = []
        self.discarded_pile = []
        self.name = "Player"
        self.player_turn = False

    def get_energy(self) -> int:
        return self.player_energy

    def get_hand(self) -> list[Card]:
        return self.card_hand

    def get_deck(self) -> list[Card]:
        return self.card_deck

    def get_discarded(self) -> list[Card]:
        return self.discarded_pile

    def start_new_encounter(self) -> None:
        for idx in range(len(self.discarded_pile)):
            self.card_deck.append(self.discarded_pile[idx])
        self.discarded_pile.clear()

    def end_turn(self) -> None:
        for card in range(len(self.card_hand)):
            self.discarded_pile.append(self.card_hand[card])

        self.card_hand.clear()
        self.player_turn = False 

    def new_turn(self) -> None:
        self.block = 0
        self.player_energy = 3
        draw_cards(self.card_deck, self.card_hand, self.discarded_pile)
        self.player_turn = True

        if self.status_modifiers["weak"] > 0:
            self.status_modifiers["weak"] -= 1
        if self.status_modifiers["vulnerable"] > 0:
            self.status_modifiers["vulnerable"] -= 1

    def play_card(self, card_name: str) -> Card | None: 
        card_name = card_setter(card_name)

        for card in self.card_hand:
            if type(card_name).__name__ == type(card).__name__ and self.player_energy >= card_name.get_energy_cost():
                self.card_hand.remove(card)
                self.discarded_pile.append(card)
                self.player_energy -= card_name.get_energy_cost()
                
                return card

    def __repr__(self) -> str:
        if self.card_deck != []:
            return f"{type(self).__name__}({self.max_hp}, {self.card_deck})"
        elif self.card_deck == []:
            return f"{type(self).__name__}()" 

class IronClad(Player):
    def __init__(self) -> None:
        super().__init__(max_hp=80)
        self.card_deck = [
            Strike(), Strike(), Strike(), Strike(), Strike(), 
            Defend(), Defend(), Defend(), Defend(), 
            Bash()
            ]
        self.name = "IronClad"

    def __repr__(self) -> str:
        return f"{type(self).__name__}()"

class Silent(Player):
    def __init__(self) -> None:
        super().__init__(max_hp=70)
        self.card_deck = [
            Strike(), Strike(), Strike(), Strike(), Strike(), 
            Defend(), Defend(), Defend(), Defend(), Defend(), 
            Neutralize(), 
            Survivor()
            ]
        self.name = "Silent"

    def __repr__(self) -> str:
        return f"{type(self).__name__}()"

class Watcher(Player):
    def __init__(self) -> None:
        super().__init__(max_hp = 72)
        self.name = "Watcher"
        self.card_deck = [
            Strike(), Strike(), Strike(), Strike(),
            Defend(), Defend(), Defend(), Defend(),
            Eruption(), 
            Vigilance()
        ]
    
    def __repr__(self) -> str:
        return f"{type(self).__name__}()"
        
class Monster(Entity):
    mon_id = -1

    def __init__(self, max_hp: int) -> None:
        super().__init__(max_hp=max_hp)
        #increases the id every time the monster entity is called (0,1,2,3...)
        Monster.mon_id += 1
        self.monster_name = self.name = "Monster"
        self.new_mon_id = Monster.mon_id

    def get_id(self) -> int:
        return self.new_mon_id

    def action(self) -> dict[str, int]:
        raise NotImplementedError

class Louse(Monster):
    def __init__(self, max_hp: int) -> None:
        super().__init__(max_hp)
        self.damage = random_louse_amount()
        self.name = "Louse"

    def action(self) -> dict[str, int]:
        return {"damage": self.damage}

class Cultist(Monster):
    def __init__(self, max_hp: int) -> None:
        super().__init__(max_hp)
        self.damage_amount = 0
        self.name = "Cultist"
        self.weak_amount = 0
        self.num_actions= -1


    def action(self) -> dict[str, int]:
        self.num_actions += 1
        if not (self.damage_amount == 0 and self.num_actions == 0):
            self.damage_amount = 6 + self.num_actions
        
        if self.num_actions % 2 != 0:
            self.weak_amount = 1
        else:
            self.weak_amount = 0
        return {"damage": self.damage_amount, "weak": self.weak_amount}

class JawWorm(Monster):
    def __init__(self, max_hp: int) -> None:
        super().__init__(max_hp)
        self.damage_taken = 0
        self.block = 0
        self.damage = 0
        self.monster_name = "Jaw Worm"

    action_counter = 0
    
    def action(self) -> dict[str, int]:
        self.damage_taken = Entity.get_max_hp(self) - Entity.get_hp(self)
        
        self.damage = self.damage_taken // 2
        self.block = self.damage_taken - self.damage 

        return {'damage': self.damage}

class Encounter(object):
    def __init__(
            self, player: Player, monsters: list[tuple[str, int]]) -> None:
        self.player = player
        self.monsters_cp = monsters.copy()

        for idx, monster in enumerate(self.monsters_cp):  
            monsters.pop(idx)
            
            if monster[0] == "Louse":
                monster_info = Louse(monster[1])
            elif monster[0] == "Cultist":
                monster_info = Cultist(monster[1])
            elif monster[0] == "JawWorm":
                monster_info = JawWorm(monster[1])

            monsters.insert(idx, monster_info)
        
        self.monsters = monsters

        self.player.start_new_encounter()
        self.player.new_turn()
    
    def start_new_turn(self) -> None:
        self.player.new_turn()

    def end_player_turn(self) -> None:
        self.player.end_turn()
        for monster in self.monsters:
            Monster.new_turn(monster)

    def get_player(self) -> Player:
        return self.player
    
    def get_monsters(self) -> list[Monster]:
        return self.monsters

    def is_active(self) -> bool:
        if self.get_monsters() != []:
            return True
        
        return False

    def player_apply_card(self, card_name: str, target_id: int | None = None) -> bool:
        selected_card = card_setter(card_name)

        # part 1. checks if it is players turn, if no target for card was 
        # given, and if the target exists in current encounter.
        check_monsters = False 
        for monster in self.monsters:
                if target_id == monster.get_id():
                    check_monsters = True 
                
        if self.player.player_turn == False and check_monsters == False:
            return False
        
        if target_id != None and self.monsters[-1].get_id() < target_id:
            return False
        
        # part 2. Check if card is in players hand, if player has sufficient 
        # energy to use card and if card_name exists within available cards
        check_hand = False
        for card in self.player.get_hand(): 
            if card.get_name() == card_name:
                check_hand = True
                break
        
        if check_hand == False:
            return False
        
        if selected_card.requires_target() == True and target_id == None:
            return False

        if selected_card.get_energy_cost() > self.player.get_energy():
            return False 
        
        if not (card_name != 'Strike' or card_name != 'Defend' or card_name != 'Bash' or card_name != 'Neutralize' or card_name != 'Survivor' or card_name != "Vigilance" or card_name != "Eruption"):
            return False 
        
        self.player.play_card(card_name)
        
        # part 3. Add any block or strength to the uesr 
        try:
            self.player.add_strength(
                selected_card.get_status_modifiers().get("strength"))
        except TypeError:
            pass
        
        try:
            self.player.add_block(selected_card.get_block())
        except TypeError:
            pass

        # part 4. If a target was specified add card effects to target
        if target_id == None and selected_card.requires_target() == True:
            return False 
        
        for monster in self.monsters: # apply stat modifiers
            if monster.get_id() == target_id:
                try:
                    monster.add_vulnerable(selected_card.get_status_modifiers().get("vulnerable"))
                except TypeError:
                    pass

                try:
                    monster.add_weak(selected_card.get_status_modifiers().get("weak"))
                except TypeError:
                    pass

        damage = selected_card.get_damage_amount()

        damage += self.player.get_strength()

        if self.player.get_weak() > 0:
            damage = int((damage * 0.75) // 1)

        for monster in self.monsters:
            if monster.get_id() == target_id and monster.get_vulnerable():
                damage = int((damage * 1.5) // 1 )

        for monster in self.monsters: 
            if monster.get_id() == target_id:
                monster.reduce_hp(damage)

            if monster.get_hp() <= 0:
                self.monsters.remove(monster)

        # part 5. Return true to indicate successful execution.
        return True

    def enemy_turn(self) -> None: 
        if self.player.player_turn == True:
            return False
        
        for monster in self.monsters:
            
            #monster attempts action
            monster_effects = monster.action()

            # monster stat modifiers are applied to player.
            # iterate through the monster effects, if effect is vulnerable do
            # the coresponding thing else move on
            for effect_name, amount in monster_effects.items():
                if effect_name == 'vulnerable' and amount > 0:
                    #weak is applied to player
                    self.player.add_vulnerable(amount)
                elif effect_name == 'weak' and amount > 0:
                    #weak is applied to player
                    self.player.add_weak(amount)
                elif effect_name == 'strength' and amount > 0: 
                    #strength is added to monster
                    monster.add_strength(amount)
            
            # damage is calculated
            damage = monster_effects.get("damage")

            damage += monster.get_strength()

            if monster.get_weak() > 0:
                damage = int((damage * 0.75) // 1)

            self.player.reduce_hp(damage)

        self.start_new_turn()

        return True          

def card_setter(card_name: str) -> Card:
    if card_name.lower() == "strike":
        card_name = Strike()
    elif card_name.lower() == "defend":
        card_name = Defend()
    elif card_name.lower() == "bash":
        card_name = Bash()
    elif card_name.lower() == "neutralize":
        card_name = Neutralize()
    elif card_name.lower() == "survivor":
        card_name = Survivor()
    elif card_name.lower() == "eruption":
        card_name = Eruption()
    elif card_name.lower() == "vigilance":
        card_name = Vigilance()
    
    return card_name

def selected_silence():
    print(Silent())

def selected_ironclad():
    print(IronClad())

def selected_watcher():
    print(Watcher())

def main():
    #ask user to see what type of player they want to play as    
    player_select = input("Enter a player type: ")
    
    if player_select.strip().lower() == "ironclad" or player_select[0].lower() == "i":
        player_select = IronClad()
    elif player_select.strip().lower() == "silent" or player_select[0].lower() == "s":
        player_select = Silent()
    elif player_select.strip().lower() == "watcher" or player_select[0].lower() == "w":
        player_select = Watcher()

    #prompt user for a game file
    game = input("Enter a game: ")

    if game == "1":
        game_info = read_game_file("games/game1.txt")
    elif game == "2":
        game_info = read_game_file("games/game2.txt")
    elif game == "3":
        game_info = read_game_file("games/game3.txt")

    #for each encounter in game file 
    for monsters in game_info:
        encounter = Encounter(player_select, monsters)

        print("New encounter!\n")

        while True:
            
            #end game if player dies/loses
            if encounter.get_player().get_hp() == 0:
                print(GAME_LOSE_MESSAGE)
                return 

            #disiplay the monsters in game file
            display_encounter(encounter)

            if encounter.get_monsters() == []:
                    print(ENCOUNTER_WIN_MESSAGE)
                    break

            while True:
                    
                move = input("Enter a move: ").strip().lower()
                
                move_bits = move.split(" ") #splits the play_card command

                if move == "end turn": #end player turn and begin enemy turn
                    encounter.end_player_turn()
                    encounter.enemy_turn()
                    break

                elif move == "inspect deck": #display card_deck
                    print(f"\n{encounter.get_player().get_deck()}\n")

                elif move == "inspect discard": #display card_discard pile
                    print(f"\n{encounter.get_player().get_discarded()}\n")

                elif move_bits[0].lower() == "describe":
                    print(f"\n{card_setter(move_bits[1].title()).get_description()}\n")

                elif len(move_bits) == 2: #for play cmd with no target_id
                    if encounter.player_apply_card(move_bits[1].title()) == False:
                        print(CARD_FAILURE_MESSAGE)
                        continue
                    break
                elif move_bits[0].lower() == "help" or move_bits[0][0] == "h":
                    print("\nMOVES ARE:\n 'inspect deck': shows cards in the deck\n 'inspect discard': shows the cards in your discard pile\n 'describe card_name': describes the card\n 'play card_name monster_id': plays the card if allowed to the monster with the matching id\n")
                
                elif len(move_bits) == 3: #for play cmd with target_id
                    if encounter.player_apply_card(move_bits[1].title(), int(move_bits[2])) == False:
                        print(CARD_FAILURE_MESSAGE)
                        continue         
                    break
        
         
    print(GAME_WIN_MESSAGE)    

if __name__ == '__main__':
    main()

