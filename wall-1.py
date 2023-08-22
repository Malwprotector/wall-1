import nextcord
from nextcord.ext import commands
import os
import random
from dotenv import load_dotenv
from googlesearch import search
from deep_translator import GoogleTranslator
import requests
import pyjokes
load_dotenv()


bot = commands.Bot()

@bot.event
async def on_ready():
    print('Logged in as ' + bot.user.name + ' (' + str(bot.user.id) + ')')
    print('Bot is now online.')
    await bot.change_presence(activity=nextcord.Game(name="/info | v2.3"))

#base

@bot.slash_command(description="Get some informations about the bot")
async def info(interaction: nextcord.Interaction):
    await interaction.send("**`Wall-1` is an multifunction bot with a variety of generation tools!**\n\n **Projet page / support:** project page not even created\n **Github / source code:** https://github.com/Malwprotector/wall-1\n\n **Current version:** `v2.1`\n\n **`/help to get the list of commands!`**\n\n *Thanks for using wall-1 <3*", ephemeral=False)

@bot.slash_command(description="Shows all available commands")
async def help(interaction: nextcord.Interaction):
    commands_list = [
        "**Mod:**",
        "**`/info`** - Get some informations about the bot",
        "**`/help`** - Get the list of commands",
        "**`/ping`** - Replies with pong!",
        "**`/userinfo <user>`** - Displays information about a user\n",
        "**Generators / Tools:**",
        "**`/story <langage>`** - Generates a random story. Use langages codes to select langage (en for english)",
        "**`/joke <langage>`** - Tells a random joke. Use langages codes to select langage (en for english)",
        "**`/mcseed <seed> <minecraft seed edition>`** - Enter your minecraft world generation seed, and convert it between java and bedrock editions! For further informations, please see **`/mcseedinfo`**.",
        "**`/google <query>`** - Searches Google for the provided query",
        "**`/translate <text> <targetted langage>`** - Translates text to the specified language. Use langages codes for the second option."
    ]
    help_text = "\n".join(commands_list)
    await interaction.send(f"**:arrow_down: Available Commands:**\n{help_text}", ephemeral=True)


@bot.slash_command(description="Displays information about a user")
async def userinfo(interaction: nextcord.Interaction, user: nextcord.User):
    user_info = f"**Username:** {user.name}\n**Discriminator:** {user.discriminator}\n**User ID:** {user.id}\n**Avatar URL:** {user.avatar.url}"
    await interaction.send(f"**User Info for {user.mention}:**\n{user_info}", ephemeral=True)

@bot.slash_command(description="Replies with pong!")
async def ping(interaction: nextcord.Interaction):
    latency = bot.latency
    await interaction.send(f'**Pong! :ping_pong: \n{latency:.2f}ms**', ephemeral=False)

@bot.listen()
async def on_message(message: nextcord.Message):
    if bot.user in message.mentions:
        await message.channel.send("**Hi there! :tada:  \n Try /info to get some informations, /help to see all commands.**")

#tools

@bot.slash_command(description="Searches Google for the provided query")
async def google(interaction: nextcord.Interaction, query: str):
    results = search(query, num_results=5)
    await interaction.send(f"**:arrow_down: Search Results for {query}:**\n" + "\n".join(results), ephemeral=False)

@bot.slash_command(description="Translates text to the specified language. Use langages codes for the second option.")
async def translate(interaction: nextcord.Interaction, source_text: str, target_lang: str):
    translated_text = GoogleTranslator(source='auto', target=target_lang).translate(source_text)
    await interaction.send(f"**:tada: Successfully translated** *{source_text}* **!**\n*`{translated_text}`*", ephemeral=False)

@bot.slash_command(description="Tells a random joke. Use langages codes to select langage (en for english)")
async def joke(interaction: nextcord.Interaction, joke_langage: str):
    joke_text = pyjokes.get_joke()
    joke_translated_text = GoogleTranslator(source='auto', target=joke_langage).translate(joke_text)
    await interaction.send(f"**Joke:**\n{joke_translated_text}", ephemeral=False)

#mc-seed-converter - source code: https://github.com/Malwprotector/mc-seed-converter

@bot.slash_command(description="Get informations about /mcseed command.")
async def mcseedinfo(interaction: nextcord.Interaction):
    await interaction.send("**Minecraft seed converter**\nThere are two different editions of the minecraft video game, the minecraft java edition and the minecraft bedrock edition. This particularity includes a fairly significant problem, world saves cannot be converted from one edition to the other: however, when you create a save, a generation seed is associated with it and is used to generate a minecraft world. **This tool allows you to convert minecraft world generation seeds from the bedrock edition to the java edition, and vice versa.**\n The bot command is taken from this project: https://github.com/Malwprotector/mc-seed-converter\n\n *When using the tool, please note that*:\n -All Minecraft Bedrock generation seeds can be converted to Java seeds.\n-You will not be able to convert all Minecraft Java edition seeds to Minecraft Bedrock seeds.\n-There will be some differences in the world generated.\n-The appearance points will probably be different.\n-Structures such as desert temples, jungle temples, mine shafts and fortresses will not be in the same place.\n-The biomes and map will be close to the seed of the original world.", ephemeral=True)

