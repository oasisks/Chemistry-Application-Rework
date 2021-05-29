import os
import discord
import re
import typing

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

    if message.content.startswith("-chembot"):
        author = message.author.mention
        command = message.content.replace("-chembot", "").strip().split()

        # print(f"Command: {command}")
        # print(f"Inputs: {inputs}")
        # print(f"Command: {re.split(r'(?<=bal eq) ', command)}")

        if len(command) == 0:
            await message.channel.send(f"{author} Missing command?")
            return

        func = command[0]  # contains the operation that the user wants to perform
        inputs = command[1:]  # this list contains all of the inputs that the user feed in for the operation

        if func.startswith("help"):
            await message.channel.send("```List of commands:\n"
                                       "-chembot m [Element(s)/Compound(s)] -"
                                       " finds the molar mass of an element/compound\n"
                                       "----------------------------------------------\n"
                                       "-chembot f {Element(s): percent(s)} [Mass] - finds the empirical formula "
                                       "given the percent composition of the compound. Inputting the mass value will "
                                       "result the bot to automatically calculate a molecular formula.```")
            return


        # if there are no inputs
        if not inputs:
            await message.channel.send(f"{author} There are no inputs?")

        print(f"Command: {func}\nInputs: {inputs}")
        # Molar mass
        if func.startswith("m"):
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
                await message.channel.send(f"{author} Error: Invalid Compound(s): "
                                           f"{', '.join(malformedCompounds)}. Please try again.")
            else:
                await message.channel.send(f"{author} ```Molar Mass(es)\n"
                                           f"{showMolarMass(validCompounds)}```")
        elif func.startswith("f"):
            # the formula function takes in a list of element percent composition
            pass

        elif command.startswith("formula") and command == "formula":
            command = re.split(f"(?<=formula) ", command)
            inputs = command[1] if len(command) > 1 else None

            if inputs is not None:
                inputs = re.split(r"-[a-z]", inputs)
                print(inputs)
            else:
                await message.channel.send(f"{author} missing inputs.")
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
        else:
            await message.channel.send(f"{author} no clue what you want.")


def showMolarMass(compounds):
    output = ""
    for compound in compounds:
        output += f"{compound}: {compound.molarMass()}\n"

    return output


def test(verbose=True):
    assert showMolarMass([Compound("H2O"), Compound("SO4")]) == f"H2O: {Compound('H2O').molarMass()}\n" \
                                                                f"SO4: {Compound('SO4').molarMass()}"
    if verbose:
        print("All tests passed for Compound")


client.run(TOKEN)

if __name__ == '__main__':
    test()
