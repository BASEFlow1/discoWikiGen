import json
from pyperclip import copy
from os import getcwd
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('--html', action='store_true',help="Generate HTML instead of wikicode")
arguments = parser.parse_args()

def loadData(filename):
    with open(f"{getcwd()}\\{filename}", "r") as file:
        data = json.load(file)
    return data

classToWikiType = {
    "Light Fighter" : "L_FIGHTER",
    "Heavy Fighter" : "H_FIGHTER",
    "Very Heavy Fighter" : "VH_FIGHTER",
    "Super Heavy Fighter" : "SH_FIGHTER",
    "Bomber" : "BOMBER",
    "Gunship" : "GUNBOAT",
    "Gunboat" : "GUNBOAT",
    "Cruiser" : "CRUISER",
    "Battlecruiser" : "BATTLECRUISER",
    "Battleship" : "BATTLESHIP",
    "Dreadnought" : "DREADNOUGHT",
    "Carrier" : "CARRIER",
    "Freighter" : "FREIGHTER",
    "Liner" : "LINER",
    "Transport" : "TRANSPORT",
    "Destroyer" : "CRUISER",
    "Repair Ship" : "FREIGHTER",
    "Train" : "TRANSPORT",
    "Super Train" : "TRANSPORT",
    "Heavy Transport" : "TRANSPORT"
}



