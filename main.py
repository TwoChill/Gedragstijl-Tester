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

    def print_scores(self):
        print("Tally of scores:")
        print(f"Denker (I): {self.scores['I']}")
        print(f"Stabiel (S): {self.scores['S']}")
        print(f"Dominant (D): {self.scores['D']}")
        print(f"Relator (O): {self.scores['O']}")

    def load_statements_from_config(self):
        # Importing statements directly from the questions.py file
        for key, value in questions.Statements.items():
            statements = value["statements"]
            styles = value["styles"]
            self.statements[int(key)] = (statements, styles)

    def run_test(self):
        ax_number = 18
        question_number = 1

        print(intro_uitleg)
        input("Veel succes!\n\nDruk op Enter om te beginnen...")
        clear_screen(intro_uitleg)

        selected_styles = {'I': 'RELATOR', 'S': 'SOCIAAL', 'D': 'DIRECTIEF', 'O': 'DENKER'}
        style_colors = {'I': 'black', 'S': 'black', 'D': 'black', 'O': 'black'}

        question_numbers = list(self.statements.keys())

        for question_num in question_numbers:
            statement_pair, styles = self.statements[question_num]
            formatted_statement_1 = statement_pair[0]
            formatted_statement_2 = statement_pair[1]
            formatted_output = f'{question_number}/{len(questions.Statements)}\n\n1.    {formatted_statement_1[0]}\n' \
                               f'2.    {formatted_statement_2[0]}\n'
            print(formatted_output)
            choice = input("Keuze (1/2): ")
            question_number += 1
            clear_screen(intro_uitleg)

            try:
                chosen_styles = styles.split(',')
                chosen_answer = int(choice) - 1
                for index, style in enumerate(chosen_styles):
                    if index == chosen_answer:
                        self.scores[style] += 1
            except (ValueError, IndexError):
                print("Ongeldige keuze. Kies 1 of 2.")
                continue

        ax_number = 10  # Change this value as needed

        # Inner lines and labels
        for i in range(1, ax_number):
            plt.plot([i, -i], [0, 0], color='gray', linestyle='dotted', linewidth=0.5)
            plt.plot([0, 0], [i, -i], color='gray', linestyle='dotted', linewidth=0.5)

        # Quadrant lines (The Grid)
        plt.plot([0, 0], [-ax_number, ax_number], color='black', linewidth=0.8)  # Vertical line at x=0
        plt.plot([-ax_number, ax_number], [0, 0], color='black', linewidth=0.8)  # Horizontal line at y=0

        # Calculate the maximum score and corresponding style
        max_score = max(self.scores.values())
        dominante_gedragsstijl = max(self.scores, key=self.scores.get)

        # Determine the style with the longest line
        longest_line_style = None
        longest_line_length = 0
        for style in self.scores:
            if self.scores[style] == max_score:
                if style == 'I':
                    line_length = self.scores['I'] - self.scores['D']
                elif style == 'O':
                    line_length = self.scores['O'] - self.scores['S']
                elif style == 'D':
                    line_length = self.scores['D'] - self.scores['I']
                elif style == 'S':
                    line_length = self.scores['S'] - self.scores['O']

                if line_length > longest_line_length:
                    longest_line_length = line_length
                    longest_line_style = style

        # Add labels to quadrants with conditional font weight
        for label, (key, x, y) in {'SOCIAAL': ('S', 0.6, 0.6), 'DIRECTIEF': ('D', -0.6, 0.6),
                                   'DENKER': ('I', -0.6, -0.6), 'RELATOR': ('O', 0.6, -0.6)}.items():
            weight = 'bold' if key == longest_line_style else 'normal'
            plt.text(ax_number * x, ax_number * y, label, color='black', ha='center', va='center', fontweight=weight)

        # Plot values of I, O, D, S against inner grid
        plt.scatter(-self.scores['I'], 0)
        plt.scatter(0, -self.scores['O'])
        plt.scatter(self.scores['D'], 0)
        plt.scatter(0, self.scores['S'])

        # Connect the points in clockwise order
        plt.plot([-self.scores['I'], 0, self.scores['D'], 0, -self.scores['I']],
                 [0, -self.scores['O'], 0, self.scores['S'], 0],
                 color='black', linestyle='-', linewidth=1)

        # Title and axis limits
        plt.title("Jouw gedragstijl is:")
        plt.xticks([])  # Hide tick labels on x-axis
        plt.yticks([])  # Hide tick labels on y-axis

        # Add numbers to the middle of the grid lines
        for i in range(1, ax_number):
            plt.text(i, -0.5, str(i), color='black', ha='center', va='center')
            plt.text(-i, -0.5, str(i), color='black', ha='center', va='center')
            plt.text(-0.5, i, str(i), color='black', ha='center', va='center')
            plt.text(-0.5, -i, str(i), color='black', ha='center', va='center')

        plt.xlim(-ax_number, ax_number)
        plt.ylim(-ax_number, ax_number)
        plt.show()


if __name__ == "__main__":
    test = BehaviorStyleTest()
    test.run_test()
