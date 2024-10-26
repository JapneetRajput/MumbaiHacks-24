from manim import *
import time

class TwoSumVisualization(Scene):
    def construct(self):
        # Configuration
        self.camera.background_color = "#0C1020"
        
        # Introduction
        self.intro_section()
        self.wait(2)  # Buffer for audio
        
        # Problem Statement
        self.problem_statement()
        self.wait(2)  # Buffer for audio
        
        # Test Case Setup
        self.test_case_setup()
        self.wait(2)  # Buffer for audio
        
        # Solution Walkthrough
        self.solution_walkthrough()
        self.wait(2)  # Buffer for audio
        
        # Complexity Analysis
        self.complexity_analysis()
        self.wait(2)  # Buffer for audio
        
        # Key Takeaways
        self.key_takeaways()
        self.wait(3)  # Final buffer for conclusion
    
    def create_array_visual(self, numbers, title="Array"):
        squares = VGroup()
        numbers_text = VGroup()
        
        for i, num in enumerate(numbers):
            square = Square(side_length=0.8)
            square.set_stroke(color=WHITE)
            number = Text(str(num), font_size=24)
            index = Text(str(i), font_size=20, color=YELLOW).next_to(square, DOWN, buff=0.1)
            
            if i > 0:
                square.next_to(squares[-1], RIGHT, buff=0.1)
                number.move_to(square.get_center())
                index.next_to(square, DOWN, buff=0.1)
            
            squares.add(square)
            numbers_text.add(number)
            squares.add(index)
        
        array_group = VGroup(squares, numbers_text)
        title = Text(title, font_size=32).next_to(array_group, UP)
        return VGroup(title, array_group)
    
    def intro_section(self):
        title = Text("Two Sum Problem", font_size=48)
        self.play(Write(title))
        self.wait(1)
        
        coffee_example = Text(
            "Imagine you're a cashier...\nMaking change: $20 - $7.50 = $12.50",
            font_size=32
        ).next_to(title, DOWN)
        
        self.play(FadeOut(title), Write(coffee_example))
        self.wait(2)
        self.play(FadeOut(coffee_example))
    
    def problem_statement(self):
        problem = VGroup(
            Text("Given an array of integers nums and a target sum,", font_size=32),
            Text("find two numbers that add up to the target.", font_size=32),
            Text("Return the indices of these numbers.", font_size=32)
        ).arrange(DOWN)
        
        self.play(Write(problem))
        self.wait(2)
        
        example = VGroup(
            self.create_array_visual([2, 7, 11, 15], "Example:"),
            Text("Target = 9", font_size=32),
            Text("Output: [0, 1] (2 + 7 = 9)", font_size=32)
        ).arrange(DOWN)
        
        self.play(FadeOut(problem), FadeIn(example))
        self.wait(2)
        self.play(FadeOut(example))
    
    def test_case_setup(self):
        test_case = [3, 2, 4, 1, 7, 11, 15, 8, 3, 6]
        array_visual = self.create_array_visual(test_case, "Test Case:")
        
        self.play(FadeIn(array_visual))
        self.wait(1)
        
        # Highlight edge cases
        edge_cases = VGroup(
            Text("Edge Cases:", font_size=32, color=YELLOW),
            Text("• Duplicates (3 at indices 0 and 8)", font_size=28),
            Text("• Can't use same index twice", font_size=28),
            Text("• Multiple valid pairs sum to target", font_size=28)
        ).arrange(DOWN, aligned_edge=LEFT).next_to(array_visual, DOWN)
        
        self.play(Write(edge_cases))
        self.wait(2)
        self.play(FadeOut(edge_cases), FadeOut(array_visual))
    
    def solution_walkthrough(self):
        # Create hashmap visualization
        hashmap = VGroup()
        hashmap_title = Text("HashMap", font_size=32)
        hashmap_box = Rectangle(height=4, width=3)
        hashmap.add(hashmap_title, hashmap_box)
        hashmap.arrange(DOWN)
        
        # Create array visualization
        nums = [3, 2, 4, 1, 7, 11, 15, 8, 3, 6]
        array_visual = self.create_array_visual(nums)
        
        # Position both visualizations
        whole_group = VGroup(array_visual, hashmap).arrange(DOWN, buff=1)
        self.play(FadeIn(whole_group))
        
        # Animate solution steps
        current_entries = []
        for i, num in enumerate(nums):
            complement = 10 - num
            
            # Highlight current number
            current_square = array_visual[1][0][i*2]
            current_number = array_visual[1][1][i]
            self.play(
                current_square.animate.set_fill(color=BLUE, opacity=0.3),
                current_number.animate.set_color(BLUE)
            )
            
            # Show complement calculation
            calc_text = Text(
                f"Target - {num} = {complement}",
                font_size=24
            ).next_to(hashmap, RIGHT)
            self.play(Write(calc_text))
            
            # Check if complement exists
            complement_exists = False
            for entry in current_entries:
                if entry[0] == complement:
                    complement_exists = True
                    # Found a solution!
                    solution_text = Text(
                        f"Found solution! Indices [{entry[1]}, {i}]",
                        font_size=32,
                        color=GREEN
                    ).next_to(calc_text, DOWN)
                    self.play(Write(solution_text))
                    self.wait(1)
                    break
            
            if not complement_exists:
                # Add to hashmap
                entry_text = Text(
                    f"{num} → {i}",
                    font_size=24
                ).move_to(hashmap_box.get_center() + UP * (1.5 - len(current_entries) * 0.5))
                current_entries.append((num, i))
                self.play(Write(entry_text))
            
            self.wait(1)
            self.play(
                current_square.animate.set_fill(opacity=0),
                current_number.animate.set_color(WHITE),
                FadeOut(calc_text)
            )
            if complement_exists:
                break
        
        self.wait(2)
        self.play(FadeOut(whole_group))
    
    def complexity_analysis(self):
        complexity = VGroup(
            Text("Time Complexity: O(n)", font_size=32),
            Text("• Single pass through array", font_size=28),
            Text("• Constant time hashmap operations", font_size=28),
            Text("Space Complexity: O(n)", font_size=32),
            Text("• Storing up to n-1 elements in hashmap", font_size=28)
        ).arrange(DOWN, aligned_edge=LEFT)
        
        self.play(Write(complexity))
        self.wait(2)
        self.play(FadeOut(complexity))
    
    def key_takeaways(self):
        takeaways = VGroup(
            Text("Key Takeaways:", font_size=36, color=YELLOW),
            Text("1. Use HashMap for O(n) solution", font_size=28),
            Text("2. Store complements for efficient lookup", font_size=28),
            Text("3. Return indices, not values", font_size=28),
            Text("4. Handle duplicates carefully", font_size=28)
        ).arrange(DOWN, aligned_edge=LEFT)
        
        self.play(Write(takeaways))
        self.wait(2)
        self.play(FadeOut(takeaways))