def main(template, data, config):
    houses = config["settings"]["houses"]
    if not arguments.html:
        if template.lower() == "ship":
            version = "{{Version|{version}}}\n"
            infobox = "{{Ship Infobox\n| name = {name}\n| image = {image}\n| nickname = {nickname}\n| shipclass = {class}\n| shipowner = {{House Link | {built_by}}}\n| shiptechcategory = {techcompat}\n| techmix = {techcompat}\n| guns = {gunCount}\n| turrets = {turretCount}\n| torpedoes = {torpedoCount}\n| mines = {mineCount}\n| CM = {cmCount}\n| hull = {hull}\n| cargo = {cargo}\n| maxregens = {regens}\n| optwepclass = {optwep}\n| maxwepclass = {maxwep}\n| maxshieldclass = {maxShield}\n| maxspeed = {impulse_speed}\n| maxturn = {turnRate}\n| maxthrust = {maxthrust}\n| maxpower = {power_output}\n| maxcruise = {maxCruise}\n| recharge = {power_recharge}\n| hullcost = {hull_price}\n| fullcost = {package_price}\n}}\n\n"
            infocard = "{infocard}\n\n"
            handling = "==Handling==\n{handling}\n"
            hardpoints = "==Hardpoints==\n{hardpoints}\n"
            includes = "==Purchase Includes==\n{{Spoiler|\n{includes}\n}}\n\n"
            availability = "==Availability==\n{| class=\"wikitable collapsible collapsed\"\n!Spoiler: Buying Locations\n|-\n|\n{| class=\"wikitable sortable\"\n|-\n!Base!!Owner!!System!!Location\n{sold_at}\n|}\n|}"
            category = "\n[[Category: {built_by}]]"
            while True:
                name = str(input("Enter ship name (as displayed in FLStat): "))
                try:
                    if data["Ships"][name]:
                        break
                except:
                    print("Ship name could not be found in database, retrying...")
            image = str(input("Enter image name (copy-paste from page source): "))
            if image == "":
                image = "li_fighter.png"
                print(f"No Image has been specified, defaulting to {image}")
            elif image.lower() == "nickname":
                image = f'{data["Ships"][name]["nickname"]}.png'
                print("Using Ship's nickname as image name.")

            version = version.replace("{version}", data["Version"])

            infobox = infobox.replace("{name}", data["Ships"][name]["longName"])
            infobox = infobox.replace("{image}", image)
            infobox = infobox.replace("{nickname}", data["Ships"][name]["nickname"])
            infobox = infobox.replace("{class}", classToWikiType[data["Ships"][name]["type"]])
            if data["Ships"][name]["built_by"] != "":
                infobox = infobox.replace("{built_by}", data["Ships"][name]["built_by"])
            else:
                built = str(input("Enter ship owner faction: "))
                infobox = infobox.replace("{{House Link | {built_by}}}", f"[[{built}]]")
            infobox = infobox.replace("{techcompat}", data["Ships"][name]["techcompat"])
            infobox = infobox.replace("{gunCount}", str(data["Ships"][name]["gunCount"]))
            infobox = infobox.replace("{turretCount}", str(data["Ships"][name]["turretCount"]))
            infobox = infobox.replace("{torpedoCount}", str(data["Ships"][name]["torpedoCount"])) if data["Ships"][name]["torpedoCount"] != 0 else infobox.replace("{torpedoCount}", "")
            infobox = infobox.replace("{mineCount}", str(data["Ships"][name]["mineCount"])) if data["Ships"][name]["mineCount"] != 0 else infobox.replace("{mineCount}", "")
            infobox = infobox.replace("{cmCount}", str(data["Ships"][name]["cmCount"])) if data["Ships"][name]["cmCount"] != 0 else infobox.replace("{cmCount}", "")
            infobox = infobox.replace("{maxthrust}", str(data["Ships"][name]["maxThrust"]))
            infobox = infobox.replace("{hull}", str(data["Ships"][name]["hit_pts"]))
            infobox = infobox.replace("{cargo}", str(data["Ships"][name]["hold_size"]))
            infobox = infobox.replace("{regens}", str(data["Ships"][name]["bat_limit"]))
            infobox = infobox.replace("{optwep}", str(data["Ships"][name]["maxClass"]))
            infobox = infobox.replace("{maxwep}", str(data["Ships"][name]["maxClass"]))
            infobox = infobox.replace("{maxShield}", str(data["Ships"][name]["maxShield"]))
            infobox = infobox.replace("{impulse_speed}", str(data["Ships"][name]["impulse_speed"]))
            infobox = infobox.replace("{turnRate}", str(data["Ships"][name]["turnRate"]))
            infobox = infobox.replace("{power_output}", str(data["Ships"][name]["power_output"]))
            infobox = infobox.replace("{maxCruise}", str(data["Ships"][name]["maxCruise"]))
            infobox = infobox.replace("{power_recharge}", str(data["Ships"][name]["power_recharge"]))
            infobox = infobox.replace("{hull_price}", str(data["Ships"][name]["hull_price"]))
            infobox = infobox.replace("{package_price}", str(data["Ships"][name]["package_price"]))


            info = data["Ships"][name]["infocard"].split("\n", 1)[1]
            while True:
                if info[0].isspace():
                    info = info[1:len(info)]
                else:
                    break
            infocard = infocard.replace("{infocard}", info)

            handle = data["Ships"][name]["maneuverability"]
            if data["Ships"][name]["mustUseMoors"] == True:
                
                handle = f"* This ship is too large to use docking bays, it must use mooring points.{handle}"
                handling = handling.replace("{handling}", handle)
            else:
                handling = handling.replace("{handling}", handle)


            hardpoint = ""
            for x in data["Ships"][name]["hardpoints"]:
                if "Cruiser Shield Upgrade" in x:
                    x = x.replace("Cruiser Shield Upgrade", "Shield Harmonic Reinforcement")
                try:
                    if "Gun" in x:
                        temp = x.split("(")[1]
                        temp = temp.split(")")[0]
                        temp = temp.replace(" ", "_")
                        temp2 = x.split(":")[0]
                        #print(f"* [[{temp}_Guns|{temp2}]]")
                        x = x.replace(temp2, f"{temp}_Guns|{temp2}")
                except IndexError:
                    pass
                hardpoint = f"{hardpoint}{x}\n"
            hardpoints = hardpoints.replace("{hardpoints}", hardpoint)

            include = ""
            temp = ""
            for x in data["Ships"][name]["equipment"]:
                number = "{:,}".format(x[1])
                if "Shield" in x[0]:
                    temp = x[0].split("[[")[1]
                    temp = temp.split("]]")[0]
                    x[0] = x[0].replace(temp, f"Shields|{temp}")
                elif "Armor" in x[0]:
                    temp = x[0].split("[[")[1]
                    temp = temp.split("]]")[0]
                    x[0] = x[0].replace(temp, f"Armor_Upgrades|{temp}")
                include = f"{include}{x[0]} (${number})\n"
            includes = includes.replace("{includes}", include)

            available = ""
            for x in data["Ships"][name]["sold_at"]:
                if x[3] == "Independent":
                    x[3] = "Independent Worlds"
                available = f"{available}|-\n|[[{x[0]}]]||[[{x[1]}]]||[[{x[2]}]]||[[{x[3]}]]\n"
            availability = availability.replace("{sold_at}", available)

            if data["Ships"][name]["built_by"] != "":
                category = category.replace("{built_by}", data["Ships"][name]["built_by"])
            else:
                category = ""
            if handle != "":
                return f"{version}{infobox}{infocard}{handling}{hardpoints}{includes}{availability}{category}"
            else:
                return f"{version}{infobox}{infocard}{hardpoints}{includes}{availability}{category}"
        elif "sys" in template.lower():    
            version = "{{Version|{version}}}\n"
            infobox = "{{System v2\n| name = {name}\n| nickname = {nickname}\n| image = {nickname}.png\n| government = {government}\n| region = {region}\n| neighbors = {neighbors}\n"
            description = "| description = {description}\n"
            overview = "| suns = {suns}\n| fields = {fields}\n| lawful-factions = {lawfuls}\n| trade-factions = {traders}\n| unlawful-factions = {unlawfuls}\n| stations = {bases}\n| planets = {planets}\n| mining-zones = {miningZones}\n}}\n"
            navmap = "=System Map=\n[https://space.discoverygc.com/navmap/#q={name} Navmap]\n"
            AoI = "=Areas of Interest=\n"
            nebulae = "==Nebulae==\n\n{nebulae}\n"
            asteroids = "==Asteroid Fields==\n\n{asteroids}\n"
            jumps = '==Jump Gates/Holes==\n{| class="wikitable collapsible collapsed"\n!Spoiler: Jump Hole/Gate Locations\n|-\n|\n|-\n|\n{| class="wikitable sortable"\n!Target System!!Location!!Type\n{gates}\n|}\n|}'
            category = "\n[[Category: {region}]]"

            while True:
                name = str(input("Enter system name: "))
                try:
                    if data["Systems"][name]:
                        break
                except:
                    print("System could not be found in database, retrying...")
            version = version.replace("{version}", data["Version"])

            infobox = infobox.replace("{name}", name)
            infobox = infobox.replace("{nickname}", data["Systems"][name]["nickname"])
            region = data["Systems"][name]["region"]
            if region == "Independent": region = "Independent Worlds"
            if region in config["settings"]["houses"]: 
                infobox = infobox.replace("{government}", "{{" + f'House Link|{region}' + "}}")
            else:
                infobox = infobox.replace("{government}", 'Independent')
            infobox = infobox.replace("{region}", region)
            temp = ""        
            for neighbor in data["Systems"][name]["neighbors"]:
                temp = f"{temp}[[{neighbor}]]<br/>"
            infobox = infobox.replace("{neighbors}", temp)

            description = description.replace("{description}", "")

            temp = ""
            for star, card in data["Systems"][name]["stars"].items():
                card = '\n' + card[:-1]
                card = card.replace("\n", "\n* ")
                temp = f"{temp}'''{star}'''\n{card}\n"
            overview = overview.replace("{suns}", temp)
            temp = ""
            temp2 = []
            nebs = []
            asts = []
            for zone, nick, info in data["Systems"][name]["zones"]:
                if zone in temp2: continue
                temp2.append(zone)
                temp = f"{temp}{zone}\n" if nick in [field[0] for field in data["Systems"][name]["asteroids"]] or nick in [nebula[0] for nebula in data["Systems"][name]["nebulae"]] else temp
                if nick in [nebula[0] for nebula in data["Systems"][name]["nebulae"]]: nebs.append([zone, nick, info])
                elif nick in [field[0] for field in data["Systems"][name]["asteroids"]]: asts.append([zone, nick, info])
            temp = "* " + temp.replace('\n', '\n* ')
            overview = overview.replace("{fields}", temp)
            temp = ""
            bases = []
            lawfulFactions = []
            unlawfulFactions = []
            corporateFactions = []
            for base, dicty in data["Systems"][name]["bases"].items():
                if dicty["type"] != "<class 'flint.entities.solars.PlanetaryBase'>":
                    bases.append([base, dicty["owner"]])
                if dicty["owner"] in [x[0] for x in config["settings"]["corporations"]]:
                    corporateFactions.append(dicty["owner"])
                elif dicty["factionLegality"] == "Lawful":
                    lawfulFactions.append(dicty["owner"])
                elif dicty["factionLegality"] == "Unlawful":
                    unlawfulFactions.append(dicty["owner"])
            lawfulFactions = list(dict.fromkeys(lawfulFactions))
            corporateFactions = list(dict.fromkeys(corporateFactions))
            unlawfulFactions = list(dict.fromkeys(unlawfulFactions))
            lawfulFactions.sort()
            corporateFactions.sort()
            unlawfulFactions.sort()
            lawfuls = "* "
            corporates = "* "
            unlawfuls = "* "
            for faction in lawfulFactions:
                lawfuls = f"{lawfuls}[[{faction}]]\n"
            for faction in corporateFactions:
                corporates = f"{corporates}[[{faction}]]\n"
            for faction in unlawfulFactions:
                unlawfuls = f"{unlawfuls}[[{faction}]]\n"
            lawfuls = lawfuls.replace("\n", "\n* ")
            corporates = corporates.replace("\n", "\n* ")
            unlawfuls = unlawfuls.replace("\n", "\n* ")
            overview = overview.replace("{lawfuls}", lawfuls)
            overview = overview.replace("{traders}", corporates)
            overview = overview.replace("{unlawfuls}", unlawfuls)
            stations = "* "
            for base, owner in bases:
                stations = f"{stations}'''[[{base}]]''' -- ''[[{owner}]]''\n"
            stations = stations.replace("\n", "\n* ")
            overview = overview.replace("{bases}", stations)
            planets = "\n"
            brrt = ""
            for planet, nickname, owner in data["Systems"][name]["planets"]:
                inhabited = "Inhabited" if owner != "" else "Uninhabited"
                planet = planet if planet != " " else "Unknown"
                if inhabited == "Inhabited":
                    planets = f"{planets}????Planet|{planet}|{inhabited} -- [[{owner}]]|{nickname}.png$$\n"
                else:
                    planets = f"{planets}????Planet|{planet}|{inhabited}|{nickname}.png$$\n"
                brrt = f"{brrt}<br/><br/>"
            planets = planets.replace("??", "{")
            planets = planets.replace("$", "}")
            planets = f"{planets}{brrt}"
            overview = overview.replace("{planets}", planets)
            mineableCommodities = ""
            mineableCommodity = []
            for doesnt, matter, commodity in data["Systems"][name]["asteroids"]:
                if commodity != None:
                    mineableCommodity.append(commodity)
            mineableCommodity = list(dict.fromkeys(mineableCommodity))
            mineableCommodity.sort()
            for commodity in mineableCommodity:
                mineableCommodities = f"{mineableCommodities}* [[{commodity}]]\n"
            overview = overview.replace("{miningZones}", mineableCommodities)

            navmap = navmap.replace("{name}", name.replace(" ", "%20"))

            nebul = "\n"
            ast = "\n"
            for nebula, nick, info in nebs:
                nebul = f"{nebul}\n'''{nebula}'''\n\n<p>{info}\n"
            for field, nick, info in asts:
                ast = f"{ast}\n'''{field}'''\n\n<p>{info}\n"
            nebul = nebul.replace("<p></b>", "</b>")
            ast = ast.replace("<p></b>", "</b>")
            nebulae = nebulae.replace("{nebulae}", nebul)
            asteroids = asteroids.replace("{asteroids}", ast)

            gates = ""
            for system, type, sector in data["Systems"][name]["holes"]:
                gates = f"{gates}|-\n|[[{system}]]||{sector}||{type}\n"
            jumps = jumps.replace("{gates}", gates)

            category = category.replace("{region}", data["Systems"][name]["region"])





            return f"{version}{infobox}{description}{overview}{navmap}{AoI}{nebulae}{asteroids}{jumps}{category}"
        else:
            return False
    else:
        if template.lower() == "ship":
            infobox = '__NOTOC__\n<table class="infobox bordered" style="float: right; margin-left: 1em; margin-bottom: 10px; width: 270px; font-size: 11px; line-height: 14px; border: 2px solid black;" cellpadding="3">\n\n<tr>\n<td colspan="2" class="infobox-name"><b>{name}</b>\n</td></tr>\n<tr>\n<td colspan="2" class="shipDisplay" style="padding: 0; text-align: center; padding: 5px 0px;"><div class="center"><div class="floatnone">[[File:{image}|center|254px]]</div></div>\n</td></tr>\n<tr>\n<td class="infobox-data-title" style="width: 120px;"><b>Ship Class</b>\n</td>\n<td style="padding-right: 1em;">{class}\n</td></tr>\n<tr>\n<td class="infobox-data-title"><b>Built by</b>\n</td>\n<td style="padding-right: 1em;">{built_by}\n</td></tr>\n<tr title="What column on the Tech Mix chart this ship belongs to">\n<td class="infobox-data-title">[http://discoverygc.com/techcompat/techcompat_table.php Tech Column]\n</td>\n<td style="padding-right: 1em;">{techcompat}\n</td></tr>\n<tr>\n<td colspan="2" class="infobox-section">Technical information\n</td></tr>\n<tr title="Amount of gun and turret hardpoints on this ship">\n<td class="infobox-data-title"><b>Guns/Turrets</b>\n</td>\n<td style="padding-right: 1em; font-weight: bold; letter-spacing: 1px;">{gunCount} / {turretCount}\n</td></tr>\n<tr title="Maximum class of weapons that can be mounted on this ship">\n<td class="infobox-data-title"><b>Max. weapon class</b>\n</td>\n<td style="padding-right: 1em;">{maxwep}\n</td></tr>\n<tr>\n<td class="infobox-data-title"><b>Other equipment</b>\n</td>\n<td style="padding-right: 1em;">\n<ul>\n{other}\n</ul></td></tr>\n<tr title="Amount of hull hitpoints">\n<td class="infobox-data-title"><b>Hull strength</b>\n</td>\n<td style="padding-right: 1em; color: #009900; font-weight: bold;">{hull}\n</td></tr>\n<tr title="Maximum class of shield that can be mounted on this ship">\n<td class="infobox-data-title"><b>Max. shield class</b>\n</td>\n<td style="padding-right: 1em; color: #006699; font-weight: bold;">{maxShield}\n</td></tr>\n<tr title="Amount of cargo this ship is able to carry">\n<td class="infobox-data-title"><b>Cargo space</b>\n</td>\n<td style="padding-right: 1em;">{cargo} units\n</td></tr>\n<tr title="Maximum number of shield batteries carried by this ship">\n<td class="infobox-data-title"><b>Batteries</b>\n</td>\n<td style="padding-right: 1em;">{batteries}\n</td></tr>\n<tr title="Maximum number of shield nanobots carried by this ship">\n<td class="infobox-data-title"><b>Nanobots</b>\n</td>\n<td style="padding-right: 1em;">{bots}\n</td></tr>\n<tr title="Maximum speed of this ship on impulse drive">\n<td class="infobox-data-title"><b>Max. impulse speed</b>\n</td>\n<td style="padding-right: 1em;">{impulse} m/s\n</td></tr>\n<tr title="Maximum turning speed in degrees per second">\n<td class="infobox-data-title"><b>Max. turn speed</b>\n</td>\n<td style="padding-right: 1em;">{turnRate} deg/s\n</td></tr>\n<tr title="Maximum speed of this ship on thrusters">\n<td class="infobox-data-title"><b>Max. thrust speed</b>\n</td>\n<td style="padding-right: 1em;">{maxthrust} m/s\n</td></tr>\n<tr title="Maximum speed of this ship on cruise engines">\n<td class="infobox-data-title"><b>Max. cruise speed</b>\n</td>\n<td style="padding-right: 1em;">{maxCruise} m/s\n</td></tr>\n<tr title="Maximum reactor energy storage (capacitance)">\n<td class="infobox-data-title"><b>Power output</b>\n</td>\n<td style="padding-right: 1em;">{power_output} u\n</td></tr>\n<tr title="Amount of energy units generated per second">\n<td class="infobox-data-title"><b>Power recharge</b>\n</td>\n<td style="padding-right: 1em;">{power_recharge} u/s\n</td></tr>\n<tr>\n<td colspan="2" class="infobox-section">Additional information\n</td></tr>\n<tr title="Price of the ship without any mounted equipment">\n<td class="infobox-data-title"><b>Ship price</b>\n</td>\n<td style="padding-right: 1em;">${hull_price}\n</td></tr>\n<tr title="Price of the ship with the default equipment">\n<td class="infobox-data-title"><b>Package price</b>\n</td>\n<td style="padding-right: 1em;">${package_price}\n</td></tr></table>\n'
            infocard = '<p>{infocard}\n</p><p><br/>\n</p>\n'
            handling = '<h2>Handling</h2>\n<ul>\n{handling}\n</ul>\n'
            hardpoints = '<h2>Hardpoints</h2>\n<ul>\n{hardpoints}\n</ul>\n'
            includes = '<h2>Purchase Includes</h2>\n<ul>\n{includes}\n</ul>'
            availability = '<h2>Availability</h2>\n<table class="wikitable collapsible collapsed">\n<tr>\n<th>Buying Locations\n</th></tr>\n<tr>\n<td>\n<table class="wikitable sortable">\n<tr>\n<th>Base</th>\n<th>Owner</th>\n<th>System</th>\n<th>Location\n</th></tr>\n{sold_at}\n</td></tr></table>\n</td></tr></table>'

            while True:
                name = str(input("Enter ship name (as displayed in FLStat): "))
                try:
                    if data["Ships"][name]:
                        break
                except:
                    print("Ship name could not be found in database, retrying...")
            image = str(input("Enter image name (copy-paste from page source): "))
            if image == "":
                image = f'{data["Ships"][name]["nickname"]}.png'
                print(f'No Image has been specified, defaulting to {data["Ships"][name]["nickname"]}')
            elif image.lower() == "nickname":
                image = f'{data["Ships"][name]["nickname"]}.png'
                print("Using Ship's nickname as image name.")
            
            infobox = infobox.replace("{name}", data["Ships"][name]["longName"])
            infobox = infobox.replace("{image}", image)
            infobox = infobox.replace("{class}", data["Ships"][name]["type"])
            if data["Ships"][name]["built_by"] != "":
                if data["Ships"][name]["built_by"] in houses:
                    infobox = infobox.replace("{built_by}", f'[[File:Flag-{data["Ships"][name]["built_by"].lower()}.png|19px]] [[{data["Ships"][name]["built_by"]}]]')
                else:
                    infobox = infobox.replace("{built_by}", f'[[{data["Ships"][name]["built_by"]}]]')
            else:
                built = str(input("Enter ship owner faction: "))
                if built in houses:
                    infobox = infobox.replace("{built_by}", f"[[File:Flag-{built.lower()}.png|19px]] [[{built}]]")
                else:
                    infobox = infobox.replace("{built_by}", f"[[{built}]]")
            infobox = infobox.replace("{techcompat}", data["Ships"][name]["techcompat"])
            infobox = infobox.replace("{gunCount}", str(data["Ships"][name]["gunCount"]))
            infobox = infobox.replace("{turretCount}", str(data["Ships"][name]["turretCount"]))
            other = ""
            if data["Ships"][name]["torpedoCount"] > 0:
                other = f'{other}<li>{data["Ships"][name]["torpedoCount"]}x[[Cruise Disruptors|CD]]/[[Torpedoes|T]]</li>\n'
            if data["Ships"][name]["cmCount"] > 0:
                other = f'{other}<li>{data["Ships"][name]["cmCount"]}x[[Countermeasures|CM]]</li>\n'
            if data["Ships"][name]["mineCount"] > 0:
                other = f'{other}<li>{data["Ships"][name]["mineCount"]}x[[Mines|M]]</li>\n'
            infobox = infobox.replace("{other}", other)
            if data["Ships"][name]["maxThrust"] > 0:
                infobox = infobox.replace("{maxthrust}", str(data["Ships"][name]["maxThrust"]))
            else:
                infobox = infobox.replace("{maxthrust} m/s", '<span style="color: #990000; font-style: italic;">Thruster not available</span>')
            infobox = infobox.replace("{hull}", "{:,}".format(data["Ships"][name]["hit_pts"]))
            infobox = infobox.replace("{cargo}", "{:,}".format(data["Ships"][name]["hold_size"]))
            infobox = infobox.replace("{batteries}", "{:,}".format(data["Ships"][name]["bat_limit"]))
            infobox = infobox.replace("{bots}", "{:,}".format(data["Ships"][name]["bot_limit"]))
            infobox = infobox.replace("{maxwep}", str(data["Ships"][name]["maxClass"]))
            infobox = infobox.replace("{maxShield}", "{:,}".format(data["Ships"][name]["maxShield"]))
            infobox = infobox.replace("{impulse}", "{:,}".format(data["Ships"][name]["impulse_speed"]))
            infobox = infobox.replace("{turnRate}", "{:,}".format(data["Ships"][name]["turnRate"]))
            infobox = infobox.replace("{power_output}", "{:,}".format(data["Ships"][name]["power_output"]))
            infobox = infobox.replace("{maxCruise}", "{:,}".format(data["Ships"][name]["maxCruise"]))
            infobox = infobox.replace("{power_recharge}", "{:,}".format(data["Ships"][name]["power_recharge"]))
            infobox = infobox.replace("{hull_price}", "{:,}".format(data["Ships"][name]["hull_price"]))
            infobox = infobox.replace("{package_price}", "{:,}".format(data["Ships"][name]["package_price"]))

            info = data["Ships"][name]["infocard"].split("\n", 1)[1]
            while True:
                if info[0].isspace():
                    info = info[1:len(info)]
                else:
                    break
            infocard = infocard.replace("{infocard}", info)

            handleList = data["Ships"][name]["maneuverability"].split("\n")
            handle = ""
            if data["Ships"][name]["mustUseMoors"] == True:
                handle = "<li>This ship is too large to use docking bays, it must use mooring points.</li>\n"
            for entry in handleList:
                if entry != "":
                    handle = f"{handle}<li>{entry}</li>\n"
            handling = handling.replace("{handling}", handle)

            harderpoint = ""
            for hardpoint in data["Ships"][name]["hardpoints"]:
                title = hardpoint.split(":")[0]
                count = hardpoint.split(":")[1]
                harderpoint = f"{harderpoint}<li>{count}x {title}</li>\n"
            hardpoints = hardpoints.replace("{hardpoints}", harderpoint)

            included = ""
            for title, price in data["Ships"][name]["equipment"]:
                included = f'{included}<li>{title} (${"{:,}".format(price)})'
            includes = includes.replace("{includes}", included)

            sold_at = ""
            for base, owner, system, region in data["Ships"][name]["sold_at"]:
                sold_at = f"{sold_at}<tr><td>{base}</td>\n<td>{owner}</td>\n<td>{system}</td>\n<td>{region}</td></tr>\n"
            availability = availability.replace("{sold_at}", sold_at)

            return f"{infobox}{infocard}{handling}{hardpoints}{includes}{availability}"
        elif "sys" in template.lower():
            raise NotImplementedError
loadedData = loadData("flData.json")
configData = loadData("config.json")
while True:
    templates = ["Ship", "System"]
    source = main(template = input(f"Select template ({templates}): "), data = loadedData, config = configData)
    if source != False:
        copy(source)
        print("Page source copied!")
    else:
        print("Page source could not be copied.")
    
    repeat = input("Generate another page? (yes/No): ")
    if repeat == "" or 'n' in repeat.lower(): break