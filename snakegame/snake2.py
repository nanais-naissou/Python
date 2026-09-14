import turtle
import time
import random
import pygame

pygame.mixer.init()

son = pygame.mixer.Sound("musique.mp3")
nourritureson = pygame.mixer.Sound("eating.mp3")
gameoverson = pygame.mixer.Sound("gameover.mp3")

son.play(-1)

fenetre = turtle.Screen()
fenetre.title("Snake - Menu")
fenetre.setup(width=1020, height=1020)
fenetre.bgpic("snake_title.png")

modejeu = False
mode = None
jeu_actif = False

LARGEUR = 1000
HAUTEUR = 1000

VITESSE_EASY = 100
VITESSE_HARD = 60

delai = VITESSE_EASY

score = 0
meilleur_score = 0

vies = 3

tete = None
oeil_gauche = None
oeil_droit = None
nourriture = None

segments = []

texte_score = None
texte_vies = None
texte_gameover = None

mur = None

OUTLINE_COLOR = "#0a190a"
COLORS = ["#4ade80", "#facc15"]

tortues_menu = []

def fun_text(
    t,
    text,
    x,
    y,
    font_size=30,
    font_name="DejaVu Sans",
    letter_spacing=None,
    wave=6
):
    if letter_spacing is None:
        letter_spacing = font_size * 1.5

    total_width = letter_spacing * (len(text) - 1)
    start_x = x - total_width / 2

    for i, ch in enumerate(text):
        cx = start_x + i * letter_spacing
        cy = y + (wave if i % 2 == 0 else -wave)

        color = COLORS[i % len(COLORS)]

        offsets = [
            (-2, -2),
            (-2, 2),
            (2, -2),
            (2, 2),
            (-2, 0),
            (2, 0),
            (0, -2),
            (0, 2)
        ]

        for dx, dy in offsets:
            t.goto(cx + dx, cy + dy)
            t.color(OUTLINE_COLOR)

            t.write(
                ch,
                align="center",
                font=(font_name, font_size, "bold")
            )

        t.goto(cx, cy)
        t.color(color)

        t.write(
            ch,
            align="center",
            font=(font_name, font_size, "bold")
        )

bouton_easy = turtle.Turtle()
bouton_easy.penup()
bouton_easy.goto(-250, -230)
bouton_easy.shape("square")
bouton_easy.shapesize(3, 5)
bouton_easy.color("white")
bouton_easy.fillcolor("")
tortues_menu.append(bouton_easy)

bouton_hard = turtle.Turtle()
bouton_hard.penup()
bouton_hard.goto(250, -230)
bouton_hard.shape("square")
bouton_hard.shapesize(3, 5)
bouton_hard.color("white")
bouton_hard.fillcolor("")
tortues_menu.append(bouton_hard)

easytexte = turtle.Turtle()
easytexte.hideturtle()
easytexte.penup()
easytexte.speed(0)

tortues_menu.append(easytexte)

fun_text(
    easytexte,
    "EASY",
    -250,
    -270,
    font_size=30
)

hardtexte = turtle.Turtle()
hardtexte.hideturtle()
hardtexte.speed(0)
hardtexte.penup()

tortues_menu.append(hardtexte)

fun_text(
    hardtexte,
    "HARD",
    250,
    -270,
    font_size=30
)

def supprimer_menu():
    for tortue in tortues_menu:
        tortue.clear()
        tortue.hideturtle()

def haut():
    global tete

    if tete is not None:
        if tete.direction != "bas":
            tete.direction = "haut"
            tete.setheading(90)

def bas():
    global tete

    if tete is not None:
        if tete.direction != "haut":
            tete.direction = "bas"
            tete.setheading(270)

def gauche():
    global tete

    if tete is not None:
        if tete.direction != "droite":
            tete.direction = "gauche"
            tete.setheading(180)

def droite():
    global tete

    if tete is not None:
        if tete.direction != "gauche":
            tete.direction = "droite"
            tete.setheading(0)

def avancer():
    if tete.direction == "haut":
        tete.sety(tete.ycor() + 20)
    elif tete.direction == "bas":
        tete.sety(tete.ycor() - 20)
    elif tete.direction == "gauche":
        tete.setx(tete.xcor() - 20)
    elif tete.direction == "droite":
        tete.setx(tete.xcor() + 20)

def mettre_a_jour_yeux():
    x = tete.xcor()
    y = tete.ycor()

    if tete.direction == "droite":
        oeil_gauche.goto(x + 8, y + 8)
        oeil_droit.goto(x + 8, y - 8)
    elif tete.direction == "gauche":
        oeil_gauche.goto(x - 8, y + 8)
        oeil_droit.goto(x - 8, y - 8)
    elif tete.direction == "haut":
        oeil_gauche.goto(x - 8, y + 8)
        oeil_droit.goto(x + 8, y + 8)
    elif tete.direction == "bas":
        oeil_gauche.goto(x - 8, y - 8)
        oeil_droit.goto(x + 8, y - 8)

def afficher_vies():
    texte_vies.clear()
    texte_vies.goto(-460, 420)

    coeurs = ""

    for i in range(vies):
        coeurs += "♥ "

    texte_vies.write(
        coeurs,
        align="left",
        font=("Arial", 30, "bold")
    )

def afficher_score():
    texte_score.clear()

    texte_score.write(
        f"Score : {score}    Meilleur score : {meilleur_score}",
        align="center",
        font=("Arial", 14, "bold")
    )

