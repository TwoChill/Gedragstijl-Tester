# Importing statements from the questions.py file
import questions
import matplotlib.pyplot as plt
import os
import random

# Introductory explanation
intro_uitleg = '''Vragentest over gedragsstijl

Dit is een interactieve vragentest die je helpt inzicht te krijgen in je persoonlijke gedragsstijl.
Bij elke van de 18 vragen kies je het antwoord dat het beste bij je past.
Je hebt telkens twee opties waaruit je kunt kiezen.
Kies wat het beste bij je past - LET OP! - de vragen komen maar één keer voor!
Na het beantwoorden van alle vragen zal jouw dominante gedragsstijl worden aangegeven.\n'''


# Clear screen function for different platforms
def clear_screen(permanent_print_statement):
    os.system('cls' if os.name == 'nt' else 'clear')
    print(permanent_print_statement)

# Creating the BehaviorStyleTest class
class BehaviorStyleTest:
    def __init__(self):
        self.statements = {}
        self.scores = {"O": 0, "S": 0, "I": 0, "D": 0}
        self.load_statements_from_config()

    def load_statements_from_config(self):
        # Importing statements directly from the questions.py file
        for key, value in questions.Statements.items():
            statements = value["statements"]
            styles = value["styles"]
            self.statements[int(key)] = (statements, styles)

    def run_test(self):
        question_number = 1

        print(intro_uitleg)
        input("Veel succes!\n\nDruk op Enter om te beginnen...")
        clear_screen(intro_uitleg[289:])

        selected_styles = {'I': 'RELATOR', 'S': 'SOCIAAL', 'D': 'DIRECTIEF', 'O': 'DENKER'}
        style_colors = {'I': 'red', 'S': 'yellow', 'D': 'green', 'O': 'blue'}
        axis_labels = {'I': 'Introvert', 'S': 'Stabiel', 'D': 'Dominant', 'O': 'Outgoing'}

        # Loop through statements in random order
        question_numbers = list(self.statements.keys())
        random.shuffle(question_numbers)
        for question_num in question_numbers:
            statement_pair, styles = self.statements[question_num]
            formatted_statement_1 = statement_pair[0]
            formatted_statement_2 = statement_pair[1]
            formatted_output = f'{question_number}/{len(questions.Statements)}\n\n1.    {formatted_statement_1[0]}\n' \
                               f'2.    {formatted_statement_2[0]}\n'
            print(formatted_output)
            choice = input("Keuze (1/2): ")
            question_number += 1
            clear_screen(intro_uitleg[289:])

            try:
                chosen_styles = styles.split(',')
                for style in chosen_styles:
                    self.scores[style] += 1
            except (ValueError, IndexError):
                print("Ongeldige keuze. Kies 1 of 2.")
                continue


        # Create the plot
        plt.figure()
        plt.xlabel('I')
        plt.ylabel('S')
        plt.plot([self.scores['I'], self.scores['O']], [self.scores['S'], self.scores['S']],
                 color=style_colors['S'])
        plt.plot([self.scores['I'], self.scores['I']], [self.scores['S'], self.scores['D']],
                 color=style_colors['D'])
        plt.plot([self.scores['O'], self.scores['O']], [self.scores['S'], self.scores['I']],
                 color=style_colors['I'])
        plt.plot([self.scores['O'], self.scores['I']], [self.scores['I'], self.scores['I']],
                 color=style_colors['O'])

        # Highlight quadrant with highest score
        max_style = max(self.scores, key=self.scores.get)
        plt.fill([self.scores['I'], self.scores['O'], self.scores['O'], self.scores['I']],
                 [self.scores['S'], self.scores['S'], self.scores['D'], self.scores['I']],
                 color=style_colors[max_style], alpha=0.5)

        # Add labels to quadrants
        for style, (x, y) in self.scores.items():
            plt.text(x, y, selected_styles[style], color=style_colors[style], ha='center', va='center')

        plt.title("Gedragsstijl Grafiek")
        plt.xlim(0, 18)
        plt.ylim(0, 18)
        plt.show()

if __name__ == "__main__":
    test = BehaviorStyleTest()
    test.run_test()