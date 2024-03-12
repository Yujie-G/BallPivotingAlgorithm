import argparse

from bpa import BPA

args = argparse.ArgumentParser(description="BPA")
args.add_argument("--path", type=str)
args.add_argument("--radius", type=float, default=0.0005)
args.add_argument("--limit_iterations", type=int, default=None)
args.add_argument("--visualizer", type=bool, default=False)
args = args.parse_args()

bpa = BPA(path=args.path, radius=args.radius, visualizer=args.visualizer)
bpa.create_mesh(limit_iterations=args.limit_iterations)
bpa.save_mesh(bpa.model_name + '.obj')