def perdre_une_vie():
    global vies
    global score

    vies -= 1

    gameoverson.play()

    afficher_vies()

    for segment in segments:
        segment.goto(2000, 2000)

    segments.clear()

    tete.goto(0, 0)

    tete.direction = "stop"

    mettre_a_jour_yeux()

    score = 0

    afficher_score()

    fenetre.update()

    if vies <= 0:
        afficher_game_over()
        return True

    return False

def afficher_game_over():
    global jeu_actif

    jeu_actif = False

    texte_gameover.clear()

    texte_gameover.write(
        "GAME OVER !",
        align="center",
        font=("Arial", 50, "bold")
    )

    fenetre.update()

def manger():
    global score
    global meilleur_score

    nourritureson.play()

    x = random.randint(-19, 19) * 20
    y = random.randint(-19, 19) * 20

    nourriture.goto(x, y)

    nouveau_segment = turtle.Turtle()

    nouveau_segment.speed(0)
    nouveau_segment.shape("circle")
    nouveau_segment.color("green")
    nouveau_segment.shapesize(1.5)
    nouveau_segment.penup()

    segments.append(nouveau_segment)

    score += 10

    if score > meilleur_score:
        meilleur_score = score

    afficher_score()

def collision_corps():
    for segment in segments[1:]:
        if tete.distance(segment) < 20:
            return True

    return False

def boucle_jeu():
    global jeu_actif

    if not jeu_actif:
        return

    for i in range(len(segments) - 1, 0, -1):
        x = segments[i - 1].xcor()
        y = segments[i - 1].ycor()

        segments[i].goto(x, y)

    if len(segments) > 0:
        segments[0].goto(
            tete.xcor(),
            tete.ycor()
        )

    avancer()

    mettre_a_jour_yeux()

    collision_mur = (
        tete.xcor() > LARGEUR / 2 - 10
        or tete.xcor() < -LARGEUR / 2 + 10
        or tete.ycor() > HAUTEUR / 2 - 10
        or tete.ycor() < -HAUTEUR / 2 + 10
    )

    if collision_mur:
        game_over = perdre_une_vie()

        if game_over:
            return

    if tete.distance(nourriture) < 40:
        manger()

    if collision_corps():
        game_over = perdre_une_vie()

        if game_over:
            return

    fenetre.update()

    fenetre.ontimer(boucle_jeu, delai)

def demarrer_jeu(difficulte):
    global modejeu
    global mode
    global jeu_actif
    global tete
    global oeil_gauche
    global oeil_droit
    global nourriture
    global segments
    global score
    global vies
    global meilleur_score
    global texte_score
    global texte_vies
    global texte_gameover
    global mur
    global delai

    modejeu = True
    mode = difficulte
    jeu_actif = True

    if mode == "easy":
        delai = VITESSE_EASY
    elif mode == "hard":
        delai = VITESSE_HARD

    supprimer_menu()

    fenetre.title("Snake")

    fenetre.setup(width=1020, height=1020)

    fenetre.bgpic("snakess.png")

    fenetre.addshape("pomme.png")

    fenetre.tracer(0)

    mur = turtle.Turtle()

    mur.speed(0)
    mur.color("black")
    mur.pensize(20)
    mur.penup()

    mur.goto(
        -LARGEUR / 2,
        -HAUTEUR / 2
    )

    mur.pendown()

    for i in range(2):
        mur.forward(LARGEUR)
        mur.left(90)

        mur.forward(HAUTEUR)
        mur.left(90)

    mur.hideturtle()

    tete = turtle.Turtle()

    tete.speed(0)
    tete.shape("circle")
    tete.shapesize(2)
    tete.color("dark green")
    tete.penup()

    tete.goto(0, 0)

    tete.direction = "stop"

    oeil_gauche = turtle.Turtle()

    oeil_gauche.speed(0)
    oeil_gauche.shape("circle")
    oeil_gauche.color("white")
    oeil_gauche.shapesize(0.3, 0.3)
    oeil_gauche.penup()

    oeil_droit = turtle.Turtle()

    oeil_droit.speed(0)
    oeil_droit.shape("circle")
    oeil_droit.color("white")
    oeil_droit.shapesize(0.3, 0.3)
    oeil_droit.penup()

    mettre_a_jour_yeux()

    nourriture = turtle.Turtle()

    nourriture.speed(0)
    nourriture.shape("pomme.png")
    nourriture.penup()

    nourriture.goto(0, 100)

    segments = []

    score = 0

    texte_score = turtle.Turtle()

    texte_score.speed(0)
    texte_score.color("red")
    texte_score.penup()
    texte_score.hideturtle()

    texte_score.goto(250, 450)

    vies = 3

    texte_vies = turtle.Turtle()

    texte_vies.speed(0)
    texte_vies.color("red")
    texte_vies.penup()
    texte_vies.hideturtle()

    texte_vies.goto(0, 450)

    texte_gameover = turtle.Turtle()

    texte_gameover.speed(0)
    texte_gameover.color("red")
    texte_gameover.penup()
    texte_gameover.hideturtle()

    texte_gameover.goto(0, 0)

    afficher_score()
    afficher_vies()

    fenetre.listen()

    fenetre.onkeypress(haut, "Up")
    fenetre.onkeypress(bas, "Down")
    fenetre.onkeypress(gauche, "Left")
    fenetre.onkeypress(droite, "Right")

    fenetre.update()

    fenetre.ontimer(boucle_jeu, delai)

def easy_mode(x, y):
    demarrer_jeu("easy")

def hard_mode(x, y):
    demarrer_jeu("hard")

bouton_easy.onclick(easy_mode)
bouton_hard.onclick(hard_mode)

fenetre.listen()

fenetre.mainloop()