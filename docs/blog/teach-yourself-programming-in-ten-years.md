---
title: "Teach Yourself Programming in Ten Years"
type: "blog"
date: "2024-10-21"
license: "cc-by-nc-sa-4.0"
---

# Teach Yourself Programming in Ten Years
- Posted in 2022
- Revised in 2023
- Edited in 2024

## Introduction
Learning to program is a long, often frustrating journey, but with persistence and the right mindset, it's achievable. Over the past decade, I've come to understand that programming isn't just about mastering syntax or tools—it's about developing patience, problem-solving skills, and a solid foundation in mathematics.

In this article, I'll share the lessons I've learned through my self-taught journey. Whether you're just starting or looking to improve your skills, the insights here will help guide you in the right direction.

## Browsing, Lurking, and Commiserating
A few years ago, I stumbled upon a question in the r/learnprogramming subreddit: *What can help amateur coders learn faster?*

The top-voted response was simple: *Take your time.* This advice may seem counterintuitive in an age of quick-fix solutions, but it's a hard truth—programming is a skill that can't be rushed.

Another response that struck me was from /u/RonaldHarding, who highlighted the difference between learning syntax and learning how to solve real-world problems. Syntax can be learned relatively quickly, but becoming a proficient programmer requires an understanding of data structures, algorithms, networking, operating systems, and more.

His words resonated deeply with me because I've spent years feeling exactly like this—like I was learning the basics but struggling to apply them meaningfully. It was only after accepting that programming is a long-term commitment that I started to make real progress.

## Programming is Mathematics (Whether You Like It or Not)
No one told me when I started out, but programming is, at its core, mathematics. Like many programmers, I initially dreaded math, but eventually, I couldn't ignore its role in solving problems and writing efficient code.

Computer Science is grounded in mathematical concepts—everything from logic gates to algorithms is rooted in mathematical reasoning. Understanding this early on can save you from frustration later. It's not just about crunching numbers but about developing the problem-solving mindset that math cultivates.

So, if you're serious about programming, you'll need to embrace math. I won't sugarcoat it—it's a band-aid that's better ripped off quickly. The sooner you accept this, the sooner you can start building the skills that will make you a more effective programmer.

### Persistence is Key
Programming is a marathon, not a sprint. It's easy to pick up a language, but learning to apply it to real-world problems is where things get tough. Like exercising a muscle, developing problem-solving skills takes time and consistent effort.

You don't need a formal education to become a good programmer, but you do need discipline. Trial and error is part of the process, and it's how you grow. Stay with the problems longer, keep learning from your mistakes, and you'll get there. As Einstein said: *“It's not that I'm so smart; it's just that I stay with problems longer.”*

### Mathematical Foundations
Before diving into programming, make sure you have a solid foundation in mathematics. This will help you grasp the underlying principles behind many programming concepts, especially as you move into more advanced topics.

Here's a list of the essential math subjects that will serve you well:

| Prerequisite Math |
| ----------------- |
| Arithmetic        |
| Algebra           |
| Geometry          |
| Trigonometry      |
| Calculus          |
| Discrete Math     |
| Statistics        |
| Linear Algebra    |

Each of these subjects contributes to different aspects of programming. For example, Algebra introduces the concept of variables and equations, which directly translates to how we handle data in code. Discrete Math helps with understanding algorithms and logic, while Calculus and Linear Algebra come in handy for fields like computer graphics or machine learning.

If you've already got a solid math background, you're ready to start diving into programming. If not, consider brushing up on these subjects to give yourself a head start.

Now that you've got a solid foundation in the fundamentals of programming, the next step is choosing the right tools for the job. But here's something that took me a while to realize: the tools you use aren't just a matter of preference—they're shaped by the platform you're working on. Programming languages, like the hardware and operating systems they're built on, evolve within specific ecosystems. Understanding the relationship between hardware, the operating system, and the tools available is key to making smarter choices when picking your programming language.

Let's break down how different platforms influence the languages you should consider and why understanding this connection is key to working efficiently and effectively.

## Choose a Language
When selecting a programming language, it's important to think beyond just syntax or ease of learning. The real key is understanding how your choice fits into the broader ecosystem of hardware, operating systems, and tools. 

Languages don't exist in a vacuum—they're shaped by the platforms they run on. Every project has a foundation, and that foundation starts with hardware. The hardware determines the operating system, and the operating system dictates the available tools and languages. The language you choose should align with the platform you're targeting, making your work more efficient and your code more portable.

Let's break it down:

### Hardware: The Foundation of Everything
Hardware is the base layer of any computing ecosystem. Whether it's a CPU, GPU, or specialized hardware like ARM processors, the hardware defines the fundamental capabilities of the system. At this level, languages are designed to interact directly with the architecture.

- **Assembly**: The lowest-level language that directly interacts with hardware. Every processor has its own instruction set architecture (ISA), and Assembly is the language used to work with that ISA. It's crucial for situations where performance and direct control over the hardware are necessary.
- **C**: Created at Bell Labs for building the UNIX operating system, C is both portable and low-level enough to interact with hardware efficiently. It abstracts away some of the complexities of Assembly while remaining close to the machine, making it ideal for system-level programming.

