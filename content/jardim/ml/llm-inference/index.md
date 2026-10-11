+++
title = "LLM Inference"
aliases = ["/lists/"]
tags = ["machine-learning"]
draft = false

+++

The lifecycle of a model is implemented in the following steps:

1. Open the model file and read the shapes of the weights, but don't load the
   weights yet.

2. Using the loaded shapes and optional metadata, instantiate a model struct
   with `Tensor`s, representing the shape and layout of each layer of the NN.

3. Compile the model struct and it's `forward` function into an accelerator
   specific executable. The `forward` function describes the mathematical
   operations corresponding to the model inference.

4. Load the model weights from disk, onto the accelerator memory.

5. Load some user inputs, and copy them to the accelerator.

6. Call the executable using the weights and the user inputs.

7. Fetch the returned model output from accelerator into host memory, and
   finally present it to the user.

8. When all user inputs have been processed, free the executable resources,
   weights and inputs.
