import os
import argparse
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import matplotlib.image as mpimg
# import cv2
from skimage.transform import estimate_transform

# ======= Load Keyframes =======
def load_keyframes(path):
    kf = []
    with open(path, 'r') as f:
        for line in f:
            if line.strip() == "" or line.startswith("#"):
                continue
            parts = line.strip().split()
            tx, ty = float(parts[1]), float(parts[2])
            kf.append([tx, ty])
    return np.array(kf)

# ======= Load Map Points =======
def load_map_points(path):
    points = []
    with open(path, 'r') as f:
        for line in f:
            if line.strip() == "" or line.startswith("pos_x"):
                continue
            parts = line.strip().replace(",", " ").split()
            x, y = float(parts[0]), float(parts[1])
            points.append([x, y])
    return np.array(points)

# ======= Click GUI =======
class AlignmentTool:
    def __init__(self, floorplan_img, keyframe_positions):
        self.img = floorplan_img
        self.kf = keyframe_positions
        self.kf_pts = []
        self.img_pts = []

        self.fig, self.ax = plt.subplots()
        self.ax.imshow(self.img, cmap='gray')
        self.ax.set_title("Click 3+ point correspondences (image ↔ SLAM)")

        self.cid = self.fig.canvas.mpl_connect('button_press_event', self.onclick)
        self.ax_kf = self.ax.scatter([], [], c='red', label='SLAM')
        self.ax_img = self.ax.scatter([], [], c='cyan', label='Floorplan')
        self.ax.legend()

        # Button to finish
        ax_button = plt.axes([0.8, 0.01, 0.15, 0.05])
        self.done_button = Button(ax_button, 'Compute Align')
        self.done_button.on_clicked(self.finish)

    def onclick(self, event):
        if event.inaxes != self.ax:
            return

        print(f"Clicked image point: ({event.xdata:.1f}, {event.ydata:.1f})")

        # Ask user for keyframe index (we'll improve this later)
        idx = input(f"Which keyframe index to associate with this? [0–{len(self.kf)-1}]: ")
        try:
            idx = int(idx)
            if 0 <= idx < len(self.kf):
                self.img_pts.append([event.xdata, event.ydata])
                self.kf_pts.append(self.kf[idx])
                self.update_plot()
        except ValueError:
            print("Invalid index. Try again.")

    def update_plot(self):
        if self.kf_pts:
            self.ax_img.set_offsets(self.img_pts)
            self.ax_kf.set_offsets(self.kf_pts)
            self.fig.canvas.draw_idle()

    def finish(self, _event):
        if len(self.kf_pts) < 3:
            print("❌ Need at least 3 points to compute alignment.")
            return

        # Compute similarity transform
        tform = estimate_transform('similarity', np.array(self.kf_pts), np.array(self.img_pts))
        print("✅ Alignment complete. Showing result...")

        # Apply transform to trajectory
        transformed = tform(self.kf)

        self.ax.plot(transformed[:, 0], transformed[:, 1], 'r--', label='Aligned SLAM Trajectory')
        self.ax.legend()
        self.fig.canvas.draw()

# ======= Main =======
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--floor', type=str, required=True, help='Floor name (e.g., FRB2)')
    args = parser.parse_args()

    base_path = os.path.expanduser(f"~/Dev/ORB_SLAM_data/results/{args.floor}")
    img_path = os.path.join(base_path, "floorplan.png")
    kf_path = os.path.join(base_path, f"kf_{args.floor}.txt")
    map_path = os.path.join(base_path, "map_points.txt")

    if not os.path.exists(img_path) or not os.path.exists(kf_path):
        print("❌ Missing required files.")
        return

    # img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    img = mpimg.imread(img_path)
    kf = load_keyframes(kf_path)

    AlignmentTool(img, kf)
    plt.show()

if __name__ == "__main__":
    main()
