try:
    import google.colab

    in_colab = True
except ImportError:
    in_colab = False


in_notebook = in_colab
try:
    py = get_ipython()
    shell = py.__class__.__name__
    if shell == "ZMQInteractiveShell":
        in_notebook = True
    in_colab = in_colab or py.__class__.__module__ == "google.colab._shell"
except NameError:
    pass
