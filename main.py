import os
from wave_function_collapse import WaveFunctionCollapse

script_path = os.path.realpath(__file__)
script_dir = os.path.dirname(script_path)

if __name__ == "__main__":
    wave = WaveFunctionCollapse(os.path.join(script_dir, "samples", "Cat.png"), 50, 50)
    wave.run()

