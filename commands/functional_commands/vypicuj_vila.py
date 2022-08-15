from signalbot import Context
import random

spravicky = ["VILO UZ DRZ PICU", "VILO KLUD", "VILO OMG UZ CICHO", "KURVA DO PICI VILO ACH", "...", "uz si picujte sami, ja uz nevladzem", "VILO TY RETARDOS"]

async def execute_vypicuj_vila(c: Context):
    await c.send(random.choice(spravicky))
