import numpy as np
import manim

class BinarySearch(Scene):
    def construct(self):
        # Create the array
        array = [3, 1, 4, 1, 5, 9, 2, 6]
        array_mob = VGroup(*[Text(str(i)) for i in array])
        array_mob.arrange(RIGHT, buff=0.5)
        self.add(array_mob)

        # Create the search value
        search_value = 5
        search_mob = Text(str(search_value))
        search_mob.to_edge(UP, buff=1.0)
        self.add(search_mob)

        # Perform the binary search
        low = 0
        high = len(array) - 1

        while low <= high:
            mid = (low + high) // 2
            mid_mob = array_mob[mid]
            mid_mob.set_color(YELLOW)
            self.wait(1.0)

            if array[mid] == search_value:
                self.wait(1.0)
                break
            elif array[mid] < search_value:
                low = mid + 1
            else:
                high = mid - 1

        mid_mob.set_color(WHITE)
        self.wait(1.0)

        # Highlight the found element
        mid_mob.set_color(GREEN)
        self.wait(2.0)

        # Clean up
        self.remove(array_mob)
        self.remove(search_mob)

        # Display the result
        result_mob = Text(f"Found {search_value} at index {mid}")
        result_mob.to_edge(DOWN, buff=1.0)
        self.add(result_mob)
        self.wait(2.0)

        # Clean up
        self.remove(result_mob)


if __name__ == "main":
    scene = BinarySearch()
    scene.render()