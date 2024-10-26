from manim import *
import networkx as nx
from collections import defaultdict
import math

config.max_files_cached = 2000

class BinaryTreeCousinsAlgorithm(Scene):
    def construct(self):
        self.camera.background_color = "#1a1a1a"
        self.show_algorithm_overview()
        self.show_basic_test_case()
        self.show_advanced_test_case()
        self.show_time_complexity()

    def show_algorithm_overview(self):
        # Keeping the original overview section as it works well
        title = Text("Cousins in Binary Tree II", font_size=36)
        title.to_corner(UL, buff=0.5)
        
        algorithm_steps = VGroup(
            Text("Algorithm Steps:", font_size=24, color=YELLOW),
            Text("1. Use BFS to traverse the tree level by level", font_size=20),
            Text("2. For each level:", font_size=20),
            Text("   a. Group nodes by their parent", font_size=20),
            Text("   b. Sum values of nodes with different parents", font_size=20),
            Text("3. Create new tree with cousin sums", font_size=20)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        algorithm_steps.next_to(title, DOWN, buff=0.5).to_edge(LEFT, buff=0.5)
        
        data_structures = VGroup(
            Text("Data Structures:", font_size=24, color=YELLOW),
            Text("• Queue: For BFS traversal", font_size=20),
            Text("• HashMap: Group nodes by parent", font_size=20),
            Text("• HashMap: Store level-wise nodes", font_size=20)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        data_structures.to_edge(RIGHT, buff=0.5).align_to(algorithm_steps, UP)
        
        self.play(Write(title))
        self.wait(0.5)
        
        for step in algorithm_steps:
            self.play(Write(step), run_time=0.8)
        
        for ds in data_structures:
            self.play(Write(ds), run_time=0.5)
        
        self.wait(2)
        
        # Fade out everything except title for transition
        self.play(
            FadeOut(algorithm_steps),
            FadeOut(data_structures)
        )
        self.title = title

    def show_basic_test_case(self):
        # Keep the title from previous section
        subtitle = Text("Basic Test Case Analysis", font_size=28, color=YELLOW)
        subtitle.next_to(self.title, DOWN, buff=0.7)
        
        # Enhanced initial explanation with more detail
        initial_explanation = VGroup(
            Text("Let's analyze a Binary Tree Cousin Problem:", font_size=20),
            Text("Key Concepts:", font_size=20, color=BLUE),
            Text("• Nodes at same level with different parents are cousins", font_size=18),
            Text("• Each node's value will be replaced by sum of its cousins", font_size=18),
            Text("• If no cousins exist, the value becomes 0", font_size=18),
            Text("\nExample Tree Structure:", font_size=20, color=BLUE),
            Text("• Root node: 5", font_size=18),
            Text("• Left subtree: 4 as parent, with children 1 and 10", font_size=18),
            Text("• Right subtree: 9 as parent, with child 7", font_size=18)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        initial_explanation.scale(0.8)  # Scale down to fit better
        initial_explanation.next_to(subtitle, DOWN, buff=0.5)
        
        self.play(Write(subtitle))
        self.play(Write(initial_explanation))
        self.wait(3)  # Give more time to read
        
        self.play(FadeOut(initial_explanation))
        
        # Create and show the initial tree with more spacing
        values = [5, 4, 9, 1, 10, None, 7]
        vertices, edges, labels = self.create_tree_visualization(
            values,
            node_spacing=2.5,  # Increase horizontal spacing
            level_spacing=1.5   # Increase vertical spacing
        )
        
        # Center the tree more to the left to make room for processing box
        tree_group = VGroup(vertices, edges, labels)
        tree_group.shift(LEFT * 3 + DOWN * 1.5) 
        
        # Enhanced processing display
        process_box = Rectangle(height=4, width=5, color=BLUE_C)
        process_box.to_edge(RIGHT, buff=1.0)
        process_title = Text("Analysis Steps", font_size=24, color=YELLOW)
        process_title.next_to(process_box, UP, buff=0.2)
        
        # Add a legend
        legend = VGroup(
            Text("Color Legend:", font_size=18, color=WHITE),
            Text("• Yellow: Current level being processed", font_size=16),
            Text("• Green: Node being updated", font_size=16),
            Text("• White: Unprocessed nodes", font_size=16)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        legend.scale(0.8)
        legend.next_to(process_box, DOWN, buff=0.3)
        
        # Create level indicator with better styling
        level_tracker = VGroup(
            Text("Processing Level: ", font_size=20),
            Text("0", font_size=20, color=YELLOW)
        ).arrange(RIGHT, buff=0.2)
        level_tracker.next_to(process_title, DOWN, buff=0.3)
        
        # Show initial setup with animations
        self.play(
            Create(edges),
            Create(vertices),
            Write(labels)
        )
        self.play(
            Create(process_box),
            Write(process_title),
            Write(legend)
        )
        self.wait(1)
        
        # Process level by level with enhanced explanations
        for level in range(3):
            # Update level tracker
            new_level = Text(str(level), font_size=20, color=YELLOW)
            new_level.move_to(level_tracker[1])
            self.play(
                Transform(level_tracker[1], new_level) if level > 0 
                else Write(level_tracker)
            )
            
            # Get nodes at current level
            level_nodes = self.get_nodes_at_level(values, level)
            current_vertices = VGroup(*[
                vertices[i] for i in level_nodes 
                if i < len(vertices) and values[i] is not None
            ])
            
            # Highlight current level with explanation
            self.play(current_vertices.animate.set_color(YELLOW))
            
            # Enhanced processing text with more detail
            process_text = VGroup(
                Text(f"Level {level} Analysis:", font_size=18, color=YELLOW),
                *self.create_detailed_level_analysis(values, level, level_nodes)
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
            process_text.scale(0.8)
            process_text.move_to(process_box.get_center())
            
            self.play(Write(process_text))
            self.wait(2)
            
            # Calculate and show cousin sums with enhanced animations
            cousin_sums = self.calculate_cousin_sums(values, level, level_nodes)
            for idx, sum_val in cousin_sums.items():
                if values[idx] is not None:
                    # Create updating arrow
                    if 0 <= idx < len(vertices):
                        arrow = Arrow(process_box.get_left(), vertices[idx].get_center(), color=GREEN)
                    else:
                        print(f"Index {idx} is out of range for vertices with length {len(vertices)}")
                    # arrow = Arrow(
                    #     process_box.get_left(),
                    #     vertices[idx].get_center(),
                    #     color=GREEN
                    # )
                    new_label = Text(str(sum_val), font_size=18)
                    if 0 <= idx < len(labels):
                        new_label.move_to(labels[idx].get_center())
                    else:
                        print(f"Index {idx} is out of range for labels with length {len(labels)}")
                    
                    if 0 <= idx < len(labels):
                        self.play(
                            Create(arrow),
                            Transform(labels[idx], new_label),
                            Flash(vertices[idx], color=GREEN, flash_radius=0.3),
                            run_time=0.8
                        )
                    else:
                        print(f"Index {idx} is out of range for labels with length {len(labels)}")
                    
                    self.play(FadeOut(arrow))
            
            # Reset colors and clear process text
            self.play(
                current_vertices.animate.set_color(WHITE),
                FadeOut(process_text)
            )
            self.wait(1)
        
        # Enhanced final explanation
        final_explanation = VGroup(
            Text("Final Analysis:", font_size=20, color=GREEN),
            Text("Level-by-Level Summary:", font_size=18),
            Text("• Level 0 (Root):", font_size=16),
            Text("  - Node 5 has no cousins → Value = 0", font_size=16),
            Text("• Level 1:", font_size=16),
            Text("  - Nodes 4 and 9 are siblings, not cousins → Value = 0", font_size=16),
            Text("• Level 2:", font_size=16),
            Text("  - Nodes 1, 10 are cousins with 7", font_size=16),
            Text("  - 1, 10 get sum of 7", font_size=16),
            Text("  - 7 gets sum of 1 + 10 = 11", font_size=16)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        final_explanation.scale(0.8)
        final_explanation.move_to(process_box.get_center())
        
        self.play(Write(final_explanation))
        self.wait(4)
        
        # Clean up
        self.play(
            *[FadeOut(mob) for mob in [
                vertices, edges, labels, process_box, process_title,
                level_tracker, legend, final_explanation, subtitle
            ]]
        )

    def create_detailed_level_analysis(self, values, level, level_nodes):
        """Helper method to create detailed analysis text for each level"""
        texts = []
        if level == 0:
            texts = [
                Text("• Single root node", font_size=16),
                Text("• No cousins possible at root", font_size=16),
                Text("• Value will be set to 0", font_size=16)
            ]
        elif level == 1:
            texts = [
                Text("• Examining parent nodes", font_size=16),
                Text("• Nodes share same parent (root)", font_size=16),
                Text("• These are siblings, not cousins", font_size=16),
                Text("• Values will be set to 0", font_size=16)
            ]
        else:
            cousin_groups = self.identify_cousin_groups(values, level_nodes)
            texts = [
                Text("• Identifying cousin relationships", font_size=16),
                *[Text(f"• Group {i+1}: {', '.join(map(str, group))}", font_size=16)
                for i, group in enumerate(cousin_groups)],
                Text("• Calculating cousin sums...", font_size=16)
            ]
        return texts

    def show_advanced_test_case(self):
        subtitle = Text("Advanced Test Case Analysis", font_size=28, color=YELLOW)
        subtitle.next_to(self.title, DOWN, buff=0.7)
        
        # Enhanced initial explanation
        initial_explanation = VGroup(
            Text("Advanced Binary Tree Cousin Analysis:", font_size=20),
            Text("Key Features of this Example:", font_size=20, color=BLUE),
            Text("• Complete binary tree with 4 levels", font_size=18),
            Text("• Multiple cousin relationships per level", font_size=18),
            Text("• More complex sum calculations", font_size=18),
            Text("• Demonstrates scalability of the algorithm", font_size=18)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        initial_explanation.scale(0.8)
        initial_explanation.next_to(subtitle, DOWN, buff=0.5)
        
        self.play(Write(subtitle))
        self.play(Write(initial_explanation))
        self.wait(3)
        
        self.play(FadeOut(initial_explanation))
        
        # Create larger tree with adjusted spacing
        values = [3, 1, 2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
        vertices, edges, labels = self.create_tree_visualization(
            values,
            node_spacing=1.8,  # Adjusted spacing for larger tree
            level_spacing=1.2,
            is_advanced=True
        )
        
        # Shift tree to left side
        tree_group = VGroup(vertices, edges, labels)
        tree_group.shift(LEFT * 3 + DOWN * 1.5) 
        
        # Enhanced visualization tools
        process_box = Rectangle(height=4.5, width=5, color=BLUE_C)
        process_box.to_edge(RIGHT, buff=0.8)
        
        # Add detailed legend
        legend = VGroup(
            Text("Visualization Guide:", font_size=18, color=WHITE),
            Text("• Yellow: Active level", font_size=16),
            Text("• Green: Updated nodes", font_size=16),
            Text("• Blue: Cousin relationships", font_size=16),
            Text("• White: Unprocessed nodes", font_size=16)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        legend.scale(0.8)
        legend.next_to(process_box, DOWN, buff=0.3)
        
        level_info = VGroup(
            Text("Processing Level: ", font_size=20),
            Text("0", font_size=20, color=YELLOW)
        ).arrange(RIGHT, buff=0.2)
        level_info.next_to(process_box, UP, buff=0.2)
        
        # Show initial setup
        self.play(
            Create(edges),
            Create(vertices),
            Write(labels)
        )
        self.play(
            Create(process_box),
            Write(legend)
        )
        self.wait(1)
        
        # Process each level with enhanced explanations
        for level in range(4):
            new_level = Text(str(level), font_size=20, color=YELLOW)
            new_level.move_to(level_info[1])
            self.play(
                Transform(level_info[1], new_level) if level > 0 
                else Write(level_info)
            )
            
            level_nodes = self.get_nodes_at_level(values, level)
            current_vertices = VGroup(*[
                vertices[i] for i in level_nodes 
                if i < len(vertices) and values[i] is not None
            ])
            
            # Highlight current level
            self.play(current_vertices.animate.set_color(YELLOW))
            
            # Enhanced processing text
            process_text = VGroup(
                Text(f"Level {level} Detailed Analysis:", font_size=18, color=YELLOW),
                *self.create_advanced_level_analysis(values, level, level_nodes)
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
            process_text.scale(0.8)
            process_text.move_to(process_box.get_center())
            
            self.play(Write(process_text))
            self.wait(2)
            
            # Calculate and update values with enhanced animations
            cousin_sums = self.calculate_cousin_sums(values, level, level_nodes)
            for idx, sum_val in cousin_sums.items():
                if values[idx] is not None:
                    # Create updating arrow with path
                    start = process_box.get_left()
                    end = vertices[idx].get_center()
                    
                    arrow = Arrow(start, end, color=GREEN)
                    new_label = Text(str(sum_val), font_size=14)
                    new_label.move_to(labels[idx].get_center())
                    
                    self.play(
                        Create(arrow),
                        Transform(labels[idx], new_label),
                        Flash(vertices[idx], color=GREEN, flash_radius=0.2),
                        run_time=0.6
                    )
                    self.play(FadeOut(arrow))
            
            # Reset and clean up
            self.play(
                current_vertices.animate.set_color(WHITE),
                FadeOut(process_text)
            )
            self.wait(1)
        
        # Enhanced final summary
        summary = VGroup(
            Text("Complete Analysis Summary:", font_size=20, color=YELLOW),
            Text("1. Tree Structure:", font_size=18),
            Text("   • Perfect binary tree with 15 nodes", font_size=16),
            Text("   • 4 levels with increasing complexity", font_size=16),
            Text("2. Cousin Relationships:", font_size=18),
            Text("   • Level 1: No cousins", font_size=16),
            Text("   • Level 2: First cousin pairs appear", font_size=16),
            Text("   • Level 3: Multiple cousin groups", font_size=16),
            Text("3. Performance Notes:", font_size=18),
            Text("   • Efficient level-by-level processing", font_size=16),
            Text("   • Constant time cousin sum calculations", font_size=16)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        summary.scale(0.8)
        summary.move_to(process_box.get_center())
        
        self.play(Write(summary))
        self.wait(4)
        
        # Clean up
        self.play(
            *[FadeOut(mob) for mob in [
                vertices, edges, labels, process_box,
                level_info, legend, summary, subtitle
            ]]
        )
    def create_advanced_level_analysis(self, values, level, level_nodes):
        """Helper method to create detailed analysis text for advanced cases"""
        texts = []
        if level == 0:
            texts = [
                Text("• Examining root node (value: 3)", font_size=16),
                Text("• No cousins possible at root level", font_size=16),
                Text("• Root value will be set to 0", font_size=16)
            ]
        elif level == 1:
            texts = [
                Text("• Examining nodes 1 and 2", font_size=16),
                Text("• Both nodes share root as parent", font_size=16),
                Text("• Siblings, not cousins - values set to 0", font_size=16),
                Text("• This pattern is consistent for level 1", font_size=16)
            ]
        elif level == 2:
            texts = [
                Text("• Four nodes at this level (4,5,6,7)", font_size=16),
                Text("• First cousin relationships appear", font_size=16),
                Text("• Nodes 4,5 are cousins with 6,7", font_size=16),
                Text("• Calculating cross-parent sums", font_size=16)
            ]
        else:
            texts = [
                Text("• Eight nodes at leaf level", font_size=16),
                Text("• Multiple cousin groups present", font_size=16),
                Text("• Complex sum calculations needed", font_size=16),
                Text("• Demonstrating full algorithm capability", font_size=16)
            ]
        return texts

    def create_tree_visualization(self, values, node_spacing=2.0, level_spacing=1.2, is_advanced=False):
        """
        Enhanced tree visualization with adjustable spacing
        """
        vertices = VGroup()
        edges = VGroup()
        labels = VGroup()
        
        # Calculate tree dimensions
        max_depth = int(math.log2(len(values))) + 1
        
        # Adjust spacing based on tree size
        if is_advanced:
            node_spacing *= 0.7  # Reduce spacing for larger trees
            level_spacing *= 0.9
        
        # Calculate positions for all nodes
        positions = {}
        for i in range(len(values)):
            if values[i] is not None:
                level = int(math.log2(i + 1))
                nodes_in_level = 2 ** level
                position_in_level = i - (2 ** level - 1)
                
                # Calculate x position with adjusted spacing
                x = (position_in_level - (nodes_in_level - 1) / 2) * node_spacing
                
                # Calculate y position with adjusted spacing
                y = (max_depth - level - 1) * level_spacing
                
                positions[i] = np.array([x, y, 0])
        
        # Create vertices and labels
        for i, value in enumerate(values):
            if value is not None:
                # Create vertex
                vertex = Circle(radius=0.3, color=WHITE)
                vertex.move_to(positions[i])
                vertices.add(vertex)
                
                # Create label
                label = Text(str(value), font_size=16)
                label.move_to(vertex.get_center())
                labels.add(label)
                
                # Create edges to children
                left_child = 2 * i + 1
                right_child = 2 * i + 2
                
                for child in [left_child, right_child]:
                    if child < len(values) and values[child] is not None:
                        edge = Line(
                            positions[i],
                            positions[child],
                            color=WHITE,
                            stroke_width=2
                        )
                        edges.add(edge)
        
        return vertices, edges, labels

    def identify_cousin_groups(self, values, level_nodes):
        """
        Helper method to identify groups of cousin nodes
        Returns list of lists, where each inner list contains indices of cousin nodes
        """
        cousin_groups = []
        parent_groups = {}
        
        # Group nodes by their parent's parent (grandparent)
        for node in level_nodes:
            if values[node] is not None:
                parent = (node - 1) // 2
                grandparent = (parent - 1) // 2
                
                if grandparent not in parent_groups:
                    parent_groups[grandparent] = {}
                
                if parent not in parent_groups[grandparent]:
                    parent_groups[grandparent][parent] = []
                
                parent_groups[grandparent][parent].append(node)
        
        # Create cousin groups
        for grandparent, parents in parent_groups.items():
            if len(parents) > 1:
                parent_nodes = list(parents.values())
                for i in range(len(parent_nodes)):
                    for j in range(i + 1, len(parent_nodes)):
                        cousin_groups.append(parent_nodes[i] + parent_nodes[j])
        
        return cousin_groups

    def show_tree_properties(self):
        """
        Additional method to show important tree properties
        """
        properties_title = Text("Binary Tree Properties", font_size=28, color=YELLOW)
        properties_title.next_to(self.title, DOWN, buff=0.7)
        
        properties = VGroup(
            Text("1. Node Relationships:", font_size=20, color=BLUE),
            Text("   • Parent: (i-1)/2", font_size=18),
            Text("   • Left Child: 2i + 1", font_size=18),
            Text("   • Right Child: 2i + 2", font_size=18),
            Text("\n2. Cousin Definition:", font_size=20, color=BLUE),
            Text("   • Same level nodes", font_size=18),
            Text("   • Different parent nodes", font_size=18),
            Text("   • Parents share same parent", font_size=18),
            Text("\n3. Level Properties:", font_size=20, color=BLUE),
            Text("   • Level i has 2^i nodes max", font_size=18),
            Text("   • Perfect tree has 2^h - 1 nodes", font_size=18),
            Text("   • h is height of tree (0-based)", font_size=18)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        
        properties.scale(0.8)
        properties.next_to(properties_title, DOWN, buff=0.5)
        
        self.play(Write(properties_title))
        self.play(Write(properties))
        self.wait(3)
        
        # Create small example tree
        example_values = [1, 2, 3, 4, 5, 6, 7]
        vertices, edges, labels = self.create_tree_visualization(
            example_values,
            node_spacing=1.5,
            level_spacing=1.0
        )
        
        tree_group = VGroup(vertices, edges, labels)
        tree_group.next_to(properties, RIGHT, buff=1.0)
        
        self.play(
            Create(edges),
            Create(vertices),
            Write(labels)
        )
        
        # Add annotations
        annotations = VGroup(
            Text("Root", font_size=16).next_to(vertices[0], UP),
            Text("Level 1", font_size=16).next_to(vertices[1:3], LEFT),
            Text("Level 2", font_size=16).next_to(vertices[3:], LEFT),
            Arrow(vertices[1].get_center(), vertices[3].get_center(), color=YELLOW),
            Arrow(vertices[2].get_center(), vertices[6].get_center(), color=YELLOW)
        )
        
        self.play(Write(annotations))
        self.wait(2)
        
        # Clean up
        self.play(
            *[FadeOut(mob) for mob in [
                properties_title, properties, vertices, edges,
                labels, annotations
            ]]
        )

    def add_helper_methods(self):
        """
        Additional helper methods for better visualization
        """
        def get_node_color(self, value, level, current_level):
            """Determine node color based on state"""
            if level == current_level:
                return YELLOW
            elif value == 0:
                return BLUE_C
            return WHITE

        def create_node_label(self, value, size=16):
            """Create formatted node label"""
            return Text(str(value), font_size=size)

        def create_arrow_between_nodes(self, start, end, color=YELLOW):
            """Create animated arrow between nodes"""
            return Arrow(
                start.get_center(),
                end.get_center(),
                color=color,
                buff=0.2
            )

        def create_highlight_box(self, text, color=YELLOW):
            """Create highlighted box around text"""
            box = SurroundingRectangle(text, color=color, buff=0.1)
            return box

        return locals()
    
    def show_time_complexity(self):
        # Keeping the original time complexity section
        title = Text("Time and Space Complexity", font_size=32)
        title.to_corner(UL, buff=0.5)
        
        complexity = VGroup(
            Text("Time Complexity:", font_size=24, color=YELLOW),
            Text("• BFS Traversal: O(n)", font_size=20),
            Text("• Processing each level: O(n)", font_size=20),
            Text("• Total: O(n)", font_size=20, color=GREEN),
            Text("Space Complexity:", font_size=24, color=YELLOW).shift(DOWN),
            Text("• Queue: O(w) where w is max width", font_size=20),
            Text("• HashMaps: O(n)", font_size=20),
            Text("• Total: O(n)", font_size=20, color=GREEN)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        
        complexity.next_to(title, DOWN, buff=0.5)
        
        self.play(Write(title))
        for line in complexity:
            self.play(Write(line))
            self.wait(0.3)
        
        self.wait(2)

    # Helper methods
    def get_nodes_at_level(self, values, level):
        start = 2**level - 1
        end = 2**(level + 1) - 1
        return range(start, min(end, len(values)))

    def create_level_processing_text(self, values, level, nodes):
        text_lines = [
            f"Processing Level {level}",
            f"Nodes: {[values[i] for i in nodes if values[i] is not None]}",
            "Finding cousins...",
            "Calculating sums..."
        ]
        return VGroup(*[Text(line, font_size=16) for line in text_lines]).arrange(DOWN, buff=0.2)

    def create_advanced_processing_text(self, values, level, nodes):
        text_lines = [
            f"Level {level} Analysis",
            f"Active Nodes: {[values[i] for i in nodes if values[i] is not None]}",
            "Grouping by parents...",
            "Finding cousin relationships..."
        ]
        return VGroup(*[Text(line, font_size=16) for line in text_lines]).arrange(DOWN, buff=0.2)
    
    def create_cousin_relationships_text(self, values, level, nodes):
        parent_groups = defaultdict(list)
        for idx in nodes:
            if values[idx] is not None:
                parent = (idx - 1) // 2
                parent_groups[parent].append(values[idx])
        
        text_lines = [
            "Cousin Groups:",
            *[f"Parent {values[parent]}: {children}" 
              for parent, children in parent_groups.items()
              if values[parent] is not None]
        ]
        return VGroup(*[Text(line, font_size=14) for line in text_lines]).arrange(DOWN, buff=0.1)
    
    # def create_tree_visualization(self, values, is_advanced=False):
    #     vertices = VGroup()
    #     edges = VGroup()
    #     labels = {}
        
    #     # Adjust spacing based on tree size
    #     level_width = 6 if not is_advanced else 4
    #     level_height = 1.2 if not is_advanced else 0.8
    #     circle_radius = 0.25 if not is_advanced else 0.15
    #     font_size = 18 if not is_advanced else 14
        
    #     def create_node(value, position):
    #         # Create circle with slightly thicker stroke
    #         circle = Circle(radius=circle_radius, color=WHITE, stroke_width=2)
    #         # Add shadow effect
    #         shadow = Circle(radius=circle_radius, color=GREY, stroke_width=1)
    #         shadow.shift(RIGHT * 0.02 + DOWN * 0.02)
    #         # Create label
    #         label = Text(str(value), font_size=font_size)
    #         label.move_to(circle.get_center())
    #         # Group everything
    #         node = VGroup(shadow, circle, label)
    #         node.move_to(position)
    #         return node, label
        
    #     max_depth = int(math.log2(len(values))) + 1
        
    #     # Calculate vertical offset to center the tree
    #     total_height = (max_depth - 1) * level_height
    #     y_offset = total_height / 2
        
    #     # Create nodes with improved visual style
    #     for i, value in enumerate(values):
    #         if value is not None:
    #             level = int(math.log2(i + 1))
    #             position_in_level = i - (2**level - 1)
    #             total_positions = 2**level
                
    #             x = (position_in_level - (total_positions - 1)/2) * (level_width / (2**level))
    #             y = -level * level_height + y_offset
                
    #             node, label = create_node(value, np.array([x, y, 0]))
    #             vertices.add(node)
    #             labels[i] = label
                
    #             # Create straight edges with improved style
    #             if i > 0:
    #                 parent_idx = (i - 1) // 2
    #                 if values[parent_idx] is not None:
    #                     parent_pos = vertices[len(list(filter(lambda x: x is not None, values[:parent_idx])))].get_center()
    #                     # Create straight edge with slightly thicker stroke
    #                     edge = Line(
    #                         start=parent_pos,
    #                         end=node.get_center(),
    #                         stroke_width=1.5 if is_advanced else 2,
    #                         stroke_opacity=0.8  # Slightly transparent for better look
    #                     )
    #                     edges.add(edge)
        
    #     # Group everything and center
    #     tree = VGroup(edges, vertices)
    #     tree.move_to(ORIGIN)
    #     tree.shift(DOWN * 0.5)
        
    #     return vertices, edges, labels

    def calculate_cousin_sums(self, values, level, nodes):
        # Enhanced cousin sum calculation with grouping by parents
        parent_groups = defaultdict(list)
        node_indices = defaultdict(list)
        
        # Group nodes by their parents
        for idx in nodes:
            if values[idx] is not None:
                parent = (idx - 1) // 2
                parent_groups[parent].append(values[idx])
                node_indices[parent].append(idx)
        
        cousin_sums = {}
        # Calculate sums for each node
        for parent, indices in node_indices.items():
            # Get all values from other parents' children
            cousin_values = []
            for other_parent, other_children in parent_groups.items():
                if other_parent != parent:
                    cousin_values.extend(other_children)
            
            # Calculate sum for each node in current parent group
            for idx in indices:
                cousin_sums[idx] = sum(cousin_values)
        
        return cousin_sums

    def create_highlight_animation(self, mobject, color=YELLOW):
        # Create a highlighting effect for nodes
        highlight = mobject.copy()
        highlight.set_color(color)
        highlight.set_stroke(width=4)
        return Succession(
            ShowCreationThenDestruction(highlight),
            Wait(0.2)
        )

    def create_value_update_animation(self, old_value, new_value, position):
        # Create smooth animation for value updates
        new_text = Text(str(new_value), font_size=18)
        new_text.move_to(position)
        return Transform(
            old_value,
            new_text,
            path_arc=PI/2,
            run_time=0.5
        )

    def create_level_indicator(self, level, total_levels):
        # Create a visual indicator for current level progress
        progress = VGroup()
        for i in range(total_levels):
            dot = Circle(radius=0.1)
            dot.set_fill(GREEN if i < level else GREY, opacity=1)
            progress.add(dot)
        progress.arrange(RIGHT, buff=0.2)
        return progress

    def create_explanation_box(self, text, position=ORIGIN, width=4, height=2):
        # Create a box with explanation text
        box = Rectangle(width=width, height=height, color=BLUE)
        text_mob = Text(text, font_size=16)
        text_mob.set_width(width - 0.5)
        text_mob.move_to(box.get_center())
        return VGroup(box, text_mob)

    def create_legend(self):
        # Create a legend for the visualization
        legend_items = VGroup(
            VGroup(
                Circle(radius=0.1, color=YELLOW),
                Text("Current Node", font_size=14)
            ).arrange(RIGHT, buff=0.2),
            VGroup(
                Circle(radius=0.1, color=GREEN),
                Text("Updated Value", font_size=14)
            ).arrange(RIGHT, buff=0.2),
            VGroup(
                Circle(radius=0.1, color=BLUE),
                Text("Cousin Node", font_size=14)
            ).arrange(RIGHT, buff=0.2)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        
        legend_box = SurroundingRectangle(legend_items, color=WHITE, buff=0.2)
        return VGroup(legend_box, legend_items)