### Operating Systems: Managing Hardware
The operating system (OS) acts as the intermediary between the hardware and the user space, providing the environment for applications to run. Each OS has its own set of languages that are optimized for interacting with its core components, both for system development and automation through scripting.

- **Linux**: Languages like **C** and **C++** dominate because Linux itself is largely built with them. These languages provide direct control over system resources like memory, processes, and file systems, making them essential for kernel development and system-level applications. **Bash** is widely used for scripting and automating tasks within the Linux environment.

- **Windows**: The **.NET** ecosystem is tightly integrated with Windows, making **C#** a natural choice for developing desktop applications. **C++** remains important for system-level programming and game development, especially when working with DirectX. For scripting and automation, **PowerShell** is commonly used, offering a powerful command-line toolset within Windows.

- **Mac OS X**: For native macOS and iOS development, **Objective-C** and **Swift** are the key languages. These languages are tightly integrated with Apple's frameworks and offer the best tools for building applications within Apple's ecosystem. **Bash** is also frequently used for scripting and automating tasks within Mac OS X's UNIX-like environment.

### Ecosystem and Tooling: Building on Top of the OS
The tools you use as a programmer are defined by the combination of hardware and operating system, forming the larger ecosystem. This ecosystem provides the libraries, frameworks, and APIs that shape how you build applications.

- **Web Development**: The web is a unique ecosystem, mostly independent of hardware or OS. Whether you're on Linux, Windows, or Mac, the core languages—**JavaScript**, **HTML**, and **CSS**—remain constant. However, backend languages and tools may vary depending on your platform. **Node.js**, **Python**, and **Ruby** are popular choices in a Linux environment, whereas **ASP.NET** may dominate in Windows.
- **Game Development**: Platforms like **Windows** and **consoles** are often driven by **C++**, as it offers the performance necessary for graphics-intensive applications. Game engines like Unity use **C#**, which integrates seamlessly with the .NET environment on Windows, while **Lua** is frequently used for scripting within engines.
- **Mobile Development**: For mobile platforms like iOS and Android, the choice of language is clear-cut. **Swift** and **Objective-C** for iOS, and **Java** or **Kotlin** for Android, as these are the languages that give you access to native mobile APIs provided by the OS vendors.

### Portability: Making Your Code Work Across Platforms
Some languages are built with portability in mind, meaning they can be used across different platforms with minimal changes. This was one of the reasons **C** became so popular—it could be compiled and run on various hardware and operating systems without significant rewrites. Similarly, **Python** is often chosen for its ability to run on almost any platform, whether you're on Linux, Windows, or Mac OS X.

### Final Thoughts
The project you're working on should always determine the tools you use, and those tools are shaped by the ecosystem around them. By understanding the relationship between hardware, operating systems, and the software stack, you can make smarter choices about which language to learn and use. Instead of focusing purely on the features of a language, consider the platform it operates on, the problems it was designed to solve, and how it fits into the broader ecosystem.

### Learn About What You Don't Know
You might feel like you've covered a lot, but there are core aspects of programming that are often overlooked, especially if you're self-taught. Some of the key areas you may still need to dive into include:
- **Algorithms and Data Structures**
- **Compiler Design**
- **Systems Design**
- **Design Patterns**
- **Agile & Scrum Methodologies**
- **Test-Driven Development (TDD)**
- **Behavior-Driven Development (BDD)**

These are crucial to becoming not just a coder, but a well-rounded software engineer. You don't need to master all of them at once, but being aware of what's out there is the first step. As the saying goes, "You don't know what you don't know."

### Tools of the Trade
The tools we use will always evolve, but the fundamentals rarely change—they just get updated over time. This is where many self-taught developers get stuck: How can you improve if you don't know what gaps exist in your knowledge?

Here are a few essential resources to help you build that strong foundation. They're just a small sample in the vast sea of knowledge out there, but they cover critical topics that will stick with you throughout your career:

- [Calculus](https://leanpub.com/apexcalculus)
- [Discrete Mathematics](https://discrete.openmathbooks.org/dmoi3.html)
- [Statistics and Probability](https://stats.libretexts.org/Courses/Las_Positas_College/Math_40%3A_Statistics_and_Probability)
- [Linear Algebra](https://understandinglinearalgebra.org/home.html)
- [Digital Signal Processing](https://www.dspguide.com/)
- [Introduction to Algorithms](https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/)
- [Design Patterns](https://sourcemaking.com/)
- [Refactoring](https://refactoring.guru/)
- [Crafting Interpreters](https://craftinginterpreters.com/contents.html)

### Conclusion
I've got plenty more bookmarked, so feel free to comment and ask for more. If I can help, I will. And if I don't respond, it's probably because I don't know the answer—hopefully someone more experienced will.

Best of luck on your programming journey. Remember, it's the journey that matters, not the destination. The destination will be a byproduct of the effort and learning you put into the process.

## References
- [Original Post](https://www.reddit.com/r/learnprogramming/comments/zpevpm/teach_yourself_programming_in_ten_years/)
- [Peter Norvig's Teach Yourself Programming in Ten Years](https://norvig.com/21-days.html)
- [Why Learning to Code is So Damn Hard](https://medium.com/@andrewlatta/why-learning-to-code-is-so-damn-hard-303eae632820)

---

<p align="center">Copyright (C) 2022 Austin Berrio</p>
