+++
title = "Tutoring systems"
date = "2024-02-18"
tags = ["tutoring-systems"]
draft = false
+++

Design and development methods:
1. needs assesment
2. cognitive task analysis - how domain experts think when solving problems
3. initial tutor implementation
4. evaluation

An intelligent tutor system should enable the student to work to the successful conclusion of problem solving.

- Represent student competence as a production set.
- Communicate the goal structure underlying the problem solving.
- Provide instruction in the problem solving context.
- Promote an abstract understanding of the problem-solving knowledge.
- Minimize working memory load.
- Provide immediate feedback on errors.
- Adjust the grain size of instruction with learning.
- Facilitate successive approximations to the target skill

4 Components architecture:
1. **domain model (expert knowledge)**: contains the concepts, rules, and problem-solving strategies of the domain to be learned
2. **student model**: gather explicit and implicit data about the student, must use this data to create a representation of the student knowledge
and learning process, must use this to select optimal pedagogical strategies. 1) Corrective: to help
eradicate bugs in the student's knowledge; 2) Elaborative: to help correct 'incomplete' student knowledge; 3) Strategic: to help initiate significant changes in the
tutorial strategy other than the tactical decisions of 1 and 2 above; 3) Diagnostic:
to help diagnose bugs in the student's knowledge; 5) Predictive: to help determine
the student's likely response to tutorial actions; 6) Evaluative: to help assess the
student or the ITS
3. **tutoring model**: receives input from the domain and student models and makes decisions about tutoring strategies and actions
4. **interface component**

# References
[https://en.wikipedia.org/wiki/Intelligent_tutoring_system#cite_ref-Nkambou_29-1](https://en.wikipedia.org/wiki/Intelligent_tutoring_system#cite_ref-Nkambou_29-1)
[https://www.youtube.com/watch?v=B1wBwVA90M4](https://www.youtube.com/watch?v=B1wBwVA90M4)
