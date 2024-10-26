import pyttsx3

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Set the narration script text
script_text = """
Now, let’s explore an advanced Binary Tree Cousin Problem. This example features a complete binary tree with four levels, showing multiple cousin relationships per level. This setup will demonstrate the algorithm's scalability and handling of complex cousin sums.

Our binary tree starts with a root node, three, and branches into a structured pattern of nodes, giving us a perfect binary structure.

We’ll process each level one by one. At level zero, we find only the root node with no cousins, so it defaults to zero.

At level one, nodes one and two are siblings, not cousins, meaning both receive a value of zero.

At level two, cousin relationships start to appear. Nodes four and five have cousins six and seven. Therefore, nodes four and five receive a sum value based on nodes six and seven, while six and seven get the sum of four and five.

At level three, the complexity increases with several cousin groups, such as nodes eight, nine, ten, and eleven, which update based on each other’s values.

In summary, this advanced test case shows a perfect binary tree with multiple levels. We see cousin pairs appearing at level two, followed by more complex cousin groups in level three. This test case validates efficient level-by-level processing, enabling constant-time cousin sum calculations.
"""

# Set the audio properties to adjust the length to around 78 seconds
engine.setProperty('rate', 200)  # Adjust the rate of speech if needed for timing
engine.setProperty('volume', 0.9)  # Optional: Set volume level

# Save narration to an audio file
engine.save_to_file(script_text, "advanced_binary_tree_cousin_analysis.mp3")

# Run the text-to-speech engine to generate the file
engine.runAndWait()

print("Narration audio saved as 'advanced_binary_tree_cousin_analysis.mp3'.")
