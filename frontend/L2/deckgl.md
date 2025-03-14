# DeckGL Data Loading and Optimization Test

Welcome!

This take-home test is designed to evaluate your expertise in **data loading and optimization** within a **DeckGL application**. While UI implementation is not the focus of this exercise, we aim to assess your proficiency in memory management, efficient data handling, and automated testing.

---

## Objective

The task involves creating a React application that:

1. Loads a dataset into a DeckGL map visualization.
2. Implements optimizations for memory and performance.
3. Includes automated testing for verifying the integrity of the data-loading process, especially for edge cases like partial or failed data loads.

## Requirements

### 1. **Data Loading**
- Load a given dataset (you can mock one or use a sample GeoJSON dataset). Alternatively, you can request access to one of our datasets [here](https://drive.google.com/drive/folders/1Jymhj1gIvx7L858M8QTNFYiGykvaCYkM) or a larger dataset [here](https://drive.google.com/file/d/1C-nHyXE_hLtUz0WvARgwiO1QRd0KcwNU/view)
- Handle large datasets efficiently to prevent memory overflows or application crashes.
- Ensure the application is capable of loading and rendering the data in DeckGL layers.
- Explore **data types** for efficient data handling on the frontend.

### 2. **Memory Management**
- Optimize memory usage when handling large datasets.
- Consider strategies such as **lazy loading**, **chunking**, and **data compression** to reduce memory overhead.
- Utilize **Chrome Developer Tools** to analyze memory usage and identify potential bottlenecks or memory leaks.

### 3. **Data Compression**
- Implement data compression techniques to reduce payload size (e.g., gzip, zlib, or binary formats like Arrow.js).
- Evaluate the trade-offs between data compression and decompression time to maintain performance.
- Ensure compressed data can be seamlessly integrated into DeckGL layers.

### 4. **Data Testing**
- Implement automated tests to ensure:
  - The dataset has loaded successfully.
  - The application handles scenarios where the dataset is partially loaded or not loaded at all.
  - Data consistency and integrity are maintained.
- Use testing libraries like **Jest** or **React Testing Library**.
- Test edge cases where malformed or incomplete datasets are provided.

## Guidelines

### Dataset
- You can use any publicly available dataset or mock one if needed.
- Ensure the dataset is in a format compatible with DeckGL layers (e.g., GeoJSON).

### Technology Stack
- Use **React** for the application.
- Use **DeckGL** for data visualization.
- Implement tests using **Jest**, **React Testing Library**, or any other testing framework of your choice.

### Bonus Points
- Implement streaming data loading (e.g., loading in chunks).
- Provide a clear mechanism to display errors or warnings for failed data loads.
- Document your thought process and decision-making in the code or a separate `README.md` file.
- Explore advanced data loading libraries to improve performance.

## Submission

1. Fork or clone the provided repository (link shared in your email).
2. Complete the implementation.
3. Share the repository link with us (ensure we have access to view it).
4. Include a brief `README.md` describing:
   - Your approach to solving the problem.
   - Any challenges you faced.
   - How to run your tests and application locally.

## Evaluation Criteria

1. **Data Loading and Optimization**:
   - Efficient handling of large datasets.
   - Strategies for memory optimization and data compression.

2. **Code Quality**:
   - Clean, maintainable, and production-grade code.
   - Adherence to best practices and conventions.

3. **Testing**:
   - Comprehensive automated tests for data-loading scenarios.
   - Robustness against edge cases (e.g., partial or failed loads).

4. **Documentation**:
   - Clear explanation of your approach.
   - Instructions for running and testing the application.

5. **Performance**:
   - Effective handling of computational and rendering overhead.
   - Demonstrated usage of Chrome Developer Tools for memory analysis.

## Timeline

You will have **7 days** from receiving this task to submit your solution. Please ensure your work is complete and well-tested before submission.

---

## Submission
- Create a private repo and add AISuhasDattatreya as a reviewer to your PR. 
- Submit the PR link and the your notes (timelines, breakdown and what you've implented) to suhas@advanced-infrastructure.co.uk
- We'll go over your code together and discuss your architecture 

---
We look forward to seeing your expertise in action. Good luck, and happy coding!
