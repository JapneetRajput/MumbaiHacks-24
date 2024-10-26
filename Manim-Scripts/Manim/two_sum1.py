from manim import *
import numpy as np

config.background_color = "#2D3747"

class TwoSumVisualization(Scene):
    def construct(self):
        # Introduction Section [0:00-0:35]
        self.intro_section()
        self.wait(2)

        # Test Case Setup [0:35-2:00]
        self.test_case_section()
        self.wait(2)

        # Solution Walkthrough [2:00-4:30]
        self.solution_walkthrough()
        self.wait(2)

        # Complexity Analysis [4:30-5:00]
        self.complexity_analysis()
        self.wait(2)

        # Key Takeaways [5:00-5:30]
        self.key_takeaways()
        self.wait(2)

    def intro_section(self):
        # Title
        title = Text("Two Sum Problem", font_size=48)
        title.to_edge(UP)
        
        # Problem statement
        problem = VGroup(
            Text("Given an array of integers nums and an integer target,", font_size=24),
            Text("return indices of two numbers that add up to target.", font_size=24)
        ).arrange(DOWN)
        
        # Example array
        example_array = VGroup(
            *[Square(side_length=0.8, color=WHITE) for _ in range(4)]
        ).arrange(RIGHT, buff=0.1)
        array_values = VGroup(
            *[Text(str(val), font_size=24) for val in [2, 7, 11, 15]]
        )
        for value, square in zip(array_values, example_array):
            value.move_to(square)
        
        example = VGroup(example_array, array_values).arrange(DOWN)
        example.next_to(problem, DOWN, buff=1)
        
        # Target value
        target = Text("Target = 9", font_size=32)
        target.next_to(example, DOWN)
        
        # Animations
        self.play(Write(title))
        self.wait(0.5)
        self.play(Write(problem))
        self.wait(1)
        self.play(Create(example_array), Write(array_values))
        self.wait(0.5)
        self.play(Write(target))
        self.wait(2)
        
        # Clear screen for next section
        self.play(
            *[FadeOut(obj) for obj in [title, problem, example_array, array_values, target]]
        )

    def test_case_section(self):
        # Create test case array
        nums = [3, 2, 4, 1, 7, 11, 15, 8, 3, 6]
        squares = VGroup(
            *[Square(side_length=0.8, color=WHITE) for _ in range(len(nums))]
        ).arrange(RIGHT, buff=0.1)
        values = VGroup(
            *[Text(str(val), font_size=24) for val in nums]
        )
        for value, square in zip(values, squares):
            value.move_to(square)
        
        array_group = VGroup(squares, values).to_edge(UP)
        
        # Edge cases text
        edge_cases = VGroup(
            Text("Edge Cases:", font_size=32),
            Text("1. Duplicate numbers (3 appears twice)", font_size=24, color=RED),
            Text("2. Same index restriction", font_size=24, color=BLUE),
            Text("3. Multiple valid pairs", font_size=24, color=GREEN)
        ).arrange(DOWN, aligned_edge=LEFT)
        edge_cases.next_to(array_group, DOWN, buff=1)
        
        # Animations
        self.play(Create(squares), Write(values))
        self.wait(1)
        self.play(Write(edge_cases))
        self.wait(2)
        
        # Clear screen
        self.play(
            *[FadeOut(obj) for obj in [squares, values, edge_cases]]
        )

    def solution_walkthrough(self):
        # Create hashmap visualization
        hashmap = VGroup()
        hashmap_title = Text("HashMap", font_size=32)
        hashmap_title.to_edge(UP)
        
        # Array visualization
        nums = [3, 2, 4, 1, 7, 11, 15, 8, 3, 6]
        squares = VGroup(
            *[Square(side_length=0.8, color=WHITE) for _ in range(len(nums))]
        ).arrange(RIGHT, buff=0.1)
        values = VGroup(
            *[Text(str(val), font_size=24) for val in nums]
        )
        for value, square in zip(values, squares):
            value.move_to(square)
        
        array_group = VGroup(squares, values).next_to(hashmap_title, DOWN, buff=1)
        
        # Show solution process
        self.play(Write(hashmap_title))
        self.play(Create(squares), Write(values))
        
        # Simulate hashmap population
        seen = {}
        target = 10
        
        for i, num in enumerate(nums):
            complement = target - num
            
            # Highlight current number
            self.play(squares[i].animate.set_color(BLUE))
            
            if complement in seen:
                # Found a match
                self.play(
                    squares[seen[complement]].animate.set_color(GREEN),
                    squares[i].animate.set_color(GREEN)
                )
                break
            
            # Add to hashmap
            seen[num] = i
            self.wait(0.5)
            
            # Reset color
            self.play(squares[i].animate.set_color(WHITE))
        
        self.wait(2)
        
        # Clear screen
        self.play(
            *[FadeOut(obj) for obj in [hashmap_title, squares, values]]
        )

    def complexity_analysis(self):
        # Create complexity text
        complexity = VGroup(
            Text("Time Complexity: O(n)", font_size=32),
            Text("• Single pass through array", font_size=24),
            Text("• Constant time hashmap operations", font_size=24),
            Text("Space Complexity: O(n)", font_size=32),
            Text("• Stores up to n-1 elements in hashmap", font_size=24)
        ).arrange(DOWN, aligned_edge=LEFT)
        
        self.play(Write(complexity))
        self.wait(2)
        self.play(FadeOut(complexity))

    def key_takeaways(self):
        # Create takeaways text
        takeaways = VGroup(
            Text("Key Takeaways:", font_size=32),
            Text("1. Use HashMap for O(n) time complexity", font_size=24),
            Text("2. Store complements for efficient lookup", font_size=24),
            Text("3. Return indices, not values", font_size=24),
            Text("4. Handle edge cases properly", font_size=24)
        ).arrange(DOWN, aligned_edge=LEFT)
        
        self.play(Write(takeaways))
        self.wait(2)
        self.play(FadeOut(takeaways))