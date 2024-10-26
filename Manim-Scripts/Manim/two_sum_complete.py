from manim import *
import numpy as np

class TwoSumComplete(Scene):
    def construct(self):
        # Colors
        self.edge_case_color = "#FF6B6B"    # Red
        self.process_color = "#4DABF7"       # Blue
        self.solution_color = "#51CF66"      # Green
        self.warning_color = "#FFD43B"       # Yellow
        self.mistake_color = "#FFA94D"       # Orange
        self.special_color = "#CC5DE8"       # Purple
        
        # [0:00-0:35] Introduction
        self.play_introduction()
        
        # [0:35-2:00] Test Case Setup
        self.play_test_case_setup()
        
        # [2:00-4:30] Solution Walkthrough
        self.play_solution_walkthrough()
        
        # [4:30-5:00] Complexity Analysis
        self.play_complexity_analysis()
        
        # [5:00-5:30] Conclusion
        self.play_conclusion()

    def play_introduction(self):
        # Title (5s)
        title = Text("Two Sum Algorithm", font_size=48, color=BLUE)
        subtitle = Text("Visual Guide", font_size=36).next_to(title, DOWN)
        self.play(Write(title), Write(subtitle))
        self.wait(2)
        self.play(FadeOut(title), FadeOut(subtitle))

        # Coffee shop analogy (10s)
        shop_example = VGroup(
            Text("Coffee Shop Example", font_size=48, color=self.process_color),
            Text("Customer pays: $20.00", font_size=36),
            Text("Coffee costs: $7.50", font_size=36),
            Text("Need change: $12.50", font_size=36)
        ).arrange(DOWN, buff=0.5)
        self.play(Write(shop_example))
        self.wait(2)
        self.play(FadeOut(shop_example))

        # Problem statement (20s)
        problem = VGroup(
            Text("Problem:", font_size=48, color=self.process_color),
            Text("Given: Array [2, 7, 11, 15]", font_size=36),
            Text("Target: 9", font_size=36),
            Text("Find two numbers that sum to target", font_size=36),
            Text("Return their indices", font_size=36)
        ).arrange(DOWN, buff=0.5)
        self.play(Write(problem))
        self.wait(3)
        self.play(FadeOut(problem))

    def play_test_case_setup(self):
        # Array visualization (30s)
        nums = [3, 2, 4, 1, 7, 11, 15, 8, 3, 6]
        squares, indices = self.create_array_viz(nums)
        array_group = VGroup(squares, indices).to_edge(UP)
        target_text = Text("Target = 10", font_size=36).next_to(array_group, UP)
        
        self.play(Create(array_group), Write(target_text))
        
        # Edge cases (30s)
        edge_cases = VGroup(
            Text("Edge Cases:", font_size=40, color=self.edge_case_color),
            Text("1. Duplicate numbers (3 appears twice)", font_size=32),
            Text("2. Can't use same index twice", font_size=32),
            Text("3. Multiple valid pairs exist", font_size=32)
        ).arrange(DOWN, aligned_edge=LEFT).to_edge(LEFT)
        
        self.play(Write(edge_cases))
        
        # Highlight duplicates
        self.play(
            squares[0].animate.set_fill(self.edge_case_color, opacity=0.3),
            squares[8].animate.set_fill(self.edge_case_color, opacity=0.3)
        )
        self.wait(2)
        
        # Reset colors
        self.play(
            squares[0].animate.set_fill(opacity=0),
            squares[8].animate.set_fill(opacity=0)
        )
        
        # Common mistakes (25s)
        mistakes = VGroup(
            Text("Common Mistakes:", font_size=40, color=self.mistake_color),
            Text("• Returning values instead of indices", font_size=32),
            Text("• Using same element twice", font_size=32),
            Text("• Ignoring duplicates", font_size=32)
        ).arrange(DOWN, aligned_edge=LEFT).next_to(edge_cases, RIGHT, buff=1)
        
        self.play(Write(mistakes))
        self.wait(2)
        self.play(FadeOut(edge_cases), FadeOut(mistakes))
        
        # Store for later use
        self.array_squares = squares
        self.array_indices = indices
        self.target_text = target_text

    def play_solution_walkthrough(self):
        # Hash map visualization setup (30s)
        hash_title = Text("Hash Map Approach", font_size=40).next_to(self.target_text, DOWN, buff=1)
        hash_box = Rectangle(height=4, width=6).next_to(hash_title, DOWN)
        hash_label = Text("Value → Index", font_size=24).next_to(hash_box, UP)
        
        self.play(
            Write(hash_title),
            Create(hash_box),
            Write(hash_label)
        )
        
        # Algorithm walkthrough (90s)
        nums = [3, 2, 4, 1, 7]  # We'll find solution at 7
        hash_entries = VGroup()
        
        for i, num in enumerate(nums):
            # Current element processing
            current = Text(f"Current: {num}", font_size=32).next_to(hash_box, RIGHT)
            complement = Text(f"Need: {10-num}", font_size=32).next_to(current, DOWN)
            
            self.play(
                self.array_squares[i].animate.set_fill(self.process_color, opacity=0.3),
                Write(current),
                Write(complement)
            )
            
            if num == 7:  # Solution found
                self.play(
                    self.array_squares[0].animate.set_fill(self.solution_color, opacity=0.3),
                    self.array_squares[i].animate.set_fill(self.solution_color, opacity=0.3)
                )
                
                solution = Text(
                    "Solution: [0, 4]",
                    font_size=40,
                    color=self.solution_color
                ).next_to(hash_box, DOWN)
                
                self.play(Write(solution))
                self.wait(2)
                break
            
            # Add to hash map
            entry = Text(
                f"{num} → {i}",
                font_size=24
            ).move_to(hash_box.get_center() + UP * (1 - i * 0.5))
            
            hash_entries.add(entry)
            self.play(Write(entry))
            
            # Clean up current step
            self.play(
                FadeOut(current),
                FadeOut(complement),
                self.array_squares[i].animate.set_fill(opacity=0)
            )
        
        self.wait(2)

    def play_complexity_analysis(self):
        # Clear previous content
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        
        # Time complexity (15s)
        time_analysis = VGroup(
            Text("Time Complexity: O(n)", font_size=48, color=self.process_color),
            Text("• Single pass through array", font_size=36),
            Text("• Hash map lookups are O(1)", font_size=36)
        ).arrange(DOWN, aligned_edge=LEFT)
        
        self.play(Write(time_analysis))
        self.wait(2)
        
        # Space complexity (15s)
        space_analysis = VGroup(
            Text("Space Complexity: O(n)", font_size=48, color=self.process_color),
            Text("• Hash map stores at most n elements", font_size=36),
            Text("• Additional space grows with input", font_size=36)
        ).arrange(DOWN, aligned_edge=LEFT)
        
        self.play(ReplacementTransform(time_analysis, space_analysis))
        self.wait(2)

    def play_conclusion(self):
        # Key takeaways (20s)
        takeaways = VGroup(
            Text("Key Takeaways", font_size=48, color=self.warning_color),
            Text("1. Hash map optimizes to O(n)", font_size=36),
            Text("2. Store complements for quick lookup", font_size=36),
            Text("3. Handle edge cases properly", font_size=36),
            Text("4. Return indices, not values", font_size=36)
        ).arrange(DOWN, buff=0.5)
        
        self.play(Write(takeaways))
        self.wait(3)
        
        # Final screen (10s)
        final = VGroup(
            Text("Two Sum Algorithm", font_size=48, color=BLUE),
            Text("Visual Guide Complete", font_size=36)
        ).arrange(DOWN, buff=0.5)
        
        self.play(ReplacementTransform(takeaways, final))
        self.wait(2)

    def create_array_viz(self, nums):
        squares = VGroup(*[
            Square(side_length=1)
            .set_stroke(WHITE)
            .add(Text(str(num), font_size=24))
            for num in nums
        ]).arrange(RIGHT, buff=0.1)
        
        indices = VGroup(*[
            Text(str(i), font_size=20).next_to(square, DOWN, buff=0.1)
            for i, square in enumerate(squares)
        ])
        
        return squares, indices