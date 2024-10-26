from manim import *

class TwoSumVisualization(Scene):
    def construct(self):
        # Create the title
        title = Text("Two Sum Algorithm Visualization", font_size=32)
        title.to_edge(UP)
        self.play(Write(title))
        
        # Input array and target
        numbers = [2, 7, 11, 15]
        target = 9
        
        # Create array visualization
        squares = VGroup()
        number_labels = VGroup()
        index_labels = VGroup()
        
        # Create squares with numbers
        for i, num in enumerate(numbers):
            square = Square(side_length=1)
            number = Text(str(num), font_size=24)
            index = Text(str(i), font_size=20, color=BLUE)
            
            square.set_stroke(WHITE)
            number.move_to(square.get_center())
            index.next_to(square, DOWN, buff=0.3)
            
            squares.add(square)
            number_labels.add(number)
            index_labels.add(index)
        
        # Arrange squares horizontally
        squares.arrange(RIGHT, buff=0.5)
        squares.move_to(ORIGIN)
        
        # Position numbers and indices
        for i in range(len(numbers)):
            number_labels[i].move_to(squares[i].get_center())
            index_labels[i].next_to(squares[i], DOWN, buff=0.3)
        
        # Create target sum text
        target_text = Text(f"Target Sum: {target}", font_size=24)
        target_text.next_to(squares, UP, buff=1)
        
        # Show array and target
        self.play(
            Create(squares),
            Write(number_labels),
            Write(index_labels),
            Write(target_text)
        )
        self.wait()
        
        # Visualization of checking pairs
        found = False
        for i in range(len(numbers)):
            if found:
                break
            # Highlight current number
            self.play(squares[i].animate.set_fill(YELLOW, opacity=0.3))
            
            for j in range(i + 1, len(numbers)):
                # Highlight second number
                self.play(squares[j].animate.set_fill(BLUE, opacity=0.3))
                
                # Show sum calculation
                sum_text = Text(f"{numbers[i]} + {numbers[j]} = {numbers[i] + numbers[j]}", 
                              font_size=24)
                sum_text.next_to(squares, DOWN, buff=1)
                self.play(Write(sum_text))
                
                if numbers[i] + numbers[j] == target:
                    # Found the pair!
                    found = True
                    result_text = Text(f"Found pair: [{i}, {j}]", font_size=24, color=GREEN)
                    result_text.next_to(sum_text, DOWN, buff=0.5)
                    self.play(
                        squares[i].animate.set_fill(GREEN, opacity=0.3),
                        squares[j].animate.set_fill(GREEN, opacity=0.3),
                        Write(result_text)
                    )
                    break
                else:
                    # Not the right pair, reset second number
                    self.play(
                        squares[j].animate.set_fill(opacity=0),
                        FadeOut(sum_text)
                    )
            
            if not found:
                # Reset first number if pair not found
                self.play(squares[i].animate.set_fill(opacity=0))
        
        self.wait(2)