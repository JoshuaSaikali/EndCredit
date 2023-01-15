# Student ID: 101238835
# Name: Joshua Saikali
import pygame

pygame.font.init()
# initializing font and defining constants
FONT_TYPE = pygame.font.Font('starwars1.ttf', 30)
BLUE = (255, 232, 31)
BACKGROUND = pygame.image.load("background.jpg")
SCREEN = pygame.display.set_mode((1400, 900))
SCREEN_RECT = SCREEN.get_rect()


def get_credit_file():
    # read each line of the file and puts it into a list
    # returns the list
    try:
        filehandler = open("end_credits.txt", "r")
        data = []
        line = filehandler.readline()
        cnt = 1
        while line:
            data.append(line.strip("\n"))
            line = filehandler.readline()
            cnt += 1
        filehandler.close()
        return data
    except FileNotFoundError:
        print("No File Found")
    except:
        print("An error has occured... Terminating.")
        exit()


def render_font(credits, posY, centerx, centery, credit_text_list, pos_list, counter):
    # creates a list for the font and appends each element in the credits list
    # creates a position list for the corresponding fonts in the font list
    for line in credits:
        credit_text = FONT_TYPE.render(line, True, BLUE)
        credit_text_list.append(credit_text)
        pos = credit_text.get_rect(center=(centerx, centery+posY+60*counter))
        pos_list.append(pos)
        counter += 1
    return credit_text_list, pos_list, counter


def save_credits(i, last_line):
    # Checks if the last line was a space, if so it goes to the next one
    # creates a file if there isnt one and writes the last line
    while last_line[i] == "":
        print("Worked")
        i += 1
    try:
        filehandler = open("last_line.txt", "w")
        filehandler.seek(0)
        filehandler.write(last_line[i])
        filehandler.close()
    except:
        print("An error has occured... Cannot save credits.\nTerminating...")


def read_saved_credits():
    # reads the file with the last line in it
    # if there is no file then it returns false
    # returns the line if its true
    try:
        filehandler = open("last_line.txt", "r")
        line = filehandler.readline()
        return True, line
    except FileNotFoundError:
        return False
    except:
        print("An error has occured... Terminating...")
        exit()


def get_saved_line(line, credits):
    # returns the index at where the last line is
    return credits.index(line)


def main():
    # loads the credits file
    # checks if there is a saved file
    # if true it resumes if not it restarts the credits
    credits = get_credit_file()
    if read_saved_credits():
        _, line = read_saved_credits()
        index = get_saved_line(line, credits)
        credits = credits[index:]

    centerx, centery = SCREEN.get_rect().centerx, SCREEN.get_rect().centery
    posY = centery + 50
    pos_of_line = 0

    # while loop that continuously blits the font to the screen
    while True:
        SCREEN.blit(BACKGROUND, (0, 0))

        posY -= 1
        credit_text_list = []
        pos_list = []
        counter = 0

        credit_text_list, pos_list, counter = render_font(
            credits, posY, centerx, centery, credit_text_list, pos_list, counter)

        # checks if the credits are done (off the screen)
        if (centery + posY + 60*(len(credits)) < 0):
            exit()

        # this loop blits the font at the corresponding positions in the lists
        # it gets the y position of the font and if it is in the middle of the screen
        # the index is set to the position of the last line (line in the middle of the screen)
        for j in range(counter):
            SCREEN.blit(credit_text_list[j], pos_list[j])
            (_, y, _, _) = pos_list[j]
            if y > centery - 50 and y < centery + 50:
                pos_of_line = j

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # if the user quits it calls the save credits function
                # using the position of the last line and the original credits list
                save_credits(pos_of_line, credits)
                exit()

        pygame.time.delay(10)
        pygame.display.update()


main()
