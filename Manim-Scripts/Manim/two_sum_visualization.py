from manim import *
import numpy as np

class TwoSumVisualization(Scene):
    def construct(self):
        # Colors for consistent theming
        self.edge_case_color = "#FF6B6B"    # Red
        self.process_color = "#4DABF7"       # Blue
        self.solution_color = "#51CF66"      # Green
        self.warning_color = "#FFD43B"       # Yellow
        self.mistake_color = "#FFA94D"       # Orange
        self.special_color = "#CC5DE8"       # Purple
        
        # Introduction [0:00-0:35]
        self.introduction_scene()
        
        # Test Case Setup [0:35-2:00]
        self.test_case_setup()
        
        # Solution Walkthrough [2:00-4:30]
        self.solution_walkthrough()
        
        # Complexity Analysis [4:30-5:00]
        self.complexity_analysis()
        
        # Key Takeaways [5:00-5:30]
        self.key_takeaways()

    def introduction_scene(self):
        # [0:00-0:10] Coffee shop analogy
        coffee_scene = VGroup(
            Text("Coffee Shop Analogy", font_size=48),
            Text("$20 bill → $7.50 drink", font_size=36),
            Text("Need: $12.50 change", font_size=36)
        ).arrange(DOWN, buff=0.5)
        
        self.play(Write(coffee_scene), run_time=2)
        self.wait(1)
        self.play(FadeOut(coffee_scene))
        
        # [0:10-0:20] Problem statement
        problem = VGroup(
            Text("Two Sum Problem", font_size=48, color=BLUE),
            Text("Find two numbers in array that sum to target", font_size=36),
            MathTex(r"\text{nums} = [2, 7, 11, 15], \text{ target} = 9", font_size=36),
            Text("Answer: [0, 1] (2 + 7 = 9)", font_size=36)
        ).arrange(DOWN, buff=0.5)
        
        self.play(Write(problem), run_time=2)
        self.wait(2)
        
        # [0:20-0:35] Constraints
        constraints = VGroup(
            Text("Constraints:", font_size=40, color=YELLOW),
            Text("• Exactly one solution exists", font_size=32),
            Text("• Can't use same element twice", font_size=32),
            Text("• Return indices, not values", font_size=32)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        
        self.play(FadeOut(problem))
        self.play(Write(constraints), run_time=2)
        self.wait(2)
        self.play(FadeOut(constraints))

    def test_case_setup(self):
        # [0:35-1:15] Test case array setup
        nums = [3, 2, 4, 1, 7, 11, 15, 8, 3, 6]
        array_group = self.create_array_visualization(nums)
        target_text = Text("Target = 10", font_size=36).next_to(array_group, UP)
        
        self.play(
            Write(target_text),
            Create(array_group),
            run_time=2
        )
        
        # [1:15-1:30] Edge Cases Demonstration
        edge_cases = VGroup(
            Text("Edge Cases:", font_size=40, color=self.edge_case_color),
            Text("1. Duplicate numbers (3's)", font_size=32),
            Text("2. Same index sum invalid", font_size=32),
            Text("3. Multiple valid pairs", font_size=32)
        ).arrange(DOWN, aligned_edge=LEFT)
        
        # Highlight duplicates
        self.play(
            array_group[0][0].animate.set_fill(self.edge_case_color, opacity=0.3),
            array_group[0][8].animate.set_fill(self.edge_case_color, opacity=0.3),
            Write(edge_cases),
            run_time=2
        )
        self.wait(2)
        
        # [1:30-2:00] Common Pitfalls
        pitfalls = VGroup(
            Text("Common Pitfalls:", font_size=40, color=self.mistake_color),
            Text("• Returning values instead of indices", font_size=32),
            Text("• Using same element twice", font_size=32),
            Text("• Not handling duplicates", font_size=32)
        ).arrange(DOWN, aligned_edge=LEFT)
        
        self.play(
            FadeOut(edge_cases),
            Write(pitfalls),
            run_time=2
        )
        self.wait(2)
        self.play(FadeOut(pitfalls))
        
        # Store for later use
        self.array_group = array_group
        self.target_text = target_text

    def solution_walkthrough(self):
        # [2:00-2:15] Hash Map Introduction
        hash_map_title = Text("Hash Map Approach", font_size=40).to_edge(UP)
        hash_map = self.create_hash_map_visualization()
        
        self.play(
            Write(hash_map_title),
            Create(hash_map),
            run_time=2
        )
        
        # [2:15-3:45] Algorithm Walkthrough
        nums = [3, 2, 4, 1, 7, 11, 15, 8, 3, 6]
        for i, num in enumerate(nums):
            if i > 4:  # We find solution at index 4
                break
                
            # Current element processing
            complement = 10 - num
            current_step = VGroup(
                Text(f"Current: {num} (index {i})", font_size=32),
                Text(f"Looking for: {complement}", font_size=32)
            ).arrange(DOWN).next_to(hash_map, RIGHT)
            
            self.play(
                self.array_group[0][i].animate.set_fill(self.process_color, opacity=0.3),
                Write(current_step),
                run_time=1
            )
            
            # Add to hash map
            hash_entry = self.add_to_hash_map(hash_map, num, i)
            self.play(Write(hash_entry), run_time=1)
            
            if num == 7:  # Solution found
                solution_text = Text(
                    "Solution Found! [0, 4]",
                    font_size=40,
                    color=self.solution_color
                ).next_to(hash_map, DOWN)
                
                self.play(
                    self.array_group[0][0].animate.set_fill(self.solution_color, opacity=0.3),
                    self.array_group[0][4].animate.set_fill(self.solution_color, opacity=0.3),
                    Write(solution_text),
                    run_time=2
                )
                
            self.play(
                FadeOut(current_step),
                self.array_group[0][i].animate.set_fill(opacity=0),
                run_time=0.5
            )
            
        self.wait(2)
        
        # [3:45-4:30] Final Code Display
        code = Code(
            code="""
def twoSum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
            """,
            language="python",
            font_size=24,
            line_spacing=0.8,
        ).next_to(hash_map, DOWN)
        
        self.play(
            Write(code),
            run_time=2
        )
        self.wait(2)
        self.play(FadeOut(code))

    def complexity_analysis(self):
        # [4:30-5:00] Complexity Analysis
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        
        complexity = VGroup(
            Text("Time Complexity", font_size=48, color=BLUE),
            Text("O(n) - Single pass through array", font_size=36),
            Text("Hash map lookups are O(1)", font_size=36),
            Text("Space Complexity", font_size=48, color=BLUE).shift(DOWN * 2),
            Text("O(n) - Hash map storage", font_size=36),
            Text("Worst case: store n-1 elements", font_size=36)
        ).arrange(DOWN, buff=0.3)
        
        self.play(Write(complexity), run_time=2)
        self.wait(3)
        self.play(FadeOut(complexity))

    def key_takeaways(self):
        # [5:00-5:30] Key Takeaways
        takeaways = VGroup(
            Text("Key Takeaways", font_size=48, color=YELLOW),
            Text("1. Hash maps optimize from O(n²) to O(n)", font_size=36),
            Text("2. Store complements for efficient lookup", font_size=36),
            Text("3. Return indices, not values", font_size=36),
            Text("4. Handle edge cases carefully", font_size=36)
        ).arrange(DOWN, buff=0.5)
        
        self.play(Write(takeaways), run_time=2)
        self.wait(3)
        
        # Final fade out
        self.play(FadeOut(takeaways))

    def create_array_visualization(self, nums):
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
        
        return VGroup(squares, indices)

    def create_hash_map_visualization(self):
        hash_map = VGroup(
            Rectangle(height=4, width=6),
            Text("Value → Index", font_size=24).next_to(Rectangle(height=4, width=6), UP)
        )
        return hash_map

    def add_to_hash_map(self, hash_map, value, index):
        entry = Text(
            f"{value} → {index}",
            font_size=24
        ).move_to(hash_map.get_center() + UP * (1.5 - index * 0.5))
        return entry

class IntroScene(Scene):
    def construct(self):
        title = Text("Two Sum Algorithm", font_size=48)
        subtitle = Text("Visual Guide", font_size=36).next_to(title, DOWN)
        
        self.play(Write(title))
        self.play(Write(subtitle))
        self.wait(2)
        self.play(FadeOut(title), FadeOut(subtitle))

class OutroScene(Scene):
    def construct(self):
        thanks = Text("Thanks for watching!", font_size=48)
        subtitle = Text("Practice more coding problems", font_size=36).next_to(thanks, DOWN)
        
        self.play(Write(thanks))
        self.play(Write(subtitle))
        self.wait(2)
        self.play(FadeOut(thanks), FadeOut(subtitle))