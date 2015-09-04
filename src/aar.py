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


def remove_units(units, hits):
    # removal is infantry -> artillery -> tank -> plane?
    # TODO
    for i in range(0, hits):
        if units['i'] > 0:
            units['i'] -= 1
        elif units['a'] > 0:
            units['a'] -= 1
        elif units['t'] > 0:
            units['t'] -= 1
        elif units['p'] > 0:
            units['p'] -= 1
        else:
            # out of units, return
            return


def count_units(units):
    return sum(units.values())

class LandBattle:
    def __init__(self, attacker, defender):
        """
        `attacker` and `defender` are each pairs (<front line units>, <reserve units>)
        """
        self.attacker = attacker
        self.defender = defender
        self.display_player_units(True)
        self.display_player_units(False)

    def fight(self):
        if self.attacker[0]['a'] != 0:
            print("The attacker has an opening salvo with {} artillery.".format(self.attacker[0]['a']))
            roll = roll_attack_dice(self.attacker[0]['a'])
            num_hits = roll['a']
            print("Opening salvo hits: {}".format(num_hits))

            if num_hits > 0:
                remove_units(self.defender[0], num_hits)
                # TODO: prompt defender to reinforce

    def display_player_units(self, is_attacker):
        if is_attacker:
            player = self.attacker
        else:
            player = self.defender

        print()
        print("Front line: {}".format(display_frontline(player[0])))
        print("Reserve: {}".format(display_units(player[1])))


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
    for i in range(1, count_units(units) + 1):
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

        if inp not in "iatp":
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

attacker = prompt_player_units(True)
defender = prompt_player_units(False)

battle = LandBattle(attacker, defender)
