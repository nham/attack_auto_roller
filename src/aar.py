import random

def roll_attack_die():
    roll = random.randint(1, 6)
    if roll == 1:
        return 'i'
    elif roll == 2:
        return 'a'
    elif roll == 3:
        return 't'
    elif roll == 4:
        return 'p'
    elif roll == 5:
        return 'p'
    else:
        return None

def roll_attack_dice(n):
    hits = {'i': 0, 'a': 0, 't': 0, 'p': 0}
    for i in range(0, n):
        roll = roll_attack_die()
        if roll is not None:
            hits[roll] += 1

    return hits

def num_dice_for_units(units):
    return count_units(units) + units['t']

def number_of_hits(units, roll):
    hits = 0
    for u in "iatp":
        hits += min(units[u], roll[u])
    return hits



def remove_units(units, hits):
    lost = {'i': 0, 'a': 0, 't': 0, 'p': 0}
    for i in range(0, hits):
        if units['i'] > 0:
            units['i'] -= 1
            lost['i'] += 1
        elif units['a'] > 0:
            units['a'] -= 1
            lost['a'] += 1
        elif units['t'] > 0:
            units['t'] -= 1
            lost['t'] += 1
        elif units['p'] > 0:
            units['p'] -= 1
            lost['p'] += 1
        else:
            # out of units, return
            return lost
    return lost

def count_units(units):
    return sum(units.values())

def prompt_player_units(is_attacker):
    print()
    if is_attacker:
        print("Attacker")
    else:
        print("Defender")

    print("==================")
    i = prompt_for_number("# of infantry:  ")
    a = prompt_for_number("# of artillery: ")
    t = prompt_for_number("# of tanks:     ")
    p = prompt_for_number("# of planes:    ")

    units = {'i': i, 'a': a, 't': t, 'p': p}

    print()
    front_line = {'i': 0, 'a': 0, 't': 0, 'p': 0}
    if count_units(units) <= 4:
        units, front_line = front_line, units
    else:
        for i in range(1, 5):
            u = prompt_for_unit("Specify front line unit {}: ".format(i), units)
            front_line[u] += 1

    return (front_line, units)

def prompt_for_number(msg):
    while True:
        inp = input(msg)
        try:
            i = int(inp)
            return i
        except ValueError as e:
            print("Error, must enter a number")


def prompt_for_unit(msg, available_units):
    while True:
        inp = input(msg).lower()

        if inp not in "iatp" or inp == '':
            print("\nError, must enter one of 'i', 'a', 't', or 'p'\n")
            continue

        if available_units[inp] == 0:
            print("\nError, no {} units available, pick another.".format(abbrev_to_word(inp)))
            print("Available units: {}\n".format(display_units(available_units)))
            continue
        else:
            available_units[inp] -= 1
            return inp

def abbrev_to_word(abbr):
    if abbr == 'i':
        return "infantry"
    elif abbr == 'a':
        return "artillery"
    elif abbr == 't':
        return "tank"
    elif abbr == 'p':
        return "plane"


def display_units(units):
    x = ""
    x_is_empty = True
    if units['i'] != 0:
        x += "I x {}".format(units['i'])
        x_is_empty = False

    if units['a'] != 0:
        if not x_is_empty:
            x += ",  "
        else:
            x_is_empty = False

        x += "A x {}".format(units['a'])

    if units['t'] != 0:
        if not x_is_empty:
            x += ",  "
        else:
            x_is_empty = False

        x += "T x {}".format(units['t'])

    if units['p'] != 0:
        if not x_is_empty:
            x += ",  "
        else:
            x_is_empty = False

        x += "P x {}".format(units['p'])

    return x.strip()

def display_frontline(units):
    display_str = ""
    for i in range(0, units['i']):
        display_str += " I"
    for i in range(0, units['a']):
        display_str += " A"
    for i in range(0, units['t']):
        display_str += " T"
    for i in range(0, units['p']):
        display_str += " P"
    return display_str


class LandBattle:
    def __init__(self, attacker, defender):
        """
        `attacker` and `defender` are each pairs (<front line units>, <reserve units>)
        """
        self.attacker = ("Attacker", attacker[0], attacker[1])
        self.defender = ("Defender", defender[0], defender[1])
        self.turn = 0


    def fight(self):
        print("\n\n********** {} **********".format("Beginning battle"))

        attacker_num_artillery = self.attacker[1]['a']
        if attacker_num_artillery != 0:
            print("\n\n********** {} **********".format("Opening salvo"))
            self.display_both_player_units()
            print("The attacker has an opening salvo with {} artillery.".format(attacker_num_artillery))
            roll = roll_attack_dice(attacker_num_artillery)
            num_hits = roll['a']
            print("Opening salvo hits: {}".format(num_hits))

            if num_hits > 0:
                lost = remove_units(self.defender[1], num_hits)
                print("Defender loses units: {}".format(display_frontline(lost)))
                self.prompt_player_reinforce(self.defender)

        # potential salvo is finished, we're ready for first turn of rolling
        self.turn = 1

        self.player_roll_reinforce(self.defender, self.attacker)
        self.player_roll_reinforce(self.attacker, self.defender)


    def player_roll_reinforce(self, player, other_player):
        print("\n\n********** Turn {}, {} rolling **********".format(self.turn, player[0]))
        self.display_both_player_units()

        num_dice = num_dice_for_units(player[1])
        roll = roll_attack_dice(num_dice)
        num_hits = number_of_hits(player[1], roll)
        print("{} rolls {} dice, rolls {} ({} hit{})".format(
              player[0],
              num_dice,
              display_frontline(roll),
              num_hits,
              "" if num_hits == 1 else "s"))

        if num_hits > 0:
            lost = remove_units(other_player[1], num_hits)
            print("{} loses units: {}".format(other_player[0], display_frontline(lost)))
            self.prompt_player_reinforce(other_player)


    def display_both_player_units(self):
        self.display_player_units(self.attacker)
        self.display_player_units(self.defender)
        print()

    def display_player_units(self, player):
        print("\n{}".format(player[0]))
        print("==================")
        print("Front line: {}".format(display_frontline(player[1])))
        print("Reserve: {}".format(display_units(player[2])))


    def prompt_player_reinforce(self, player):
        if count_units(player[2]) == 0:
            print("\n{} cannot reinforce, no units in reserve.".format(player[0]))
            return

        print("\n{} needs to reinforce.".format(player[0]))
        print("Front line: {}".format(display_frontline(player[1])))
        print("Reserve: {}".format(display_units(player[2])))

        num_in_front = count_units(player[1])
        max_for_round = front_line_size_per_round(self.turn)
        num_in_reserve = count_units(player[2])
        num_missing = max_for_round - num_in_front

        if num_in_reserve <= num_missing:
            for u in "iatp":
                player[1][u] += player[2][u]
                player[2][u] = 0
            print("Automatically reinforced with remaining units.")
        else:
            for i in range(1, num_missing + 1):
                u = prompt_for_unit("Specify front line unit {}: ".format(num_in_front+i), player[2])
                player[1][u] += 1


def front_line_size_per_round(r):
    if r== 0 or r== 1:
        return 4
    else:
        return round + 3

attacker = prompt_player_units(True)
defender = prompt_player_units(False)

battle = LandBattle(attacker, defender)
battle.fight()
