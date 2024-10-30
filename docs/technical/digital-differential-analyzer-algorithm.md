---
title: "The Digital Differential Analyzer Algorithm"
type: "blog"
date: "2024-07-05"
license: "cc-by-nc-sa-4.0"
---

# The Digital Differential Analyzer Algorithm

The [Digital Differential Analyzer](https://en.wikipedia.org/wiki/Digital_differential_analyser) is used for line drawing in computer graphics, providing a simple and efficient method to render lines. Understanding the underlying mathematics behind algorithms like DDA is crucial for developing creative solutions to complex problems in computer graphics and video game development.

## Introduction

The DDA (Digital Differential Analyzer) algorithm is an efficient way to draw a straight line between two points in a 2D space. The core idea is to calculate the intermediate points along the line by incrementally adding a small, fixed-step size to the starting point's coordinates.

## Mathematical Foundations

The DDA (Digital Differential Analyzer) algorithm can be understood through several mathematical concepts:

- **Midpoint Calculation**: Determines the midpoint between two endpoints of a line segment.
- **Iterative Increments**: Moves to the next point by adding fractional increments to each coordinate.
- **Slope and Rate of Change**: Utilizes the slope and rate of change of a line.
- **Average Rate of Change**: Applies the average rate of change.
- **Gradient Steps**: Incrementally determines the next point based on the number of steps with respect to a gradient.

This document aims to provide an accessible understanding of the DDA algorithm while connecting it to relevant mathematical concepts from various resources, such as Blitzer's *Introductory Algebra* and Wiley's *Applied Calculus*.

## Algorithm Steps

### 1. Input the coordinates of the start $(x_1, y_1)$ and end $(x_2, y_2)$ points

The algorithm begins by taking the coordinates of the two endpoints of a line segment. Let’s denote them as $(x_1, y_1)$ for the starting point and $(x_2, y_2)$ for the ending point.

#### Defining Our Parameters

- **Starting Point**: Define the starting point as $start = (x_1, y_1) = (0, 0)$.
- **Ending Point**: Define the ending point as $end = (x_2, y_2) = (4, 5)$.

#### Data Structures for Points

We define a data structure representing points that use floating-point precision. This provides higher fidelity and range of expression, which is particularly useful for rendering graphics accurately.

> Note: While SDL provides an `SDL_FPoint` structure for this purpose, we will use our custom `FloatPoint` structure for illustration.

```c
typedef struct FloatPoint { // Coordinates of a point
    float x; // horizontal axis
    float y; // vertical axis
} float_point_t; // type alias
```

#### Instantiating Points

We then create instances of this structure for the starting and ending points:

```c
// Example points for illustration
float_point_t start = {0.0f, 0.0f};  // x_1, y_1
float_point_t end   = {4.0f, 5.0f};  // x_2, y_2
```

### 2. Calculate the differences between the coordinates

We define the **Slope of a Line** as follows:

$$\text{slope} = \frac{Δy}{Δx} = \frac{y_2 - y_1}{x_2 - x_1}$$

The changes in $x$ and $y$ represent the horizontal and vertical distances between the start and end points.

- **Change in $y$ ($\Delta y$)** is defined as $\Delta y = y_2 - y_1$
- **Change in $x$ ($\Delta x$)** is defined as $\Delta x = x_2 - x_1$

Given $(x_1, y_1) = (0.0f, 0.0f)$ and $(x_2, y_2) = (4.0f, 5.0f)$, we have:

$$\Delta y = y_2 - y_1 = 5.0f - 0.0f = 5.0f$$

$$\Delta x = x_2 - x_1 = 4.0f - 0.0f = 4.0f$$

We can reason this as having a 2-dimensional plane where we move **right** by 4 units and **upward** by 5 units. The **Slope of the Line (m)** between these points is $\frac{Δy}{Δx} = \frac{5.0f}{4.0f}$ (or $1.25f$).

We can define the changes in the positions of these points in C as follows:

```c
// Calculate delta values
float_point_t delta = {
    .y = end.y - start.y,
    .x = end.x - start.x,
};
```

### 3. Determine the number of steps required to draw the line

The number of steps required to draw the line is determined by the maximum of the absolute values of $\Delta x$ and $\Delta y$. This ensures that we take enough steps to cover the entire line.

$$\text{steps} = \max(|\Delta x|, |\Delta y|)$$

Given $\Delta x = 4.0f$ and $\Delta y = 5.0f$, we calculate the steps as follows:

$$\text{steps} = \max(|4.0f|, |5.0f|) = 5$$

This calculation is straightforward with whole integers but can become more complex with floating-point values, which is beyond the scope of this article.

We can calculate this in C by defining a function to determine the steps:

```c
// Function to calculate the maximum of two integer values
int calculate_steps(float_point_t delta) {
    // Explicitly type cast to an integer so we can set the limit
    int x = (int) delta.x;
    int y = (int) delta.y;
    // Return the limit based on the point's axis with the greater absolute value
    return abs(x) > abs(y) ? abs(x) : abs(y);
}
```

In the main implementation, we use this function to calculate the steps:

```c
// Calculate the number of steps required
int steps = calculate_steps(delta);
```

### 4. Calculate the increments for each step in $x$ and $y$

The increments $y_{increment}$ and $x_{increment}$ are the changes in the $y$ and $x$ coordinates for each step. These increments determine how much to move in the $y$ and $x$ directions at each step to reach the next point on the line.

$$y_{increment} = \frac{\Delta y}{steps}$$

$$x_{increment} = \frac{\Delta x}{steps}$$

Given $\Delta x = 4.0f$, $\Delta y = 5.0f$, and $steps = 5$, we calculate the increments as follows:

$$y_{increment} = \frac{5.0f}{5} = 1.0f$$

$$x_{increment} = \frac{4.0f}{5} = 0.8f$$

We can implement this in C as follows:

```c
// Calculate increment values
float_point_t increment = {
    .y = delta.y / (float) steps,
    .x = delta.x / (float) steps,
};
```

_Note that we type cast `steps` back to `float` to ensure the division yields a floating-point result. This step, similar to when we calculated the differences between the coordinates, highlights a limitation of the DDA algorithm as it may lose precision during this phase of the process._

### 5. Initialize the starting point $(x, y)$

The starting point $(x, y)$ is initialized to the starting coordinates $(x_1, y_1)$.

$$x_{current} = start$$

We initialize the current point to the starting point in our C code as follows:

```c
// Initialize current point to start point
float_point_t current = start;
```

This sets the starting point of the line, from which the algorithm will begin incrementing to plot each point along the line.

### 6. Loop through the number of steps, incrementing the current point and plotting it

For each step, the algorithm increments the $x$ and $y$ coordinates by $x_{increment}$ and $y_{increment}$ respectively. The new point $(x, y)$ is then plotted. This process repeats until all steps are completed, effectively drawing the line from the start point to the end point.

$$
\begin{aligned}
    \sum_{i = 0}^{i \leq steps}
    \text{plot}(x_i, y_i) \quad \text{where} \quad
    \begin{cases}
        x_{i+1} = x_i + x_{increment} \\
        y_{i+1} = y_i + y_{increment}
    \end{cases}
\end{aligned}
$$

In our C code, we implement the loop to increment the current point and plot it as follows:

```c
// Loop through and plot each point
for (int i = 0; i <= steps; i++) {
    SDL_RenderDrawPointF(renderer, current.x, current.y);
    current.y += increment.y;
    current.x += increment.x;
}
```

The `SDL_RenderDrawPointF` function plots the current point on the screen. The `current` point is then incremented by $x_{increment}$ and $y_{increment}$ for each step. This continues until the loop has run for the total number of steps calculated earlier.

- **Incrementing the Coordinates**: The current $x$ and $y$ coordinates are incremented by the values of $x_{increment}$ and $y_{increment}$. This ensures that the points are spaced evenly along the line.
  
- **Plotting the Points**: The `SDL_RenderDrawPointF` function is responsible for rendering the point on the screen. By using the current floating-point coordinates directly, it ensures precision in the rendering process.

## Putting it all together

### Step-by-Step Explanation

1. **Initialize the Endpoints**:
   - **Define the start and end points**: Specify the coordinates of the start $(x_1, y_1)$ and end $(x_2, y_2)$ points using floating-point precision.

2. **Calculate Differences**:
   - **Compute differences**: Determine $\Delta x$ and $\Delta y$, the changes in $x$ and $y$ coordinates between the start and end points.

3. **Calculate Steps**:
   - **Determine steps**: Calculate the number of steps required to draw the line as the maximum of $|\Delta x|$ and $|\Delta y|$.

4. **Calculate Increments**:
   - **Compute increments**: Calculate $x_{increment}$ and $y_{increment}$, the incremental changes in $x$ and $y$ coordinates per step.

5. **Initialize and Plot**:
   - **Initialize current point**: Set the starting point $(x_{current}, y_{current})$ to $(x_1, y_1)$.
   - **Plot starting point**: Render the starting point on the screen.

6. **Iterate and Plot**:
   - **Increment and plot**: Iterate through each step, updating $(x_{current}, y_{current})$ by adding $x_{increment}$ and $y_{increment}$ respectively, and plot each updated point using `SDL_RenderDrawPointF`.

### Code Implementation

Here's a complete implementation of the DDA algorithm in C:

```c
// Example implementation of the Digital Differential Analyzer (DDA) algorithm
void draw_line(SDL_Renderer* renderer, float_point_t start, float_point_t end) {
    // Calculate delta values
    float_point_t delta = {
        .y = end.y - start.y,
        .x = end.x - start.x,
    };

    // Calculate the number of steps required
    int steps = calculate_steps(delta);

    // Calculate increment values
    float_point_t increment = {
        .y = delta.y / (float) steps,
        .x = delta.x / (float) steps,
    };

    // Initialize current point to start point
    float_point_t current = start;

    // Loop through and plot each point
    for (int i = 0; i <= steps; i++) {
        SDL_RenderDrawPointF(renderer, current.x, current.y);
        current.y += increment.y;
        current.x += increment.x;
    }
}
```

### Integration with SDL

To integrate this function into an SDL application, we need to initialize SDL, create a window and renderer, and then call the `draw_line` function within the rendering loop. Here’s a complete example:

```c
#include <SDL2/SDL.h>
#include <stdio.h>

// Define your float_point_t structure here

// Include the draw_line function here

int main(int argc, char* argv[]) {
    // Initialize SDL
    if (SDL_Init(SDL_INIT_VIDEO) != 0) { // errors on truthy values
        fprintf(stderr, "SDL_Init Error: %s\n", SDL_GetError());
        return 1;
    }

    // Create SDL window
    SDL_Window* window = SDL_CreateWindow(
        "DDA Line Drawing",
        SDL_WINDOWPOS_UNDEFINED,
        SDL_WINDOWPOS_UNDEFINED,
        640,
        480,
        SDL_WINDOW_SHOWN
    );
    if (NULL == window) {
        fprintf(stderr, "SDL_CreateWindow Error: %s\n", SDL_GetError());
        SDL_Quit();
        return 1;
    }

    // Create SDL renderer
    SDL_Renderer* renderer
        = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED | SDL_RENDERER_PRESENTVSYNC);
    if (NULL == renderer) {
        SDL_DestroyWindow(window);
        fprintf(stderr, "SDL_CreateRenderer Error: %s\n", SDL_GetError());
        SDL_Quit();
        return 1;
    }

    // Set the background to black
    SDL_SetRenderDrawColor(renderer, 0, 0, 0, SDL_ALPHA_OPAQUE);
    // Clear the window
    SDL_RenderClear(renderer);

    // Define start and end points here
    float_point_t start = {0.0f, 0.0f};     // x_1, y_1
    float_point_t end   = {320.0f, 240.0f}; // x_2, y_2

    // Set the line color to white
    SDL_SetRenderDrawColor(renderer, 255, 255, 255, SDL_ALPHA_OPAQUE);

    // Draw the line using DDA algorithm
    draw_line(renderer, start, end);

    // Present the renderer
    SDL_RenderPresent(renderer);

    // Wait for a few seconds before quitting
    SDL_Delay(5000);

    // Cleanup
    SDL_DestroyRenderer(renderer);
    SDL_DestroyWindow(window);
    SDL_Quit();

    return 0;
}
```

This example initializes SDL, creates a window and renderer, and uses the `draw_line` function to draw a line between two points. The window displays the line for 5 seconds before quitting.

## Conclusion

The Digital Differential Analyzer (DDA) algorithm is a fundamental method for line drawing in computer graphics, offering a simple yet effective way to render lines. By understanding and implementing the DDA algorithm, we gain insight into how graphics systems translate mathematical descriptions into visual representations.

This document outlines the steps to implement the DDA algorithm, emphasizing the mathematical concepts that underlie each step. By exploring these connections, we deepen our understanding of both the algorithm and the mathematical principles that support it.

This document's approach serves as a valuable reference for learning and implementing the DDA algorithm, bridging the gap between theory and practical application in computer graphics.
