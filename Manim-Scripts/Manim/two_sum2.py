from manim import *
import numpy as np

config.background_color = "#2D3747"

class TwoSumVisualization(Scene):
    def construct(self):
        # Introduction Section [0:00-0:35]
        self.intro_section()
        self.wait(5)  # Buffer for audio explanation

        # Test Case Setup [0:35-2:00]
        self.test_case_section()
        self.wait(5)  # Buffer for audio explanation

        # Solution Walkthrough [2:00-4:30]
        self.solution_walkthrough()
        self.wait(5)  # Buffer for audio explanation

        # Complexity Analysis [4:30-5:00]
        self.complexity_analysis()
        self.wait(5)  # Buffer for audio explanation

        # Key Takeaways [5:00-5:30]
        self.key_takeaways()
        self.wait(5)  # Buffer for final explanation

    def create_hashmap_visual(self, title="HashMap", position=RIGHT):
        # Create a visual representation of hashmap
        hashmap_box = Rectangle(height=4, width=3, color=WHITE)
        hashmap_title = Text(title, font_size=24).next_to(hashmap_box, UP)
        hashmap_content = VGroup()
        hashmap = VGroup(hashmap_box, hashmap_title, hashmap_content)
        hashmap.to_edge(position)
        return hashmap, hashmap_content

    def update_hashmap_visual(self, hashmap_content, key, value):
        # Add new key-value pair to hashmap visualization
        entry = Text(f"{key} → {value}", font_size=20)
        if len(hashmap_content) == 0:
            entry.next_to(hashmap_content.get_top(), DOWN, buff=0.5)
        else:
            entry.next_to(hashmap_content[-1], DOWN)
        return entry

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
        
        # Create initial empty hashmap
        hashmap, hashmap_content = self.create_hashmap_visual()
        
        # Animations
        self.play(Write(title))
        self.wait(2)  # Pause for explanation
        self.play(Write(problem))
        self.wait(2)  # Pause for explanation
        self.play(Create(example_array), Write(array_values))
        self.wait(2)  # Pause for explanation
        self.play(Write(target))
        self.wait(2)  # Pause for explanation
        self.play(Create(hashmap))
        self.wait(3)  # Pause for hashmap explanation
        
        # Clear screen for next section
        self.play(
            *[FadeOut(obj) for obj in [title, problem, example_array, array_values, target, hashmap]]
        )
        self.wait(2)  # Transition pause

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
        
        array_group = VGroup(squares, values).to_edge(LEFT)
        
        # Create hashmap visual
        hashmap, hashmap_content = self.create_hashmap_visual()
        
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
        self.wait(3)  # Pause for array explanation
        self.play(Create(hashmap))
        self.wait(3)  # Pause for hashmap explanation
        self.play(Write(edge_cases))
        self.wait(4)  # Pause for edge cases explanation
        
        # Clear screen
        self.play(
            *[FadeOut(obj) for obj in [squares, values, edge_cases, hashmap]]
        )
        self.wait(2)  # Transition pause

    def solution_walkthrough(self):
        # Create hashmap visualization
        hashmap, hashmap_content = self.create_hashmap_visual()
        
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
        
        array_group = VGroup(squares, values).to_edge(LEFT)
        
        # Target text
        target_text = Text("Target = 10", font_size=32).to_edge(UP)
        
        # Show initial setup
        self.play(
            Create(squares),
            Write(values),
            Create(hashmap),
            Write(target_text)
        )
        self.wait(3)  # Pause for setup explanation
        
        # Simulate hashmap population
        seen = {}
        target = 10
        
        for i, num in enumerate(nums):
            complement = target - num
            
            # Highlight current number and show complement calculation
            complement_text = Text(
                f"Looking for: {target} - {num} = {complement}",
                font_size=24
            ).next_to(target_text, DOWN)
            
            self.play(
                squares[i].animate.set_color(BLUE),
                Write(complement_text)
            )
            self.wait(2)  # Pause for complement explanation
            
            if complement in seen:
                # Found a match
                self.play(
                    squares[seen[complement]].animate.set_color(GREEN),
                    squares[i].animate.set_color(GREEN)
                )
                match_text = Text(
                    f"Found match! {num} + {complement} = {target}",
                    font_size=24,
                    color=GREEN
                ).next_to(complement_text, DOWN)
                self.play(Write(match_text))
                self.wait(3)  # Pause for match explanation
                break
            
            # Add to hashmap
            entry = self.update_hashmap_visual(hashmap_content, num, i)
            hashmap_content.add(entry)
            self.play(Write(entry))
            self.wait(2)  # Pause for hashmap update explanation
            
            # Reset colors and remove temporary text
            self.play(
                squares[i].animate.set_color(WHITE),
                FadeOut(complement_text)
            )
            self.wait(1)  # Pause between iterations
        
        self.wait(4)  # Final pause for solution explanation
        
        # Clear screen
        self.play(
            *[FadeOut(obj) for obj in [squares, values, hashmap, target_text, hashmap_content]]
        )
        if 'match_text' in locals():
            self.play(FadeOut(match_text))
        self.wait(2)  # Transition pause

    def complexity_analysis(self):
        # Create complexity text
        complexity = VGroup(
            Text("Time Complexity: O(n)", font_size=32),
            Text("• Single pass through array", font_size=24),
            Text("• Constant time hashmap operations", font_size=24),
            Text("Space Complexity: O(n)", font_size=32),
            Text("• Stores up to n-1 elements in hashmap", font_size=24)
        ).arrange(DOWN, aligned_edge=LEFT)
        
        # Animate each point separately with pauses
        self.play(Write(complexity[0]))
        self.wait(3)  # Pause for time complexity explanation
        self.play(Write(complexity[1:3]))
        self.wait(3)  # Pause for details explanation
        self.play(Write(complexity[3]))
        self.wait(3)  # Pause for space complexity explanation
        self.play(Write(complexity[4]))
        self.wait(3)  # Pause for details explanation
        
        self.play(FadeOut(complexity))
        self.wait(2)  # Transition pause

    def key_takeaways(self):
        # Create takeaways text
        takeaways = VGroup(
            Text("Key Takeaways:", font_size=32),
            Text("1. Use HashMap for O(n) time complexity", font_size=24),
            Text("2. Store complements for efficient lookup", font_size=24),
            Text("3. Return indices, not values", font_size=24),
            Text("4. Handle edge cases properly", font_size=24)
        ).arrange(DOWN, aligned_edge=LEFT)
        
        # Animate each takeaway separately with pauses
        self.play(Write(takeaways[0]))
        self.wait(2)  # Pause for title
        for i in range(1, len(takeaways)):
            self.play(Write(takeaways[i]))
            self.wait(3)  # Pause for each takeaway explanation
        
        self.wait(4)  # Final pause for conclusion
        self.play(FadeOut(takeaways))