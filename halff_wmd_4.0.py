#!/usr/bin/ python3
# -*- coding: utf-8 -*-

# Dependencies: reportlab, openai
# Follow Harpo's epicurean journey via snippets of his autobiography and the NYPL menu collection!

# Changes from 3.5:
#   Conceptual:
#       - adds computer generated illustrations
#       - exponentionally increases Harpo's orders and consumption (and presumably digestive abilities), hence increasing the international, translingual and transcultural nature of food to equal the international, translingual and transcultural nature of the best Marx brother

#   Technical:
#       - makes a pdf version
#       - formats prices with variance
#       - cleans place and dish names

import pickle
import random
import requests
import re
from math import modf
import openai
from os.path import exists, isdir
from os import mkdir
from reportlab.lib import utils
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import A5, LETTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

harpos_f = open('harpos_menu.pkl', 'rb')
harpos = pickle.load(harpos_f)
harpos_f.close()

def titlecase(s):
    return re.sub(r"[A-Za-z]+('[A-Za-z]+)?", lambda word: word.group(0).capitalize(),s)

def get_dish():
    dish = random.choice(list(harpos.keys()))
    return {'dish': dish, 'price': harpos[dish][0], 'date': harpos[dish][1], 'place': harpos[dish][2]}

def get_image(path, width=1):
    img = utils.ImageReader(path)
    iw, ih = img.getSize()
    aspect = ih / float(iw)
    return Image(path, width=width, height=(width * aspect))

def price_it(p):
    d = ["dollar", "smacker", "buck", "clam", "greenback"]
    one = ["one", "a", "1"]
    price = modf(float(p))
    dollars = int(price[1])
    cents = int(price[0]*100)
    price_string = ""
    if cents == 0:
        if dollars > 1:
            return "{} {}s".format(dollars, random.choice(d))
        elif dollars == 1:
            return "{} {}".format(random.choice(one), random.choice(d))
    elif cents > 0 and dollars == 0:
        c = "{} cents".format(cents)
        if cents % 25 == 0:
            option = ""
            if cents / 25 == 1:
                option = "a quarter"
            else:
                option = "{} quarters".format(int(cents / 25))
            return random.choice([c, option])
        elif cents % 10 == 0:
            option = ""
            if cents / 10 == 1:
                option = "a dime"
            else:
                option = "{} dimes".format(int(cents / 10))
            return random.choice([c, option])
        elif cents % 5 == 0:
            option = ""
            if cents / 5 == 1:
                option = "a nickel"
            else:
                option = "{} nickels".format(int(cents / 5))
            return random.choice([c, option])
        elif cents < 5:
            option = ""
            if cents == 1:
                option = "a penny"
            else:
                option = "{} pennies".format(int(cents))
            return random.choice([c, option])
        else:
            return c
    elif cents > 0 and dollars > 0:
        return "${}.{}".format(dollars, cents)

def auth_openai():
    if exists("auth.txt"):
        with open("auth.txt") as f:
            openai.organization = f.readline().strip()
            openai.api_key = f.readline().strip()
        return "OpenAI credentials loaded from file."
    else:
        openai.organization = input("Please enter your OpenAI organization ID: ")
        openai.api_key = input("Please enter your OpenAI API key: ")
        return "OpenAI credentials input from user."

def clean_dish(d):
    punc = "[]\\"
    for c in punc:
        d = d.replace(c, "")
    return d

def main():
    print(auth_openai())
    openai.Model.list()

    excerpts_f = open("excerpts.txt", "r")
    excerpts = excerpts_f.read().split("*")
    excerpts_f.close()

    styles = getSampleStyleSheet()
    ph_style = ParagraphStyle('harpo',
                               fontName="times",
                               fontSize=12,
                               parent=styles['BodyText'],
                               alignment=0,
                               spaceAfter=10)
    title_style = ParagraphStyle('harpo',
                               fontName="times",
                               fontSize=18,
                               parent=styles['BodyText'],
                               alignment=1,
                               spaceAfter=20)
    caption_style = ParagraphStyle('harpo',
                               fontName="times",
                               fontSize=10,
                               parent=styles['BodyText'],
                               alignment=1,
                               spaceAfter=10)
    harpo_eats_pdf = SimpleDocTemplate(
                "harpo_eats.pdf",
                pagesize=A5,
                rightMargin=72, leftMargin=72,
                topMargin=72, bottomMargin=72,
                title="Harpo Eats!"
                )


    credits = "By Harpo Marx and Raphael Halff with the help of OpenAI's <i>DALL·E 2</i> and NYPL's <i>What's on the Menu?</i>"
    paragraphs = []
    paragraphs.append(Paragraph("Harpos Eats!", style=title_style))
    paragraphs.append(Paragraph(credits, style=caption_style))

    print("Starting. Harpo's epicurean adventures are thoroughly extensive. This may take awhile. Have hope and patience.")
    is_illustrated = True
    dishes = 0
    length = 0
    for excerpt in excerpts:
        excerpt = excerpt.strip()

        image_url = ""
        prompt = ""
        round = 0
        while excerpt.count("{dish}") > 0 or \
            excerpt.count("{place}") > 0 or \
            excerpt.count("{price}") > 0:

            dish = {}
            the_dish = ""
            for i in range(int(pow(2, dishes))):
                if i == 0:
                    dish = get_dish()
                    the_dish = clean_dish(dish['dish'])
                else:
                    the_dish += clean_dish(get_dish()['dish']) + ", "
            dishes += .25

            if round == 0 and is_illustrated:
                prompt = "A woodcut of Harpo Marx eating a " + titlecase(dish['dish'])
                image_url = openai.Image.create(prompt=prompt, n=1, size="512x512")['data'][0]['url']
                round = 1

            excerpt = excerpt.replace("{dish}", titlecase(the_dish), 1)
            excerpt = excerpt.replace("{place}", titlecase(dish['place']), 1)
            while not dish['price'].strip():
                dish = get_dish()
            excerpt = excerpt.replace("{price}", price_it(dish['price']), 1)

        if is_illustrated:
            image_data = requests.get(image_url).content
            if not isdir("images"):
                mkdir("images")
            image_file = "images/" + prompt.replace(" ", "")[-25:] + ".png"
            with open(image_file, 'wb') as handler:
                handler.write(image_data)

        length += len(excerpt.split())
        paragraphs.append(Paragraph(excerpt, style=ph_style))
        if is_illustrated:
            paragraphs.append(get_image(image_file, width=200))
            paragraphs.append(Paragraph("<i>" + prompt + "</i>", style=caption_style))
    harpo_eats_pdf.build(paragraphs)

main()
print("See the reuslting file: harpo_eats.pdf")
