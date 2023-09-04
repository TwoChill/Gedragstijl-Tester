import questions, descriptions
import textwrap
import matplotlib.pyplot as plt
import os

# Introductory explanation
intro_text = '''Behavior Style Test

Welcome to the Behavior Style Assessment!

This interactive questionnaire is designed to provide insights into your unique behavior style. 
For each of the 18 questions, select the answer that most accurately reflects you.
Keep in mind that each question is presented only once.
You'll have two options to choose from on each question, so pick the one that resonates with you the most.
Once you've completed all the questions, your dominant behavior style will be unveiled.\n'''


def clear_screen():
    """Clear the screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def make_bold(text):
    return "\033[1m" + text + "\033[0m"

def print_behavior_style_results(text, max_line_width=100):
    # Split the text into paragraphs
    paragraphs = text.split(' .')  # Assume paragraphs are separated by two newlines
    for paragraph in paragraphs:
        wrapped_lines = textwrap.wrap(paragraph, width=max_line_width)
        for lines in wrapped_lines:
            print(lines)

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

    def load_statements_from_config(self):
        """Load the statements from the config file."""
        # Import statements from the questions.py file
        for key, value in questions.Statements.items():
            statements = value["statements"]
            styles = value["styles"]
            self.statements[int(key)] = (statements, styles)

    def get_dominant_styles(self):
        """Determine the dominant quadrant."""
        # Define a dictionary to map quadrant scores to names
        quadrant_names = {
            'Relator': self.scores['I'] * self.scores['O'],
            'Social': self.scores['O'] * self.scores['D'],
            'Directive': self.scores['D'] * self.scores['S'],
            'Thinker': self.scores['S'] * self.scores['I']
        }
        # Determine the dominant quadrant using the max function
        dominant_style = max(quadrant_names, key=quadrant_names.get)

        return dominant_style

    def calculate_quadrant_coordinates(self):
        """Calculate the quadrant coordinates and add them to the quadrants dictionary."""
        for quadrant in self.quadrants:
            if quadrant == 'Relator':
                self.quadrants[quadrant]['x_coords'] = [-self.scores['I'],
                                                        0, self.scores['D'], 0]
                self.quadrants[quadrant]['y_coords'] = [
                    0, self.scores['O'], 0, -self.scores['S']]
            elif quadrant == 'Social':
                self.quadrants[quadrant]['x_coords'] = [
                    0, self.scores['I'], 0, -self.scores['D']]
                self.quadrants[quadrant]['y_coords'] = [-self.scores['O'],
                                                        0, self.scores['S'], 0]
            elif quadrant == 'Directive':
                self.quadrants[quadrant]['x_coords'] = [
                    self.scores['I'], 0, -self.scores['D'], 0]
                self.quadrants[quadrant]['y_coords'] = [
                    0, -self.scores['O'], 0, self.scores['S']]
            elif quadrant == 'Thinker':
                self.quadrants[quadrant]['x_coords'] = [
                    0, -self.scores['I'], 0, self.scores['D']]
                self.quadrants[quadrant]['y_coords'] = [
                    self.scores['O'], 0, -self.scores['S'], 0]


    def show_behavior_results(self, dominant_styles):
        """Display detailed information about a behavior style."""

        # Check if key exists in dictionary 'unique_descriptions'
        behavior_data = explanation.unique_descriptions.get(dominant_styles)

        if behavior_data is None:
            print("Behavior style not found.")
            return

        # Assuming you have a clear_screen() function to clear the screen.
        clear_screen()

        # Print the description
        print(make_bold(dominant_styles) + "\n")

        # Print description of behavior
        print_behavior_style_results(behavior_data['Description'])

        # Create space between description and questions
        print()

        # Print core qualities
        print(make_bold("Core Qualities:"))
        for quality in behavior_data['Core Qualities']:
            print(quality)
        print()

        # Print pitfalls
        print(make_bold("Pitfalls:"))
        for pitfall in behavior_data['Pitfalls']:
            print(pitfall)
        print()

        # Print challenges
        print(make_bold("Challenges:"))
        for challenge in behavior_data['Challenges']:
            print(challenge)
        print()

        # Print allergies
        print(make_bold("Allergies:"))
        for allergy in behavior_data['Allergies']:
            print(allergy)
        print()

    def behavior_style_assesment(self):
        """
        Runs the test for the user.

        This function displays the intro text and waits for the user to press Enter to begin the test.
        It then iterates through each question, displays the question number and the two formatted statements.
        The user is prompted to choose either option 1 or option 2.
        The chosen answer is recorded and the scores for the corresponding styles are updated.
        If an invalid choice is made, the user is prompted to choose again.
        After all questions have been answered, the quadrant coordinates are calculated based on the scores.
        The largest quadrant is determined and the inner lines and labels are plotted.
        The values of I, O, D, S are plotted against the inner grid.
        The points are connected in clockwise order to form a shape.
        The title, axis limits, and numbers for the middle of the grid lines are added.
        Finally, the plot is displayed.
        """

        print(intro_text)
        input("Good luck!\n\nPress Enter to begin...")
        clear_screen()

        question_number = 1
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
                # Update scores
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

        # Determine the number visible on the axis
        num_on_axis = 10

        # Determine the largest quadrant
        dominant_styles = self.get_dominant_styles()

        # Show the results
        self.show_behavior_results(dominant_styles)

        # Inner lines and labels
        for i in range(1, num_on_axis):
            plt.plot([i, -i], [0, 0], color='gray',
                     linestyle='dotted', linewidth=0.5)
            plt.plot([0, 0], [i, -i], color='gray',
                     linestyle='dotted', linewidth=0.5)

        # Quadrant lines (The Grid)
        plt.plot([0, 0], [-num_on_axis, num_on_axis],
                 color='black', linewidth=0.8)
        plt.plot([-num_on_axis, num_on_axis], [0, 0],
                 color='black', linewidth=0.8)

        # Split the dominant_styles string into a list
        dominant_styles_list = dominant_styles.split('-')

        # Add labels to quadrants with references
        for label, (key, x, y) in {'Thinker': ('I', -0.5, -0.5), 'Social': ('S', 0.5, 0.5),
                                   'Directive': ('D', 0.5, -0.5), 'Relator': ('O', -0.5, 0.5)}.items():
            # Check if the current label is the same as the first style in dominant_styles_list
            weight = 'bold' if label == dominant_styles_list[0] else 'normal'
            plt.text(num_on_axis * x, num_on_axis * y, label,
                     color='black', ha='center', va='center', fontweight=weight)

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
        for i in range(1, num_on_axis):
            plt.text(i, -0.5, str(i), color='black', ha='center', va='center')
            plt.text(-i, -0.5, str(i), color='black', ha='center', va='center')
            plt.text(-0.5, i, str(i), color='black', ha='center', va='center')
            plt.text(-0.5, -i, str(i), color='black', ha='center', va='center')

        plt.xlim(-num_on_axis, num_on_axis)
        plt.ylim(-num_on_axis, num_on_axis)
        plt.show()

# Run the test
if __name__ == "__main__":
    run = BehaviorStyleTest()
    run.behavior_style_assesment()
