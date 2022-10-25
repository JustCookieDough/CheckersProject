import pygame as p, Variables as Var

PANEL_HEIGHT = Var.NUM_OF_SQUARES * Var.SQ_SIZE
PANEL_WIDTH = Var.STAT_PANEL_WIDTH

def drawPanel(screen, stats):  # function that draws the text in the ingredients
    if type(stats) == str:
        stats = stats.split("\n")  # splits text input into a list separated on the new lines
    p.draw.rect(screen, (147, 237, 255), ((Var.NUM_OF_SQUARES * Var.SQ_SIZE, 0, PANEL_WIDTH, PANEL_HEIGHT)))  # draws the actual panel
    font = p.font.SysFont("Courier New", 15, True)  # loads the font
    i = 0
    for stat in stats:  # renders each line individually
        tempText = font.render(stat, True, (0, 0, 0))
        screen.blit(tempText, ((Var.NUM_OF_SQUARES * Var.SQ_SIZE), i*15))
        i += 1