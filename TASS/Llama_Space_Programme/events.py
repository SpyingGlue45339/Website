import random
import global_variables


# Checks whether an event should happen.
# This is called by Phase 3 after every turn.
def should_trigger_event(round_number):

    if round_number % 5 == 0:

        random_number = random.randint(1, 100)

        if random_number <= 30:
            return True

    return False


def item_is_owned(item_name):
    """Check the shared inventory, accepting both lists and plain strings."""

    wanted_name = str(item_name).strip().casefold()

    for item in getattr(global_variables, "inventory", []):

        if isinstance(item, (list, tuple)) and len(item) > 0:
            owned_name = str(item[0]).strip().casefold()

        elif isinstance(item, str):
            owned_name = item.strip().casefold()

        else:
            continue

        if owned_name == wanted_name:
            return True

    return False


def get_personal_power_capacity():
    """Return the same power capacity used by Phase 3."""

    capacity = 100

    if item_is_owned("Backup battery"):
        capacity = capacity + 100

    return capacity


# Runs a random event and applies its effects.
# The updated resources and popup information are returned to Phase 3.
# base_positions is optional so older calls using the original six arguments
# continue to work. Phase 3 supplies the positions of all currently built bases.
def run_random_event(
    money,
    energy,
    power,
    oxygen,
    water,
    base_oxygen,
    base_positions=None
):

    # Pick a random event.
    # Dysentery appears several times to make it more likely to occur.
    numb = random.randint(1, 46)

    # These variables will contain the popup information.
    event_title = ""
    event_description = ""
    event_subtitle = ""
    deathmessage = None

    # Llama dysentry
    if numb == 1 or numb == 32 or numb == 33 or numb == 34:

        event_title = "Llama dysentry"
        event_description = "'Sometimes, when you've gotta go, you've gotta go' - Bear in the Big Blue House"

        medical_kit_found = False
        inventory = getattr(global_variables, "inventory", [])

        for item in list(inventory):

            if isinstance(item, (list, tuple)) and len(item) > 0:
                item_name = str(item[0]).strip().casefold()
            elif isinstance(item, str):
                item_name = item.strip().casefold()
            else:
                continue

            if item_name == "emergency medical kit":
                inventory.remove(item)
                medical_kit_found = True
                break

        if medical_kit_found:

            event_subtitle = "Emergency medical kit consumed"

        else:

            energy = energy - 30
            event_subtitle = "Energy decreased"

        if energy <= 0:
            deathmessage = "poop"

    # Llamageddon
    elif numb == 2:

        event_title = "LLAMAGEDDON"
        event_description = "LLAMAGEDDON! An asteroid hits your base. You wander through the Martian wilderness for days on end, before breathing your last breathe as you wish you'd have invested in your cousin's piano repair business..."
        event_subtitle = "Base destroyed"
        deathmessage = "oxygen run out"

    # Professor Reginald Panda
    elif numb == 3 or numb == 35 or numb == 36 or numb == 37:

        event_title = "Professor Reginald Panda"
        event_description = "As you wander across the landscapes, you see a familiar face... Professor Reginald Panda! His paper on thermozootropolopics destroyed your previously seminal work on bear mating strategies. He laughs at your useless operation and you feel demoralised."

        energy = energy - 50
        event_subtitle = "Energy decreased"

        if energy <= 0:
            deathmessage = "humiliation"

    # Hackathon time
    elif numb == 4:

        event_title = "Hackathon time!"
        event_description = "Hackathon time! You hack into Starlink, and join your buddies at the free event in making your new OnlyFox clone. Unfortunately, this drains your power..."

        power = power - 50

        if power < 0:
            power = 0

        event_subtitle = "Power decreased"

    # Electrical failure
    elif numb == 5:

        event_title = "Electrical failure"
        event_description = "Your electrical systems suddenly begin making a rather unpleasant buzzing noise. You rush over to investigate and discover that something has gone horribly wrong. Fortunately, there is a small chance that the malfunction has somehow improved your electrical efficiency. Probably best not to ask how."

        electrical_random_number = random.randint(1, 100)

        if electrical_random_number <= 10:

            power = power + 20
            event_subtitle = "Power increased"

        else:

            power = power - 20

            if power < 0:
                power = 0

            event_subtitle = "Power decreased"

    # Tully Monster
    elif numb == 6:

        event_title = "The Tully Monster"
        event_description = "The Tully Monster you hired to wire your electrics plugged seven things into one surge protector."

        base_oxygen = 0
        event_subtitle = "Base oxygen storage emptied"

    # Steven the Sloth
    elif numb == 7:

        event_title = "Steven the Sloth"
        event_description = "You discover something hiding in your cargo hold... it's Steven the Sloth! You pay the fine to deport him."

        money = money * 0.8
        event_subtitle = "Money decreased"

    # Alien peace treaty
    elif numb == 8:

        event_title = "Intergalactic diplomacy"
        event_description = "Alien species have entered your solar system. They have discovered you first, and see you as a representative. You sign their peace treaty, securing llama supremacy from Slough to the nearest supernova!"

        event_subtitle = "No change"

    # Astrology budget cuts
    elif numb == 9:

        event_title = "Budget cuts"
        event_description = "Conservative Governments have cut the astrology budget and you find your funding drying up!"

        money = money * 0.9
        event_subtitle = "Money decreased"

    # University recognition
    elif numb == 10:

        event_title = "Academic recognition"
        event_description = "Such is the success of your mission, the head of the racial justice department at your University claims credit for your enterprise and innovation!"

        money = money * 1.1
        event_subtitle = "Money increased"

    # Radioactive carrot
    elif numb == 11:

        event_title = "The radioactive carrot"
        event_description = "Somehow, you find a carrot growing. Unfortunately, it has grown horizontally and is transmitting radio signals. You decide to take a bite regardless."

        energy = energy * 0.5
        event_subtitle = "Energy decreased"

    # Forgotten hay
    elif numb == 12:

        event_title = "A serious oversight"
        event_description = "Despite the success of your mission and your spiffing planning, you forgot to bring hay. You deduce the insulation is a suitable alternative..."

        energy = 10
        event_subtitle = "Energy critically decreased"

    # Cosmic Ray Lottery
    elif numb == 13 or numb == 38:

        event_title = "Cosmic Ray Lottery"
        event_description = "Cosmic Ray Lottery - somehow a bit on your computer has been flipped. Your oxygen metre now says BANANA. You ponder this insight..."

        event_subtitle = "No change"

    # Inguanagram influencer
    elif numb == 14:

        event_title = "Inguanagram fame"
        event_description = "An Iguanagram influencer likes your base. She critisizes the lighting, but sends you a canister of oxygen via Royal Mail."

        oxygen = oxygen + 10
        event_subtitle = "Oxygen increased"

    # Another llama
    elif numb == 15:

        event_title = "Another llama?"
        event_description = "You look to your scanners. There appears to be a...nother llama?!?! You take a rest."

        energy = energy + 10
        event_subtitle = "Energy increased"

    # The smiling moon
    elif numb == 16:

        event_title = "The smiling moon"
        event_description = "Your readings suggest the moon has a... face? It smiles at you."

        energy = energy + 10
        event_subtitle = "Energy increased"

    # The cockroach
    elif numb == 17:

        event_title = "A most helpful cockroach"
        event_description = "You consult a random homeless cockroack and he tells you the coordinates of where to dig. You strike it rich!"

        money = money + 10000
        event_subtitle = "Money increased"

    # Copyright claim
    elif numb == 18:

        event_title = "Copyright infringement"
        event_description = "Your onboard music has been copyright claimed by HollywoodLouse Pictures. Try double checking with your lawyer Bartholomew Blobfish next time..."

        money = money - 1000
        energy = energy * 0.9
        event_subtitle = "Money and energy decreased"

    # Existential crisis
    elif numb == 19:

        event_title = "An existential crisis"
        event_description = "After listenning to fellow master debater Badger Shapino, you question the purpose of this mission. What is the meaning of life anyway? Pineapples? The Government? Why did they send those dogs into space and did they come back???"

        if energy < 20:
            energy = 0
        else:
            energy = energy - 20

        event_subtitle = "Energy decreased"

    # The goat
    elif numb == 20:

        event_title = "The goat"
        event_description = "You find a goat."

        event_subtitle = "No change"

    # Forgotten oxygen canister
    elif numb == 21:

        event_title = "A pleasant surprise"
        event_description = "You remember when you left that oxygen canister! Result!"

        oxygen = oxygen + 10
        event_subtitle = "Oxygen increased"

    # Martian establishment
    elif numb == 22:

        event_title = "A night out on Mars"
        event_description = "Embracing the local Martian culture, you take a trip into one of those Martian establishments the locals praise so much. It gets so lonely out here..."

        oxygen = oxygen * 0.7
        energy = 100
        event_subtitle = "Oxygen decreased, energy increased"

    # Aunt Marge
    elif numb == 23:

        event_title = "A familiar rock"
        event_description = "You find a rock that looks suspiciously like your Aunt Marge. She was a fine woman..."

        event_subtitle = "No change"

    # Martian tourist
    elif numb == 24:

        event_title = "An unhappy tourist"
        event_description = "A female Martian tourist complains that your base is ruining the view. You are fined £50."

        money = money - 50
        event_subtitle = "Money decreased"

    # The pit
    elif numb == 25:

        event_title = "One small step for Llama"
        event_description = "One small step for Llama, you tell yourself. You tumble into the pit. It is short enough to climb out, but you question if your ego will ever recover. At least the pit gave you five star reviews..."

        event_subtitle = "No change"

    # Alien salesman
    elif numb == 26:

        event_title = "A questionable business opportunity"
        event_description = "A small alien comes up to youand offers to sell you a revolutionary new water filtration system. It promises to remove 99.9 percent of impurities, improve your life expectancy, and make your teeth considerably whiter. You politely decline. The alien looks offended and asks whether you would at least like to hear about its extended warranty."

        event_subtitle = "No change"

    # The sad rock
    elif numb == 27:

        event_title = "The sad rock"
        event_description = "That rock nearby looks so sad. It's not his fault. You empty your water onto it, and recommend your therapist. IBS can be tough."

        water = water * 0.5
        event_subtitle = "Water decreased"

    # Ethan Elephant
    elif numb == 28:

        event_title = "Ethan Elephant"
        event_description = "You consult a geologist friend, Ethan Elephant. Despite his name, he is a very slender man. You can't stop laughing that he spent his entire time looking at rocks and he leaves."

        event_subtitle = "No change"

    # Martian gold
    elif numb == 29:

        event_title = "A very profitable discovery"
        event_description = "As you scroll Inguanagram Reels, you find gold beneath your feet! You're pretty sure it's just that rock you weed on, but the cantankerous crab you're selling to on eBay probably won't care, right?"

        money = money + 50000
        event_subtitle = "Money increased"

    # GoldMouse Sachs
    elif numb == 30:

        event_title = "Financial consultancy"
        event_description = "To boost your fortunes, you hire a consultant from GoldMouse Sachs. They just don't provide the value you're after, and you cancel your subscription eleven seconds before the free trial ends."

        event_subtitle = "No change"

    # Official fax
    elif numb == 31:

        event_title = "An official communication"
        event_description = "The Chief Executive from the Artiodactyla Space and Cosmic Expansion Management Agency of Zambia sends an official fax. He says HEEEEEEEEEEEEEEEEEEEEEEEE"

        event_subtitle = "No change"

    # Poland?
    elif numb == 39:

        event_title = "Poland?"
        event_description = "Your To-Do list for today says Polish Spacesuit. But why is the Spacesuit from Poland?"

        event_subtitle = "No change"

    # New Hope?
    elif numb == 40:

        event_title = "New Hope?"
        event_description = "Emperor Pawpatine has enacted Order 67 Across the Stars. Lord Vulture begins to track down and kill all remaining llamas, including Herbert. You hope he doesn't come across you..."

        event_subtitle = "No effect"

    # Farafish's Law
    elif numb == 41:

        event_title = "Farafish's Law"
        event_description = "Your experiments with electromagnetism finally pay off! That ray-finned fish you locked in a jar seventeen years ago lit up spontaneously and you harvest the power."

        power = get_personal_power_capacity()
        event_subtitle = "Power restored to full"

    # Fishing Fun
    elif numb == 42:

        event_title = "Fishing Fun"
        event_description = "You go fish for... quantum? You rethink the idea entirely, and wish you would have studied anteaters instead. They're clearly the future."

        event_subtitle = "No effect"

    # Sahara Prime
    elif numb == 43:

        event_title = "Sahara Prime"
        event_description = "After someone thought the wires would taste like peanut butter, you have to pay for Sahara Prime for a month to get faster delivery"

        money = money - 100
        event_subtitle = "Money decreased"

    # monkey mayhem
    elif numb == 44:

        event_title = "monkey mayhem"
        event_description = "Some goshdarned black-crowned central american squirrel monkey has launched a hack-attack on your base! How dare organisations promote hacking. One of your bases is disabled for five turns."

        available_base_positions = []

        if base_positions is not None:
            for position in base_positions:
                if isinstance(position, (list, tuple)) and len(position) == 2:
                    available_base_positions.append((position[0], position[1]))

        if available_base_positions:
            disabled_position = random.choice(available_base_positions)
        else:
            disabled_position = None

        # Phase 3 reads these shared values and temporarily prevents the
        # player from using the affected base's storage and refill services.
        global_variables.disabled_base_position = disabled_position
        global_variables.disabled_base_turns = 5

        event_subtitle = "Base benefits disabled for five turns"

        if disabled_position is not None:
            try:
                disabled_base_number = available_base_positions.index(disabled_position) + 1
                event_subtitle = (
                    "Base " + str(disabled_base_number)
                    + " benefits disabled for five turns"
                )
            except ValueError:
                pass

    # Methane
    elif numb == 45:

        event_title = "Methane"
        event_description = "You can barely breathe. All you can hear is your own raspy, spluttering gasps. The stench is suffocating. You knew that curry last night was a mistake, but in a much greater and more meaningful sense how could you have known? Who could have foreseen the flatulence that has unfolded. Did you buy a filtration system? You can't remember. If you didn't then the only possible solution is to open your helmet and embrace the cool Martian breeze"

        if item_is_owned("Air filtration system"):
            event_subtitle = "Air filtration system prevented oxygen loss"
        else:
            oxygen = oxygen - 40
            event_subtitle = "Oxygen decreased"

    # Cracked Calcs
    elif numb == 46:

        event_title = "Cracked Calcs"
        event_description = "That drug dealer assured you he was arriving relativistically. Thinking back to the lectures of Christine Dog, what did you really learn about relativity? Cats somehow dominate your memory."

        energy = energy - 5
        event_subtitle = "Energy decreased"

    # Return everything to Phase 3.
    return (
        money,
        energy,
        power,
        oxygen,
        water,
        base_oxygen,
        event_title,
        event_description,
        event_subtitle,
        deathmessage
    )