@bot.slash_command(description="Enter your minecraft world generation seed, and convert it to java or bedrock!")
async def mcseed(interaction: nextcord.Interaction, seed_to_be_converted: str, minecraft_seed_edition: str):
    new_seed = 0
    seed =int(seed_to_be_converted)
    if minecraft_seed_edition == 'java':
        if seed <= 0:
            await interaction.send("**Minecraft seed converter:**\n`Error: seed cannot be converted to minecraft bedrock edition.` Please see **`/mcseedinfo`** for further informations. :sob:", ephemeral=False)
        elif seed <= 2147483648:
            await interaction.send(f"**Minecraft seed converter:**\n`The seed is the same in minecraft bedrock edition` :white_check_mark:\n **seed: {seed}**", ephemeral=False)
        elif seed >= 2147483649 and seed <= 4294967296:
            new_seed = seed - 4294967296
            await interaction.send(f"**Minecraft seed converter:**\n`The seed has been successfully converted to minecraft bedrock edition` :white_check_mark:\n **seed: {new_seed}**", ephemeral=False)
        else:
            await interaction.send("**Minecraft seed converter:**\n`Error: seed cannot be converted to bedrock edition.` Please see **`/mcseedinfo`** for further informations. :sob:", ephemeral=False)
    elif minecraft_seed_edition == 'bedrock':
        if seed > 0 and seed <= 2147483648:
            await interaction.send(f"**Minecraft seed converter:**\n`The seed is the same in minecraft java edition` :white_check_mark:\n **seed: {seed}**", ephemeral=False)
        elif seed < 0:
            new_seed = seed + 4294967296
            await interaction.send(f"**Minecraft seed converter:**\n`The seed has been successfully converted to minecraft java edition` :white_check_mark:\n **seed: {new_seed}**", ephemeral=False)
        else:
            await interaction.send("**Minecraft seed converter:**\n`Error: the seed is incorrect. Please check that the generation seed you have entered is functional.` Please see **`/mcseedinfo`** for further informations. :x: ", ephemeral=False)
    else:
        await interaction.send("**Minecraft seed converter:**\n`Error: the minecraft edition you entered is incorrect. Please check that the minecraft edition you entered exists (java or bedrock).` Please see **`/mcseedinfo`** for further informations. :x: ", ephemeral=False)




#random_story_generator
enemy = random.choice (["chihuahua", "border collie", "wolf", "cat", "tiger", "elephant", "monster", "beagle", "shark", "t-rex"])
father = random.choice (["John", "Mr.Pickles", "Hairyface", "Willy Wonka", "Steve", "Bob", "Bastien", "Jordan", "Maya", "Patrick"])


enemyadj = ["grimy", "muddy", "awful", "grotesque", "hideous", "adorable", "cute", "wonderful", "terrifying", "annoying"]
intro1 = "I was sitting on the edge of the rocky cliff beside my favourite tree."
intro2 = "alone in the searing desert, I was wondering why I was leaning against a cactus."
intro3 = "staring out my apartment window, I saw my reflection staring back at me."
intro4 = "I was drinking a cup of tea inside my house."
intro5 = "It was raining outside, I was playing minecraft."
intro6 = "I woke up very tired: I'd been chatting on discord all night, which is why I hadn't slept."
intro7 = "I was chatting with my friends on discord: we had played fall guys the night before, it was very fun."
intro8 = "I was waiting for my friend; we had to go on holiday, school was over. When he didn't reply, I sent him a message on discord."
intro9 = "I was walking in the park, alone; the weather was nice, but I wasn't caring about that."
intro10 = "I was in bed, falling asleep. I'd turned off my computer after spending 3 sleepless nights farming netherite on minecraft."

char1 = "As I looked out into the distance, I thought about my past and all of the drama in it."
char2 = "I wondered if this was my destiny- trying to find happiness."
char3 = "I pulled out the photo of my long lost mother and where on earth she could be."
char4 = "I stared into space and thought about my life and my future."
char5 = "I opened my phone and was dazzled by the light."

prob1 = "Suddenly I was covered from head to toe with darkness. I couldn't breathe or see. Everything went black..."
prob2 = "All of a sudden a psychopathic " + enemy + " grinned at me,showing all his razor sharp teeth. Suddenly it started to claw at my face. From the loss of blood, I collapsed onto the tough ground..."
prob3 = "I suddenly felt a sharp needle sink into my flesh. It was a tranquilizer. But before I knew it I started feeling really drowsy. Everything went black..."

sol1 = "I forced my drowsy eyes open my eyes to see a bright light."
sol2 = "I forced my drowsy eyes open to find myself on the back of a massive dragon and a man in front of me."
sol3 = "I forced my drowsy eyes open to the sounds of a " + random.choice(enemyadj) + " " +enemy + " licking my face."

end1 = "A man came to my side with a knife. It was my father!" + father + "!" "'Go to sleep young one...'"
end2 = "It was difficult to keep my eyes open as I stuggled to breathe. "
end3 = "Out of nowhere, a duck wearing a deerstalker looked me in the eye and pointed a gun at me. 'Quack.' And that was the last thing I heard..."

intros = [intro1, intro2, intro3, intro4, intro5, intro6, intro7, intro8, intro9, intro10]
characters = [char1, char2, char3, char4, char5]
problems = [prob1, prob2, prob3]
solutions = [sol1, sol2, sol3]
endings = [end1, end2, end3]

@bot.slash_command(description="Generates a random story. Use langages codes to select langage (en for english).")
async def story(interaction: nextcord.Interaction, story_langage: str):
    random_intro = random.choice(intros)
    random_characters = random.choice(characters)
    random_problems = random.choice(problems)
    random_solutions = random.choice(solutions)
    random_endings = random.choice(endings)
    story_text = f"*Once upon a time, {random_intro} {random_characters} {random_problems} {random_solutions} {random_endings}*"
    story_translated_text = GoogleTranslator(source='en', target=story_langage).translate(story_text)
    await interaction.send(f"**:tada: Story successfully generated!**\n{story_translated_text}", ephemeral=False)



bot.run(os.getenv("TOKEN"))