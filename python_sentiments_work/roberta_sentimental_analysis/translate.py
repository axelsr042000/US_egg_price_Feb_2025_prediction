from googletrans import Translator
import asyncio

translator = Translator()



async def translate_text(original_text):
    translation = await translator.translate(original_text, dest="en")
    translated_text, original_language = translation.text, translation.src
    return translated_text, original_language



async def main(original_text):
    translated_text, original_language = await translate_text(original_text)
    return translated_text, original_language 



#original_text = "Hola, ¿cómo estás?"
#print(asyncio.run(main(original_text)))