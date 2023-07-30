import nextcord
from nextcord.ext import commands
from googletrans import Translator, LANGUAGES
from langcodes import lang_codes
import os

intents = nextcord.Intents.all()
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents) # I have made the prefix for a command a "!", but you can change that as you wish 
translator = Translator()

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @bot.command() # to tell the bot that is is a command (keyword is info)
    async def info(self, ctx):
        await ctx.channel.send("I'm a translator bot built based off the python Googletrans library. I can detect several language codes in the ISO 639-1 standard, or even the entire language name itself. For information on how to use me, type: ```!translate``` For a list of ISO 639-1 codes, type: ```!isocodes``` Created by IbyCodes (Mohammad Ibrahim Khan). Link to github and source code: https://github.com/IbyCodes/LangTranslatorDiscordBot")

    @bot.command() # !isocodes command
    async def isocodes(self, ctx):
        await ctx.channel.send("As of Release 3.0.0 of Googletrans Documentation, the following language codes are supported (Source: https://readthedocs.org/projects/py-googletrans/downloads/pdf/latest/)")
        codes = "```\n" + "\n".join([f"{code}: {name}" for code, name in lang_codes.items()]) + "\n```" # will receive all codes from langcodes.py dictionary 
        await ctx.channel.send(codes)
        
    
    @bot.command() # to tell the bot that is is a command to attempt translation
    async def translate(self, ctx, target_lang=None, *, text_to_translate=None):
        if not target_lang and not text_to_translate: # when no arguments are provided
            await ctx.channel.send("Hey there! Here's how to use me: ```!translate <target_language> <text_to_translate>```\n If you want to translate a txt file, attach a .txt file and provide the following: ```!translatefile <target_language>``` \nFor detailed information, type **!info**")
            return
        elif not target_lang or not text_to_translate: # when only one argument is provided but not the other 
            await ctx.channel.send("You have not entered your arguments correctly. Here's a quick reminder on how to use me: ```!translate <target_language> <text_to_translate>```")
            return
        

    # Translating the text using googletrans python library. Note some of the code is to just make sure that a valid, readable language is returned when it returns the translated string
        try:
            translation = translator.translate(text_to_translate, dest=target_lang)
            original_language = LANGUAGES.get(translation.src) 
            if original_language == None:
                original_language = translation.src
            target_language = LANGUAGES.get(target_lang)
            if target_language == None:
                target_language = target_lang
            await ctx.channel.send("Success! \n" f'Original language: {original_language}\nTranslated ({target_language}): {translation.text}')
        except Exception as e: # catching any errors in the translation here 
            print(f'Error translating: {e}')
            await ctx.channel.send("An error occurred while translating. Please make sure you are using a valid language in your request, and that spaces are used correctly. If you're unsure about the languages I support, use **!isocodes** for more information.")



    # code to translate a txt file (separate from the code to translate in the text channel directly)
    @bot.command()
    async def translatefile(self, ctx, target_lang=None): #!translatefile will the command to use to do this
        # Checking if a file has been attached to the message
        if not ctx.message.attachments:
            await ctx.channel.send("Please attach a .txt file to translate.") # if a file is not attached, letting the user know this
            return

        # Making sure the target language is provided
        if not target_lang:
            await ctx.channel.send("Please provide the target language. Reminder of how to use me with .txt files: `!translate_file <target_language>`") # reminding the user to provide a target language with the file
            return

        # Getting the attached file
        attachment = ctx.message.attachments[0]
        if not attachment.filename.endswith('.txt'):
            await ctx.channel.send("Please attach a valid .txt file.")
            return

        # Attempting to download and read the file content provided 
        try:
            file_content = await attachment.read()
            text_to_translate = file_content.decode('utf-8')
        except Exception as e:
            await ctx.channel.send(f"Error reading the file: {e}")
            return

        # Translating the text using googletrans python library, same way as reading normal text in the channel
        try:
            translation = translator.translate(text_to_translate, dest=target_lang)
            original_language = LANGUAGES.get(translation.src)
            if original_language is None:
                original_language = translation.src
            target_language = LANGUAGES.get(target_lang)
            if target_language is None:
                target_language = target_lang

           # Creating a new .txt file with the translation result. This will be a temporary file made on the system, written to, then delete
            translated_filename = f"translated_text_{ctx.author.id}.txt"
            with open(translated_filename, "w", encoding="utf-8") as file:
                file.write(f"Original language: {original_language}\nTranslated ({target_language}): {translation.text}")

            # Send the .txt file as an attachment
            with open(translated_filename, "rb") as file:
                translated_file = nextcord.File(file, filename=translated_filename)
                await ctx.send(file=translated_file)
            await ctx.channel.send("Success! \n" f'Original language: {original_language} Translated to: {target_language}\n File is attached above.')

        except Exception as e:
            print(f'Error translating: {e}')
            await ctx.channel.send("An error occurred while translating. Please make sure you are using a valid language in your request, and that spaces are used correctly. If you're unsure about the languages I support, use **!isocodes** for more information.")

        finally:
            # deleting the temporary .txt file on our system
            try:
                os.remove(translated_filename)
            except Exception as e:
                print(f'Error deleting the temporary file: {e}')



def setup(bot): # setting up the bot with all of the commands I defined above 
    bot.add_cog(Commands(bot))
        