from manim import *

class BinarySearchOverview(Scene):
    def construct(self):
        # Title slide
        title = Text("Binary Search Overview").scale(1.5)
        self.play(FadeIn(title))
        self.wait(2)

        # Algorithm slide
        algorithm = Tex(r"""
        1. Set L = 0, R = N-1
        2. While L <= R
            3. Mid = (L + R) / 2
            4. Compare T[Mid] to the target value
            5. If T[Mid] is equal to the target value
            6. Return M
            7. Else if T[Mid] is less than the target value
            8. L = M + 1
            9. Else
            10. R = M - 1
        """).scale(0.8)
        self.play(Write(algorithm))
        self.wait(4)

        # Visual slide
        array = number_line(range(1, 11))
        target = Integer(7)
        target.point.set_color(YELLOW)
        self.play(FadeIn(array), FadeIn(target))
        self.wait()

        # Algorithm steps
        for i in range(10):
            midpoint = array.get_point_from_index(5)
            target.move_to(midpoint)
            self.play(ApplyMethod(target.shift, 2*LEFT), run_time=0.5)
            self.play(target.animate.set_color(RED), run_time=0.5)
            self.wait(0.5)

        self.play(target.animate.set_color(YELLOW), run_time=0.5)
        self.wait()

        # Target found
        self.play(FadeOut(array), FadeOut(target))
        found = Text("Target found!").scale(1.5)
        self.play(FadeIn(found))
        self.wait(3)

class number_line(Mobject):
    def __init__(self, numbers, **kwargs):
        digest_start = kwargs.pop("digest_start", False)
        self.numbers = numbers
        if digest_start:
            x = [0]
        else:
            x = [1]
        for n in numbers:
            x.append(x[-1] + 1)
        kwargs.setdefault("x_range", (min(x), max(x)))
        super().__init__(**kwargs)

    def get_point_from_index(self, i):
        return self.point_from_proportion((i - self.x_range[0]) / (self.x_range[1] - self.x_range[0]))

config = {
    "background_color": "#f0f0f0",
    "ground": True
}
Scene().config = config

BinarySearchOverview().play()