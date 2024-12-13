from PIL import Image, ImageDraw

# Define the width and height of the image
width, height = 200,200

# Create a new image with a white background
image = Image.new("RGB", (width, height), "white")
draw = ImageDraw.Draw(image)

# Define the condition function
def condition(x, y, w, h):
    # return (h // 24) > y or y > (h - (h // 24))
    return ((h // 3) < y < h - (h // 3)) and ((w // 3) < x < w - (w // 3))

# Define the size of each grid cell
cell_size = 1  # You can adjust this value as needed

meets = 0
# Loop over the grid cells
for x in range(0, width, cell_size):
    for y in range(0, height, cell_size):
        if condition(x, y, width, height):
            meets += 1
            draw.rectangle([x, y, x + cell_size - 1, y + cell_size - 1], fill="red")

print(meets / (width * height) * 100)

# Save the image
image.save("grid_image.png")

# Optionally, show the image
image.show()
