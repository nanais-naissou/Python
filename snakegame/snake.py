import turtle
import time
import random

fenetre = turtle.Screen()
fenetre.title("Snake")

#fenetre.bgcolor("dark green")
fenetre.setup(width=1020, height=1020)
fenetre.bgpic("snakess.png")
fenetre.addshape("pomme.png")

fenetre.tracer(1)


# Dimensions des vrais murs
LARGEUR = 1000
HAUTEUR = 1000


# =========================
# DESSIN DES MURS
# =========================

mur = turtle.Turtle()
mur.speed(10)
mur.color("black")
mur.pensize(20)
mur.penup()

mur.goto(-LARGEUR / 2, -HAUTEUR / 2)
mur.pendown()

for i in range(2):
    mur.forward(LARGEUR)
    mur.left(90)
    mur.forward(HAUTEUR)
    mur.left(90)

mur.hideturtle()
fenetre.tracer(0)

tete = turtle.Turtle()
tete.speed(0)
tete.shape("circle")
tete.shapesize(2)
tete.color("dark green")
tete.penup()
tete.goto(0, 0)

tete.direction = "stop"

oeil_gauche = turtle.Turtle()
oeil_gauche.shape("circle")
oeil_gauche.color("white")
oeil_gauche.shapesize(0.3, 0.3)
oeil_gauche.penup()

oeil_droit = turtle.Turtle()
oeil_droit.shape("circle")
oeil_droit.color("white")
oeil_droit.shapesize(0.3, 0.3)
oeil_droit.penup()

# =========================
# NOURRITURE
# =========================

nourriture = turtle.Turtle()
nourriture.speed(0)
nourriture.shape("pomme.png")
nourriture.penup()
nourriture.goto(0, 100)


# =========================
# CORPS DU SERPENT
# =========================

segments = []


# =========================
# SCORE
# =========================

score = 0
meilleur_score = 0


texte = turtle.Turtle()
texte.speed(0)
texte.color("red")
texte.penup()
texte.hideturtle()
texte.goto(250, 450)

text = turtle.Turtle()
text.speed(0)
text.color("red")
text.penup()
text.hideturtle()
text.goto(0, 0)

texte.write(
    "Score : 0    Meilleur score : 0",
    align="center",
    font=("Arial", 10, "bold"))

# =========================
# DÉPLACEMENT
# =========================

def haut():

    if tete.direction != "bas":
        tete.direction = "haut"
        tete.setheading(90)



def bas():

    if tete.direction != "haut":
        tete.direction = "bas"
        tete.setheading(270)



def gauche():

    if tete.direction != "droite":
        tete.direction = "gauche"
        tete.setheading(180)



def droite():

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

    else:
        oeil_gauche.goto(x - 8, y + 8)
        oeil_droit.goto(x + 8, y + 8)

# =========================
# TOUCHES DU CLAVIER
# =========================

fenetre.listen()

fenetre.onkeypress(haut, "Up")
fenetre.onkeypress(bas, "Down")
fenetre.onkeypress(gauche, "Left")
fenetre.onkeypress(droite, "Right")


# =========================
# BOUCLE PRINCIPALE
# =========================

while True:

    # -------------------------
    # DÉPLACER LE CORPS
    # -------------------------

    for i in range(len(segments) - 1, 0, -1):

        x = segments[i - 1].xcor()
        y = segments[i - 1].ycor()

        segments[i].goto(x, y)


    # Le premier segment suit la tête

    if len(segments) > 0:

        segments[0].goto(
            tete.xcor(),
            tete.ycor()
        )


    # -------------------------
    # DÉPLACER LA TÊTE
    # -------------------------

    avancer()
    mettre_a_jour_yeux()

    # -------------------------
    # COLLISION AVEC LES MURS
    # -------------------------

    if (
        tete.xcor() > LARGEUR / 2 - 10
        or tete.xcor() < -LARGEUR / 2 + 10
        or tete.ycor() > HAUTEUR / 2 - 10
        or tete.ycor() < -HAUTEUR / 2 + 10
    ):

        text.write(
            f"GAME OVER !",
            align="center",
            font=("Arial", 50, "bold")
        )
        fenetre.update()
        
        time.sleep(1)
        text.clear()
        tete.goto(0, 0)
        tete.direction = "stop"

        for segment in segments:
            segment.goto(1000, 1000)

        segments.clear()

        score = 0

        texte.clear()

        texte.write(
            f"Score : {score}    Meilleur score : {meilleur_score}",
            align="center",
            font=("Arial", 10, "bold")
        )


    # -------------------------
    # MANGER LA NOURRITURE
    # -------------------------

    if tete.distance(nourriture) < 40:

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


        texte.clear()

        texte.write(
            f"Score : {score}    Meilleur score : {meilleur_score}",
            align="center",
            font=("Arial", 10, "bold")
        )


    # -------------------------
    # COLLISION AVEC LE CORPS
    # -------------------------

    for segment in segments[1:]:

        if tete.distance(segment) < 20:

            text.write(
                f"GAME OVER !",
                align="center",
                font=("Arial", 50, "bold")
            )
            fenetre.update()
            
            time.sleep(1)
            text.clear()
            tete.goto(0, 0)
            tete.direction = "stop"

            for segment in segments:
                segment.goto(1000, 1000)

            segments.clear()

            score = 0

            texte.clear()

            texte.write(
                f"Score : {score}    Meilleur score : {meilleur_score}",
                align="center",
                font=("Arial", 10, "bold")
            )


    # -------------------------
    # RAFRAÎCHIR L'ÉCRAN
    # -------------------------

    fenetre.update()

    time.sleep(0.05)