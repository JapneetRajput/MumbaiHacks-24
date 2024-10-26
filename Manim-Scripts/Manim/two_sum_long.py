from manim import *

class ComprehensiveTwoSumVisualization(Scene):
    def construct(self):
        self.show_introduction()
        self.clear()
        self.show_simple_case()
        self.clear()
        self.show_duplicate_case()
        self.clear()
        self.show_no_solution_case()
        self.clear()
        self.show_hash_table_explanation()
        self.clear()
        self.show_space_time_complexity()
        
    def show_introduction(self):
        # Title and problem statement
        title = Text("Two Sum Algorithm", font_size=40)
        title.to_edge(UP)
        
        problem = self.create_text_box("""
        Problem: Given an array of integers 'nums' 
        and a target sum 'target', find two numbers 
        that add up to the target.
        
        Return the indices of these numbers.
        """.strip(), font_size=24)
        
        problem.next_to(title, DOWN, buff=1)
        
        self.play(Write(title))
        self.play(Create(problem), run_time=2)
        self.wait(2)
        
        # Show approaches
        approaches = VGroup()
        approaches.add(Text("Two Main Approaches:", font_size=28))
        approaches.add(Text("1. Brute Force (O(n²))", font_size=24))
        approaches.add(Text("2. Hash Table (O(n))", font_size=24))
        
        approaches.arrange(DOWN, buff=0.5, aligned_edge=LEFT)
        approaches.next_to(problem, DOWN, buff=1)
        
        for approach in approaches:
            self.play(Write(approach))
            self.wait(0.5)
            
        self.wait(2)

    def show_simple_case(self):
        title = Text("Example 1: Simple Case", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))
        
        description = self.create_text_box("""
        Array: [2, 7, 11, 15]
        Target: 9
        Expected: [0, 1] (2 + 7 = 9)
        """.strip(), font_size=24)
        description.next_to(title, DOWN, buff=1)
        
        self.play(Create(description))
        self.wait(1)
        
        # Create and show array
        numbers = [2, 7, 11, 15]
        array_group = self.create_array(numbers, "Input Array:", UP * 0.5)
        array_group.next_to(description, DOWN, buff=1)
        
        self.play(*[Create(obj) for obj in array_group])
        
        # Show step-by-step process
        current_calculation = VGroup()
        found = False
        squares = array_group[1]
        
        step_text = Text("Step-by-step process:", font_size=24)
        step_text.next_to(array_group, DOWN, buff=1)
        self.play(Write(step_text))
        
        for i in range(len(numbers)):
            if found:
                break
                
            self.play(squares[i].animate.set_fill(YELLOW, opacity=0.3))
            current_value = numbers[i]
            
            step = Text(f"Starting with index {i} (value = {current_value})", font_size=20)
            step.next_to(step_text, DOWN, buff=0.5)
            
            if current_calculation:
                self.play(FadeOut(current_calculation))
            current_calculation = VGroup(step)
            self.play(Write(step))
            
            for j in range(i + 1, len(numbers)):
                self.play(squares[j].animate.set_fill(BLUE, opacity=0.3))
                
                calc = Text(
                    f"Checking {current_value} + {numbers[j]} = {current_value + numbers[j]}",
                    font_size=20
                )
                calc.next_to(step, DOWN, buff=0.5)
                
                if current_calculation.submobjects[-1] != step:
                    self.play(FadeOut(current_calculation.submobjects[-1]))
                current_calculation.add(calc)
                self.play(Write(calc))
                
                if current_value + numbers[j] == 9:
                    found = True
                    result = Text(f"Found solution! Indices [{i}, {j}]", font_size=24, color=GREEN)
                    result.next_to(calc, DOWN, buff=0.5)
                    current_calculation.add(result)
                    
                    self.play(
                        squares[i].animate.set_fill(GREEN, opacity=0.3),
                        squares[j].animate.set_fill(GREEN, opacity=0.3),
                        Write(result)
                    )
                    break
                else:
                    self.play(squares[j].animate.set_fill(opacity=0))
            
            if not found:
                self.play(squares[i].animate.set_fill(opacity=0))
                
        self.wait(2)

    def show_duplicate_case(self):
        title = Text("Example 2: Duplicate Numbers", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))
        
        description = self.create_text_box("""
        Array: [3, 3, 4, 1]
        Target: 6
        Expected: [0, 1] (3 + 3 = 6)
        Special Case: Handling duplicates
        """.strip(), font_size=24)
        description.next_to(title, DOWN, buff=1)
        
        self.play(Create(description))
        self.wait(1)
        
        numbers = [3, 3, 4, 1]
        array_group = self.create_array(numbers, "Input Array:", UP * 0.5)
        array_group.next_to(description, DOWN, buff=1)
        
        self.play(*[Create(obj) for obj in array_group])
        
        # Show process for duplicate case...
        # (Similar structure to show_simple_case but with duplicate-specific explanations)
        
    def show_no_solution_case(self):
        title = Text("Example 3: No Solution", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))
        
        description = self.create_text_box("""
        Array: [1, 2, 3, 4]
        Target: 10
        Expected: No solution exists
        Important: Handle edge cases!
        """.strip(), font_size=24)
        description.next_to(title, DOWN, buff=1)
        
        self.play(Create(description))
        self.wait(1)
        
        # Show process for no-solution case...

    def show_hash_table_explanation(self):
        title = Text("Hash Table Approach Deep Dive", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))
        
        explanation = self.create_text_box("""
        Hash Table Method:
        1. Store complement (target - current)
        2. Single pass through array
        3. O(n) time complexity
        4. O(n) space complexity
        """.strip(), font_size=24)
        explanation.next_to(title, DOWN, buff=1)
        
        self.play(Create(explanation))
        self.wait(1)
        
        # Show detailed hash table process...

    def show_space_time_complexity(self):
        title = Text("Space & Time Complexity Analysis", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))
        
        comparison = self.create_text_box("""
        Brute Force:
        - Time: O(n²)
        - Space: O(1)
        - Best for small arrays
        
        Hash Table:
        - Time: O(n)
        - Space: O(n)
        - Better for large arrays
        """.strip(), font_size=24)
        comparison.next_to(title, DOWN, buff=1)
        
        self.play(Create(comparison))
        self.wait(2)

    def create_text_box(self, text, font_size=24):
        result = VGroup()
        box = Rectangle(height=3, width=6)
        text_obj = Text(text, font_size=font_size)
        text_obj.move_to(box.get_center())
        result.add(box, text_obj)
        return result
        
    def create_array(self, numbers, label_text, direction):
        group = VGroup()
        
        # Create label
        label = Text(label_text, font_size=20)
        group.add(label)
        
        # Create squares with numbers
        squares = VGroup()
        for num in numbers:
            square = Square(side_length=1)
            number = Text(str(num), font_size=24)
            number.move_to(square.get_center())
            square_group = VGroup(square, number)
            squares.add(square_group)
        
        squares.arrange(RIGHT, buff=0.5)
        label.next_to(squares, direction, buff=0.5)
        group.add(squares)
        
        group.move_to(ORIGIN)
        return group