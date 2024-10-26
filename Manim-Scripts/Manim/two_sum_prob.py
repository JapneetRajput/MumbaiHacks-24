from manim import *

class TwoSumProblemExplanation(Scene):
    def construct(self):
        # Create and animate the title
        title = Text("Two Sum Problem", font_size=40)
        subtitle = Text("Find two numbers that add up to target", font_size=24)
        title_group = VGroup(title, subtitle)
        title_group.arrange(DOWN, buff=0.3)
        title_group.to_edge(UP, buff=1)
        
        self.play(Write(title))
        self.play(Write(subtitle))
        
        # Create problem statement on the left
        problem_text = """
        Given: 
        - Array of integers
        - Target sum
        
        Return: 
        - Indices of two numbers
        - Numbers must add up to target
        - Each input has exactly one solution
        """
        problem = Text(problem_text.strip(), font_size=20)
        problem.to_edge(LEFT, buff=1).shift(UP * 2)
        
        self.play(Write(problem), run_time=2)
        self.wait(1)
        
        # Create comprehensive test case with various scenarios
        numbers = [7, 2, 11, 15, 3, 6, 4, 1, 9, 10]
        target = 13
        
        # Create input array visualization on left side
        array_title = Text("Input Array:", font_size=24)
        array_title.next_to(problem, DOWN, buff=1)
        
        array_group = VGroup()
        squares = VGroup()
        numbers_text = VGroup()
        index_labels = VGroup()
        
        # Create array visualization with indices
        for i, num in enumerate(numbers):
            # Create square
            square = Square(side_length=0.8)
            square.set_stroke(WHITE)
            
            # Create number
            number = Text(str(num), font_size=20)
            number.move_to(square.get_center())
            
            # Create index label
            index = Text(str(i), font_size=16, color=BLUE)
            index.next_to(square, DOWN, buff=0.2)
            
            squares.add(square)
            numbers_text.add(number)
            index_labels.add(index)
        
        # Arrange array elements in 2 rows
        row_length = 5
        for i in range(len(squares)):
            row = i // row_length
            col = i % row_length
            squares[i].shift(RIGHT * col * 1.2 + DOWN * row * 1.5)
            numbers_text[i].move_to(squares[i].get_center())
            index_labels[i].next_to(squares[i], DOWN, buff=0.2)
        
        array_group.add(squares, numbers_text, index_labels)
        array_group.next_to(array_title, DOWN, buff=0.5)
        
        # Create variable tracking on right side
        var_box = Rectangle(height=4, width=3)
        var_box.to_edge(RIGHT, buff=1)
        
        var_title = Text("Variables", font_size=24)
        var_title.next_to(var_box, UP, buff=0.3)
        
        # Initialize variable trackers
        target_text = Text(f"Target: {target}", font_size=20)
        current_idx = Text("Current Index: ", font_size=20)
        current_num = Text("Current Number: ", font_size=20)
        complement = Text("Need to find: ", font_size=20)
        
        var_group = VGroup(target_text, current_idx, current_num, complement)
        var_group.arrange(DOWN, buff=0.5, aligned_edge=LEFT)
        var_group.move_to(var_box.get_center())
        
        # Show array and variable box
        self.play(
            Create(array_title),
            Create(squares),
            Write(numbers_text),
            Write(index_labels),
            Create(var_box),
            Write(var_title),
            Write(var_group)
        )
        self.wait(1)
        
        # Explanation text at the bottom
        explanation = Text("How it works:", font_size=24)
        explanation.to_edge(LEFT, buff=1)
        explanation.shift(DOWN * 2)
        self.play(Write(explanation))
        
        # Demonstrate the process with the first few numbers
        for i, num in enumerate(numbers[:4]):  # Only show first 4 for brevity
            # Update current index and number
            new_idx = Text(f"Current Index: {i}", font_size=20)
            new_num = Text(f"Current Number: {num}", font_size=20)
            new_complement = Text(f"Need to find: {target - num}", font_size=20)
            
            new_vars = VGroup(target_text.copy(), new_idx, new_num, new_complement)
            new_vars.arrange(DOWN, buff=0.5, aligned_edge=LEFT)
            new_vars.move_to(var_box.get_center())
            
            # Highlight current square
            self.play(
                squares[i].animate.set_fill(YELLOW, opacity=0.3),
                Transform(var_group, new_vars)
            )
            
            # Show explanation for this step
            step_text = Text(
                f"Looking for {target - num} to add with {num}",
                font_size=20
            )
            step_text.next_to(explanation, DOWN, buff=0.5)
            
            self.play(Write(step_text))
            self.wait(1)
            
            # Clean up for next iteration
            self.play(
                squares[i].animate.set_fill(opacity=0),
                FadeOut(step_text)
            )
        
        # Final summary
        summary = VGroup(
            Text("For each number:", font_size=20),
            Text("1. Calculate needed complement", font_size=20),
            Text("2. Check if complement exists", font_size=20),
            Text("3. Return indices if found", font_size=20)
        )
        summary.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        summary.next_to(explanation, DOWN, buff=0.5)
        
        self.play(Write(summary))
        self.wait(2)