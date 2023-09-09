import questions, descriptions
import textwrap
import matplotlib.pyplot as plt
import os

# Introductory explanation
intro_message = '''
Welcome to the Behavior Style Assessment!

This interactive questionnaire is designed to provide insights into your unique behavior style. 
For each of the 18 questions, select the answer that most accurately reflects you.
Keep in mind that each question is presented only once.
You'll have two options to choose from on each question, so pick the one that resonates with you the most.
Once you've completed all the questions, your dominant behavior style will be unveiled.\n'''

title = 'Behavior Style Test'

def clear_screen(text=None):
    """
    Clear the screen and optionally display text.

    Args:
        text (str, optional): Text to display after clearing the screen.

    Returns:
        None
    """

    # Clear the screen
    os.system('cls' if os.name == 'nt' else 'clear')
    if text:
        print(make_bold(text))

def make_bold(text):
    """
    Make the given text bold.

    Args:
        text (str): The text to be made bold.

    Returns:
        str: The input text wrapped in bold tags.
    """

    return "\033[1m" + text + "\033[0m"

def print_behavior_style_results(text, max_paragraph_width=100):
    """
    Print text with line wrapping.

    Args:
        text (str): The text to be printed.
        max_paragraph_width (int, optional): Maximum line width for wrapping. Default is 100.

    Returns:
        None
    """

    # Split the text into paragraphs
    paragraphs = text.split(' .')  # Assume paragraphs are separated by two newlines
    for paragraph in paragraphs:
        wrapped_lines = textwrap.wrap(paragraph, width=max_paragraph_width)
        for lines in wrapped_lines:
            print(lines)

class BehaviorStyleTest:
    def __init__(self):
        self.statements = {}
        self.scores = {"O": 0, "D": 0, "S": 0, "I": 0}
        self.quadrants = {
            'Relator': {'x_coordinates': None, 'y_coordinates': None},
            'Social': {'x_coordinates': None, 'y_coordinates': None},
            'Directive': {'x_coordinates': None, 'y_coordinates': None},
            'Thinker': {'x_coordinates': None, 'y_coordinates': None}
        }
        self.load_statements_from_config()

    def load_statements_from_config(self):
        """
        Load behavior statements from a configuration file.

        Loads statements and associated styles into the 'statements' dictionary.
        """

        """Load the statements from the config file."""
        # Import statements from the questions.py file
        for key, value in questions.Question_Statements.items():
            statements = value["question_statement"]
            styles = value["styles"]
            self.statements[int(key)] = (statements, styles)

    def get_dominant_styles(self):
        """Determine the dominant behavior style quadrant.

    Returns:
        str: The name of the dominant behavior style quadrant."""

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
        """
        Calculate the coordinates of behavior style quadrants.

        Populates the 'quadrants' dictionary with x and y coordinates for each quadrant.
        """

        # Populate the quadrants
        for quadrant in self.quadrants:
            if quadrant == 'Relator':
                self.quadrants[quadrant]['x_coordinates'] = [-self.scores['I'],
                                                        0, self.scores['D'], 0]
                self.quadrants[quadrant]['y_coordinates'] = [
                    0, self.scores['O'], 0, -self.scores['S']]
            elif quadrant == 'Social':
                self.quadrants[quadrant]['x_coordinates'] = [
                    0, self.scores['I'], 0, -self.scores['D']]
                self.quadrants[quadrant]['y_coordinates'] = [-self.scores['O'],
                                                        0, self.scores['S'], 0]
            elif quadrant == 'Directive':
                self.quadrants[quadrant]['x_coordinates'] = [
                    self.scores['I'], 0, -self.scores['D'], 0]
                self.quadrants[quadrant]['y_coordinates'] = [
                    0, -self.scores['O'], 0, self.scores['S']]
            elif quadrant == 'Thinker':
                self.quadrants[quadrant]['x_coordinates'] = [
                    0, -self.scores['I'], 0, self.scores['D']]
                self.quadrants[quadrant]['y_coordinates'] = [
                    self.scores['O'], 0, -self.scores['S'], 0]


    def show_behavior_results(self, dominant_styles):
        """Display detailed information about a behavior style."""

        # Check if key exists in dictionary 'unique_descriptions'
        dominant_style_data = descriptions.unique_descriptions.get(dominant_styles)

        # Check if key exists in dictionary: 'unique_descriptions'
        if dominant_style_data is None:
            print(make_bold("Behavior style not found."))
            return

        # Assuming you have a clear_screen(title) function to clear the screen.
        clear_screen(title)

        # Print the description
        print(make_bold(dominant_styles) + "\n")

        # Print description of behavior
        print_behavior_style_results(dominant_style_data['Description'])

        # Create space between description and questions
        print()

        # Print core qualities
        print(make_bold("Core Qualities:"))
        for core_quality in dominant_style_data['Core Qualities']:
            print(core_quality)
        print()

        # Print pitfalls
        print(make_bold("Pitfalls:"))
        for pitfall_description in dominant_style_data['Pitfalls']:
            print(pitfall_description)
        print()

        # Print challenges
        print(make_bold("Challenges:"))
        for challenge_description in dominant_style_data['Challenges']:
            print(challenge_description)
        print()

        # Print allergies
        print(make_bold("Allergies:"))
        for allergy_description in dominant_style_data['Allergies']:
            print(allergy_description)
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

        print(intro_message)
        input("Good luck!\n\nPress Enter to begin...")
        clear_screen(title)

        # Iterate through each question
        current_question_number = 1
        all_question_numbers = list(self.statements.keys())

        for question_num in all_question_numbers:
            statement_pair, styles = self.statements[question_num]
            question_option_1 = statement_pair[0]
            question_option_2 = statement_pair[1]

            while True:  # Keep asking until a valid choice (1 or 2) is entered
                clear_screen(title)
                print(f'\n      {current_question_number}/{len(questions.Question_Statements)}\n')
                print(f'1.    {question_option_1[0]}')
                print(f'2.    {question_option_2[0]}\n')

                choice = input("Choice (1/2): ")
                try:
                    # Convert the choice to an integer
                    choice = int(choice)

                    if choice == 1 or choice == 2:
                        break  # Valid choice, exit the loop
                    else:
                        continue
                except ValueError:
                    continue

            # Question numbering
            current_question_number += 1
            clear_screen()

            try:
                # Update scores based on the user's choice
                chosen_styles = styles.split(',')
                chosen_answer = int(choice) - 1
                for index, style in enumerate(chosen_styles):
                    if index == chosen_answer:
                        self.scores[style] += 1
            except (ValueError, IndexError):
                print(make_bold("Invalid choice. Choose 1 or 2."))
                continue

        # Calculate quadrant coordinates based on the scores
        self.calculate_quadrant_coordinates()

        # Determine the number visible on the axis
        num_on_axis = 10

        # Determine the largest quadrant
        dominant_style = self.get_dominant_styles()

        # Show the results
        self.show_behavior_results(dominant_style)

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
        dominant_styles_list = dominant_style.split('-')

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

        # Show the plot
        plt.xlim(-num_on_axis, num_on_axis)
        plt.ylim(-num_on_axis, num_on_axis)
        plt.show()

# Run the test
if __name__ == "__main__":
    run = BehaviorStyleTest()
    clear_screen(title)
    run.behavior_style_assesment()

    # Close the plot
    input("\nPress Enter to exit...")