#!/bin/bash

# === CONFIGURATION ===
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ORB_SLAM_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
PARENT_DIR="$(cd "$ORB_SLAM_DIR/.." && pwd)"
DATA_DIR="$PARENT_DIR/ORB_SLAM_data"
VIDEOS_DIR="$DATA_DIR/videos"
FRAMES_DIR="$DATA_DIR/frames"
SLAM_BIN="$ORB_SLAM_DIR/Examples/Monocular/mono_euroc"
VOCAB="$ORB_SLAM_DIR/Vocabulary/ORBvoc.txt"
CAMERA_CONFIG="$ORB_SLAM_DIR/Examples/Monocular/my_camera.yaml"

# === INPUT CHECK ===
if [ $# -ne 1 ]; then
    echo "Usage: ./ORB-SLAM.sh <video_filename>"
    sleep 3
    exit 1
fi

VIDEO_FILE="$1"
VIDEO_PATH="$VIDEOS_DIR/$VIDEO_FILE"

if [ ! -f "$VIDEO_PATH" ]; then
    echo "Error: $VIDEO_PATH not found"
    sleep 3
    exit 1
fi

# === FOLDER SETUP ===
BASENAME="${VIDEO_FILE%.*}"
FRAME_FOLDER="$FRAMES_DIR/$BASENAME"
FRAME_OUTPUT="$FRAME_FOLDER/mav0/cam0/data"
TIMESTAMPS_FILE="$FRAME_FOLDER/mav0/cam0/timestamps.txt"



# # === 1. EXTRACT FRAMES ===
# mkdir -p "$FRAME_OUTPUT"
# echo "Extracting frames to $FRAME_OUTPUT..."
# ffmpeg -i "$VIDEO_PATH" -qscale:v 2 "$FRAME_OUTPUT/frame_%06d.png"

# # === 2. GENERATE TIMESTAMPS ===
# echo "Generating timestamps.txt with frame names..."
# > "$TIMESTAMPS_FILE"
# for frame_path in "$FRAME_OUTPUT"/frame_*.png; do
#     frame_name=$(basename "$frame_path" .png)
#     echo "$frame_name" >> "$TIMESTAMPS_FILE"
# done

# === 3. RUN ORB-SLAM ===
echo "Running ORB-SLAM3..."
cd "$ORB_SLAM_DIR"
$SLAM_BIN "$VOCAB" "$CAMERA_CONFIG" "$FRAME_FOLDER" "$TIMESTAMPS_FILE" "$BASENAME"
echo "Done with SLAM for $VIDEO_FILE"

# # === 4. MOVE RESULT FILES ===    
# RESULTS_DIR="$DATA_DIR/results/$BASENAME"
# mkdir -p "$RESULTS_DIR"
# echo "Moving result files to $RESULTS_DIR..."
# mv "$ORB_SLAM_DIR/f_${BASENAME}.txt" "$RESULTS_DIR/" 2>/dev/null
# mv "$ORB_SLAM_DIR/kf_${BASENAME}.txt" "$RESULTS_DIR/" 2>/dev/null
# mv "$ORB_SLAM_DIR/my_map.osa" "$RESULTS_DIR/" 2>/dev/null
# echo "Results moved successfully to $RESULTS_DIR."