import questions
import matplotlib.pyplot as plt
import os

# Introductory explanation
intro_text = '''Behavior Style Test

This is an interactive questionnaire that helps you understand your personal behavior style.
You'll choose the answer that best describes you for each of the 18 questions.
You have two options to choose from each time.
Select what suits you best - NOTE! - the questions only appear once!
After answering all the questions, your dominant behavior style will be revealed.\n'''

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

class BehaviorStyleTest:
    def __init__(self):
        self.statements = {}
        self.scores = {"O": 0, "D": 0, "S": 0, "I": 0}
        self.quadrants = {
            'Relator': {'x_coords': None, 'y_coords': None},
            'Social': {'x_coords': None, 'y_coords': None},
            'Directive': {'x_coords': None, 'y_coords': None},
            'Thinker': {'x_coords': None, 'y_coords': None}
        }
        self.load_statements_from_config()

    def print_scores(self):
        print("Score Summary:")
        print(f"Thinker (I): {self.scores['I']}")
        print(f"Stable (S): {self.scores['S']}")
        print(f"Directive (D): {self.scores['D']}")
        print(f"Relator (O): {self.scores['O']}")

    def load_statements_from_config(self):
        # Import statements from the questions.py file
        for key, value in questions.Statements.items():
            statements = value["statements"]
            styles = value["styles"]
            self.statements[int(key)] = (statements, styles)

    def calculate_biggest_quadrant(self):
        dominant_quadrant = ""
        max_score = max(self.scores, key=self.scores.get)

        if max_score == "I":
            dominant_quadrant = "Thinker"
        elif max_score == "O":
            dominant_quadrant = "Relator"
        elif max_score == "D":
            dominant_quadrant = "Directive"
        elif max_score == "S":
            dominant_quadrant = "Social"

        return dominant_quadrant

    def calculate_quadrant_coordinates(self):
        for quadrant in self.quadrants:
            if quadrant == 'Relator':
                self.quadrants[quadrant]['x_coords'] = [-self.scores['I'], 0, self.scores['D'], 0]
                self.quadrants[quadrant]['y_coords'] = [0, self.scores['O'], 0, -self.scores['S']]
            elif quadrant == 'Social':
                self.quadrants[quadrant]['x_coords'] = [0, self.scores['I'], 0, -self.scores['D']]
                self.quadrants[quadrant]['y_coords'] = [-self.scores['O'], 0, self.scores['S'], 0]
            elif quadrant == 'Directive':
                self.quadrants[quadrant]['x_coords'] = [self.scores['I'], 0, -self.scores['D'], 0]
                self.quadrants[quadrant]['y_coords'] = [0, -self.scores['O'], 0, self.scores['S']]
            elif quadrant == 'Thinker':
                self.quadrants[quadrant]['x_coords'] = [0, -self.scores['I'], 0, self.scores['D']]
                self.quadrants[quadrant]['y_coords'] = [self.scores['O'], 0, -self.scores['S'], 0]

    def run_test(self):
        question_number = 1

        print(intro_text)
        input("Good luck!\n\nPress Enter to begin...")
        clear_screen()

        question_numbers = list(self.statements.keys())

        for question_num in question_numbers:
            statement_pair, styles = self.statements[question_num]
            formatted_statement_1 = statement_pair[0]
            formatted_statement_2 = statement_pair[1]

            print(f'\n      {question_number}/{len(questions.Statements)}\n')
            print(f'1.    {formatted_statement_1[0]}')
            print(f'2.    {formatted_statement_2[0]}\n')

            choice = input("Choice (1/2): ")
            question_number += 1
            clear_screen()

            try:
                chosen_styles = styles.split(',')
                chosen_answer = int(choice) - 1
                for index, style in enumerate(chosen_styles):
                    if index == chosen_answer:
                        self.scores[style] += 1
            except (ValueError, IndexError):
                print("Invalid choice. Choose 1 or 2.")
                continue

        # Calculate quadrant coordinates based on the scores
        self.calculate_quadrant_coordinates()

        ax_number = 10

        # Determine the largest quadrant
        biggest_quadrant = self.calculate_biggest_quadrant()

        # Inner lines and labels
        for i in range(1, ax_number):
            plt.plot([i, -i], [0, 0], color='gray', linestyle='dotted', linewidth=0.5)
            plt.plot([0, 0], [i, -i], color='gray', linestyle='dotted', linewidth=0.5)

        # Quadrant lines (The Grid)
        plt.plot([0, 0], [-ax_number, ax_number], color='black', linewidth=0.8)
        plt.plot([-ax_number, ax_number], [0, 0], color='black', linewidth=0.8)

        # Add labels to quadrants with references
        for label, (key, x, y) in {'Thinker': ('I', -0.5, -0.5), 'Social': ('S', 0.5, 0.5),
                                   'Directive': ('D', 0.5, -0.5), 'Relator': ('O', -0.5, 0.5)}.items():
            weight = 'bold' if label == biggest_quadrant else 'normal'
            plt.text(ax_number * x, ax_number * y, label, color='black', ha='center', va='center', fontweight=weight)

        # Plot values of I, O, D, S against inner grid
        plt.scatter(-self.scores['I'], 0)
        plt.scatter(0, self.scores['O'])
        plt.scatter(self.scores['D'], 0)
        plt.scatter(0, -self.scores['S'])

        # Connect the points in clockwise order
        plt.plot([-self.scores['I'], 0, self.scores['D'], 0, -self.scores['I']],
                 [0, self.scores['O'], 0, -self.scores['S'], 0],
                 color='black', linestyle='solid', linewidth=1)

        # Title and axis limits
        plt.title("Your behavior style is:")
        plt.xticks([])
        plt.yticks([])

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
