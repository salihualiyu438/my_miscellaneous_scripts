import os

input_label_dir = r"C:\Users\User\Documents\final_year_project\datasets\masked_armed_bandit\combined_masked_armed_bandit__annotations"
output_label_dir = r"C:\Users\User\Documents\final_year_project\datasets\masked_armed_bandit\bbox_combined_masked_armed_bandit__annotations"

os.makedirs(output_label_dir, exist_ok=True)

for filename in os.listdir(input_label_dir):

    if not filename.endswith(".txt"):
        continue

    input_path = os.path.join(input_label_dir, filename)
    output_path = os.path.join(output_label_dir, filename)

    converted_lines = []

    with open(input_path, "r") as f:

        lines = f.readlines()

        for line in lines:

            values = line.strip().split()

            if len(values) < 7:
                continue

            class_id = values[0]

            coords = list(map(float, values[1:]))

            xs = coords[0::2]
            ys = coords[1::2]

            xmin = min(xs)
            xmax = max(xs)

            ymin = min(ys)
            ymax = max(ys)

            x_center = (xmin + xmax) / 2
            y_center = (ymin + ymax) / 2

            width = xmax - xmin
            height = ymax - ymin

            converted_line = (
                f"{class_id} "
                f"{x_center} "
                f"{y_center} "
                f"{width} "
                f"{height}"
            )

            converted_lines.append(converted_line)
    if os.path.split(output_path[1]):
        with open(output_path, "w") as f:
            f.write("\n".join(converted_lines))

print("Conversion complete.")