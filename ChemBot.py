import os
import discord
import re
import typing
from ChemicalElements import periodic_table
from Formula import Formula

from dotenv import load_dotenv

from EquationBalancer import EquationBalancer
from Compound import Compound

load_dotenv(dotenv_path=".idea/.env")

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.messages = True
intents.members = True

client = discord.Client(intents=intents)


# notifies if i am connected or not
@client.event
async def on_ready():
    print(f"{client.user} has connected onto discord!")


# the server must be able to say hello to them when they join the server
@client.event
async def on_member_join(member):
    print(f"{member.name} has joined")
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to ChemBot server!'
    )


@client.event
async def on_message(message):
    if message.channel.name != "general":
        print("Wrong Channel")
        return
    if message.author == client.user:
        return
    content = message.content.split()

    # if the first part of the message is chembot
    if content[0] == "-chembot":
        author = message.author.mention
        channel = message.channel
        command = message.content.replace("-chembot", "").strip().split()

        if len(command) == 0:
            await channel.send(f"{author} Missing command?")
            return

        func = command[0]  # contains the operation that the user wants to perform
        inputs = command[1:]  # this list contains all of the inputs that the user feed in for the operation

        if func.startswith("help"):
            await helpMenu(channel)
            return

        if func not in ["m", "f"]:
            await channel.send(f"{author}```No commands found.\nTo see a list of commands, type -chembot help```")
            return

        # if there are no inputs
        if not inputs:
            await channel.send(f"{author} There are no inputs for your command.")
            return

        print(f"Command: {func}\nInputs: {inputs}")
        # Molar mass
        if func.startswith("m"):
            await molarMass(inputs, author, channel)
        elif func.startswith("f"):
            # the formula function takes in a list of element percent composition
            await formula(" ".join(inputs), author, channel)

        # elif command.startswith("formula") and command == "formula":
        #     command = re.split(f"(?<=formula) ", command)
        #     inputs = command[1] if len(command) > 1 else None
        #
        #     if inputs is not None:
        #         inputs = re.split(r"-[a-z]", inputs)
        #         print(inputs)
        #     else:
        #         await message.channel.send(f"{author} missing inputs.")
        # # Percent Composition
        # elif command.startswith("formula"):
        #     await message.channel.send(f"{author} Please enter the percentages")
        # # Equation Balancer
        # elif command.startswith("bal eq"):
        #     print(re.split(r'(?<=bal eq) ', command))
        #     await message.channel.send(f"{author} Please enter a chemical equation to balance.")
        #     msg = await client.wait_for('message', timeout=60)
        #     balancedEquation = EquationBalancer(msg.content)
        #     await message.channel.send(f"Balanced Equation: {balancedEquation}")


async def helpMenu(channel):
    await channel.send("```List of commands:\n"
                       "-chembot m [Element(s)/Compound(s)]\n"
                       "\tFinds the molar mass of an element/compound\n\n"
                       "-chembot f [Element(s): percent(s)] <Mass>\n"
                       "\tFinds the empirical formula given the percent composition of the compound."
                       " Percents should either be typed in decimals (i.e 0.2) or percents (i.e. 20%)"
                       " Inputting the mass value will result the bot to automatically "
                       "calculate a molecular formula.```")
    return


async def molarMass(inputs, author, channel):
    malformedCompounds = []
    validCompounds = []

    for item in inputs:
        if Compound.isMalformed(item):
            malformedCompounds.append(item)
            continue
        compound = Compound(item)  # class used to calculate molar mass
        validCompounds.append(compound)

    # if there are malformed compounds
    if malformedCompounds:
        await channel.send(f"{author} Error: Invalid Compound(s): "
                                   f"{', '.join(malformedCompounds)}. Please try again.")
    else:
        await channel.send(f"{author} ```Molar Mass(es)\n"
                                   f"{showMolarMass(validCompounds)}```")


async def formula(inputs, author, channel):
    print(f"{inputs=}")
    inputs = re.split(r"(?<=[A-Za-z0-9])\s*?:\s*?(?=[0-9.])", inputs)
    print(f"{inputs=}")
    rawInputs = []

    for input in inputs:
        rawInputs += re.split(r",\s+?|;\s+?|\s+", input)

    print(f"{rawInputs=}")

    percentDict = {}
    totalPercent = 0
    epsilon = 0.011
    mass = 0

    for index in range(len(rawInputs)):
        if index % 2 == 0:
            element = rawInputs[index]

            if "mass" in element:
                # this entry contains the mass
                element = element.split("=")
                mass = float(element[1])
                continue

            percent = rawInputs[index + 1]
            if "%" in percent:
                percent = int(percent.replace("%", "")) / 100
                totalPercent += percent
            elif "." in percent:
                percent = float(percent)
                totalPercent += percent
            else:
                await channel.send(f"{author} The inputs for the command are inputted wrong.")
                return

            if element not in periodic_table:
                await channel.send(f"{author} One or more of the inputted elements is not inputted correctly.")
            percentDict[rawInputs[index]] = percent

    # if the total percent is within an acceptable range
    if 1 - epsilon <= totalPercent <= 1 + epsilon:
        print(f"{percentDict=}")
        # if the user inputted a mass value
        if mass > 0:
            # give the molecular formula
            compoundFormula = Formula(**percentDict, mass=mass)
            compound = Compound(compoundFormula.molecularFormula())
            await channel.send(f"{author} The molecular formula is: {compound}")
        else:
            # give the empirical formula
            compoundFormula = Formula(**percentDict)
            compound = Compound(compoundFormula.empiricalFormula())
            await channel.send(f"{author} The empirical formula is: {compound}")
    else:
        await channel.send(f"{author} The percentages do not add up to 100%.")
    return


def showMolarMass(compounds):
    output = ""
    for compound in compounds:
        output += f"{compound}: {compound.molarMass()} g\n"

    return output


client.run(TOKEN)

if __name__ == '__main__':
    pass
